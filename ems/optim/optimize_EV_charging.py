__author__ = 'mzade'

from pyomo.environ import *


#generell: Modell bedeutet, dass die Werte wie soc_max als Variablen eingegeben werden, die entweder variabel (VAR) sind oder festgelegt
# Beschreibung einer Variable: within, bounds, initialize,

def create_ev_model(price_forecast, availability, total_hours=5, init_soc_bat=0, desired_soc=100, soc_max=100, soc_min=0,
                    p_bat_min=0, p_bat_max=11, battery_cap=50, efficiency=0.98, n_time_steps=96):

    ################################### Model Definitions ###########################################
    model = ConcreteModel()

    ############################### Parameter Definitions ###########################################                   # Einlesen der Werte aus main.py
    model.soc_max = Param(initialize=soc_max)                       # in %
    model.soc_min = Param(initialize=soc_min)                       # in %
    model.p_bat_min = Param(initialize=p_bat_min)                   # in W
    model.p_bat_max = Param(initialize=p_bat_max)                   # in W
    model.battery_cap = Param(initialize=battery_cap)               # in Wh
    model.soc_init = Param(initialize=init_soc_bat)                 # in %
    model.soc_des = Param(initialize=desired_soc)                   # in %
    model.t = RangeSet(0, n_time_steps-1)                           # range from 0 to number of time steps -1
    model.eff = Param(initialize=efficiency)                        # in the range of 0 to 1

    def energy_prices(model, t):                                                                                        # erstellt eine Matrix mit Timesteps und dazugehörigen Preisen
        return price_forecast[t]
    model.energy_prices = Param(model.t, initialize=energy_prices)  # in ct/kWh

    def ev_availability(model, t):                                                                                      # erstellt einen Vektor mit Verfügbarkeits Informationen
        return availability[t]
    model.ev_availability = Param(model.t, initialize=ev_availability)  # in 0 = not available or 1 = available

    ################################# Decision Variables ############################################
    model.soc = Var(model.t, within=NonNegativeReals, bounds=(soc_min, soc_max))                                        # Vektor für Zustand des SOCs pro Zeiteinheit
    model.p_bat_charge = Var(model.t, within=NonNegativeReals, bounds=(p_bat_min, p_bat_max))                           # Vektor für Zustand der Batterieladung pro Zeiteinheit

    ############################### Constraint Functions ############################################
    # 1.
    def init_soc_rule(model):                                                                                           # Festlegen des initialen Ladungszustands
        return model.soc[0] == model.soc_init
    model.init_soc_rule = Constraint(rule=init_soc_rule)

    # 3.
    def soc_plus1_rule(model, t):                                                                                       # SOC für den nächsten Zeitschritt durch aktuellen SOC und Zuladung berechnen
        if t < n_time_steps-1:
            return model.soc[t+1] == model.soc[t] + model.p_bat_charge[t] * total_hours / n_time_steps / model.battery_cap
        return Constraint.Skip
    model.soc_plus1_rule = Constraint(model.t, rule=soc_plus1_rule)

    # 1.
    def ev_available(model, t):                                                                                         # Wenn das EV nicht verfügbar ist, kann es nicht geladen werden
        if not model.ev_availability[t]:
            return model.p_bat_charge[t] == 0
        return Constraint.Skip
    model.ev_available = Constraint(model.t, rule=ev_available)

    # 16.
    def final_soc_rule(model):                                                                                          # Einen Zeitschritt vor dem Ende muss das EV den gewünschten Ladezustand erreicht haben
        return model.soc[n_time_steps-1] == model.soc_des
    model.final_soc = Constraint(rule=final_soc_rule)

    ############################### Objective Function ##############################################
    def cost_obj(model):                                                                                                # Gesamtkosten für den Ladevorgang des EV
        return sum((model.p_bat_charge[t] * model.energy_prices[t]) for t in model.t)
    model.cost = Objective(rule=cost_obj, sense=minimize)

    return model
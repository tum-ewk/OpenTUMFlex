###################
General information
###################
:Authors: `Babu Kumaran Nalini`_, `Zhengjie You`_, `Michel Zadé`_ 
:Organization: `Chair of Energy Economy and Application Technology`_, Technical University of Munich
:Version: 1.0
:Date: 01.06.2021
:DOI: `10.5281/zenodo.4251512`_
:Copyright: The model code is licensed under the `GNU General Public License 3.0`_.

***********
Description
***********
An open-source python-based flexibility model to quantify and price the flexibility of household devices.

* uses mixed-integer linear programming (MILP) to obtain cost-optimal operational schedules for household devices.
* calculates the flexibility potential and flexibility prices based on price, weather, generation and load forecasts of household devices.
* supports the following devices: PV, battery storage systems (BSS), electric vehicles (EV), heat pumps (HP), combined heat and power (CHP) units.
* outputs flexibility offers for each household device in formats that can be used in flexibility markets (e.g. comax by Tennet or ALF by FfE e.V.)

*******
Changes
*******
14.06.2021 - documentation release

************
Dependencies
************
* `Python`_ IDE: `Spyder`_ or `Pycharm`_ 
* Virtual environment: Please check environment_v1.0.yml
* Solver suggestions: `glpk`_ , `cplex`_ or any MILP solvers supported by Pyomo 


.. _Babu Kumaran Nalini: babu.kumaran-nalini@tum.de
.. _Zhengjie You: zhengjie.you@tum.de
.. _Michel Zadé: michel.zade@tum.de
.. _Chair of Energy Economy and Application Technology: https://www.ei.tum.de/en/ewk/
.. _GNU General Public License 3.0: https://www.gnu.org/licenses/gpl-3.0
.. _10.5281/zenodo.4251512: https://zenodo.org/record/4251512
.. _Python: https://www.python.org/
.. _Spyder: https://www.spyder-ide.org/
.. _Pycharm: https://www.jetbrains.com/pycharm/
.. _glpk: https://pypi.org/project/glpk/
.. _cplex: https://www.ibm.com/analytics/cplex-optimizer
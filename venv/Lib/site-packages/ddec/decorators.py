"""
These decorators can be used to annotate the tool functions.
Most decorators will check the argument types or input data.
"""
from functools import wraps


def accept(**types):
    """
    Decorator used to define accepted argument types for generic functions.

    The basic structure of this function was heavily inspired / extended on the basis of:
    https://stackoverflow.com/questions/15299878/how-to-use-python-decorators-to-check-function-arguments

    Usage
    -----

    .. code-block:: python

      @accept(foo=str, bar=(int,float))
      def f(foo, bar):
        pass

    :param types: arguments to the decorated function and the allowed types
    :return: decorated function
    """
    def decorator(f):
        # dig down to the original wrapped function in case more than one decorator was used
        _f = f
        while hasattr(_f, '__wrapped__'):
            _f = getattr(_f, '__wrapped__')

        # get the code, name and argnames
        code = _f.__code__
        fname = _f.__name__
        names = code.co_varnames[:code.co_argcount]

        @wraps(f)
        def decorated(*args, **kwargs):
            for argname, argtype in types.items():
                # check for argnames in kwargs
                if argname in kwargs:
                    argval = kwargs.get(argname)
                else:
                    try:
                        argval = args[names.index(argname)]
                    except IndexError:
                        # TODO: Turn this into a develop level log
                        #print('DevelWarning: arg %s not passed by function %s. (Maybe default?).' % (argname, fname))
                        continue

                # check type
                if argval is None:
                    if not (argtype == 'None' or (isinstance(argtype, (list, tuple)) and 'None' in argtype)):
                        raise TypeError('%s(...): arg %s: is None, must be %s.' % (fname, argname, argtype))
                    else:
                        continue

                elif argtype == 'callable' or (isinstance(argtype, (list, tuple)) and 'callable' in argtype):
                    if not callable(argval):
                        raise TypeError('%s(...): arg %s: type is %s, but shall be callable.' % (fname, argname, type(argval)))
                    else:
                        continue

                # check if there is a None or  callable in argtype
                if isinstance(argtype, (tuple, list)) and ('None' in argtype or 'callable' in argtype):
                    argtype = list(argtype)
                    if 'None' in argtype:
                        argtype.remove('None')
                    if 'callable' in argtype:
                        argtype.remove('callable')
                    argtype = tuple(argtype)

                if not isinstance(argval, argtype):
                    raise TypeError("%s(...): arg %s: type is %s, must be %s." %
                                    (fname, argname, type(argval), argtype))

            # all checkes passed
            return f(*args, **kwargs)
        return decorated
    return decorator


def enforce(**types):
    """
    Decorator used to define enforcing of argument type casts for the toolbox functions.

    In case a cast on one of the arguments raises a :py:class: `ValueError`, the cast will be ignored.
    Therefore it might make sense to combine a enforce decorator with a :py:func: `ddec.accept`
    decorator in order to accept only the enforced type. In this case the
    :py:func: `ddec.accept` decorator raises a :py:class: `ValueError`.

    The basic structure of this functionsudo was heavily inspired / extended on the basis of:
    https://stackoverflow.com/questions/15299878/how-to-use-python-decorators-to-check-function-arguments

    Usage
    -----

    .. code-block:: python

      @accept(foo=str)
      def f(foo):
        return 'Result: %s' % foo

    The f function can now be called and foo will be casted to a string

    .. code-block:: python

    a = f(5)
    print(type(a))

    .. code-block:: bash

    >> <class 'str'>

    :param types: arguments to the decorated function and the desired types
    :return: decorated function
    """
    def decorator(f):
        # dig down to the original wrapped function in case more than one decorator was used
        _f = f
        while hasattr(_f, '__wrapped__'):
            _f = getattr(_f, '__wrapped__')

        # get the code, name and argnames
        code = _f.__code__
        fname = _f.__name__
        names = code.co_varnames[:code.co_argcount]

        @wraps(f)
        def decorated(*args, **kwargs):
            def caster(value, destination):
                try:
                    return destination(value)
                except (ValueError, Exception):
                    # TODO: On develop log note that the cast failed
                    return value

            # turn args into a list
            args = list(args)

            # cast all defined types
            for argname, argtype in types.items():
                if argname in kwargs:
                    argval = kwargs.get(argname)
                    kwargs.update({argname: caster(argval, argtype)})
                else:
                    try:
                        index = names.index(argname)
                        args[index] = caster(args[index], argtype)
                    except IndexError:
                        # TODO: Turn this into a develop level log
                        continue

            return f(*args, **kwargs)
        return decorated
    return decorator

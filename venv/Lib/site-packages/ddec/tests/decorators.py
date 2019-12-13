import unittest
from ddec import accept, enforce
import numpy as np
from matplotlib.axes import SubplotBase
import matplotlib.pyplot as plt


class TestAcceptDecorator(unittest.TestCase):

    def test_all_native(self):
        """
        Test all native python functionality.
        """
        # define test f
        @accept(a=int, b=float, c=bool, d=tuple, e=list, g=dict)
        def f(a, b, c, d, e, g):
            pass

        # call it
        try:
            f(42, 42.3, True, (1,2), [1,2], {'foo':'bar'})
        except TypeError:
            self.fail('TypeError raised by accept decorator')

        # test failure
        with self.assertRaises(TypeError):
            f(42.3, 42.3, True, (1,2), [1,2], {'foo':'bar'})
        with self.assertRaises(TypeError):
            f(42, 42, True, (1, 2), [1, 2], {'foo': 'bar'})

    def test_fail_native(self):
        """
        Test if wrong type raises Type error.
        """
        # define test f
        @accept(a=int)
        def f(a):
            pass

        # call it
        with self.assertRaises(TypeError):
            f(42.3)

    def test_callable(self):
        """
        Test if a callable is handled correctly.
        """
        # define test
        func = lambda x: x
        @accept(a=(int, 'callable'), b='callable')
        def f(a, b):
            pass

        # call it
        try:
            f(func, func)
        except TypeError:
            self.fail('TypeError raised by accept decorator')

        # test failure
        with self.assertRaises(TypeError):
            f(5.5,func)

    def test_none_values(self):
        """
        Test if None values are handled correctly.
        """
        @accept(a='None', b=(int, 'None'))
        def f(a, b):
            pass

        # call it
        try:
            f(None, 5)
            f(None, None)
        except TypeError:
            self.fail('TypeError raised by accept decorator')

        # test failure
        with self.assertRaises(TypeError):
            f(5, 42.3)

    def test_none_and_callable(self):
        """
        Test callable and None at the same time.
        """
        func = lambda x: x
        @accept(a=('callable', 'None', int), b=int)
        def f(a, b):
            pass

        # call it
        try:
            f(func, 5)
            f(None, 5)
        except TypeError:
            self.fail('TypeError raised by accept decorator')

        # test failure
        with self.assertRaises(TypeError):
            f(5, 5)


    def test_matplotlib_numpy(self):
        """
        Test if matplotlib Subplot and numpy ndarray are handled correctly.
        """
        @accept(a=np.ndarray, b=SubplotBase, c=(np.ndarray, SubplotBase))
        def f(a,b,c):
            pass

        # create obj.
        arr = np.zeros(10)
        ax = plt.plot([1,2,3], [4,5,6])[0].axes

        # call it
        try:
            f(arr, ax, arr)
            f(arr, ax, ax)
        except TypeError:
            self.fail('TypeError raised by accept decorator')

        # test failure
        with self.assertRaises(TypeError):
            f(ax, arr, arr)
        with self.assertRaises(TypeError):
            f(arr, arr, arr)
        with self.assertRaises(TypeError):
            f(arr, ax, 5)


class TestEnforceDecorator(unittest.TestCase):

    def test_int(self):
        """
        Test the int type cast
        """
        @enforce(a=int, b=int)
        def f(a, b=5):
            return a, b

        # assert positional
        self.assertEqual(f(4.2, 4.9), (4, 4))
        # assert default
        self.assertEqual(f(4.2), (4, 5))
        # assert with cast fail
        self.assertEqual(f(4.2, 'mystring'), (4, 'mystring'))
        # assert keyword argument
        self.assertEqual(f(4.2, b=7.5), (4, 7))
        # assert bool
        self.assertEqual(f(True, False), (1, 0))
        # assert string
        self.assertEqual(f('5', '4'), (5, 4))

    def test_float(self):
        """
        Test the float type cast
        """
        @enforce(a=float, b=float)
        def f(a, b=5.5):
            return a, b

        # assert positional
        self.assertEqual(f(4, 3), (4.0, 3.0))
        # assert default
        self.assertEqual(f(4), (4, 5.5))
        # assert with cast fail
        self.assertEqual(f(4, 'mystring'), (4.0, 'mystring'))
        # assert keyword argument
        self.assertEqual(f(4, b=7), (4.0, 7.0))
        # assert bool
        self.assertEqual(f(True, False), (1.0, 0.0))
        # assert string
        self.assertEqual(f('5', '4.6'), (5.0, 4.6))

    def test_bool(self):
        """
        Test the bool type cast
        """
        @enforce(a=bool, b=bool)
        def f(a, b=True):
            return a, b

        # assert positional
        self.assertEqual(f(0, 0), (False, False))
        # assert default
        self.assertEqual(f(1), (True, True))
        # assert with cast fail
        self.assertEqual(f(4, 'mystring'), (True, True))
        # assert keyword argument
        self.assertEqual(f(4, b=0.0), (True, False))



if __name__ == '__main__':
    unittest.main()

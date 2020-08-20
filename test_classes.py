import classes
import unittest
import math

class TestVector(unittest.TestCase):
    
    def setUp(self):
        self.null = classes.Vector(0,0)
        self.i = classes.Vector(0,1)
        self.unit = classes.Vector(1,0)
        self.v1 = classes.Vector(-1,-1)
        self.v2 = classes.Vector(1,1)
    
    def test_getLength(self):
        self.assertEqual(self.null.getLength(),0)
        self.assertEqual(self.i.getLength(), 1)
        self.assertEqual(self.unit.getLength(), 1)
        self.assertEqual(self.v1.getLength(),math.sqrt(2))
    
    def test_getAngle(self):
        self.assertEqual(self.null.getAngle(),0)
        self.assertEqual(self.unit.getAngle(),0)
        self.assertEqual(self.i.getAngle(),math.pi/2)
        self.assertEqual(self.v1.getAngle(),-math.pi*(3/4))

    def test_getNormal(self):
        self.assertEqual(self.unit.getNormal(),self.unit)
        self.assertEqual(self.i.getNormal(),self.i)
        self.assertEqual(self.v1.getNormal(),classes.Vector(-1/math.sqrt(2),-1/math.sqrt(2)))

    def test_add(self):
        self.assertEqual(self.unit.__add__(self.i),self.v2)
        self.assertEqual(self.v1.__add__(self.v2),self.null)
        self.assertEqual(self.unit.__add__(self.null),self.unit)
        
    
if __name__ == '__main__':
    unittest.main()

'''
class TestCalc(unittest.TestCase):

    def test_add(self):
        self.assertEqual(calc.add(10, 5), 15)
        self.assertEqual(calc.add(-1, 1), 0)
        self.assertEqual(calc.add(-1, -1), -2)

    def test_subtract(self):
        self.assertEqual(calc.subtract(10, 5), 5)
        self.assertEqual(calc.subtract(-1, 1), -2)
        self.assertEqual(calc.subtract(-1, -1), 0)

    def test_multiply(self):
        self.assertEqual(calc.multiply(10, 5), 50)
        self.assertEqual(calc.multiply(-1, 1), -1)
        self.assertEqual(calc.multiply(-1, -1), 1)

    def test_divide(self):
        self.assertEqual(calc.divide(10, 5), 2)
        self.assertEqual(calc.divide(-1, 1), -1)
        self.assertEqual(calc.divide(-1, -1), 1)
        self.assertEqual(calc.divide(5, 2), 2.5)

        with self.assertRaises(ValueError):
            calc.divide(10, 0)
'''
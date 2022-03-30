from NFA import *
import unittest

class Test1(unittest.TestCase):
    def setUp(self):
        self.auto = Auto()
        self.auto.AutoCompile('мама|мыла|раму')
    def test_string1(self):
        self.assertEqual(self.auto.FindAll('мыла'), ['мыла'])

    def test_string2(self):
        self.assertEqual(set(self.auto.FindAll('мылараму')), set(['мыла','раму']))
#
    def test_string3(self):
        self.assertEqual(set(self.auto.FindAll('мамамылараму')), set(['мыла','раму','мама']))
#
    def test_string4(self):
        self.assertEqual(self.auto.FindAll('ПАПАПОЧИСТИЛ'), [])

class Test2(unittest.TestCase):
    def setUp(self):
        self.auto = Auto()
        self.auto.AutoCompile('a(a|b)*c')

    def test_string1(self):
        self.assertEqual(self.auto.FindAll('ac'), ['ac'])

    def test_string2(self):
        self.assertEqual(set(self.auto.FindAll('abac')), set(['ac', 'abac']))

    #
    def test_string3(self):
        self.assertEqual(self.auto.FindAll('bbbbcccc'), [])

    #
    def test_string4(self):
        self.assertEqual(self.auto.FindAll('aaac'), ['aaac','aac','ac'])


if __name__ == '__main__':
    unittest.main()
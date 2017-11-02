# -*- coding: utf-8 -*-
"""
Created on Thu Sep  7 22:09:57 2017

@author: thomasaref
"""

from unittest import main, TestCase, TestLoader, TextTestRunner


class WidgetTestCase(TestCase):
    def setUp(self):
        self.mystr="foo"
        
    def tearDown(self):
        pass

    def test_upper(self):
        self.assertEqual(self.mystr.upper(), 'FOO')

    def test_isupper(self):
        self.assertTrue('FOO'.isupper())
        self.assertFalse('Foo'.isupper())

    def test_split(self):
        s = 'hello world'
        self.assertEqual(s.split(), ['hello', 'world'])
        # check that s.split fails when the separator is not a string
        with self.assertRaises(TypeError):
            s.split(2)

if __name__ == '__main__':
    suite = TestLoader().loadTestsFromTestCase(WidgetTestCase)
    if 1:
        TextTestRunner(verbosity=2).run(suite)
    else:
        main(verbosity=2)


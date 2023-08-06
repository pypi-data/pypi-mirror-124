"""
Tests translator module.
"""
import unittest

import verbcalc


class TestTranslator(unittest.TestCase):
    def setUp(self):
        self.verbcalc_translator = verbcalc.Translator()
        self.values = []

    def test_addition(self):
        self.values.append(self.verbcalc_translator.translate('2 plus 2'))
        self.values.append(self.verbcalc_translator.translate('2 Plus 2'))
        self.assertListEqual(['2 + 2', '2 + 2'], self.values)


if __name__ == '__main__':
    unittest.main()

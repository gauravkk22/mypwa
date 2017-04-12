from __future__ import absolute_import
import unittest
import doctest
import sys


class NoExtensionTestSuite(unittest.TestSuite):
    def run(self, result):
        import simplejson
        simplejson._toggle_speedups(False)
        result = unittest.TestSuite.run(self, result)
        simplejson._toggle_speedups(True)
        return result


class TestMissingSpeedups(unittest.TestCase):
    def runTest(self):
        if hasattr(sys, 'pypy_translation_info'):
            "PyPy doesn't need speedups! :)"
        elif hasattr(self, 'skipTest'):
            self.skipTest('_speedups.so is missing!')


def additional_tests(suite=None):
    import simplejson
    import simplejson.encoder
    import simplejson.decoder
    if suite is None:
        suite = unittest.TestSuite()
    for mod in (simplejson, simplejson.encoder, simplejson.decoder):
        suite.addTest(doctest.DocTestSuite(mod))
    suite.addTest(doctest.DocFileSuite('../../index.rst'))
    return suite


def all_tests_suite():
    def get_suite():
        return additional_tests(
            unittest.TestLoader().loadTestsFromNames([
                'tests.test_bitsize_int_as_string',
                'tests.test_bigint_as_string',
                'tests.test_check_circular',
                'tests.test_decode',
                'tests.test_default',
                'tests.test_dump',
                'tests.test_encode_basestring_ascii',
                'tests.test_encode_for_html',
                'tests.test_errors',
                'tests.test_fail',
                'tests.test_float',
                'tests.test_indent',
                'tests.test_iterable',
                'tests.test_pass1',
                'tests.test_pass2',
                'tests.test_pass3',
                'tests.test_recursion',
                'tests.test_scanstring',
                'tests.test_separators',
                'tests.test_speedups',
                'tests.test_str_subclass',
                'tests.test_unicode',
                'tests.test_decimal',
                'tests.test_tuple',
                'tests.test_namedtuple',
                'tests.test_tool',
                'tests.test_for_json',
                'tests.test_subclass',
                'tests.test_raw_json',
            ]))
    suite = get_suite()
    import simplejson
    if simplejson._import_c_make_encoder() is None:
        suite.addTest(TestMissingSpeedups())
    else:
        suite = unittest.TestSuite([
            suite,
            NoExtensionTestSuite([get_suite()]),
        ])
    return suite


def main():
    runner = unittest.TextTestRunner(verbosity=1 + sys.argv.count('-v'))
    suite = all_tests_suite()
    raise SystemExit(not runner.run(suite).wasSuccessful())


if __name__ == '__main__':
    import os
    import sys
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
    main()

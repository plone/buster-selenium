import os

try:
    import unittest2 as unittest
    unittest  # pyflakes
except ImportError:
    import unittest

from zope.testing.testrunner import feature
from zope.testing.testrunner import find

from buster_selenium import case


def find_suites(options):
    tests_pattern = options.tests_pattern
    seen = set()
    for (p, package) in find.test_dirs(options, {}):
        if p in seen:
            continue
        for dirpath, dirs, files in os.walk(p):
            d = os.path.split(dirpath)[1]
            if not tests_pattern(d):
                # not a tests directory
                continue
            if 'buster.js' not in files:
                # This tests dir is not a buster test suite
                continue

            # TODO individual test cases for every test file specified
            # in buster.js
            yield unittest.TestSuite([case.BusterJSTestCase(
                os.path.join(dirpath, 'buster.js'), test_dir=p)])
        seen.add(p)


class FindBusterJSTests(feature.Feature):
    """
    Find Buster.js test suites.

    Test suites are directories matching the `--tests-pattern` with a
    `buster.js` file in it.  Special Python `unittest.TestSuite`
    instances are then used which will call `buster-test` to run the
    tests.  The suites use a layer to manage the `buster-server` and
    re-use parts of selenium to manage the capture of buster slave
    browsers.
    """

    def global_setup(self):
        # Ensure that our find_suites is used
        found_suites = self.runner.found_suites
        if found_suites is None:
            found_suites = find_suites(self.runner.options)

        tests = find.find_tests(self.runner.options, found_suites)
        self.runner.register_tests(tests)

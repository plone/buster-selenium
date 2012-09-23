import sys
import os
import subprocess

try:
    import unittest2 as unittest
    unittest  # pyflakes
except ImportError:
    import unittest

try:
    from zope import testrunner
    testrunner  # pyflakes
except ImportError:
    testrunner = None

from buster_selenium import layer


class BusterJSTestCase(unittest.TestCase):
    """
    Run a Buster.js test file as a Python `unittest.TestCase`.
    """

    layer = layer.BusterJSSlaveLayer

    def __init__(self, methodName='runTest', test_dir=None):
        super(BusterJSTestCase, self).__init__(methodName)
        self.test_dir = test_dir

    def setUp(self):
        if testrunner is None:
            # set up server and slave on test set up if layers are not
            # available
            self.layer.setUp()

        self.bin = os.environ.get(
            'BUSTER_TEST_BINARY', 'buster-test').strip()

        self.options = [option.strip() for option in
                        os.environ['BUSTER_TEST_OPTIONS'].split()
                        if option.strip()]

        output = os.environ['BUSTER_TEST_OUTPUT_DIR'].strip()
        if output and not os.path.isdir(output):
            os.makedirs(output)
        stdout = sys.stdout
        if output:
            result = '${test_dir}-${dirpath}.xml'.format(
                test_dir=os.path.basename(self.test_dir),
                dirpath=self._testMethodName[
                    len(self.test_dir):].strip('/').replace('/', '-'))
            stdout = open(os.path.join(output, result), 'w')
        self.stdout = stdout

    def run(self, result=None):
        retcode = subprocess.call(
            [self.bin] + self.options + ['--config', self._testMethodName]
            + sys.argv[1:], stdout=self.stdout)
        if retcode:
            failures.append(dirpath)

    def tearDown(self):
        if testrunner is None:
            # set up server and slave on test set up if layers are not
            # available
            self.layer.tearDown()

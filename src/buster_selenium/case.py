import sys

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

        options = [option.strip() for option in """${options}""".split()
                   if option.strip()]
        output = TODO  # handle XML how?
        if output and not os.path.isdir(output):
            os.makedirs(output)
        stdout = sys.stdout
        if output:
            result = dirpath[len(p):].strip('/').replace(
                '/', '-') + '.xml'
            stdout = open(os.path.join(output, result), 'w')
        self.stdout = stdout

    def run(self, result=None):
        retcode = subprocess.call(
            [self.bin] + options + ['--config', os.path.join(dirpath, filename)]
            + sys.argv[1:], stdout=stdout)
        if retcode:
            failures.append(dirpath)

    def tearDown(self):
        if testrunner is None:
            # set up server and slave on test set up if layers are not
            # available
            self.layer.tearDown()

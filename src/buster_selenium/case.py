import sys

try:
    import unittest2 as unittest
    unittest  # pyflakes
except ImportError:
    import unittest

try:
    from zope import testrunner
except ImportError:
    layer = None
else:
    from buster_selenium import layer


class BusterJSTestCase(unittest.TestCase):
    """
    Run a Buster.js test file as a Python `unittest.TestCase`.
    """

    if layer:
        layer = layer.BusterJSSlaveLayer

    def run(self, result=None):
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
                    retcode = subprocess.call(
                        [os.path.join('bin', 'buster-test')] + options
                        + ['--config', os.path.join(dirpath, filename)]
                        + sys.argv[1:], stdout=stdout)
                    if retcode:
                        failures.append(dirpath)

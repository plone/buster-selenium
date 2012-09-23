import subprocess
import os


class BusterJSServerLayer(object):
    """
    Start up and shutdown a `buster-server`.

    For use by `buster_selenium.case.BusterJSTestCase`.
    """

    @classmethod
    def setUp(cls):
        # From http://trodrigues.net/presentations/buster-ci/#/24
        cls.server = subprocess.Popen(
            [os.path.join('bin', 'buster-server'), '-v'],
            stdout=subprocess.PIPE)

    @classmethod
    def tearDown(cls):
        cls.server.terminate()
        cls.server.wait()
        del cls.server


class BusterJSSlaveLayer(BusterJSServerLayer):
    """
    Start up and shutdown a BusterJS slave browser via Selenium.

    For use by `buster_selenium.case.BusterJSTestCase`.  Can be
    configured to capture a local browser or to capture browsers
    through Selenium Grid.
    """

    @classmethod
    def setUp(cls):
        cls.slave = subprocess.Popen(
            ['${:firefox-bin}', '${:firefox-options}',
             'http://localhost:1111/capture'])

        # Wait for slave to be captured
        server = BusterJSServerLayer.server
        line = server.stdout.readline()
        while line != '':
            if line.startswith('Slave captured'):
                break
            line = server.stdout.readline()
        else:
            raise subprocess.CalledProcessError(
                'Server closed stdout without capturing a slave.')

    @classmethod
    def tearDown(cls):
        cls.slave.terminate()
        cls.slave.wait()
        del cls.slave

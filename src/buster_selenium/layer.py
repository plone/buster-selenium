import subprocess
import os


class BusterJSServerLayer(object):
    """
    Start up and shutdown a `buster-server`.

    For use by `buster_selenium.case.BusterJSTestCase`.
    """

    @classmethod
    def setUp(cls):
        executable = os.environ.get(
            'BUSTER_SERVER_EXECUTABLE', 'buster-server').strip()

        # From http://trodrigues.net/presentations/buster-ci/#/24
        cls.server = subprocess.Popen([executable, '-v'],
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

    capture_url = 'http://localhost:1111/capture'

    @classmethod
    def setUp(cls):
        browser_executable = os.environ.get(
            'BUSTER_SLAVE_BROWSER_EXECUTABLE', None)
        if browser_executable is not None:
            # BUSTER_SLAVE_BROWSER_EXECUTABLE overrides selenium
            cls.openSubprocess(browser_executable)

        try:
            from selenium import webdriver
        except ImportError:
            # Fall back to running the browser directly
            cls.openSubprocess(browser_executable or 'firefox')
        else:
            cls.openSelenium(webdriver)

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
    def openSelenium(cls, webdriver):
        driver_class = getattr(
            webdriver,
            os.environ.get('BUSTER_SLAVE_SELENIUM_DRIVER', 'Firefox'))
        driver_args = [
            arg.strip() for arg in
            os.environ.get('BUSTER_SLAVE_SELENIUM_ARGS', '').split()
            if arg.split()]
        desired_capabilities = dict(
            (key, os.environ.get(
                'BUSTER_SLAVE_SELENIUM_GRID_' + key.upper(), value))
             for key, value in
            webdriver.DesiredCapabilities.FIREFOX.items())

        cls.driver = driver_class(*driver_args,
                              desired_capabilities=desired_capabilities)
        cls.driver.get(cls.capture_url)

        return cls.driver

    @classmethod
    def openSubprocess(cls, browser_executable):
        cls.slave = subprocess.Popen(
            [browser_executable] +
            [opt.strip() for opt in
             os.environ.get('BUSTER_SLAVE_BROWSER_OPTIONS', '').split()
             if opt.strip()] + [cls.capture_url])
        return cls.slave

    @classmethod
    def tearDown(cls):
        if hasattr(cls, 'slave'):
            cls.slave.terminate()
            cls.slave.wait()
            del cls.slave
        elif hasattr(cls, 'driver'):
            cls.driver.quit()
            del cls.driver

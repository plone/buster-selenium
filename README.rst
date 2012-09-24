==============================================
buster-selenium
==============================================
Buster.js Selenium and Python Test Integration
==============================================

This package provides wrappers for the `Buster.js`_ server and test
runner that integrate bits of selenium to control the capture of
`Buster slaves`_.  It also provides wrappers for running Buster.js
tests as a part of a `Python`_ test suite and further integration with
`zope.testrunner`_ for doing test discovery and `testing layers`_ for
controlling the `buster-server`_ and capturing Buster.JS browser
slaves.

Managing ``buster-server`` and Capturing Browser Slaves
=======================================================

The ``buster_selenium.case.BusterJSTestCase`` class is a sub-class of
`unittest.TestCase`_ and can be used to create Python test cases that
will run a Buster.JS test suite corresponding to one ``buster.js`` test
configuration:

    >>> from buster_selenium import case
    >>> def suite():
    >>>     suite = unittest.TestSuite()
    ...     suite.addTest(
    ...         case.BusterJSTestCase('/path/to/buster.js'))
    ...     return suite

The test case will start ``buster-server``, launch a browser, and
capture a browser slave in the test ``setUp``.  Then it will invoke
``buster-test`` passing the ``buster.js`` config file and will report
failure if ``buster-test`` exits with a status code of ``1`` or will
report erro if it exits with any other non-zero status code.  Finally,
it will shutdown the browser slave and the ``buster-server``.

The ``BusterJSTestCase`` class uses a few environment variables to
control how the ``buster-test`` executable is invoked and what is done
with its output:

BUSTER_TEST_EXECUTABLE
  If defined, the value of this will be used as the path to the
  ``buster-test`` executable to be used to run the tests.  Useful if
  you're installing/building Buster.JS as a part of your
  build/deployment environment.  If this variable is not defined, the
  first ``buster-test`` available on ``PATH`` will be used.

BUSTER_TEST_OPTIONS
  If defined, the value of this variable will be passed to Python's
  `shlex.split`_ and passed as arguments/options to the ``buster-test``
  executable.  This can be useful, for example, to use different
  `buster-test --report`_ options.

BUSTER_TEST_STDOUT
  If defined, the stdout output of the ``buster-test`` executable will
  be written to this file.

BUSTER_SERVER_EXECUTABLE
  Like ``BUSTER_TEST_EXECUTABLE``, if defined, the path given will be
  used as the ``buster-server`` executable.  Otherwise the first
  ``buster-server`` found on ``PATH`` will be used.

BUSTER_SLAVE_BROWSER_EXECUTABLE
  If defined, the executable at the path given will be invoked as a
  slave browser and captured by the ``buster-server`` previously
  started.  If the ``selenium.webdriver`` package is availble, setting
  this overrides the default behavior of capturing a browser slave via
  Selenium.

BUSTER_SLAVE_BROWSER_OPTIONS
  If defined, the value of this variable will be passed to Python's
  `shlex.split`_ and passed as arguments/options to the
  ``BUSTER_SLAVE_BROWSER_EXECUTABLE`` executable.

BUSTER_SLAVE_SELENIUM_DRIVER
  If the ``selenium.webdriver`` package is availble and this variable is
  set, the value will be used to retrieve a Selenium driver from the
  `selenium.webdriver Python module`_.  By default, ``Firefox`` is used.

BUSTER_SLAVE_SELENIUM_ARGS
  If defined, the value of this variable will be passed to Python's
  `shlex.split`_ and passed as positional arguments to the
  ``selenium.webdriver`` used.

BUSTER_SLAVE_SELENIUM_GRID_BROWSERNAME, BUSTER_SLAVE_SELENIUM_GRID_VERSION, BUSTER_SLAVE_SELENIUM_GRID_PLATFORM, BUSTER_SLAVE_SELENIUM_GRID_JAVASCRIPTENABLED
  If using `Selenium Grid`_ by setting
  ``BUSTER_SLAVE_SELENIUM_DRIVER=Remote`` and this variable defined,
  these values will be used to modify the values for the
  ``browserName``, ``version``, ``platform``, and ``javascriptEnabled`` keys
  in the ``selenium.webdriver.DesiredCapabilities`` dictionaries.  This
  is useful to run your buster tests against different OS's, browsers,
  and versions.

Buster.JS Test Discovery
========================

The ``buster-selenium`` package provides a ``buster-testrunner`` console
script which adds discovery of Buster.JS tests to the
`zope.testrunner`_ support for `automatically finding tests`_
throughout a project.  In particular, it will create test suites from
any directory under a valid ``buster-testrunner --test-path`` that has a
``buster.js`` file::

    $ buster-testrunner --test-path=/path/to/project/module --test-path=/path/to/project/other-module

See the `zope.testrunner`_ docs or ``buster-testrunner --help`` for more
details on controlling test discovery and which tests are run.

Sharing ``buster-server`` and Browser Slave Capture Between Tests
=================================================================

The ``buster_selenium.layer`` module uses ``zope.testrunner`` support for
`testing layers`_ to start ``buster-server``, launch a browser, and
capture a browser slave and use those for all ``buster-test`` runs when
the tests are run with ``buster-testrunner``.  This can help speed up
the running of multiple Buster.JS test suites while still providing
clean mangement of the ``buster-server`` and captured browser slaves.
These layers are used automatically when using the test discovery
described above.

Managing Browser Slaves with Selenium Webdriver
===============================================

If the selenium Python package is available, by default the
``BusterJSTestCase`` and testing layer support described above will
use `selenium.webdriver`_ to open, capture, and clean up a browser
slave.  The way that ``selenium.webdriver`` launches browsers provides
an additional degree of isolation from user extensions, profiles,
themes, and other add-ons and provides greater isolation for Buster.JS
tests.


.. _Buster.js: http://busterjs.org/
.. _Buster slaves: http://busterjs.org/docs/capture-server/
.. _Python: http://python.org
.. _zope.testrunner: http://pypi.python.org/pypi/zope.testrunner
.. _testing layers: http://pypi.python.org/pypi/zope.testrunner#layers
.. _buster-server: http://busterjs.org/docs/server-cli/
.. _unittest.TestCase: http://docs.python.org/library/unittest.html#unittest.TestCase
.. _automatically finding tests: http://pypi.python.org/pypi/zope.testrunner#test-runner
.. _selenium.webdriver: http://seleniumhq.org/docs/03_webdriver.html
.. _shlex.split: http://docs.python.org/library/shlex.html#shlex.split
.. _buster-test --report: http://busterjs.org/docs/test/reporters
.. _selenium.webdriver Python module: http://seleniumhq.org/docs/03_webdriver.html#selenium-webdriver-s-drivers
.. _Selenium Grid: http://selenium-grid.seleniumhq.org/

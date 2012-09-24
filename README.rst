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

Managing `buster-server` and Capturing Browser Slaves
=====================================================

The `buster_selenium.case.BusterJSTestCase` class is a sub-class of
`unittest.TestCase`_ and can be used to create Python test cases that
will run a Buster.JS test suite corresponding to one `buster.js` test
configuration:

    >>> from buster_selenium import case
    >>> def suite():
    >>>     suite = unittest.TestSuite()
    ...     suite.addTest(
    ...         case.BusterJSTestCase('/path/to/buster.js'))
    ...     return suite

The test case will start `buster-server`, launch a browser, and
capture a browser slave in the test `setUp`.  Then it will invoke
`buster-test` passing the `buster.js` config file and will report
failure if `buster-test` exits with a status code of `1` or will
report erro if it exits with any other non-zero status code.

.. _Buster.js: http://busterjs.org/
.. _Buster slaves: http://busterjs.org/docs/capture-server/
.. _Python: http://python.org
.. _zope.testrunner: http://pypi.python.org/pypi/zope.testrunner
.. _testing layers: http://pypi.python.org/pypi/zope.testrunner#layers
.. _buster-server: http://busterjs.org/docs/server-cli/
.. _unittest.TestCase: http://docs.python.org/library/unittest.html#unittest.TestCase

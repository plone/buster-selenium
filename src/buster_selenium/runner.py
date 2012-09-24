import sys

try:
    from zope.testrunner import runner
    runner  # pyflakes
except ImportError:
    from zope.testing.testrunner import runner

from buster_selenium import find


class Runner(runner.Runner):

    def configure(self):
        """Include Buster.JS tests."""
        super(Runner, self).configure()
        self.features.append(find.FindBusterJSTests(self))


# Copied from zope.testrunner

def run(defaults=None, args=None, script_parts=None):
    """Main runner function which can be and is being used from main programs.

    Will execute the tests and exit the process according to the test result.

    """
    failed = run_internal(defaults, args, script_parts=script_parts)
    sys.exit(int(failed))


def run_internal(defaults=None, args=None, script_parts=None):
    """Execute tests.

    Returns whether errors or failures occured during testing.

    """
    # XXX Bah. Lazy import to avoid circular/early import problems
    runner = Runner(defaults, args, script_parts=script_parts)
    runner.run()
    return runner.failed

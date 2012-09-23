import sys
import os
import pkg_resources

from zope.testrunner import runner

import zc.buildout.easy_install
from zc.recipe import testrunner as recipe

from buster_selenium import find


class Runner(runner.Runner):

    def configure(self):
        """Include Buster.JS tests."""
        super(Runner, self).configure()
        self.features.append(find.Find(self))


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


class TestRunnerRecipe(recipe.TestRunner):

    # Copied from zc.recipe.testrunner

    def install(self):
        options = self.options
        dest = []
        eggs, ws = self.egg.working_set(
            ('zope.testing <3.10.0', 'buster-selenium'))

        test_paths = [ws.find(pkg_resources.Requirement.parse(spec)).location
                      for spec in eggs]

        defaults = options.get('defaults', '').strip()
        if defaults:
            defaults = '(%s) + ' % defaults

        wd = options.get('working-directory', '')
        if not wd:
            wd = options['location']
            if os.path.exists(wd):
                assert os.path.isdir(wd)
            else:
                os.mkdir(wd)
            dest.append(wd)
        wd = os.path.abspath(wd)

        if self.egg._relative_paths:
            wd = recipe._relativize(self.egg._relative_paths, wd)
            test_paths = [recipe._relativize(self.egg._relative_paths, p)
                          for p in test_paths]
        else:
            wd = repr(wd)
            test_paths = map(repr, test_paths)

        initialization = recipe.initialization_template % wd

        env_section = options.get('environment', '').strip()
        if env_section:
            env = self.buildout[env_section]
            for key, value in env.items():
                initialization += recipe.env_template % (key, value)

        initialization_section = options.get('initialization', '').strip()
        if initialization_section:
            initialization += initialization_section

        dest.extend(zc.buildout.easy_install.scripts(
            [(options['script'], 'buster-selenium', 'testrunner')],
            ws, options['executable'],
            self.buildout['buildout']['bin-directory'],
            extra_paths=self.egg.extra_paths,
            arguments = defaults + (
                    '[\n'+
                    ''.join(("        '--test-path', %s,\n" % p)
                            for p in test_paths)
                    +'        ]'),
            initialization = initialization,
            relative_paths = self.egg._relative_paths,
            ))

        return dest

    update = install

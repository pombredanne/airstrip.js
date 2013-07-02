# -*- coding: utf8 -*-

from optparse import OptionParser
import sys
import os

from . import __version__
from puke2 import settings
from puke2 import fs
from puke2 import tasks
from puke2 import exceptions

# XXX temporary hack to allow for airstrip internal resolution
base = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(1, base)

class CommandLine(object):

    def __init__(self):
        self.parser = OptionParser()
        self.parser.add_option(
            "-c", "--clear", action="store_true", dest="clearcache",
            help="Spring time, clean all the vomit")
        self.parser.add_option(
            "-q", "--quiet", action="store_false", dest="verbose",
            help="don't print status messages to stdout")
        self.parser.add_option(
            "-v", "--verbose", action="store_true", dest="verbose",
            help="print more detailed status messages to stdout")
        self.parser.add_option(
            "-t", "--tasks", action="store_true", dest="list_tasks",
            help="list tasks")
        self.parser.add_option("-l", "--log", dest="logfile",
                               help="Write debug messages to given logfile")
        self.parser.add_option("-f", "--file", dest="file",
                               help="Use the given build script")
        self.parser.add_option(
            "-i", "--info", action="store_true", dest="info",
            help="puke task --info show task informations")
        self.parser.add_option(
            "-V", "--version", action="store_true", dest="version",
            help="print the Airstrip version")

        if sys.platform.lower() == "darwin":
            self.parser.add_option(
                "-s", "--speak", action="store_true", dest="speak",
                help="puke speaks on fail/success")

    def run(self):
        (options, args) = self.parser.parse_args()

        # output version
        if options.version:
            print("Airstrip %s" % __version__)
            sys.exit(0)

        scriptpath = None
        for filename in os.listdir(base):
            filepath = fs.join(base, filename)
            if filename.lower() in settings.PUKEFILES and fs.isfile(filepath):
                scriptpath = filepath
                break

        if options.file and fs.isfile(options.file):
            scriptpath = options.file

        if not scriptpath:
            raise exceptions.PukefileNotFound(
                options.file or settings.PUKEFILES)

        # TODO remove puke legacy
        scope = {
            'puke': sys.modules['puke2'],
            'puke2': sys.modules['puke2'],
            'task': tasks.task
        }
        scriptvalue = execfile(scriptpath, scope, scope)

        if not args and tasks.hasDefault():
            return tasks.execute('default')

        if not args:
            print("No default task to execute")
            sys.exit(1)

        task_name = args.pop(0)
        if options.info:
            print(tasks.help(task_name))
            return

        kwargs = {}
        for arg in args:
            if '=' in arg:
                kwargs.update(dict(tuple((arg.split('=', 1),))))
                args.remove(arg)

        tasks.execute(task_name, *args, **kwargs)


def main():
    cli = CommandLine()
    try:
        cli.run()
    # except Exception as error:
    #     raise error
    #     sys.exit(1)
    except KeyboardInterrupt:
        print("Build interrupted")
        sys.exit(2)

    sys.exit(0)


if __name__ == '__main__':
    sys.exit(main())

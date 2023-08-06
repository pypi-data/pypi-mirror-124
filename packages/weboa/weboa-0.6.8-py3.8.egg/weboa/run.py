#!/usr/bin/env python
from weboa import *
from weboa import __VERSION__
from time import sleep
import sys
import glob

from weboa.utils.Processing import Processing


def runcli():
    print("Welcome to Weboa!")
    commands = {
        "version": ("--version", "-v"),
        "help": ("-h", "--help"),
        "init": ("-i",),
        "update": ("--update","-u"),

        "less": ("--less",),
        "sass": ("--sass","--scss",),
        "css": ("--css",),
    }

    args = sys.argv
    for i in range(len(args)):
        if args[i] in commands["version"]:
            print(f"Weboa version is {__VERSION__}")

        elif args[i] in commands["help"]:
            print("Usage: weboa [--init OUTPUT_DIR]\n"
                  "Project/Package manager. \n"
                  "\n"
                  "positional arguments: \n"
                  "--css\t\t\t\t\t Select preprocess (less|sass|scss) \n"
                  "\n"
                  "optional arguments: \n"
                  "-h, --help\t\t\t\t Show this help text\n "
                  "\n"
                  "-l, --less\t\t\t\t Start LESS watcher. Use with & in the end \n"
                  "-s, --sass\t\t\t\t Start SASS watcher. Use with & in the end\n "
                  "-s, --scss\t\t\t\t Start SCSS watcher. Use with & in the end \n"
                  "\n"
                  "-v, --version\t\t\t\t Show current version of Weboa \n"
                  "-u, --update\t\t\t\t Update Weboa through pip \n"
                  "-i, --init\t\t\t\t Initi project (use --init with OUTPUT_DIR)\n")

        elif args[i] in commands["update"]:
            for _ in (1,2):
                os.system("pip install weboa --upgrade")
                os.system("pip3 install weboa --upgrade")
                sleep(1)
                os.system("pip3 install weboa --upgrade")

        elif args[i] in commands["less"]:
            _path = os.getcwd()
            _weboa = Processing.Weboa_Open()
            Printer.log(_weboa)
            Printer.log(_path)
            Printer.log(glob.glob(_path + "/css/*.less"))
            if(_weboa):
                while True:
                    for i in glob.glob(_path + "/css/*.less"):
                        if not Processing.is_file_changed(_weboa, i, precss="less"):
                            continue
                        Processing.pre_css(_weboa, i, precss="less")
                        sleep(0.5)
                    sleep(2)

        elif args[i] in commands["sass"]:
            _path = os.getcwd()
            _weboa = Processing.Weboa_Open()
            _warning_was = False
            if(_weboa):
                while True:
                    for i in glob.glob(_path + "/css/*.scss"):
                        if (not Processing.is_file_changed(_weboa, i, precss="scss")):
                            continue
                        Processing.pre_css(_weboa, i, precss="scss")
                    for i in glob.glob(_path + "/css/*.sass"):
                        if (not Processing.is_file_changed(_weboa, i, precss="sass")):
                            continue
                        _proc = Processing.pre_css(_weboa, i, precss="sass")
                        if not _proc:
                            if not _warning_was:
                                Printer.warning(f"{precss} compiled with an error!")
                                _warning_was = True
                        else:
                            _warning_was = False


        elif args[i] in commands["init"]:
            _path = os.getcwd()
            _build_folder = _path + "/"

            try:
                if (args[i] == commands["init"][0]):
                    _build_folder += args[i + 1]
                    os.mkdir(_build_folder)
            except IndexError:
                Printer.error("Index Error")

            Processing.Save_Path(_path)
            precss = "css"
            try:
                if commands["css"][0] in args:
                    cssindex = args.index(commands["css"][0])
                    precss = args[cssindex+1]
                    Printer.info(f"Css {precss}")
            except IndexError:
                Printer.error("Index Error [css]")

            php=PHP(path="", BUILDFOLDER=_build_folder)
            php.FS()
            php.index()
            php.language()
            php.controller()
            php.project()
            php.ico()
            php.css(precss)
            php.robots()
            php.js()
            php.img()
            php.readme()
            php.gitignore()
            php.icons_pwa()

if(__name__=="__main__"):
    runcli()
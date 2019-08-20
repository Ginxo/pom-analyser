#!/usr/bin/python

import getopt
import sys

from emingora.pom.analyser.tools.GAVDeclaredAndDefine import GAVDeclaredAndDefine
from emingora.pom.analyser.tools.RepeatedGAVS import RepeatedGAVS
from emingora.pom.analyser.utils.PomReaderUtil import PomReaderUtil


def main(argv):
    try:
        opts, args = getopt.getopt(argv, "hdrf:", ["file="])
    except getopt.GetoptError:
        print_help()
        sys.exit(2)

    if len(opts) == 0:
        print_help()
        sys.exit(2)

    pom_path = "./pom.xml"
    for opt, arg in opts:
        if opt == '-h':
            print_help()
            sys.exit()
        elif opt in ("-f", "--file"):
            pom_path = arg

        if opt in "-d":
            run_gdad_check(pom_path)

        if opt in "-r":
            run_repeated_check(pom_path)


def print_help():
    print("pom-analyser.py -f path_to_pom.xml")
    print("-h help")
    print("-r check the repeated dependencies")
    print("-d analyse whether a dependency has been declared and defined in the project structure")


def run_gdad_check(pom_file_path):
    print("Loading pom file from [{0}]".format(pom_file_path))
    pom = PomReaderUtil.read(pom_file_path)
    print("Running the -d checking...".format(pom_file_path))
    result = GAVDeclaredAndDefine.get_repeated_gavs(pom)
    print("------- Check finished ---------")
    print_gdad_check(result)
    print("")


def print_gdad_check(result):
    for project in result:
        print("---------------------------------------")
        print("PROJECT: {0}".format(project))
        print("---------------------------------------")
        print("")
        for dependency in result[project]:
            print(" DEPENDENCY: {0}".format(dependency))
            for gav in result[project][dependency]:
                print("     project: {0}".format(gav.belonging_pom))

        print("")


def run_repeated_check(pom_file_path):
    print("Loading pom file from [{0}]".format(pom_file_path))
    pom = PomReaderUtil.read(pom_file_path)
    print("Running the -r checking...".format(pom_file_path))
    result = RepeatedGAVS.get_repeated_gavs(pom)
    print("------- Check finished ---------")
    print(result)
    print("")

if __name__ == "__main__":
    main(sys.argv[1:])

#!/usr/bin/python

import getopt
import sys

from emingora.pom.analyser.tools.GAVDeclaredAndDefine import GAVDeclaredAndDefine
from emingora.pom.analyser.utils.PomReaderUtil import PomReaderUtil


def main(argv):
    try:
        opts, args = getopt.getopt(argv, "hf:", ["file="])
    except getopt.GetoptError:
        print_help()
        sys.exit(2)

    pom_path = "./pom.xml"
    for opt, arg in opts:
        if opt == '-h':
            print_help()
            sys.exit()

        if opt in ("-f", "--file"):
            pom_path = arg

    run_gdad_check(pom_path)


def print_help():
    print("pom-analyser.py -f pom.xml")


def run_gdad_check(pom_file_path):
    print("Loading pom file from [{0}]".format(pom_file_path))
    pom = PomReaderUtil.read(pom_file_path)
    print("Running the checking...".format(pom_file_path))
    result = GAVDeclaredAndDefine.get_repeated_gavs(pom)
    print("------- Check finished ---------")
    print_gdad_check(result)


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


if __name__ == "__main__":
    main(sys.argv[1:])

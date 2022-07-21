import argparse
import sys

import src.cloneDetection as Ccd


def manage_args(argv):
    FILE_NAME = argv[0]

    argParser = argparse.ArgumentParser(description='ProSmart: Vulnerable Code Clone Detection '
                                                    'in Propagated Smart Contracts')
    argParser.add_argument('--version', '-v', action='store_true', help='prints out the version of this program. ')
    argParser.add_argument('--input_path', '-i', help='tell us the file path to the Solidity code you wish to verify. ')
    argParser.add_argument('--output_path', '-o', help='tell us the directory path to which '
                                                       'you wish to have the result saved into. ')

    args = argParser.parse_args()

    if args.version:
        print("v0.1.0")
    #TODO


if __name__ == '__main__':
    # 1. args: version, input file path, output file path
    manage_args(sys.argv)

    #TODO
    # 2. read vdb file and structure data as obj
    # 3. parse functions from input source code
    # 4. compare vdb functions vs parsed functions
    # 5. structure detected functions data
    # 6. safe output file
    # 7. return execution terminated message

import argparse
import json
import os.path

import src.cloneDetection as Ccd
from src import constants as const


def manage_args() -> (str, str):
    argParser = argparse.ArgumentParser(prog='ProSmart', description='ProSmart: Vulnerable Code Clone Detection '
                                                                     'in Propagated Smart Contracts')

    argParser.add_argument('--version', '-v', action='version', version=const.version)
    argParser.add_argument('--input_path', '-i', required=True, help='tell us the file path to '
                                                                     'the Solidity code you wish to verify. ')
    argParser.add_argument('--output_path', '-o', required=True, help='tell us the directory path to which '
                                                                      'you wish to have the result saved into. ')
    args = argParser.parse_args()

    if args.__contains__('version'):
        print("v0.1.0")
    else:
        return args.input_path, args.output_path


if __name__ == '__main__':
    # 1. args: version, input file path, output file path
    input_path, output_path = manage_args()

    # 2. read vdb file and structure data as obj
    vdb = json.load(open(const.path_vdb, 'r'))

    # 3. parse functions from input source code
    input_funcs, input_func_names, input_contract_names = Ccd.parse_functions(open(input_path, 'r').read())

    # 4. compare vdb functions vs parsed functions
    vuln_funcs = [i['Svccd'] for i in vdb]
    detected_funcs = []
    for function, func_name in zip(input_funcs, input_func_names):
        function = function.strip()

        func_hash = None
        if func_name not in input_contract_names:
            func_hash = Ccd.run_vccd(function)

        # 5. structure detected functions data
        if (func_hash is not None) and (func_hash in vuln_funcs):
            detected_func = dict()
            detected_func['function_name'] = func_name
            detected_func['function_code'] = function

            detected_func['cve_ids'] = list()
            detected_func['vulnerability_types'] = set()

            vulns = filter(lambda x: x['Svccd'] == func_hash, vdb)
            for i in vulns:
                detected_func['cve_ids'].append(i['cve_id'])
                detected_func['vulnerability_types'].add(i['VulnType'])

            detected_func['vulnerability_types'] = list(detected_func['vulnerability_types'])
            detected_funcs.append(detected_func)

    # 6. save output file
    if len(detected_funcs):
        if not os.path.exists(output_path):
            os.makedirs(output_path)
        output_path = os.path.join(output_path, input_path.split('/')[-1].split('.')[0] + '.json')
        with open(output_path, "w", encoding='UTF-8') as f:
            json.dump(detected_funcs, f)

    # 7. return execution terminated message
    print("Execution terminated succesfully. Check your output path. ")

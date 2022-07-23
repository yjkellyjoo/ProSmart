# ProSmart: *Pro*pagated Vulnerable *Smart* Contracts Code Clone Detection for Solidity
Using [Solidity-complete-parser](https://github.com/yjkellyjoo/Solidity-complete-parser),
this python-based tool reads a .sol file, analyzes the received file and returns the code's vulnerability information if detected.

### Prerequisites
#### Python 3
Python version 3.8.X (I have used 3.8.9) with [antlr4-python3-runtime](https://pypi.org/project/antlr4-python3-runtime/) package installed.
```sh
$ pip install antlr4-python3-runtime

or

$ pip install -r ./requirements.txt
```

## Usage
Run `run.py`, with INPUT_PATH and OUTPUT_PATH arguments.
```
optional arguments:
  -h, --help            show this help message and exit
  --version, -v         show program's version number and exit
  --input_path INPUT_PATH, -i INPUT_PATH
                        tell us the file path to the Solidity code you wish to verify.
  --output_path OUTPUT_PATH, -o OUTPUT_PATH
                        tell us the directory path to which you wish to have the result saved into.
```

### Usage example
A sample input file is included in the `input` directory.

Sample execution:
```
$ python run.py -i input/sample_vuln.sol -o output/
```


Output is given in JSON format, with the following information:
* `function_name`: detected vulnerable function name
* `function_code`: function source code
* `lines`: function's line number range in the given source code
* `cve_ids`: vulnerability's related CVEs' ID
* `vulnerability_types`: detected vulnerability type: 'IntegerOverflow', 'ReplayAttack', 'ImproperInputValidation', 'FunctionVisibility', 'InsufficientlyRandomValues', 'UnprotectedOwnershipTransfer', 'TradeTrap', 'PRNG', or  'IncorrectCalculation'.
Can be multiple values.

Sample output:
```
[
  {
    "function_name": "batchTransfer",
    "function_code": "function batchTransfer ( address [ ] _receivers , uint256 _value ) public whenNotPaused returns ( bool ) { uint cnt = _receivers . length ; uint256 amount = uint256 ( cnt ) * _value ; require ( cnt > 0 && cnt <= 20 ) ; require ( _value > 0 && balances [ msg . sender ] >= amount ) ; balances [ msg . sender ] = balances [ msg . sender ] . sub ( amount ) ; for ( uint i = 0 ; i < cnt ; i ++ ) { balances [ _receivers [ i ] ] = balances [ _receivers [ i ] ] . add ( _value ) ; Transfer ( msg . sender , _receivers [ i ] , _value ) ; } return true ; }",
    "lines": [259, 271],
    "cve_ids": ["CVE-2018-10299"],
    "vulnerability_types": ["IntegerOverflow"]
  }
]
```

import os
from pathlib import Path
cwd = Path(os.getcwd())
test_dir = str(cwd/"unit_tests").replace('\\', '/')
def run_test(feature_file_name):
    from behave import __main__
    test_command = test_dir+" -i "+feature_file_name
    __main__.main(test_command)

run_test("unit_tests/rule_process.feature")

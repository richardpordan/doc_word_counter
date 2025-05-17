"""Unit tests"""


import sys
import unittest
import importlib.util


# -------------------- Import main module -------------------------------------
spec = importlib.util.spec_from_file_location("wordcounter", "wordcounter.py")
main_module = importlib.util.module_from_spec(spec)
sys.modules["wordcounter"] = main_module
spec.loader.exec_module(main_module)
wcounter = main_module.WordCounter()


# -------------------- Custom context manager for cli func --------------------
class SysArgvContext:
    def __init__(self, args: list):
        self.args = args
        self.sys_argv_backup = sys.argv

    def __enter__(self):
        sys.argv = [self.sys_argv_backup[0]] + self.args
        return self.args

    def __exit__(self, exc_type, exc_value, traceback):
        sys.argv = self.sys_argv_backup


# -------------------- Define tests -------------------------------------------
class TestWordCounter(unittest.TestCase):

    def test_0_count_words(self):
        for file_path in TEST_FILES:
            self.assertEqual(wcounter.count_words(file_path), CORRECT_COUNT)
            print("Tested `count_words` on", file_path)

    # test case function to check the Person.get_name function
    def test_1_cli_run(self):
        for file_path in TEST_FILES:
            with SysArgvContext([file_path]) as custom_args:
                wcounter.cli_run()
                print("Tested `cli_run` on", custom_args)
                for target in TEST_TARGETS:
                    with SysArgvContext([file_path, target]) as custom_args:
                        wcounter.cli_run()
                        print("cli_run tested on", custom_args)


if __name__ == '__main__':
    # -------------------- Set up constants ---------------------------------------
    CORRECT_COUNT = 16
    TEST_FILES = ["./test/data/test_file.ipynb", "./test/data/test_file.md"]
    TEST_TARGETS = [10, 20]
    # -------------------- Run ----------------------------------------------------
    unittest.main()

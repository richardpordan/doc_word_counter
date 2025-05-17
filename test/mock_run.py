"""WIP playground"""

import sys
import importlib.util


spec = importlib.util.spec_from_file_location("wordcounter", "wordcounter.py")
main_module = importlib.util.module_from_spec(spec)
sys.modules["wordcounter"] = main_module
spec.loader.exec_module(main_module)

wcounter = main_module.WordCounter()

CORRECT_COUNT = 16
TEST_FILES = ["./test/data/test_file.ipynb", "./test/data/test_file.md"]
TEST_TARGETS = [10, 20]
OLD_SYS_ARGV = sys.argv

for file_path in TEST_FILES:
    assert(wcounter.count_words(file_path) == 16)
    print("count_words tested on", file_path)

    args = [file_path]
    sys.argv = [OLD_SYS_ARGV[0]] + args
    wcounter.cli_run()
    print("cli_run tested on", args)
    sys.argv = OLD_SYS_ARGV
    
    for target in TEST_TARGETS:
        args = [file_path, target]
        sys.argv = [OLD_SYS_ARGV[0]] + args
        wcounter.cli_run()
        print("cli_run tested on", args)
        sys.argv = OLD_SYS_ARGV

"""ipynb word counter tool"""

import sys
import re
import json
from pathlib import Path


def _json_to_md(json_data) -> list:
    extracted_md = map(
        lambda x: x["source"] if x["cell_type"] == "markdown" else [],
        json_data["cells"],
    )
    all_content = []
    for content in extracted_md:
        all_content.extend(content)

    return all_content


def _drop_headings_and_html(all_content) -> list:
    filtd_content = []

    for text_string in all_content:

        if any([re.search(".*<.*>.*", text_string), re.search("^#.*", text_string)]):
            result = None
        else:
            result = text_string

        if result:
            if result != "\n":
                filtd_content.append(result)

    return filtd_content


def _remove_all_mdlatex(text):
    output = re.sub("\\$\\$.*?(?<!\\\\)\\$\\$", "", text)
    output = re.sub("\\$.*?(?<!\\\\)\\$", "", output)

    return output


def count_words(notebook_path):
    """Word counter main func.

    Takes an ipynb notebook path, selects markdown cells,
    cleans text arbitrarily, returns the count of words.
    """

    if not Path(notebook_path).is_file():
        raise FileNotFoundError(f"File {notebook_path} not found")

    # Open file and load as json
    with open(Path(notebook_path), encoding="utf-8") as infile:
        data = json.load(infile)

    # From json, filter markdown cells,
    # returning a list of strings
    all_content = _json_to_md(data)

    # Drop everything after references
    ref_index = all_content.index("## References\n")
    all_content = all_content[0:ref_index]

    # Drop html and markdown headingss
    filtd_content = _drop_headings_and_html(all_content)

    # Drop newlines and join list into one string
    joined_content = re.sub(r"\n", "", " ".join(filtd_content))

    # Remove MD latex
    clean_content = _remove_all_mdlatex(joined_content)

    # Work out final count
    clean = clean_content.split(" ")

    final = [word for word in clean if (len(word) > 1 or word == "a" or word == "a,")]
    final_count = len(final)

    return final_count


if __name__ == "__main__":
    print("----------------- Result count: -----------------")
    count = count_words(sys.argv[1])
    print("Count of words in cleaned markdown text: ")
    print(count)
    print("-------------------------------------------------")

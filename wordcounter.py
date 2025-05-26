"""Doc word counter tool"""

import os
import sys
import re
import json
import itertools
from pathlib import Path

from rich.console import Console
from rich.panel import Panel


class WordCounter():

    def __init__(self):
        self.encoding = "utf-8"
        self.printer = Console()
        self.path = None
        self.ext = None


    def _setup_file_path(self, file_path) -> None:
        self.path = Path(file_path)
        
        if not self.path.is_file():
            raise FileNotFoundError(f"File {file_path} not found")

        file_name, file_ext = os.path.splitext(file_path)
        self.ext = file_ext.lstrip('.').lower()

        if self.ext not in ["ipynb", "md", "qmd"]:
            raise Exception("Only `ipynb` and `md`/`qmd` files are supported.")


    def _json_to_list(self, json_data) -> list:
        extracted = map(
            lambda x: x["source"] if x["cell_type"] == "markdown" else [],
            json_data["cells"],
        )
        unnested = list(itertools.chain.from_iterable(extracted))

        return unnested


    def _open_file_as_text(self) -> str:
        if self.ext == "ipynb":
            # Open file and load as json
            with open(self.path, encoding=self.encoding) as infile:
                json_data = json.load(infile)
            # From json, filter markdown cells,
            # returning a list of strings
            data = self._json_to_list(json_data)
            # Join into one string
            raw_doc = " ".join(data)

        if self.ext in ["md", "qmd"]:
            # open md as text file
            with open(self.path, encoding=self.encoding) as infile:
                raw_doc = infile.read()

        return raw_doc


    def _rgx_clean(self, doc) -> str:
        # Turn new lines into spaces (for good reason)
        doc = re.sub(r"\n", " ", doc)
        # Remove supported html includding inner
        doc = re.sub(r"(<table(.*(>).*)</table>)", "", doc)
        doc = re.sub(r"<img[^>]*>", "", doc)
        doc = re.sub(r"(<p(.*(>).*)</p>)", "", doc)
        doc = re.sub(r"(<div(.*(>).*)</div>)", "", doc)
        # Remove anything after and including references md heading
        doc = re.sub(r"([#]{2,5}\s{0,2}References).*", "", doc)
        doc = re.sub(r"[#]{1,5}\s?\w*(?=\s)", "", doc)
        # Remove latex equations
        doc = re.sub("\\$\\$.*?(?<!\\\\)\\$\\$", "", doc)
        doc = re.sub("\\$.*?(?<!\\\\)\\$", "", doc)
        # Remove any standalone char that isn't the word "a" 
        # or a digit - if preceded AND followed by space
        doc = re.sub(r"(?<=\s)[^a\d]{1}(?=\s)", " ", doc)
        # Groups of 2 or more spaces into one space
        doc = re.sub(r"\s{2,}", " ", doc)
        # Remove trailing spaces
        doc = re.sub(r"\s?$", "", doc)
        doc = re.sub(r"^\s?", "", doc)

        return doc


    def count_words(self, file_path: Path | str | None = None) -> int:
        """Function that works out word counts"""
        if not file_path:
            raise ValueError("`file_path` is a required argument.")

        self._setup_file_path(file_path)

        raw_doc = self._open_file_as_text()
        doc = self._rgx_clean(raw_doc)

        count = len(doc.split(" "))

        return count

    
    def cli_run(self) -> None:
        """Use when ran from terminal"""
        file_path = sys.argv[1]
        if len(sys.argv) > 2:
            target = int(sys.argv[2])
        else: 
            target = None

        count = self.count_words(file_path)

        output = f"Word count in '{str(self.path)}':"
        if target and (count > target):
            output += f"\n[bold red]{count}"
            output += f"\n[red]Over the target {target} :("
        elif target and (count < target):
            output += f"\n[bold green]{count}"
            output += f"\n[green]Under the target {target} :)"
        else:
            output += f"\n[bold yellow]{count}"

        self.printer.print(Panel(
            output, 
            title="Doc Word Counter"
        ))


if __name__ == "__main__":
    wcounter = WordCounter()
    wcounter.cli_run()

# ipynb_word_counter

[![QA and test](https://github.com/richardpordan/doc_word_counter/actions/workflows/qa.yml/badge.svg?branch=main)](https://github.com/richardpordan/doc_word_counter/actions/workflows/qa.yml)
[![Build package](https://github.com/richardpordan/doc_word_counter/actions/workflows/build.yml/badge.svg)](https://github.com/richardpordan/doc_word_counter/actions/workflows/build.yml)

Word counter for assignments in `.ipynb` or `.md` formats. 

For personal use and not in active development.

## Requirements

In ipynb, only reads markdown cells. In both MD and ipynb, the following aren't counted:

- html imgs
- html tables
- p and div html tags and inner content
- latex eqs are removed
- references are removed

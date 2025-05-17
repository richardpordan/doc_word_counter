# doc_word_counter

[![QA and test](https://github.com/richardpordan/doc_word_counter/actions/workflows/qa.yml/badge.svg?branch=main)](https://github.com/richardpordan/doc_word_counter/actions/workflows/qa.yml)
[![Build package](https://github.com/richardpordan/doc_word_counter/actions/workflows/build.yml/badge.svg)](https://github.com/richardpordan/doc_word_counter/actions/workflows/build.yml)

Word counter for assignments in `.ipynb` or `.md` formats. 

For personal use and not in active development.

## Features

In ipynb, only reads markdown cells. In both MD and ipynb, the following aren't counted:

- html img elements
- html tables and their inner content
- p and div html tags and their inner content
- latex equations (either inline or newline)
- md headers 
- "references" header and everything that comes after

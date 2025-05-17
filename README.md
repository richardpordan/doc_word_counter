# ipynb_word_counter

Word counter for assignments in `.ipynb` or `.md` formats. 

For personal use and not in active development.

## Requirements

In ipynb, only reads markdown cells. In both MD and ipynb, the following aren't counted:

- html imgs
- html tables
- p and div html tags and inner content
- latex eqs are removed
- references are removed

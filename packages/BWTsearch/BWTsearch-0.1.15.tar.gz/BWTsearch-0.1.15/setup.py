from distutils.core import setup

long_description = """
**Burrows Wheeler Transform (BWT) search**

Import the `BWT` class into your namespace for convenience:

```
from BWTsearch import BWT
```

Initialize a BWT of text with instantiating the BWT class:

```
text = "AGATA"
```

```
bwt = BWT(text)
```

The instance bwt now will contain all necessary indices for efficiently searching:

- `bwt.bwt` ... contains the BWT string
- `bwt.position_list` ... contains the start positions of the rotations for each character of bwt
- `bwt.ranks` ... contains rank indices for each character of the alphabet in bwt
- `bwt.cnums` ... contains number of character occurances of the alphabet in bwt

Use the `search()` function to obtain a list of positions of exact matches for pattern in text:

```
pattern = "AT"
```

```
bwt.search(pattern)
```

This returns a list with indexes into text where an exact match occurs. Empty list if none.
The pattern will be searched case-sensitive and should not contain $.

Use the `get_text()` function to retrieve the original text from the BWT instance:

```
bwt.get_text()
```

If a sequence file is available, a genome can be loaded from a FASTA file:

```
phix = BWT.from_fast_file("phix.fa")
```

```
phix.search("AGATA")
```
"""

setup(
  name = 'BWTsearch',         # How you named your package folder (MyLib)
  packages = ['BWTsearch'],   # Chose the same as "name"
  version = '0.1.15',      # Start with a small number and increase it with every change you make
  license='MIT',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
  description = 'Burrows Wheeler Transform (BWT) search',   # Give a short description about your library
  long_description=long_description,
  long_description_content_type="text/markdown",
)

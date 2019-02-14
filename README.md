# Python Script Utilities

Utility functions for python scripts (especially for research experiments) that
I use across projects.


## Most common usage

Most of the time, I write scripts that write some output to an output directory.
The most common way I use this package is as follows:

```python
import argparse
import logging

from script_utils.common import common_setup

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('output_dir')
    args = parser.parse_args()

    common_setup(script_name=__file__, output_dir=args.output_dir, args=args)

    logging.info('Ready!')
```

The common_setup function above currently takes care of the following:
    - **Setup logging** to standard out as well as to a file in the output
      directory.
    - **Log args** in a pretty format using pprint
    - **Save git state** to the output directory, using
        https://github.com/achalddave/git-state

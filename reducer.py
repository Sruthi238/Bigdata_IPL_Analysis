#!/usr/bin/env python
"""reducer.py"""

from operator import itemgetter
import sys

current_bat = None
current_bowl = None
current_count = 0
bat = None
bowl = None

# input comes from STDIN
for line in sys.stdin:
    # remove leading and trailing whitespace
    line = line.strip()

    # parse the input we got from mapper.py
    bat,bowl, count = line.split('\t', 2)

    # convert count (currently a string) to int
    try:
        count = int(count)
    except ValueError:
        # count was not a number, so silently
        # ignore/discard this line
        continue

    # this IF-switch only works because Hadoop sorts map output
    # by key (here: word) before it is passed to the reducer
    if current_bat == bat and current_bowl == bowl:
        current_count += count
    else:
        if current_bat and current_bowl == bowl:
            # write result to STDOUT
            print '%s\t%s\t%s' % (current_bat,current_bowl, current_count)
        current_count = count
        current_bat = bat
	current_bowl = bowl

# do not forget to output the last word if needed!
if current_bat == bat and current_bowl == bowl:
    print '%s\t%s\t%s' % (current_bat,current_bowl, current_count)


try:
    from itertools import zip_longest
except ImportError:
    from itertools import izip_longest as zip_longest

try:
    range = xrange
except NameError:
    range = range

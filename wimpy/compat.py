try:
    from itertools import zip_longest
except NameError:
    from itertools import izip_longest as zip_longest

#!/usr/bin/python3
"""
Main script to test Task 3: Lazy loading paginated users.
"""

import sys
lazy_paginator = __import__('2-lazy_paginate').lazy_paginate

# fetch and print users in pages of 100
try:
    for page in lazy_paginator(100):
        for user in page:
            print(user)
except BrokenPipeError:
    sys.stderr.close()

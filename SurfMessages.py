# File: SurfMessages.py
# Author: Georgiana Ogrean
#
# Errors and warnings raised by SurfFit.

import textwrap as tw

def remove_whitespace(text):
    return " ".join(text.split())

def ErrorMessages(error_number):
    errors = {
        '001': '''Too few net counts in the region.
            Enlarge the region or lower the minimum
            count threshold.''',
        '002': '''Currently only region files with one
            region defined in image coordinates are supported.'''
    }
    return tw.fill(remove_whitespace(errors[error_number]), 80)

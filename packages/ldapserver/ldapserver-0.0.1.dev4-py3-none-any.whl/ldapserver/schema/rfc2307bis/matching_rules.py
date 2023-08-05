
# pylint: disable=wildcard-import,unused-wildcard-import

from ..rfc4524.matching_rules import *
from ..rfc3112.matching_rules import ALL as RFC3112_ALL

ALL = ALL + RFC3112_ALL

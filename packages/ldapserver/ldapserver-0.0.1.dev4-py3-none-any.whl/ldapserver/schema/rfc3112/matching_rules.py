
# pylint: disable=unused-import

from ..types import MatchingRule
from ..rfc4517.matching_rules import caseIgnoreIA5Match
from . import syntaxes

authPasswordExactMatch = MatchingRule('1.3.6.1.4.1.4203.1.2.2', name='authPasswordExactMatch', desc='authentication password exact matching rule', syntax=syntaxes.AuthPasswordSyntax())

# We won't implement any actual schemes here, so the default behaviour of MatchingRule (return UNDEFINED) is fine.
authPasswordMatch = MatchingRule('1.3.6.1.4.1.4203.1.2.3', name='authPasswordMatch', desc='authentication password matching rule', syntax=syntaxes.OctetString(128))

ALL = (
	authPasswordExactMatch,
	authPasswordMatch,
)

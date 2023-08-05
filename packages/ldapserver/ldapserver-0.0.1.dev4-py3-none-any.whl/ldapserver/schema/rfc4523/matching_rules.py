from ..types import MatchingRule
from . import syntaxes

certificateExactMatch = MatchingRule('2.5.13.34', name='certificateExactMatch', desc='X.509 Certificate Exact Match', syntax=syntaxes.X509CertificateExactAssertion())

ALL = (
	certificateExactMatch,
)

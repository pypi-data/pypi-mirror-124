from ..types import AttributeType
from . import syntaxes, matching_rules

userCertificate = AttributeType('2.5.4.36', name='userCertificate', desc='X.509 user certificate', equality=matching_rules.certificateExactMatch, syntax=syntaxes.X509Certificate())

ALL = (
	userCertificate,
)

from ..types import AttributeType, AttributeTypeUsage
from . import syntaxes, matching_rules

supportedAuthPasswordSchemes = AttributeType('1.3.6.1.4.1.4203.1.3.3', name='supportedAuthPasswordSchemes', desc='supported password storage schemes', equality=matching_rules.caseIgnoreIA5Match, syntax=syntaxes.IA5String(32), usage=AttributeTypeUsage.dSAOperation)
authPassword = AttributeType('1.3.6.1.4.1.4203.1.3.4', name='authPassword', desc='password authentication information', equality=matching_rules.authPasswordExactMatch, syntax=syntaxes.AuthPasswordSyntax())

ALL = (
	supportedAuthPasswordSchemes,
	authPassword,
)

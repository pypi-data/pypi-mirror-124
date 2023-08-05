from ..types import AttributeType
from . import syntaxes, matching_rules

labeledURI = AttributeType('1.3.6.1.4.1.250.1.57', name='labeledURI', desc='Uniform Resource Identifier with optional label', equality=matching_rules.caseExactMatch, syntax=syntaxes.DirectoryString())

ALL = (
	labeledURI,
)

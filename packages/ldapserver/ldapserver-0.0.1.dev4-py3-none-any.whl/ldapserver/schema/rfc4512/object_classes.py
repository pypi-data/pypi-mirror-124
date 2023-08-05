from ..types import ObjectClass, ObjectClassKind
from . import attribute_types

top = ObjectClass('2.5.6.0', 'top', kind=ObjectClassKind.ABSTRACT, must=[attribute_types.objectClass])
alias = ObjectClass('2.5.6.1', 'alias', sup=top, kind=ObjectClassKind.STRUCTURAL, must=[attribute_types.aliasedObjectName])
subschema = ObjectClass('2.5.20.1', 'subschema', kind=ObjectClassKind.AUXILIARY, may=[attribute_types.dITStructureRules, attribute_types.nameForms, attribute_types.dITContentRules, attribute_types.objectClasses, attribute_types.attributeTypes, attribute_types.matchingRules, attribute_types.matchingRuleUse])
extensibleObject = ObjectClass('1.3.6.1.4.1.1466.101.120.111', 'extensibleObject', sup=top, kind=ObjectClassKind.AUXILIARY)

ALL = (
	top,
	alias,
	subschema,
	extensibleObject,
)

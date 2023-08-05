from ..types import AttributeType, AttributeTypeUsage
from . import syntaxes, matching_rules

aliasedObjectName = AttributeType('2.5.4.1', name='aliasedObjectName', equality=matching_rules.distinguishedNameMatch, syntax=syntaxes.DN(), single_value=True)
objectClass = AttributeType('2.5.4.0', name='objectClass', equality=matching_rules.objectIdentifierMatch, syntax=syntaxes.OID())
creatorsName = AttributeType('2.5.18.3', name='creatorsName', equality=matching_rules.distinguishedNameMatch, syntax=syntaxes.DN(), single_value=True, no_user_modification=True, usage=AttributeTypeUsage.directoryOperation)
createTimestamp = AttributeType('2.5.18.1', name='createTimestamp', equality=matching_rules.generalizedTimeMatch, ordering=matching_rules.generalizedTimeOrderingMatch, syntax=syntaxes.GeneralizedTime(), single_value=True, no_user_modification=True, usage=AttributeTypeUsage.directoryOperation)
modifiersName = AttributeType('2.5.18.4', name='modifiersName', equality=matching_rules.distinguishedNameMatch, syntax=syntaxes.DN(), single_value=True, no_user_modification=True, usage=AttributeTypeUsage.directoryOperation)
modifyTimestamp = AttributeType('2.5.18.2', name='modifyTimestamp', equality=matching_rules.generalizedTimeMatch, ordering=matching_rules.generalizedTimeOrderingMatch, syntax=syntaxes.GeneralizedTime(), single_value=True, no_user_modification=True, usage=AttributeTypeUsage.directoryOperation)
structuralObjectClass = AttributeType('2.5.21.9', name='structuralObjectClass', equality=matching_rules.objectIdentifierMatch, syntax=syntaxes.OID(), single_value=True, no_user_modification=True, usage=AttributeTypeUsage.directoryOperation)
governingStructureRule = AttributeType('2.5.21.10', name='governingStructureRule', equality=matching_rules.integerMatch, syntax=syntaxes.INTEGER(), single_value=True, no_user_modification=True, usage=AttributeTypeUsage.directoryOperation)
subschemaSubentry = AttributeType('2.5.18.10', name='subschemaSubentry', equality=matching_rules.distinguishedNameMatch, syntax=syntaxes.DN(), single_value=True, no_user_modification=True, usage=AttributeTypeUsage.directoryOperation)
objectClasses = AttributeType('2.5.21.6', name='objectClasses', equality=matching_rules.objectIdentifierFirstComponentMatch, syntax=syntaxes.ObjectClassDescription(), usage=AttributeTypeUsage.directoryOperation)
attributeTypes = AttributeType('2.5.21.5', name='attributeTypes', equality=matching_rules.objectIdentifierFirstComponentMatch, syntax=syntaxes.AttributeTypeDescription(), usage=AttributeTypeUsage.directoryOperation)
matchingRules = AttributeType('2.5.21.4', name='matchingRules', equality=matching_rules.objectIdentifierFirstComponentMatch, syntax=syntaxes.MatchingRuleDescription(), usage=AttributeTypeUsage.directoryOperation)
matchingRuleUse = AttributeType('2.5.21.8', name='matchingRuleUse', equality=matching_rules.objectIdentifierFirstComponentMatch, syntax=syntaxes.MatchingRuleUseDescription(), usage=AttributeTypeUsage.directoryOperation)
ldapSyntaxes = AttributeType('1.3.6.1.4.1.1466.101.120.16', name='ldapSyntaxes', equality=matching_rules.objectIdentifierFirstComponentMatch, syntax=syntaxes.LDAPSyntaxDescription(), usage=AttributeTypeUsage.directoryOperation)
dITContentRules = AttributeType('2.5.21.2', name='dITContentRules', equality=matching_rules.objectIdentifierFirstComponentMatch, syntax=syntaxes.DITContentRuleDescription(), usage=AttributeTypeUsage.directoryOperation)
dITStructureRules = AttributeType('2.5.21.1', name='dITStructureRules', equality=matching_rules.integerFirstComponentMatch, syntax=syntaxes.DITStructureRuleDescription(), usage=AttributeTypeUsage.directoryOperation)
nameForms = AttributeType('2.5.21.7', name='nameForms', equality=matching_rules.objectIdentifierFirstComponentMatch, syntax=syntaxes.NameFormDescription(), usage=AttributeTypeUsage.directoryOperation)
altServer = AttributeType('1.3.6.1.4.1.1466.101.120.6', name='altServer', syntax=syntaxes.IA5String(), usage=AttributeTypeUsage.dSAOperation)
namingContexts = AttributeType('1.3.6.1.4.1.1466.101.120.5', name='namingContexts', syntax=syntaxes.DN(), usage=AttributeTypeUsage.dSAOperation)
supportedControl = AttributeType('1.3.6.1.4.1.1466.101.120.13', name='supportedControl', syntax=syntaxes.OID(), usage=AttributeTypeUsage.dSAOperation)
supportedExtension = AttributeType('1.3.6.1.4.1.1466.101.120.7', name='supportedExtension', syntax=syntaxes.OID(), usage=AttributeTypeUsage.dSAOperation)
supportedFeatures = AttributeType('1.3.6.1.4.1.4203.1.3.5', name='supportedFeatures', equality=matching_rules.objectIdentifierMatch, syntax=syntaxes.OID(), usage=AttributeTypeUsage.dSAOperation)
supportedLDAPVersion = AttributeType('1.3.6.1.4.1.1466.101.120.15', name='supportedLDAPVersion', syntax=syntaxes.INTEGER(), usage=AttributeTypeUsage.dSAOperation)
supportedSASLMechanisms = AttributeType('1.3.6.1.4.1.1466.101.120.14', name='supportedSASLMechanisms', syntax=syntaxes.DirectoryString(), usage=AttributeTypeUsage.dSAOperation)

ALL = (
	aliasedObjectName,
	objectClass,
	creatorsName,
	createTimestamp,
	modifiersName,
	modifyTimestamp,
	structuralObjectClass,
	governingStructureRule,
	subschemaSubentry,
	objectClasses,
	attributeTypes,
	matchingRules,
	matchingRuleUse,
	ldapSyntaxes,
	dITContentRules,
	dITStructureRules,
	nameForms,
	altServer,
	namingContexts,
	supportedControl,
	supportedExtension,
	supportedFeatures,
	supportedLDAPVersion,
	supportedSASLMechanisms,
)

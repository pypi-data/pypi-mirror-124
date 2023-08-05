
# pylint: disable=wildcard-import,unused-wildcard-import

from ..types import AttributeType
from ..rfc4512.attribute_types import *
from . import syntaxes, matching_rules

name = AttributeType('2.5.4.41', name='name', equality=matching_rules.caseIgnoreMatch, substr=matching_rules.caseIgnoreSubstringsMatch, syntax=syntaxes.DirectoryString()) # Defined first, so sup=name works
businessCategory = AttributeType('2.5.4.15', name='businessCategory', equality=matching_rules.caseIgnoreMatch, substr=matching_rules.caseIgnoreSubstringsMatch, syntax=syntaxes.DirectoryString())
c = AttributeType('2.5.4.6', name='c', sup=name, syntax=syntaxes.CountryString(), single_value=True)
cn = AttributeType('2.5.4.3', name='cn', sup=name)
dc = AttributeType('0.9.2342.19200300.100.1.25', name='dc', equality=matching_rules.caseIgnoreIA5Match, substr=matching_rules.caseIgnoreIA5SubstringsMatch, syntax=syntaxes.IA5String(), single_value=True)
description = AttributeType('2.5.4.13', name='description', equality=matching_rules.caseIgnoreMatch, substr=matching_rules.caseIgnoreSubstringsMatch, syntax=syntaxes.DirectoryString())
destinationIndicator = AttributeType('2.5.4.27', name='destinationIndicator', equality=matching_rules.caseIgnoreMatch, substr=matching_rules.caseIgnoreSubstringsMatch, syntax=syntaxes.PrintableString())
distinguishedName = AttributeType('2.5.4.49', name='distinguishedName', equality=matching_rules.distinguishedNameMatch, syntax=syntaxes.DN())
dnQualifier = AttributeType('2.5.4.46', name='dnQualifier', equality=matching_rules.caseIgnoreMatch, ordering=matching_rules.caseIgnoreOrderingMatch, substr=matching_rules.caseIgnoreSubstringsMatch, syntax=syntaxes.PrintableString())
enhancedSearchGuide = AttributeType('2.5.4.47', name='enhancedSearchGuide', syntax=syntaxes.EnhancedGuide())
facsimileTelephoneNumber = AttributeType('2.5.4.23', name='facsimileTelephoneNumber', syntax=syntaxes.FacsimileTelephoneNumber())
generationQualifier = AttributeType('2.5.4.44', name='generationQualifier', sup=name)
givenName = AttributeType('2.5.4.42', name='givenName', sup=name)
houseIdentifier = AttributeType('2.5.4.51', name='houseIdentifier', equality=matching_rules.caseIgnoreMatch, substr=matching_rules.caseIgnoreSubstringsMatch, syntax=syntaxes.DirectoryString())
initials = AttributeType('2.5.4.43', name='initials', sup=name)
internationalISDNNumber = AttributeType('2.5.4.25', name='internationalISDNNumber', equality=matching_rules.numericStringMatch, substr=matching_rules.numericStringSubstringsMatch, syntax=syntaxes.NumericString())
l = AttributeType('2.5.4.7', name='l', sup=name)
member = AttributeType('2.5.4.31', name='member', sup=distinguishedName)
o = AttributeType('2.5.4.10', name='o', sup=name)
ou = AttributeType('2.5.4.11', name='ou', sup=name)
owner = AttributeType('2.5.4.32', name='owner', sup=distinguishedName)
physicalDeliveryOfficeName = AttributeType('2.5.4.19', name='physicalDeliveryOfficeName', equality=matching_rules.caseIgnoreMatch, substr=matching_rules.caseIgnoreSubstringsMatch, syntax=syntaxes.DirectoryString())
postalAddress = AttributeType('2.5.4.16', name='postalAddress', equality=matching_rules.caseIgnoreListMatch, substr=matching_rules.caseIgnoreListSubstringsMatch, syntax=syntaxes.PostalAddress())
postalCode = AttributeType('2.5.4.17', name='postalCode', equality=matching_rules.caseIgnoreMatch, substr=matching_rules.caseIgnoreSubstringsMatch, syntax=syntaxes.DirectoryString())
postOfficeBox = AttributeType('2.5.4.18', name='postOfficeBox', equality=matching_rules.caseIgnoreMatch, substr=matching_rules.caseIgnoreSubstringsMatch, syntax=syntaxes.DirectoryString())
preferredDeliveryMethod = AttributeType('2.5.4.28', name='preferredDeliveryMethod', syntax=syntaxes.DeliveryMethod(), single_value=True)
registeredAddress = AttributeType('2.5.4.26', name='registeredAddress', sup=postalAddress, syntax=syntaxes.PostalAddress())
roleOccupant = AttributeType('2.5.4.33', name='roleOccupant', sup=distinguishedName)
searchGuide = AttributeType('2.5.4.14', name='searchGuide', syntax=syntaxes.Guide())
seeAlso = AttributeType('2.5.4.34', name='seeAlso', sup=distinguishedName)
serialNumber = AttributeType('2.5.4.5', name='serialNumber', equality=matching_rules.caseIgnoreMatch, substr=matching_rules.caseIgnoreSubstringsMatch, syntax=syntaxes.PrintableString())
sn = AttributeType('2.5.4.4', name='sn', sup=name)
st = AttributeType('2.5.4.8', name='st', sup=name)
street = AttributeType('2.5.4.9', name='street', equality=matching_rules.caseIgnoreMatch, substr=matching_rules.caseIgnoreSubstringsMatch, syntax=syntaxes.DirectoryString())
telephoneNumber = AttributeType('2.5.4.20', name='telephoneNumber', equality=matching_rules.telephoneNumberMatch, substr=matching_rules.telephoneNumberSubstringsMatch, syntax=syntaxes.TelephoneNumber())
teletexTerminalIdentifier = AttributeType('2.5.4.22', name='teletexTerminalIdentifier', syntax=syntaxes.TeletexTerminalIdentifier())
telexNumber = AttributeType('2.5.4.21', name='telexNumber', syntax=syntaxes.TelexNumber())
title = AttributeType('2.5.4.12', name='title', sup=name)
uid = AttributeType('0.9.2342.19200300.100.1.1', name='uid', equality=matching_rules.caseIgnoreMatch, substr=matching_rules.caseIgnoreSubstringsMatch, syntax=syntaxes.DirectoryString())
uniqueMember = AttributeType('2.5.4.50', name='uniqueMember', equality=matching_rules.uniqueMemberMatch, syntax=syntaxes.NameAndOptionalUID())
userPassword = AttributeType('2.5.4.35', name='userPassword', equality=matching_rules.octetStringMatch, syntax=syntaxes.OctetString())
x121Address = AttributeType('2.5.4.24', name='x121Address', equality=matching_rules.numericStringMatch, substr=matching_rules.numericStringSubstringsMatch, syntax=syntaxes.NumericString())
x500UniqueIdentifier = AttributeType('2.5.4.45', name='x500UniqueIdentifier', equality=matching_rules.bitStringMatch, syntax=syntaxes.BitString())

ALL = ALL + (
	name,
	businessCategory,
	c,
	cn,
	dc,
	description,
	destinationIndicator,
	distinguishedName,
	dnQualifier,
	enhancedSearchGuide,
	facsimileTelephoneNumber,
	generationQualifier,
	givenName,
	houseIdentifier,
	initials,
	internationalISDNNumber,
	l,
	member,
	o,
	ou,
	owner,
	physicalDeliveryOfficeName,
	postalAddress,
	postalCode,
	postOfficeBox,
	preferredDeliveryMethod,
	registeredAddress,
	roleOccupant,
	searchGuide,
	seeAlso,
	serialNumber,
	sn,
	st,
	street,
	telephoneNumber,
	teletexTerminalIdentifier,
	telexNumber,
	title,
	uid,
	uniqueMember,
	userPassword,
	x121Address,
	x500UniqueIdentifier,
)

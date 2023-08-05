
# pylint: disable=wildcard-import,unused-wildcard-import

from ..types import AttributeType
from ..rfc4519.attribute_types import *
from . import syntaxes, matching_rules

associatedDomain = AttributeType('0.9.2342.19200300.100.1.37', name='associatedDomain', equality=matching_rules.caseIgnoreIA5Match, substr=matching_rules.caseIgnoreIA5SubstringsMatch, syntax=syntaxes.IA5String())
associatedName = AttributeType('0.9.2342.19200300.100.1.38', name='associatedName', equality=matching_rules.distinguishedNameMatch, syntax=syntaxes.DN())
buildingName = AttributeType('0.9.2342.19200300.100.1.48', name='buildingName', equality=matching_rules.caseIgnoreMatch, substr=matching_rules.caseIgnoreSubstringsMatch, syntax=syntaxes.DirectoryString(256))
co = AttributeType('0.9.2342.19200300.100.1.43', name='co', equality=matching_rules.caseIgnoreMatch, substr=matching_rules.caseIgnoreSubstringsMatch, syntax=syntaxes.DirectoryString())
documentAuthor = AttributeType('0.9.2342.19200300.100.1.14', name='documentAuthor', equality=matching_rules.distinguishedNameMatch, syntax=syntaxes.DN())
documentIdentifier = AttributeType('0.9.2342.19200300.100.1.11', name='documentIdentifier', equality=matching_rules.caseIgnoreMatch, substr=matching_rules.caseIgnoreSubstringsMatch, syntax=syntaxes.DirectoryString(256))
documentLocation = AttributeType('0.9.2342.19200300.100.1.15', name='documentLocation', equality=matching_rules.caseIgnoreMatch, substr=matching_rules.caseIgnoreSubstringsMatch, syntax=syntaxes.DirectoryString(256))
documentPublisher = AttributeType('0.9.2342.19200300.100.1.56', name='documentPublisher', equality=matching_rules.caseIgnoreMatch, substr=matching_rules.caseIgnoreSubstringsMatch, syntax=syntaxes.DirectoryString())
documentTitle = AttributeType('0.9.2342.19200300.100.1.12', name='documentTitle', equality=matching_rules.caseIgnoreMatch, substr=matching_rules.caseIgnoreSubstringsMatch, syntax=syntaxes.DirectoryString(256))
documentVersion = AttributeType('0.9.2342.19200300.100.1.13', name='documentVersion', equality=matching_rules.caseIgnoreMatch, substr=matching_rules.caseIgnoreSubstringsMatch, syntax=syntaxes.DirectoryString(256))
drink = AttributeType('0.9.2342.19200300.100.1.5', name='drink', equality=matching_rules.caseIgnoreMatch, substr=matching_rules.caseIgnoreSubstringsMatch, syntax=syntaxes.DirectoryString(256))
homePhone = AttributeType('0.9.2342.19200300.100.1.20', name='homePhone', equality=matching_rules.telephoneNumberMatch, substr=matching_rules.telephoneNumberSubstringsMatch, syntax=syntaxes.TelephoneNumber())
homePostalAddress = AttributeType('0.9.2342.19200300.100.1.39', name='homePostalAddress', equality=matching_rules.caseIgnoreListMatch, substr=matching_rules.caseIgnoreListSubstringsMatch, syntax=syntaxes.PostalAddress())
host = AttributeType('0.9.2342.19200300.100.1.9', name='host', equality=matching_rules.caseIgnoreMatch, substr=matching_rules.caseIgnoreSubstringsMatch, syntax=syntaxes.DirectoryString(256))
info = AttributeType('0.9.2342.19200300.100.1.4', name='info', equality=matching_rules.caseIgnoreMatch, substr=matching_rules.caseIgnoreSubstringsMatch, syntax=syntaxes.DirectoryString(2048))
mail = AttributeType('0.9.2342.19200300.100.1.3', name='mail', equality=matching_rules.caseIgnoreIA5Match, substr=matching_rules.caseIgnoreIA5SubstringsMatch, syntax=syntaxes.IA5String(256))
manager = AttributeType('0.9.2342.19200300.100.1.10', name='manager', equality=matching_rules.distinguishedNameMatch, syntax=syntaxes.DN())
mobile = AttributeType('0.9.2342.19200300.100.1.41', name='mobile', equality=matching_rules.telephoneNumberMatch, substr=matching_rules.telephoneNumberSubstringsMatch, syntax=syntaxes.TelephoneNumber())
organizationalStatus = AttributeType('0.9.2342.19200300.100.1.45', name='organizationalStatus', equality=matching_rules.caseIgnoreMatch, substr=matching_rules.caseIgnoreSubstringsMatch, syntax=syntaxes.DirectoryString(256))
pager = AttributeType('0.9.2342.19200300.100.1.42', name='pager', equality=matching_rules.telephoneNumberMatch, substr=matching_rules.telephoneNumberSubstringsMatch, syntax=syntaxes.TelephoneNumber())
personalTitle = AttributeType('0.9.2342.19200300.100.1.40', name='personalTitle', equality=matching_rules.caseIgnoreMatch, substr=matching_rules.caseIgnoreSubstringsMatch, syntax=syntaxes.DirectoryString(256))
roomNumber = AttributeType('0.9.2342.19200300.100.1.6', name='roomNumber', equality=matching_rules.caseIgnoreMatch, substr=matching_rules.caseIgnoreSubstringsMatch, syntax=syntaxes.DirectoryString(256))
secretary = AttributeType('0.9.2342.19200300.100.1.21', name='secretary', equality=matching_rules.distinguishedNameMatch, syntax=syntaxes.DN())
uniqueIdentifier = AttributeType('0.9.2342.19200300.100.1.44', name='uniqueIdentifier', equality=matching_rules.caseIgnoreMatch, substr=matching_rules.caseIgnoreSubstringsMatch, syntax=syntaxes.DirectoryString(256))
UserClass = AttributeType('0.9.2342.19200300.100.1.8', name='userClass', equality=matching_rules.caseIgnoreMatch, substr=matching_rules.caseIgnoreSubstringsMatch, syntax=syntaxes.DirectoryString(256))

ALL = ALL + (
	associatedDomain,
	associatedName,
	buildingName,
	co,
	documentAuthor,
	documentIdentifier,
	documentLocation,
	documentPublisher,
	documentTitle,
	documentVersion,
	drink,
	homePhone,
	homePostalAddress,
	host,
	info,
	mail,
	manager,
	mobile,
	organizationalStatus,
	pager,
	personalTitle,
	roomNumber,
	secretary,
	uniqueIdentifier,
	UserClass,
)

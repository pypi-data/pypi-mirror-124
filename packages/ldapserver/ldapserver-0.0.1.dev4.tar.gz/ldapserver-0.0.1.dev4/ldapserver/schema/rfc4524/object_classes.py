# pylint: disable=wildcard-import,unused-wildcard-import

from ..types import ObjectClass, ObjectClassKind
from ..rfc4519.object_classes import *
from . import attribute_types

account = ObjectClass('0.9.2342.19200300.100.4.5', name='account', sup=top, kind=ObjectClassKind.STRUCTURAL, must=[attribute_types.uid], may=[attribute_types.description, attribute_types.seeAlso, attribute_types.l, attribute_types.o, attribute_types.ou, attribute_types.host] )
document = ObjectClass('0.9.2342.19200300.100.4.6', name='document', sup=top, kind=ObjectClassKind.STRUCTURAL, must=[attribute_types.documentIdentifier], may=[attribute_types.cn, attribute_types.description, attribute_types.seeAlso, attribute_types.l, attribute_types.o, attribute_types.ou, attribute_types.documentTitle, attribute_types.documentVersion, attribute_types.documentAuthor, attribute_types.documentLocation, attribute_types.documentPublisher] )
documentSeries = ObjectClass('0.9.2342.19200300.100.4.9', name='documentSeries', sup=top, kind=ObjectClassKind.STRUCTURAL, must=[attribute_types.cn], may=[attribute_types.description, attribute_types.l, attribute_types.o, attribute_types.ou, attribute_types.seeAlso, attribute_types.telephoneNumber] )
domain = ObjectClass('0.9.2342.19200300.100.4.13', name='domain', sup=top, kind=ObjectClassKind.STRUCTURAL, must=[attribute_types.dc], may=[attribute_types.userPassword, attribute_types.searchGuide, attribute_types.seeAlso, attribute_types.businessCategory, attribute_types.x121Address, attribute_types.registeredAddress, attribute_types.destinationIndicator, attribute_types.preferredDeliveryMethod, attribute_types.telexNumber, attribute_types.teletexTerminalIdentifier, attribute_types.telephoneNumber, attribute_types.internationalISDNNumber, attribute_types.facsimileTelephoneNumber, attribute_types.street, attribute_types.postOfficeBox, attribute_types.postalCode, attribute_types.postalAddress, attribute_types.physicalDeliveryOfficeName, attribute_types.st, attribute_types.l, attribute_types.description, attribute_types.o, attribute_types.associatedName] )
domainRelatedObject = ObjectClass('0.9.2342.19200300.100.4.17', name='domainRelatedObject', sup=top, kind=ObjectClassKind.AUXILIARY, must=[attribute_types.associatedDomain])
friendlyCountry = ObjectClass('0.9.2342.19200300.100.4.18', name='friendlyCountry', sup=country, kind=ObjectClassKind.STRUCTURAL, must=[attribute_types.co])
rFC822localPart = ObjectClass('0.9.2342.19200300.100.4.14', name='rFC822localPart', sup=domain, kind=ObjectClassKind.STRUCTURAL, may=[attribute_types.cn, attribute_types.description, attribute_types.destinationIndicator, attribute_types.facsimileTelephoneNumber, attribute_types.internationalISDNNumber, attribute_types.physicalDeliveryOfficeName, attribute_types.postalAddress, attribute_types.postalCode, attribute_types.postOfficeBox, attribute_types.preferredDeliveryMethod, attribute_types.registeredAddress, attribute_types.seeAlso, attribute_types.sn, attribute_types.street, attribute_types.telephoneNumber, attribute_types.teletexTerminalIdentifier, attribute_types.telexNumber, attribute_types.x121Address] )
room = ObjectClass('0.9.2342.19200300.100.4.7', name='room', sup=top, kind=ObjectClassKind.STRUCTURAL, must=[attribute_types.cn], may=[attribute_types.roomNumber, attribute_types.description, attribute_types.seeAlso, attribute_types.telephoneNumber] )
simpleSecurityObject = ObjectClass('0.9.2342.19200300.100.4.19', name='simpleSecurityObject', sup=top, kind=ObjectClassKind.AUXILIARY, must=[attribute_types.userPassword])

ALL = ALL + (
	account,
	document,
	documentSeries,
	domain,
	domainRelatedObject,
	friendlyCountry,
	rFC822localPart,
	room,
	simpleSecurityObject,
)

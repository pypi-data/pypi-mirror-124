
# pylint: disable=wildcard-import,unused-wildcard-import

from ..types import ObjectClass, ObjectClassKind
from ..rfc4512.object_classes import *
from . import attribute_types

person = ObjectClass('2.5.6.6', name='person', sup=top, kind=ObjectClassKind.STRUCTURAL, must=[attribute_types.sn, attribute_types.cn], may=[attribute_types.userPassword, attribute_types.telephoneNumber, attribute_types.seeAlso, attribute_types.description]) # defined first, so sup=person works
applicationProcess = ObjectClass('2.5.6.11', name='applicationProcess', sup=top, kind=ObjectClassKind.STRUCTURAL, must=[attribute_types.cn], may=[attribute_types.seeAlso, attribute_types.ou, attribute_types.l, attribute_types.description])
country = ObjectClass('2.5.6.2', name='country', sup=top, kind=ObjectClassKind.STRUCTURAL, must=[attribute_types.c], may=[attribute_types.searchGuide, attribute_types.description])
dcObject = ObjectClass('1.3.6.1.4.1.1466.344', name='dcObject', sup=top, kind=ObjectClassKind.AUXILIARY, must=[attribute_types.dc])
device = ObjectClass('2.5.6.14', name='device', sup=top, kind=ObjectClassKind.STRUCTURAL, must=[attribute_types.cn], may=[attribute_types.serialNumber, attribute_types.seeAlso, attribute_types.owner, attribute_types.ou, attribute_types.o, attribute_types.l, attribute_types.description])
groupOfNames = ObjectClass('2.5.6.9', name='groupOfNames', sup=top, kind=ObjectClassKind.STRUCTURAL, must=[attribute_types.member, attribute_types.cn], may=[attribute_types.businessCategory, attribute_types.seeAlso, attribute_types.owner, attribute_types.ou, attribute_types.o, attribute_types.description])
groupOfUniqueNames = ObjectClass('2.5.6.17', name='groupOfUniqueNames', sup=top, kind=ObjectClassKind.STRUCTURAL, must=[attribute_types.uniqueMember, attribute_types.cn], may=[attribute_types.businessCategory, attribute_types.seeAlso, attribute_types.owner, attribute_types.ou, attribute_types.o, attribute_types.description])
locality = ObjectClass('2.5.6.3', name='locality', sup=top, kind=ObjectClassKind.STRUCTURAL, may=[attribute_types.street, attribute_types.seeAlso, attribute_types.searchGuide, attribute_types.st, attribute_types.l, attribute_types.description])
organization = ObjectClass('2.5.6.4', name='organization', sup=top, kind=ObjectClassKind.STRUCTURAL, must=[attribute_types.o], may=[attribute_types.userPassword, attribute_types.searchGuide, attribute_types.seeAlso, attribute_types.businessCategory, attribute_types.x121Address, attribute_types.registeredAddress, attribute_types.destinationIndicator, attribute_types.preferredDeliveryMethod, attribute_types.telexNumber, attribute_types.teletexTerminalIdentifier, attribute_types.telephoneNumber, attribute_types.internationalISDNNumber, attribute_types.facsimileTelephoneNumber, attribute_types.street, attribute_types.postOfficeBox, attribute_types.postalCode, attribute_types.postalAddress, attribute_types.physicalDeliveryOfficeName, attribute_types.st, attribute_types.l, attribute_types.description])
organizationalPerson = ObjectClass('2.5.6.7', name='organizationalPerson', sup=person, kind=ObjectClassKind.STRUCTURAL, may=[attribute_types.title, attribute_types.x121Address, attribute_types.registeredAddress, attribute_types.destinationIndicator, attribute_types.preferredDeliveryMethod, attribute_types.telexNumber, attribute_types.teletexTerminalIdentifier, attribute_types.telephoneNumber, attribute_types.internationalISDNNumber, attribute_types.facsimileTelephoneNumber, attribute_types.street, attribute_types.postOfficeBox, attribute_types.postalCode, attribute_types.postalAddress, attribute_types.physicalDeliveryOfficeName, attribute_types.ou, attribute_types.st, attribute_types.l])
organizationalRole = ObjectClass('2.5.6.8', name='organizationalRole', sup=top, kind=ObjectClassKind.STRUCTURAL, must=[attribute_types.cn], may=[attribute_types.x121Address, attribute_types.registeredAddress, attribute_types.destinationIndicator, attribute_types.preferredDeliveryMethod, attribute_types.telexNumber, attribute_types.teletexTerminalIdentifier, attribute_types.telephoneNumber, attribute_types.internationalISDNNumber, attribute_types.facsimileTelephoneNumber, attribute_types.seeAlso, attribute_types.roleOccupant, attribute_types.preferredDeliveryMethod, attribute_types.street, attribute_types.postOfficeBox, attribute_types.postalCode, attribute_types.postalAddress, attribute_types.physicalDeliveryOfficeName, attribute_types.ou, attribute_types.st, attribute_types.l, attribute_types.description])
organizationalUnit = ObjectClass('2.5.6.5', name='organizationalUnit', sup=top, kind=ObjectClassKind.STRUCTURAL, must=[attribute_types.ou], may=[attribute_types.businessCategory, attribute_types.description, attribute_types.destinationIndicator, attribute_types.facsimileTelephoneNumber, attribute_types.internationalISDNNumber, attribute_types.l, attribute_types.physicalDeliveryOfficeName, attribute_types.postalAddress, attribute_types.postalCode, attribute_types.postOfficeBox, attribute_types.preferredDeliveryMethod, attribute_types.registeredAddress, attribute_types.searchGuide, attribute_types.seeAlso, attribute_types.st, attribute_types.street, attribute_types.telephoneNumber, attribute_types.teletexTerminalIdentifier, attribute_types.telexNumber, attribute_types.userPassword, attribute_types.x121Address])
residentialPerson = ObjectClass('2.5.6.10', name='residentialPerson', sup=person, kind=ObjectClassKind.STRUCTURAL, must=[attribute_types.l], may=[attribute_types.businessCategory, attribute_types.x121Address, attribute_types.registeredAddress, attribute_types.destinationIndicator, attribute_types.preferredDeliveryMethod, attribute_types.telexNumber, attribute_types.teletexTerminalIdentifier, attribute_types.telephoneNumber, attribute_types.internationalISDNNumber, attribute_types.facsimileTelephoneNumber, attribute_types.preferredDeliveryMethod, attribute_types.street, attribute_types.postOfficeBox, attribute_types.postalCode, attribute_types.postalAddress, attribute_types.physicalDeliveryOfficeName, attribute_types.st, attribute_types.l])
uidObject = ObjectClass('1.3.6.1.1.3.1', name='uidObject', sup=top, kind=ObjectClassKind.AUXILIARY, must=[attribute_types.uid])

ALL = ALL + (
	person,
	applicationProcess,
	country,
	dcObject,
	device,
	groupOfNames,
	groupOfUniqueNames,
	locality,
	organization,
	organizationalPerson,
	organizationalRole,
	organizationalUnit,
	residentialPerson,
	uidObject,
)

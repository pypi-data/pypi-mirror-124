
# pylint: disable=wildcard-import,unused-wildcard-import

from ..types import ObjectClass, ObjectClassKind
from ..rfc4524.object_classes import *
from . import attribute_types

inetOrgPerson = ObjectClass('2.16.840.1.113730.3.2.2', name='inetOrgPerson', sup=organizationalPerson, kind=ObjectClassKind.STRUCTURAL, may=[attribute_types.businessCategory, attribute_types.carLicense, attribute_types.departmentNumber, attribute_types.displayName, attribute_types.employeeNumber, attribute_types.employeeType, attribute_types.givenName, attribute_types.homePhone, attribute_types.homePostalAddress, attribute_types.initials, attribute_types.jpegPhoto, attribute_types.labeledURI, attribute_types.mail, attribute_types.manager, attribute_types.mobile, attribute_types.o, attribute_types.pager, attribute_types.roomNumber, attribute_types.secretary, attribute_types.uid, attribute_types.x500UniqueIdentifier, attribute_types.preferredLanguage, attribute_types.userSMIMECertificate, attribute_types.userPKCS12, attribute_types.userCertificate, attribute_types.audio, attribute_types.photo])

ALL = ALL + (
	inetOrgPerson,
)

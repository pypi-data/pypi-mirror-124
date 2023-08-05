
# pylint: disable=wildcard-import,unused-wildcard-import,unused-import

from ..types import AttributeType
# RFC2798 is originally based on the old LDAPv3 RFC2256, the old
# COSINE RFC1274 and RFC2079 (for labeledURI). RFC2256 and RFC1274
# were obsoleted by RFC4524 and RFC4519. They also updated RFC2798.
from ..rfc4524.attribute_types import *
from ..rfc2079.attribute_types import labeledURI, ALL as RFC2079_ALL
from ..rfc4523.attribute_types import userCertificate
from ..rfc1274.attribute_types import audio, photo
from . import syntaxes, matching_rules

carLicense = AttributeType('2.16.840.1.113730.3.1.1', name='carLicense', desc='vehicle license or registration plate', equality=matching_rules.caseIgnoreMatch, substr=matching_rules.caseIgnoreSubstringsMatch, syntax=syntaxes.DirectoryString())
departmentNumber = AttributeType('2.16.840.1.113730.3.1.2', name='departmentNumber', desc='identifies a department within an organization', equality=matching_rules.caseIgnoreMatch, substr=matching_rules.caseIgnoreSubstringsMatch, syntax=syntaxes.DirectoryString())
displayName = AttributeType('2.16.840.1.113730.3.1.241', name='displayName', desc='preferred name of a person to be used when displaying entries', equality=matching_rules.caseIgnoreMatch, substr=matching_rules.caseIgnoreSubstringsMatch, syntax=syntaxes.DirectoryString(), single_value=True)
employeeNumber = AttributeType('2.16.840.1.113730.3.1.3', name='employeeNumber', desc='numerically identifies an employee within an organization', equality=matching_rules.caseIgnoreMatch, substr=matching_rules.caseIgnoreSubstringsMatch, syntax=syntaxes.DirectoryString(), single_value=True)
employeeType = AttributeType('2.16.840.1.113730.3.1.4', name='employeeType', desc='type of employment for a person', equality=matching_rules.caseIgnoreMatch, substr=matching_rules.caseIgnoreSubstringsMatch, syntax=syntaxes.DirectoryString())
jpegPhoto = AttributeType('0.9.2342.19200300.100.1.60', name='jpegPhoto', desc='a JPEG image', syntax=syntaxes.JPEG())
preferredLanguage = AttributeType('2.16.840.1.113730.3.1.39', name='preferredLanguage', desc='preferred written or spoken language for a person', equality=matching_rules.caseIgnoreMatch, substr=matching_rules.caseIgnoreSubstringsMatch, syntax=syntaxes.DirectoryString(), single_value=True)
userSMIMECertificate = AttributeType('2.16.840.1.113730.3.1.40', name='userSMIMECertificate', desc='PKCS#7 SignedData used to support S/MIME', syntax=syntaxes.Binary())
userPKCS12 = AttributeType('2.16.840.1.113730.3.1.216', name='userPKCS12', desc='PKCS #12 PFX PDU for exchange of personal identity information', syntax=syntaxes.Binary())

ALL = ALL + RFC2079_ALL + (
	userCertificate, # RFC4523
	audio, # RFC1274
	photo, # RFC1274
	carLicense,
	departmentNumber,
	displayName,
	employeeNumber,
	employeeType,
	jpegPhoto,
	preferredLanguage,
	userSMIMECertificate,
	userPKCS12,
)

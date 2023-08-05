from .ldap import LDAPResultCode

class LDAPError(Exception):
	'''Base class for all LDAP errors'''

	RESULT_CODE: LDAPResultCode

	def __init__(self, message=''):
		super().__init__()
		self.code = self.RESULT_CODE
		self.message = message

#class LDAPSuccess(LDAPError):
#	RESULT_CODE = LDAPResultCode.success

class LDAPOperationsError(LDAPError):
	RESULT_CODE = LDAPResultCode.operationsError

class LDAPProtocolError(LDAPError):
	RESULT_CODE = LDAPResultCode.protocolError

class LDAPTimeLimitExceeded(LDAPError):
	RESULT_CODE = LDAPResultCode.timeLimitExceeded

class LDAPSizeLimitExceeded(LDAPError):
	RESULT_CODE = LDAPResultCode.sizeLimitExceeded

#class LDAPCompareFalse(LDAPError):
#	RESULT_CODE = LDAPResultCode.compareFalse

#class LDAPCompareTrue(LDAPError):
#	RESULT_CODE = LDAPResultCode.compareTrue

class LDAPAuthMethodNotSupported(LDAPError):
	RESULT_CODE = LDAPResultCode.authMethodNotSupported

class LDAPStrongerAuthRequired(LDAPError):
	RESULT_CODE = LDAPResultCode.strongerAuthRequired

#class LDAPReferral(LDAPError):
#	RESULT_CODE = LDAPResultCode.referral

class LDAPAdminLimitExceeded(LDAPError):
	RESULT_CODE = LDAPResultCode.adminLimitExceeded

class LDAPUnavailableCriticalExtension(LDAPError):
	RESULT_CODE = LDAPResultCode.unavailableCriticalExtension

class LDAPConfidentialityRequired(LDAPError):
	RESULT_CODE = LDAPResultCode.confidentialityRequired

#class LDAPSaslBindInProgress(LDAPError):
#	RESULT_CODE = LDAPResultCode.saslBindInProgress

class LDAPNoSuchAttribute(LDAPError):
	RESULT_CODE = LDAPResultCode.noSuchAttribute

class LDAPUndefinedAttributeType(LDAPError):
	RESULT_CODE = LDAPResultCode.undefinedAttributeType

class LDAPInappropriateMatching(LDAPError):
	RESULT_CODE = LDAPResultCode.inappropriateMatching

class LDAPConstraintViolation(LDAPError):
	RESULT_CODE = LDAPResultCode.constraintViolation

class LDAPAttributeOrValueExists(LDAPError):
	RESULT_CODE = LDAPResultCode.attributeOrValueExists

class LDAPInvalidAttributeSyntax(LDAPError):
	RESULT_CODE = LDAPResultCode.invalidAttributeSyntax

class LDAPNoSuchObject(LDAPError):
	RESULT_CODE = LDAPResultCode.noSuchObject

class LDAPAliasProblem(LDAPError):
	RESULT_CODE = LDAPResultCode.aliasProblem

class LDAPInvalidDNSyntax(LDAPError):
	RESULT_CODE = LDAPResultCode.invalidDNSyntax

class LDAPAliasDereferencingProblem(LDAPError):
	RESULT_CODE = LDAPResultCode.aliasDereferencingProblem

class LDAPInappropriateAuthentication(LDAPError):
	RESULT_CODE = LDAPResultCode.inappropriateAuthentication

class LDAPInvalidCredentials(LDAPError):
	RESULT_CODE = LDAPResultCode.invalidCredentials

class LDAPInsufficientAccessRights(LDAPError):
	RESULT_CODE = LDAPResultCode.insufficientAccessRights

class LDAPBusy(LDAPError):
	RESULT_CODE = LDAPResultCode.busy

class LDAPUnavailable(LDAPError):
	RESULT_CODE = LDAPResultCode.unavailable

class LDAPUnwillingToPerform(LDAPError):
	RESULT_CODE = LDAPResultCode.unwillingToPerform

class LDAPLoopDetect(LDAPError):
	RESULT_CODE = LDAPResultCode.loopDetect

class LDAPNamingViolation(LDAPError):
	RESULT_CODE = LDAPResultCode.namingViolation

class LDAPObjectClassViolation(LDAPError):
	RESULT_CODE = LDAPResultCode.objectClassViolation

class LDAPNotAllowedOnNonLeaf(LDAPError):
	RESULT_CODE = LDAPResultCode.notAllowedOnNonLeaf

class LDAPNotAllowedOnRDN(LDAPError):
	RESULT_CODE = LDAPResultCode.notAllowedOnRDN

class LDAPEntryAlreadyExists(LDAPError):
	RESULT_CODE = LDAPResultCode.entryAlreadyExists

class LDAPObjectClassModsProhibited(LDAPError):
	RESULT_CODE = LDAPResultCode.objectClassModsProhibited

class LDAPAffectsMultipleDSAs(LDAPError):
	RESULT_CODE = LDAPResultCode.affectsMultipleDSAs

class LDAPOther(LDAPError):
	RESULT_CODE = LDAPResultCode.other

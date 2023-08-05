from ..rfc4517.syntaxes import BytesSyntax

class X509Certificate(BytesSyntax):
	oid = '1.3.6.1.4.1.1466.115.121.1.8'
	desc = 'X.509 Certificate'

class X509CertificateExactAssertion(BytesSyntax):
	oid = '1.3.6.1.1.15.1'
	desc = 'X.509 Certificate Exact Assertion'

ALL = (
	X509Certificate,
	X509CertificateExactAssertion,
)

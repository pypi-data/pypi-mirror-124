
# pylint: disable=unused-import

from ..rfc4517.syntaxes import IA5String, OctetString, BytesSyntax

class AuthPasswordSyntax(BytesSyntax):
	oid = '1.3.6.1.4.1.4203.1.1.2'
	desc = 'authentication password syntax'

ALL = (
	AuthPasswordSyntax,
)

from ..types import Syntax

# Only deprecated syntaxes from the old LDAP v3 RFCs

class Binary(Syntax):
	oid = '1.3.6.1.4.1.1466.115.121.1.5'
	desc = 'Binary'

	@staticmethod
	def encode(value):
		return value

	@staticmethod
	def decode(raw_value):
		return raw_value

ALL = (
	Binary,
)

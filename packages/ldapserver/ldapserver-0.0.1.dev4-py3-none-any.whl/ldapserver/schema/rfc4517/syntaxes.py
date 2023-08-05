import re
import datetime

from ..types import Syntax
from ... import dn

# Base classes
class StringSyntax(Syntax):
	@staticmethod
	def encode(value):
		return value.encode('utf8')

	@staticmethod
	def decode(raw_value):
		return raw_value.decode('utf8')

class BytesSyntax(Syntax):
	@staticmethod
	def encode(value):
		return value

	@staticmethod
	def decode(raw_value):
		return raw_value

# Syntax definitions
class AttributeTypeDescription(StringSyntax):
	oid = '1.3.6.1.4.1.1466.115.121.1.3'
	desc = 'Attribute Type Description'

class BitString(StringSyntax):
	oid = '1.3.6.1.4.1.1466.115.121.1.6'
	desc = 'Bit String'

class Boolean(Syntax):
	oid = '1.3.6.1.4.1.1466.115.121.1.7'
	desc = 'Boolean'

	@staticmethod
	def encode(value):
		return b'TRUE' if value else b'FALSE'

	@staticmethod
	def decode(raw_value):
		if raw_value == b'TRUE':
			return True
		elif raw_value == b'FALSE':
			return False
		else:
			return None

class CountryString(StringSyntax):
	oid = '1.3.6.1.4.1.1466.115.121.1.11'
	desc = 'Country String'

class DeliveryMethod(StringSyntax):
	oid = '1.3.6.1.4.1.1466.115.121.1.14'
	desc = 'Delivery Method'

class DirectoryString(StringSyntax):
	oid = '1.3.6.1.4.1.1466.115.121.1.15'
	desc = 'Directory String'

class DITContentRuleDescription(StringSyntax):
	oid = '1.3.6.1.4.1.1466.115.121.1.16'
	desc = 'DIT Content Rule Description'

class DITStructureRuleDescription(StringSyntax):
	oid = '1.3.6.1.4.1.1466.115.121.1.17'
	desc = 'DIT Structure Rule Description'

class DN(Syntax):
	oid = '1.3.6.1.4.1.1466.115.121.1.12'
	desc = 'DN'

	@staticmethod
	def encode(value):
		return str(value).encode('utf8')

	@staticmethod
	def decode(raw_value):
		try:
			return dn.DN.from_str(raw_value.decode('utf8'))
		except (UnicodeDecodeError, TypeError, ValueError):
			return None

class EnhancedGuide(StringSyntax):
	oid = '1.3.6.1.4.1.1466.115.121.1.21'
	desc = 'Enhanced Guide'

class FacsimileTelephoneNumber(StringSyntax):
	oid = '1.3.6.1.4.1.1466.115.121.1.22'
	desc = 'Facsimile Telephone Number'

class Fax(BytesSyntax):
	oid = '1.3.6.1.4.1.1466.115.121.1.23'
	desc = 'Fax'

class GeneralizedTime(Syntax):
	oid = '1.3.6.1.4.1.1466.115.121.1.24'
	desc = 'Generalized Time'

	@staticmethod
	def encode(value):
		str_value = value.strftime('%Y%m%d%H%M%S.%f')
		if value.tzinfo == datetime.timezone.utc:
			str_value += 'Z'
		elif value.tzinfo is not None:
			delta_seconds = value.tzinfo.utcoffset(value).total_seconds()
			if delta_seconds < 0:
				str_value += '-'
				delta_seconds = -delta_seconds
			else:
				str_value += '+'
			hour = delta_seconds // 3600
			minute = (delta_seconds % 3600) // 60
			str_value += '%02d%02d'%(hour, minute)
		return str_value.encode('ascii')

	@staticmethod
	def decode(raw_value):
		try:
			raw_value = raw_value.decode('utf8')
		except UnicodeDecodeError:
			return None
		match = re.fullmatch(r'([0-9]{10})(|[0-9]{2}|[0-9]{4})(|[,.][0-9]+)(Z|[+-][0-9]{2}|[+-][0-9]{4})', raw_value)
		if match is None:
			return None
		main, minute_second, fraction, timezone = match.groups()
		fraction = float('0.' + (fraction[1:] or '0'))
		result = datetime.datetime.strptime(main, '%Y%m%d%H')
		if not minute_second:
			result += datetime.timedelta(hours=fraction)
		if len(minute_second) == 2:
			result += datetime.timedelta(minutes=int(minute_second)+fraction)
		elif len(minute_second) == 4:
			minute = minute_second[:2]
			second = minute_second[2:4]
			result += datetime.timedelta(minutes=int(minute), seconds=int(second)+fraction)
		if timezone == 'Z':
			result = result.replace(tzinfo=datetime.timezone.utc)
		elif timezone:
			sign, hour, minute = timezone[0], timezone[1:3], (timezone[3:5] or '00')
			delta = datetime.timedelta(hours=int(hour), minutes=int(minute))
			if sign == '+':
				result = result.replace(tzinfo=datetime.timezone(delta))
			else:
				result = result.replace(tzinfo=datetime.timezone(-delta))
		return result

class Guide(StringSyntax):
	oid = '1.3.6.1.4.1.1466.115.121.1.25'
	desc = 'Guide'

class IA5String(StringSyntax):
	oid = '1.3.6.1.4.1.1466.115.121.1.26'
	desc = 'IA5 String'

class INTEGER(Syntax):
	oid = '1.3.6.1.4.1.1466.115.121.1.27'
	desc = 'INTEGER'

	@staticmethod
	def encode(value):
		return str(value).encode('utf8')

	@staticmethod
	def decode(raw_value):
		if not raw_value or not raw_value.split(b'-', 1)[-1].isdigit():
			return None
		return int(raw_value.decode('utf8'))

class JPEG(BytesSyntax):
	oid = '1.3.6.1.4.1.1466.115.121.1.28'
	desc = 'JPEG'

class LDAPSyntaxDescription(StringSyntax):
	oid = '1.3.6.1.4.1.1466.115.121.1.54'
	desc = 'LDAP Syntax Description'

class MatchingRuleDescription(StringSyntax):
	oid = '1.3.6.1.4.1.1466.115.121.1.30'
	desc = 'Matching Rule Description'

class MatchingRuleUseDescription(StringSyntax):
	oid = '1.3.6.1.4.1.1466.115.121.1.31'
	desc = 'Matching Rule Use Description'

class NameAndOptionalUID(StringSyntax):
	oid = '1.3.6.1.4.1.1466.115.121.1.34'
	desc = 'Name And Optional UID'

	@staticmethod
	def encode(value):
		return DN.encode(value)

	@staticmethod
	def decode(raw_value):
		escaped = False
		dn_part = raw_value
		bitstr_part = b'' # pylint: disable=unused-variable
		for index, byte in enumerate(raw_value):
			byte = bytes((byte,))
			if escaped:
				escaped = False
			elif byte == b'\\':
				escaped = True
			elif byte == b'#':
				dn_part = raw_value[:index]
				bitstr_part = raw_value[index+1:]
				break
		# We need to find a good representation of this type, maybe a subclass
		# of dn.DN that carries the bitstring part as an attribute.
		#if bitstr_part:
		#	return DN.decode(dn_part), BitString.decode(bitstr_part)
		return DN.decode(dn_part)

class NameFormDescription(StringSyntax):
	oid = '1.3.6.1.4.1.1466.115.121.1.35'
	desc = 'Name Form Description'

class NumericString(StringSyntax):
	oid = '1.3.6.1.4.1.1466.115.121.1.36'
	desc = 'Numeric String'

class ObjectClassDescription(StringSyntax):
	oid = '1.3.6.1.4.1.1466.115.121.1.37'
	desc = 'Object Class Description'

class OctetString(BytesSyntax):
	oid = '1.3.6.1.4.1.1466.115.121.1.40'
	desc = 'Octet String'

class OID(StringSyntax):
	oid = '1.3.6.1.4.1.1466.115.121.1.38'
	desc = 'OID'

class OtherMailbox(StringSyntax):
	oid = '1.3.6.1.4.1.1466.115.121.1.39'
	desc = 'Other Mailbox'

class PostalAddress(Syntax):
	# 3.3.28.  Postal Address
	#
	# A value of the Postal Address syntax is a sequence of strings of one
	# or more arbitrary UCS characters, which form an address in a physical
	# mail system.
	#
	# The LDAP-specific encoding of a value of this syntax is defined by
	# the following ABNF:
	#
	#
	#   PostalAddress = line *( DOLLAR line )
	#   line          = 1*line-char
	#   line-char     = %x00-23
	#                   / (%x5C "24")  ; escaped "$"
	#                   / %x25-5B
	#                   / (%x5C "5C")  ; escaped "\"
	#                   / %x5D-7F
	#                   / UTFMB
	#
	# Each character string (i.e., <line>) of a postal address value is
	# encoded as a UTF-8 [RFC3629] string, except that "\" and "$"
	# characters, if they occur in the string, are escaped by a "\"
	# character followed by the two hexadecimal digit code for the
	# character.  The <DOLLAR> and <UTFMB> rules are defined in [RFC4512].
	#
	# Many servers limit the postal address to no more than six lines of no
	# more than thirty characters each.
	#
	#   Example:
	#      1234 Main St.$Anytown, CA 12345$USA
	#      \241,000,000 Sweepstakes$PO Box 1000000$Anytown, CA 12345$USA
	#
	# The LDAP definition for the Postal Address syntax is:
	#
	#   ( 1.3.6.1.4.1.1466.115.121.1.41 DESC 'Postal Address' )
	#
	# This syntax corresponds to the PostalAddress ASN.1 type from [X.520];
	# that is
	#
	#   PostalAddress ::= SEQUENCE SIZE(1..ub-postal-line) OF
	#       DirectoryString { ub-postal-string }
	#
	# The values of ub-postal-line and ub-postal-string (both integers) are
	# implementation defined.  Non-normative definitions appear in [X.520].

	oid = '1.3.6.1.4.1.1466.115.121.1.41'
	desc = 'Postal Address'

	# Native values are lists of str
	@staticmethod
	def encode(value):
		return '$'.join([line.replace('\\', '\\5C').replace('$', '\\24') for line in value]).encode('utf8')

	@staticmethod
	def decode(raw_value):
		return [line.replace('\\24', '$').replace('\\5C', '\\') for line in raw_value.decode('utf8').split('$')]

class PrintableString(StringSyntax):
	oid = '1.3.6.1.4.1.1466.115.121.1.44'
	desc = 'Printable String'

class SubstringAssertion(StringSyntax):
	oid = '1.3.6.1.4.1.1466.115.121.1.58'
	desc = 'Substring Assertion'

class TelephoneNumber(StringSyntax):
	oid = '1.3.6.1.4.1.1466.115.121.1.50'
	desc = 'Telephone Number'

class TeletexTerminalIdentifier(StringSyntax):
	oid = '1.3.6.1.4.1.1466.115.121.1.51'
	desc = 'Teletex Terminal Identifier'

class TelexNumber(StringSyntax):
	oid = '1.3.6.1.4.1.1466.115.121.1.52'
	desc = 'Telex Number'

class UTCTime(Syntax):
	oid = '1.3.6.1.4.1.1466.115.121.1.53'
	desc = 'UTC Time'

	@staticmethod
	def encode(value):
		str_value = value.strftime('%y%m%d%H%M%S')
		if value.tzinfo == datetime.timezone.utc:
			str_value += 'Z'
		elif value.tzinfo is not None:
			delta_seconds = value.tzinfo.utcoffset(value).total_seconds()
			if delta_seconds < 0:
				str_value += '-'
				delta_seconds = -delta_seconds
			else:
				str_value += '+'
			hour = delta_seconds // 3600
			minute = (delta_seconds % 3600) // 60
			str_value += '%02d%02d'%(hour, minute)
		return str_value.encode('ascii')

	@staticmethod
	def decode(raw_value):
		try:
			raw_value = raw_value.decode('utf8')
		except UnicodeDecodeError:
			return None
		match = re.fullmatch(r'([0-9]{10})(|[0-9]{2})(|Z|[+-][0-9]{4})', raw_value)
		if match is None:
			return None
		main, seconds, timezone = match.groups()
		result = datetime.datetime.strptime(main, '%y%m%d%H%M')
		if seconds:
			result = result.replace(second=int(seconds))
		if timezone == 'Z':
			result = result.replace(tzinfo=datetime.timezone.utc)
		elif timezone:
			sign, hour, minute = timezone[0], timezone[1:3], timezone[3:5]
			delta = datetime.timedelta(hours=int(hour), minutes=int(minute))
			if sign == '+':
				result = result.replace(tzinfo=datetime.timezone(delta))
			else:
				result = result.replace(tzinfo=datetime.timezone(-delta))
		return result

ALL = (
	AttributeTypeDescription,
	BitString,
	Boolean,
	CountryString,
	DeliveryMethod,
	DirectoryString,
	DITContentRuleDescription,
	DITStructureRuleDescription,
	DN,
	EnhancedGuide,
	FacsimileTelephoneNumber,
	Fax,
	GeneralizedTime,
	Guide,
	IA5String,
	INTEGER,
	JPEG,
	LDAPSyntaxDescription,
	MatchingRuleDescription,
	MatchingRuleUseDescription,
	NameAndOptionalUID,
	NameFormDescription,
	NumericString,
	ObjectClassDescription,
	OctetString,
	OID,
	OtherMailbox,
	PostalAddress,
	PrintableString,
	SubstringAssertion,
	TelephoneNumber,
	TeletexTerminalIdentifier,
	TelexNumber,
	UTCTime,
)

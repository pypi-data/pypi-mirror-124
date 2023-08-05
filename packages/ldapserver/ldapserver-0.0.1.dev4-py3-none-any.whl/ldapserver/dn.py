'''LDAP Distinguished Name Utilities

Distinguished Names (DNs) identifiy objects in an LDAP directory. In LDAP
protocol messages and when stored in attribute values DNs are encoded with
a string representation scheme described in RFC4514.

This module provides classes to represent `DN` objects and theirs parts
(`RD` and `RDNAssertion`) that correctly implement encoding, decoding and
comparing.

Limitations:

* Supported attribute types: `cn`, `l`, `st`, `o`, `ou`, `c`, `street`, `dc`, `uid`
* Dotted-decimal/OID attribute types are not supported
* Hexstring attribute values (`foo=#ABCDEF...`) are not supported
'''

import typing
import unicodedata
from string import hexdigits as HEXDIGITS

__all__ = ['DN', 'RDN', 'RDNAssertion']

class DN(tuple):
	'''Distinguished Name consiting of zero ore more `RDN` objects'''
	def __new__(cls, *args, **kwargs):
		if len(args) == 1 and isinstance(args[0], DN):
			args = args[0]
		if len(args) == 1 and isinstance(args[0], str):
			args = cls.from_str(args[0])
		for rdn in args:
			if not isinstance(rdn, RDN):
				raise TypeError(f'Argument {repr(rdn)} is of type {repr(type(rdn))}, expected ldapserver.dn.RDN object')
		rdns = tuple(args)
		if kwargs:
			rdns = (RDN(**kwargs),) + rdns
		return super().__new__(cls, rdns)

	# Syntax definiton from RFC4514:
	# distinguishedName = [ relativeDistinguishedName *( COMMA relativeDistinguishedName ) ]

	@classmethod
	def from_str(cls, expr):
		escaped = False
		rdns = []
		token = ''
		for char in expr:
			if escaped:
				escaped = False
				token += char
			elif char == ',':
				rdns.append(RDN.from_str(token))
				token = ''
			else:
				if char == '\\':
					escaped = True
				token += char
		if token:
			rdns.append(RDN.from_str(token))
		return cls(*rdns)

	def __str__(self):
		return ','.join(map(str, self))

	def __bytes__(self):
		return str(self).encode('utf8')

	def __repr__(self):
		return '<ldapserver.dn.DN %s>'%str(self)

	def __eq__(self, obj):
		return type(self) is type(obj) and super().__eq__(obj)

	def __hash__(self):
		return hash((type(self), tuple(self)))

	def __add__(self, value):
		if isinstance(value, DN):
			return DN(*(tuple(self) + tuple(value)))
		elif isinstance(value, RDN):
			return self + DN(value)
		else:
			raise TypeError(f'Can only add DN or RDN to DN, not {type(value)}')

	def __getitem__(self, key):
		if isinstance(key, slice):
			return type(self)(*super().__getitem__(key))
		return super().__getitem__(key)

	def __strip_common_suffix(self, value):
		value = DN(value)
		minlen = min(len(self), len(value))
		for i in range(minlen):
			if self[-1 - i] != value[-1 - i]:
				return self[:-i or None], value[:-i or None]
		return self[:-minlen or None], value[:-minlen or None]

	def is_direct_child_of(self, base):
		rchild, rbase = self.__strip_common_suffix(DN(base))
		return not rbase and len(rchild) == 1

	def in_subtree_of(self, base):
		rchild, rbase = self.__strip_common_suffix(DN(base)) # pylint: disable=unused-variable
		return not rbase

	@property
	def object_attribute(self):
		if len(self) == 0:
			return None
		return self[0].attribute # pylint: disable=no-member

	@property
	def object_value(self):
		if len(self) == 0:
			return None
		return self[0].value # pylint: disable=no-member

	@property
	def object_value_normalized(self):
		if len(self) == 0:
			return None
		return self[0].value_normalized # pylint: disable=no-member

class RDN(tuple):
	'''Relative Distinguished Name consisting of one or more `RDNAssertion` objects'''
	def __new__(cls, *assertions, **kwargs):
		for assertion in assertions:
			if not isinstance(assertion, RDNAssertion):
				raise TypeError(f'Argument {repr(assertion)} is of type {repr(type(assertion))}, expected ldapserver.dn.RDNAssertion')
		assertions = set(assertions)
		for key, value in kwargs.items():
			assertions.add(RDNAssertion(key, value))
		if not assertions:
			raise ValueError('RDN must have at least one assertion')
		return super().__new__(cls, sorted(assertions, key=lambda assertion: (assertion.attribute, assertion.value_normalized)))

	# Syntax definiton from RFC4514:
	# relativeDistinguishedName = attributeTypeAndValue *( PLUS attributeTypeAndValue )

	@classmethod
	def from_str(cls, expr):
		escaped = False
		assertions = []
		token = ''
		for char in expr:
			if escaped:
				escaped = False
				token += char
			elif char == '+':
				assertions.append(RDNAssertion.from_str(token))
				token = ''
			else:
				if char == '\\':
					escaped = True
				token += char
		if token:
			assertions.append(RDNAssertion.from_str(token))
		return cls(*assertions)

	def __str__(self):
		return '+'.join(map(str, self))

	def __repr__(self):
		return '<ldapserver.dn.RDN %s>'%str(self)

	def __eq__(self, obj):
		return type(self) is type(obj) and super().__eq__(obj)

	def __hash__(self):
		return hash((type(self), tuple(self)))

	def __add__(self, value):
		if isinstance(value, RDN):
			return DN(self, value)
		elif isinstance(value, DN):
			return DN(self) + value
		else:
			raise TypeError(f'Can only add DN or RDN to RDN, not {type(value)}')

	@property
	def attribute(self):
		if len(self) != 1:
			return None
		return self[0].attribute

	@property
	def value(self):
		if len(self) != 1:
			return None
		return self[0].value

	@property
	def value_normalized(self):
		if len(self) != 1:
			return None
		return self[0].value_normalized

# Mandatory attribute types (RFC4514)
STRI_ATTRIBUTES = ('cn', 'l', 'st', 'o', 'ou', 'c', 'street', 'dc', 'uid')

DN_ESCAPED = ('"', '+', ',', ';', '<', '>')
DN_SPECIAL = DN_ESCAPED + (' ', '#', '=')

class RDNAssertion:
	'''A single attribute value assertion'''
	__slots__ = ['attribute', 'value', 'value_normalized']
	attribute: str
	value: typing.Any
	value_normalized: typing.Any

	def __init__(self, attribute, value):
		if not isinstance(attribute, str):
			raise TypeError(f'RDNAssertion attribute {repr(attribute)} must be a string but is {type(attribute)}')
		attribute = attribute.lower()
		value_normalized = value
		if attribute in STRI_ATTRIBUTES:
			if not isinstance(value, str):
				raise TypeError(f'RDNAssertion value {repr(value)} for attribute "{attribute}" must be a string but is {type(value)}')
			if value == '':
				raise ValueError(f'RDNAssertion value for attribute "{attribute}" must not be empty')
			value_normalized = unicodedata.normalize('NFC', value.lower())
		else:
			raise ValueError(f'RDNAssertion attribute "{attribute}" is unsupported')
		super().__setattr__('value', value)
		super().__setattr__('value_normalized', value_normalized)
		super().__setattr__('attribute', attribute)

	# Syntax definiton from RFC4514 and 4512:
	#
	# attributeTypeAndValue = attributeType EQUALS attributeValue
	# attributeType = descr / numericoid
	# attributeValue = string / hexstring
	#
	# descr = ALPHA *( ALPHA / DIGIT / HYPHEN )
	# numericoid = number 1*( DOT number )
	# number = DIGIT / ( LDIGIT 1*DIGIT )
	#
	# ; The following characters are to be escaped when they appear
	# ; in the value to be encoded: ESC, one of <escaped>, leading
	# ; SHARP or SPACE, trailing SPACE, and NULL.
	# string = [ ( leadchar / pair ) [ *( stringchar / pair ) ( trailchar / pair ) ] ]
	#
	# leadchar = LUTF1 / UTFMB
	# LUTF1 = %x01-1F / %x21 / %x24-2A / %x2D-3A / %x3D / %x3F-5B / %x5D-7F
	#
	# trailchar = TUTF1 / UTFMB
	# TUTF1 = %x01-1F / %x21 / %x23-2A / %x2D-3A / %x3D / %x3F-5B / %x5D-7F
	#
	# stringchar = SUTF1 / UTFMB
	# SUTF1 = %x01-21 / %x23-2A / %x2D-3A / %x3D / %x3F-5B / %x5D-7F
	#
	# pair = ESC ( ESC / special / hexpair )
	# special = escaped / SPACE / SHARP / EQUALS
	# escaped = DQUOTE / PLUS / COMMA / SEMI / LANGLE / RANGLE
	#
	# hexstring = SHARP 1*hexpair
	# hexpair = HEX HEX

	@classmethod
	def from_str(cls, expr):
		attribute, escaped_value = expr.split('=', 1)
		if escaped_value.startswith('#'):
			# The "#..." form is used for unknown attribute types and those without
			# an LDAP string encoding. Supporting it would require us to somehow
			# handle the hex-encoded BER encoding of the data. We'll stay away from
			# this mess for now.
			raise ValueError('Hex-encoded RDN assertion values are not supported')
		escaped = False
		hexdigit = None
		# We store the unescaped value temporarily as bytes to correctly handle
		# hex-escaped multi-byte UTF8 sequences
		encoded_value = b''
		for char in escaped_value:
			if hexdigit is not None:
				encoded_value += bytes.fromhex('%s%s'%(hexdigit, char))
				hexdigit = None
			elif escaped:
				if char in DN_SPECIAL + ('\\',):
					encoded_value += char.encode('utf8')
				elif char in HEXDIGITS:
					hexdigit = char
				else:
					raise ValueError('Invalid escape: \\%s'%char)
				escaped = False
			elif char == '\\':
				escaped = True
			else:
				encoded_value += char.encode('utf8')
		value = encoded_value.decode('utf8')
		return cls(attribute, value)

	def __str__(self):
		escaped_value = ''
		for char in self.value:
			if char in DN_ESCAPED + ('\\',):
				escaped_value += '\\' + char
			# Escape non-printable characters for readability. This goes beyond
			# what the standard requires.
			elif char in ('\x00',) or not char.isprintable():
				for codepoint in char.encode('utf8'):
					escaped_value += '\\%02x'%codepoint
			else:
				escaped_value += char
		if escaped_value.startswith(' ') or escaped_value.startswith('#'):
			escaped_value = '\\' + escaped_value
		if escaped_value.endswith(' '):
			escaped_value = escaped_value[:-1] + '\\' + escaped_value[-1]
		return '%s=%s'%(self.attribute, escaped_value)

	def __repr__(self):
		return '<ldapserver.dn.RDNAssertion %s>'%str(self)

	def __eq__(self, obj):
		return type(self) is type(obj) and self.attribute == obj.attribute and \
		       self.value_normalized == obj.value_normalized

	def __hash__(self):
		return hash((type(self), self.attribute, self.value_normalized))

	def __setattr__(self, *args):
		raise TypeError('RDNAssertion object is immutable')

	def __delattr__(self, *args):
		raise TypeError('RDNAssertion object is immutable')

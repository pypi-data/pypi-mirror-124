import enum

from .. import ldap
from ..dn import DN

__all__ = [
	'FilterResult',
	'Syntax',
	'MatchingRule',
	'AttributeTypeUsage',
	'AttributeType',
	'ObjectClassKind',
	'ObjectClass',
	'Object',
	'RootDSE',
	'Subschema',
	'WILDCARD_VALUE',
	'ObjectTemplate',
]

class FilterResult(enum.Enum):
	TRUE = enum.auto()
	FALSE = enum.auto()
	UNDEFINED = enum.auto()
	MAYBE_TRUE = enum.auto() # used by ObjectTemplate

def escape(string):
	result = ''
	for char in string:
		if char == '\'':
			result += '\\27'
		elif char == '\\':
			result += '\\5C'
		else:
			result += char
	return result

class Syntax:
	oid: str
	desc: str

	def __init__(self, max_len=None):
		self.max_len = max_len
		if max_len is None:
			self.ref = self.oid
		else:
			self.ref = self.oid + '{' + str(max_len) + '}'

	@classmethod
	def get_first_component_oid(cls):
		return cls.oid

	@classmethod
	def encode_syntax_definition(cls):
		return f"( {cls.oid} DESC '{escape(cls.desc)}' )"

	@staticmethod
	def decode(raw_value):
		'''Decode LDAP-specific encoding of a value to a native value

		:param raw_value: LDAP-specific encoding of the value
		:type raw_value: bytes

		:returns: native value (depends on syntax), None if raw_value is invalid
		:rtype: any or None'''
		return None

	@staticmethod
	def encode(value):
		'''Encode native value to its LDAP-specific encoding

		:param value: native value (depends on syntax)
		:type value: any

		:returns: LDAP-specific encoding of the value
		:rtype: bytes'''
		raise NotImplementedError()

class MatchingRule:
	def __init__(self, oid, name, syntax, **kwargs):
		self.oid = oid
		self.name = name
		self.syntax = syntax
		for key, value in kwargs.items():
			setattr(self, key, value)

	def encode_syntax_definition(self):
		return f"( {self.oid} NAME '{escape(self.name)}' SYNTAX {self.syntax.ref} )"

	def __repr__(self):
		return f'<ldapserver.schema.MatchingRule {self.encode_syntax_definition()}>'

	def match_equal(self, attribute_value, assertion_value):
		return FilterResult.UNDEFINED

	def match_approx(self, attribute_value, assertion_value):
		return self.match_equal(attribute_value, assertion_value)

	def match_less(self, attribute_value, assertion_value):
		return FilterResult.UNDEFINED

	def match_greater_or_equal(self, attribute_value, assertion_value):
		return FilterResult.UNDEFINED

	def match_substr(self, attribute_value, inital_substring, any_substrings, final_substring):
		return FilterResult.UNDEFINED

class AttributeTypeUsage(enum.Enum):
	# pylint: disable=invalid-name
	# user
	userApplications = enum.auto()
	# directory operational
	directoryOperation = enum.auto()
	# DSA-shared operational
	distributedOperation = enum.auto()
	# DSA-specific operational
	dSAOperation = enum.auto()

class AttributeType:
	# pylint: disable=too-many-instance-attributes,too-many-arguments,too-many-branches,too-many-statements
	def __init__(self, oid, name=None, desc=None, obsolete=None, sup=None,
	             equality=None, ordering=None, substr=None, syntax=None,
               single_value=None, collective=None, no_user_modification=None,
               usage=None):
		if sup is None and syntax is None:
			raise ValueError('Either SUP or, syntax=syntax.must, be specified')
		tokens = ['(', oid]
		if name is not None:
			tokens += ['NAME', "'"+escape(name)+"'"] # name is actually a list
		if desc is not None:
			tokens += ['DESC', "'"+escape(desc)+"'"]
		if obsolete is not None:
			tokens += ['OBSOLETE', obsolete]
		if sup is not None:
			tokens += ['SUP', sup.oid]
		if equality is not None:
			tokens += ['EQUALITY', equality.oid]
		if ordering is not None:
			tokens += ['ORDERING', ordering.oid]
		if substr is not None:
			tokens += ['SUBSTR', substr.oid]
		if syntax is not None:
			tokens += ['SYNTAX', syntax.ref]
		if single_value is not None:
			tokens += ['SINGLE-VALUE']
		if collective is not None:
			tokens += ['COLLECTIVE']
		if no_user_modification is not None:
			tokens += ['NO-USER-MODIFICATION']
		if usage is not None:
			tokens += ['USAGE', usage.name]
		tokens += [')']
		self.schema_encoding = ' '.join(tokens)
		self.oid = oid
		self.name = name
		self.names = set()
		if name is not None:
			self.names.add(name)
		self.obsolete = obsolete or False
		self.sup = sup
		if self.sup is not None:
			self.names |= self.sup.names
		self.equality = equality
		if self.equality is None and self.sup is not None:
			self.equality = self.sup.equality
		self.ordering = ordering
		if self.ordering is None and self.sup is not None:
			self.ordering = self.sup.ordering
		self.substr = substr
		if self.substr is None and self.sup is not None:
			self.substr = self.sup.substr
		self.syntax = syntax
		if self.syntax is None and self.sup is not None:
			self.syntax = self.sup.syntax
		self.single_value = single_value or False
		self.collective = collective or False
		self.no_user_modification = no_user_modification or False
		self.usage = usage or AttributeTypeUsage.userApplications

	def get_first_component_oid(self):
		return self.oid

	def __repr__(self):
		return f'<ldapserver.schema.AttributeType {self.schema_encoding}>'

class ObjectClassKind(enum.Enum):
	ABSTRACT = enum.auto()
	STRUCTURAL = enum.auto()
	AUXILIARY = enum.auto()

class ObjectClass:
	# pylint: disable=too-many-arguments
	def __init__(self, oid, name=None, desc=None, obsolete=None, sup=None,
	             kind=None, must=None, may=None):
		tokens = ['(', oid]
		if name is not None:
			tokens += ['NAME', "'"+escape(name)+"'"] # name is actually a list
		if desc is not None:
			tokens += ['DESC', "'"+escape(desc)+"'"]
		if obsolete is not None:
			tokens += ['OBSOLETE', obsolete]
		if sup is not None:
			tokens += ['SUP', sup.name]
		if kind is not None:
			tokens += [kind.name]
		if must and len(must) == 1:
			tokens += ['MUST', must[0].name]
		elif must and len(must) > 1:
			tokens += ['MUST', '(']
			for index, attr in enumerate(must):
				if index > 0:
					tokens += ['$']
				tokens += [attr.name]
			tokens += [')']
		if may and len(may) == 1:
			tokens += ['MAY', may[0].name]
		elif may and len(may) > 1:
			tokens += ['MAY', '(']
			for index, attr in enumerate(may):
				if index > 0:
					tokens += ['$']
				tokens += [attr.name]
			tokens += [')']
		tokens += [')']
		self.schema_encoding = ' '.join(tokens)
		self.oid = oid
		self.name = name
		self.desc = desc
		self.obsolete = obsolete or False
		self.sup = sup
		self.kind = kind or ObjectClassKind.STRUCTURAL
		self.must = must or []
		self.may = may or []

	def get_first_component_oid(self):
		return self.oid

	def __repr__(self):
		return f'<ldapserver.schema.ObjectClass {self.schema_encoding}>'

def any_3value(iterable):
	'''Extended three-valued logic equivalent of any builtin

	If all items are TRUE, return TRUE. Otherwise if any item is MAYBE_TRUE,
	return MAYBE_TRUE. If neither TRUE nor MAYBE_TRUE are in items, but any
	item is UNDEFINED, return UNDEFINED. Otherwise (all items are FALSE),
	return FALSE.'''
	result = FilterResult.FALSE
	for item in iterable:
		if item == FilterResult.TRUE:
			return FilterResult.TRUE
		elif item == FilterResult.MAYBE_TRUE:
			result = FilterResult.MAYBE_TRUE
		elif item == FilterResult.UNDEFINED and result == FilterResult.FALSE:
			result = FilterResult.UNDEFINED
	return result

def all_3value(iterable):
	'''Extended three-valued logic equivalent of all builtin

	If all items are TRUE, return TRUE. If any item is FALSE, return FALSE.
	If no item is FALSE and any item is UNDEFINED, return UNDEFINED.
	Otherwise (not item is FALSE or UNDEFINED and not all items are TRUE,
	so at least one item is MAYBE_TRUE), return MAYBE_TRUE.'''
	result = FilterResult.TRUE
	for item in iterable:
		if item == FilterResult.FALSE:
			return FilterResult.FALSE
		elif item == FilterResult.UNDEFINED:
			result = FilterResult.UNDEFINED
		elif item == FilterResult.MAYBE_TRUE and result == FilterResult.TRUE:
			result = FilterResult.MAYBE_TRUE
	return result

class AttributeDict(dict):
	def __init__(self, subschema, **attributes):
		super().__init__()
		self.subschema = subschema
		for key, value in attributes.items():
			self[key] = value

	def __contains__(self, key):
		return super().__contains__(self.subschema.lookup_attribute(key))

	def __setitem__(self, key, value):
		super().__setitem__(self.subschema.lookup_attribute(key, fail_if_not_found=True), value)

	def __getitem__(self, key):
		key = self.subschema.lookup_attribute(key, fail_if_not_found=True)
		if key not in self:
			super().__setitem__(key, [])
		result = super().__getitem__(key)
		if callable(result):
			return result()
		return result

	def setdefault(self, key, default=None):
		key = self.subschema.lookup_attribute(key, fail_if_not_found=True)
		return super().setdefault(key, default)

	def get(self, key, default=None):
		key = self.subschema.lookup_attribute(key, fail_if_not_found=True)
		if key in self:
			return self[key]
		return default

	def get_all(self, key):
		result = []
		for attr in self.subschema.lookup_attribute_list(key):
			result += self[attr]
		return result

	def match_present(self, key):
		attribute_type = self.subschema.lookup_attribute(key)
		if attribute_type is None:
			return FilterResult.UNDEFINED
		if self[attribute_type] != []:
			return FilterResult.TRUE
		else:
			return FilterResult.FALSE

	def match_equal(self, key, assertion_value):
		attribute_type = self.subschema.lookup_attribute(key)
		if attribute_type is None or attribute_type.equality is None:
			return FilterResult.UNDEFINED
		assertion_value = attribute_type.equality.syntax.decode(assertion_value)
		if assertion_value is None:
			return FilterResult.UNDEFINED
		return any_3value(map(lambda attrval: attribute_type.equality.match_equal(attrval, assertion_value), self.get_all(key)))

	def match_substr(self, key, inital_substring, any_substrings, final_substring):
		attribute_type = self.subschema.lookup_attribute(key)
		if attribute_type is None or attribute_type.equality is None or attribute_type.substr is None:
			return FilterResult.UNDEFINED
		if inital_substring:
			inital_substring = attribute_type.equality.syntax.decode(inital_substring)
			if inital_substring is None:
				return FilterResult.UNDEFINED
		any_substrings = [attribute_type.equality.syntax.decode(substring) for substring in any_substrings]
		if None in any_substrings:
			return FilterResult.UNDEFINED
		if final_substring:
			final_substring = attribute_type.equality.syntax.decode(final_substring)
			if final_substring is None:
				return FilterResult.UNDEFINED
		return any_3value(map(lambda attrval: attribute_type.substr.match_substr(attrval, inital_substring, any_substrings, final_substring), self.get_all(key)))

	def match_approx(self, key, assertion_value):
		attribute_type = self.subschema.lookup_attribute(key)
		if attribute_type is None or attribute_type.equality is None:
			return FilterResult.UNDEFINED
		assertion_value = attribute_type.equality.syntax.decode(assertion_value)
		if assertion_value is None:
			return FilterResult.UNDEFINED
		return any_3value(map(lambda attrval: attribute_type.equality.match_approx(attrval, assertion_value), self.get_all(key)))

	def match_greater_or_equal(self, key, assertion_value):
		attribute_type = self.subschema.lookup_attribute(key)
		if attribute_type is None or attribute_type.ordering is None:
			return FilterResult.UNDEFINED
		assertion_value = attribute_type.ordering.syntax.decode(assertion_value)
		if assertion_value is None:
			return FilterResult.UNDEFINED
		return any_3value(map(lambda attrval: attribute_type.ordering.match_greater_or_equal(attrval, assertion_value), self.get_all(key)))

	def match_less(self, key, assertion_value):
		attribute_type = self.subschema.lookup_attribute(key)
		if attribute_type is None or attribute_type.ordering is None:
			return FilterResult.UNDEFINED
		assertion_value = attribute_type.ordering.syntax.decode(assertion_value)
		if assertion_value is None:
			return FilterResult.UNDEFINED
		return any_3value(map(lambda attrval: attribute_type.ordering.match_less(attrval, assertion_value), self.get_all(key)))

	def match_less_or_equal(self, key, assertion_value):
		return any_3value((self.match_equal(key, assertion_value),
		                   self.match_less(key, assertion_value)))

	def match_filter(self, filter_obj):
		if isinstance(filter_obj, ldap.FilterAnd):
			return all_3value(map(self.match_filter, filter_obj.filters))
		elif isinstance(filter_obj, ldap.FilterOr):
			return any_3value(map(self.match_filter, filter_obj.filters))
		elif isinstance(filter_obj, ldap.FilterNot):
			subresult = self.match_filter(filter_obj.filter)
			if subresult == FilterResult.TRUE:
				return FilterResult.FALSE
			elif subresult == FilterResult.FALSE:
				return FilterResult.TRUE
			else:
				return subresult
		elif isinstance(filter_obj, ldap.FilterPresent):
			return self.match_present(filter_obj.attribute)
		elif isinstance(filter_obj, ldap.FilterEqual):
			return self.match_equal(filter_obj.attribute, filter_obj.value)
		elif isinstance(filter_obj, ldap.FilterSubstrings):
			return self.match_substr(filter_obj.attribute, filter_obj.initial_substring,
			                         filter_obj.any_substrings, filter_obj.final_substring)
		elif isinstance(filter_obj, ldap.FilterApproxMatch):
			return self.match_approx(filter_obj.attribute, filter_obj.value)
		elif isinstance(filter_obj, ldap.FilterGreaterOrEqual):
			return self.match_greater_or_equal(filter_obj.attribute, filter_obj.value)
		elif isinstance(filter_obj, ldap.FilterLessOrEqual):
			return self.match_less_or_equal(filter_obj.attribute, filter_obj.value)
		else:
			return FilterResult.UNDEFINED

class Object(AttributeDict):
	def __init__(self, subschema, dn, **attributes):
		super().__init__(subschema, **attributes)
		self.dn = DN(dn)
		self.setdefault('subschemaSubentry', [self.subschema.dn])

	def match_dn(self, basedn, scope):
		if scope == ldap.SearchScope.baseObject:
			return self.dn == basedn
		elif scope == ldap.SearchScope.singleLevel:
			return self.dn.is_direct_child_of(basedn)
		elif scope == ldap.SearchScope.wholeSubtree:
			return self.dn.in_subtree_of(basedn)
		else:
			return False

	def match_search(self, base_obj, scope, filter_obj):
		return self.match_dn(DN.from_str(base_obj), scope) and self.match_filter(filter_obj) == FilterResult.TRUE

	def get_search_result_entry(self, attributes=None, types_only=False):
		selected_attributes = set()
		for selector in attributes or ['*']:
			if selector == '*':
				selected_attributes |= self.subschema.user_attribute_types
			elif selector == '1.1':
				continue
			else:
				attribute = self.subschema.lookup_attribute(selector)
				if attribute is not None:
					selected_attributes.add(attribute)
		partial_attributes = []
		for attribute in self:
			if attribute not in selected_attributes:
				continue
			values = self[attribute]
			if values != []:
				if types_only:
					values = []
				partial_attributes.append(ldap.PartialAttribute(attribute.name, [attribute.syntax.encode(value) for value in values]))
		return ldap.SearchResultEntry(str(self.dn), partial_attributes)

class RootDSE(Object):
	def __init__(self, subschema, *args, **kwargs):
		super().__init__(subschema, DN(), *args, **kwargs)

	def match_search(self, base_obj, scope, filter_obj):
		return not base_obj and scope == ldap.SearchScope.baseObject and \
		       isinstance(filter_obj, ldap.FilterPresent) and \
		       filter_obj.attribute.lower() == 'objectclass'

class WildcardValue:
	pass

WILDCARD_VALUE = WildcardValue()

class ObjectTemplate(AttributeDict):
	def __init__(self, subschema, parent_dn, rdn_attribute, **attributes):
		super().__init__(subschema, **attributes)
		self.parent_dn = parent_dn
		self.rdn_attribute = rdn_attribute

	def match_present(self, key):
		attribute_type = self.subschema.lookup_attribute(key)
		if attribute_type is None:
			return FilterResult.UNDEFINED
		values = self[attribute_type]
		if values == []:
			return FilterResult.FALSE
		elif WILDCARD_VALUE in values:
			return FilterResult.MAYBE_TRUE
		else:
			return FilterResult.TRUE

	def match_equal(self, key, assertion_value):
		attribute_type = self.subschema.lookup_attribute(key)
		if attribute_type is None or attribute_type.equality is None:
			return FilterResult.UNDEFINED
		assertion_value = attribute_type.equality.syntax.decode(assertion_value)
		if assertion_value is None:
			return FilterResult.UNDEFINED
		values = self.get_all(key)
		if WILDCARD_VALUE in values:
			return FilterResult.MAYBE_TRUE
		return any_3value(map(lambda attrval: attribute_type.equality.match_equal(attrval, assertion_value), values))

	def match_substr(self, key, inital_substring, any_substrings, final_substring):
		attribute_type = self.subschema.lookup_attribute(key)
		if attribute_type is None or attribute_type.equality is None or attribute_type.substr is None:
			return FilterResult.UNDEFINED
		if inital_substring:
			inital_substring = attribute_type.equality.syntax.decode(inital_substring)
			if inital_substring is None:
				return FilterResult.UNDEFINED
		any_substrings = [attribute_type.equality.syntax.decode(substring) for substring in any_substrings]
		if None in any_substrings:
			return FilterResult.UNDEFINED
		if final_substring:
			final_substring = attribute_type.equality.syntax.decode(final_substring)
			if final_substring is None:
				return FilterResult.UNDEFINED
		values = self.get_all(key)
		if WILDCARD_VALUE in values:
			return FilterResult.MAYBE_TRUE
		return any_3value(map(lambda attrval: attribute_type.substr.match_substr(attrval, inital_substring, any_substrings, final_substring), values))

	def match_approx(self, key, assertion_value):
		attribute_type = self.subschema.lookup_attribute(key)
		if attribute_type is None or attribute_type.equality is None:
			return FilterResult.UNDEFINED
		assertion_value = attribute_type.equality.syntax.decode(assertion_value)
		if assertion_value is None:
			return FilterResult.UNDEFINED
		values = self.get_all(key)
		if WILDCARD_VALUE in values:
			return FilterResult.MAYBE_TRUE
		return any_3value(map(lambda attrval: attribute_type.equality.match_approx(attrval, assertion_value), values))

	def match_greater_or_equal(self, key, assertion_value):
		attribute_type = self.subschema.lookup_attribute(key)
		if attribute_type is None or attribute_type.ordering is None:
			return FilterResult.UNDEFINED
		assertion_value = attribute_type.ordering.syntax.decode(assertion_value)
		if assertion_value is None:
			return FilterResult.UNDEFINED
		values = self.get_all(key)
		if WILDCARD_VALUE in values:
			return FilterResult.MAYBE_TRUE
		return any_3value(map(lambda attrval: attribute_type.ordering.match_greater_or_equal(attrval, assertion_value), values))

	def match_less(self, key, assertion_value):
		attribute_type = self.subschema.lookup_attribute(key)
		if attribute_type is None or attribute_type.ordering is None:
			return FilterResult.UNDEFINED
		assertion_value = attribute_type.ordering.syntax.decode(assertion_value)
		if assertion_value is None:
			return FilterResult.UNDEFINED
		values = self.get_all(key)
		if WILDCARD_VALUE in values:
			return FilterResult.MAYBE_TRUE
		return any_3value(map(lambda attrval: attribute_type.ordering.match_less(attrval, assertion_value), values))

	def __extract_dn_constraints(self, basedn, scope):
		if scope == ldap.SearchScope.baseObject:
			if basedn[1:] != self.parent_dn or basedn.object_attribute != self.rdn_attribute:
				return False, AttributeDict(self.subschema)
			return True, AttributeDict(self.subschema, **{self.rdn_attribute: [basedn.object_value]})
		elif scope == ldap.SearchScope.singleLevel:
			return basedn == self.parent_dn, AttributeDict(self.subschema)
		elif scope == ldap.SearchScope.wholeSubtree:
			if self.parent_dn.in_subtree_of(basedn):
				return True, AttributeDict(self.subschema)
			if basedn[1:] != self.parent_dn or basedn.object_attribute != self.rdn_attribute:
				return False, AttributeDict(self.subschema)
			return True, AttributeDict(self.subschema, **{self.rdn_attribute: [basedn.object_value]})
		else:
			return False, AttributeDict(self.subschema)

	def match_dn(self, basedn, scope):
		'''Return whether objects from this template might match the provided parameters'''
		return self.__extract_dn_constraints(basedn, scope)[0]

	def extract_dn_constraints(self, basedn, scope):
		return self.__extract_dn_constraints(basedn, scope)[1]

	def extract_filter_constraints(self, filter_obj):
		if isinstance(filter_obj, ldap.FilterEqual):
			attribute_type = self.subschema.lookup_attribute(filter_obj.attribute)
			if attribute_type is None or attribute_type.equality is None:
				return AttributeDict(self.subschema)
			assertion_value = attribute_type.equality.syntax.decode(filter_obj.value)
			if assertion_value is None:
				return AttributeDict(self.subschema)
			return AttributeDict(self.subschema, **{filter_obj.attribute: [assertion_value]})
		if isinstance(filter_obj, ldap.FilterAnd):
			result = AttributeDict(self.subschema)
			for subfilter in filter_obj.filters:
				for name, values in self.extract_filter_constraints(subfilter).items():
					result[name] += values
			return result
		return AttributeDict(self.subschema)

	def match_search(self, base_obj, scope, filter_obj):
		'''Return whether objects based on this template might match the search parameters'''
		return self.match_dn(DN.from_str(base_obj), scope) and self.match_filter(filter_obj) in (FilterResult.TRUE, FilterResult.MAYBE_TRUE)

	def extract_search_constraints(self, base_obj, scope, filter_obj):
		constraints = self.extract_filter_constraints(filter_obj)
		for key, values in self.extract_dn_constraints(DN.from_str(base_obj), scope).items():
			constraints[key] += values
		return constraints

	def create_object(self, rdn_value, **attributes):
		obj = Object(self.subschema, DN(self.parent_dn, **{self.rdn_attribute: rdn_value}))
		for key, values in attributes.items():
			if WILDCARD_VALUE not in self[key]:
				raise ValueError(f'Cannot set attribute "{key}" that is not set to [WILDCARD_VALUE] in the template')
			obj[key] = values
		for attribute_type, values in self.items():
			if WILDCARD_VALUE not in values:
				obj[attribute_type] = values
		return obj

class Subschema(Object):
	def __init__(self, dn, object_classes=None, attribute_types=None, matching_rules=None, syntaxes=None):
		# Setup schema data before calling super().__init__(), because we are our own schema
		attribute_types = list(attribute_types or [])
		matching_rules = list(matching_rules or [])
		syntaxes = list(syntaxes or [])
		self.object_classes = {}
		for objectclass in object_classes or []:
			self.object_classes[objectclass.oid] = objectclass
			attribute_types += objectclass.must + objectclass.may
		self.attribute_types = {}
		self.attribute_types_by_name = {}
		self.attribute_types_by_unique_name = {}
		self.user_attribute_types = set()
		for attribute_type in attribute_types:
			self.attribute_types[attribute_type.oid] = attribute_type
			for name in attribute_type.names:
				name = name.lower()
				self.attribute_types_by_name[name] = \
					self.attribute_types_by_name.get(name, set()) | {attribute_type}
			self.attribute_types_by_unique_name[attribute_type.name.lower()] = attribute_type
			if attribute_type.usage == AttributeTypeUsage.userApplications:
				self.user_attribute_types.add(attribute_type)
			if attribute_type.equality is not None:
				matching_rules += [attribute_type.equality]
			if attribute_type.ordering is not None:
				matching_rules += [attribute_type.ordering]
			if attribute_type.substr is not None:
				matching_rules += [attribute_type.substr]
			syntaxes += [type(attribute_type.syntax)]
		self.matching_rules = {}
		for matching_rule in matching_rules:
			self.matching_rules[matching_rule.oid] = matching_rule
			syntaxes += [type(matching_rule.syntax)]
		self.syntaxes = {}
		for syntax in syntaxes:
			self.syntaxes[syntax.oid] = syntax

		super().__init__(subschema=self, dn=dn)
		# pylint: disable=invalid-name
		self.AttributeDict = lambda **attributes: AttributeDict(self, **attributes)
		self.Object = lambda dn, **attributes: Object(self, dn, **attributes)
		self.RootDSE = lambda **attributes: RootDSE(self, **attributes)
		self.ObjectTemplate = lambda *args, **kwargs: ObjectTemplate(self, *args, **kwargs)
		self['objectClass'] = [objectclass.schema_encoding for objectclass in self.object_classes.values()]
		self['ldapSyntaxes'] = [syntax.encode_syntax_definition() for syntax in self.syntaxes.values()]
		self['matchingRules'] = [matching_rule.encode_syntax_definition() for matching_rule in self.matching_rules.values()]
		self['attributeTypes'] = [attribute_type.schema_encoding for attribute_type in self.attribute_types.values()]

	def extend(self, *subschemas, dn=None, object_classes=None, attribute_types=None, matching_rules=None, syntaxes=None):
		if dn is None:
			dn = self.dn
		object_classes = list(self.object_classes.values()) + list(object_classes or [])
		attribute_types = list(self.attribute_types.values()) + list(attribute_types or [])
		matching_rules = list(self.matching_rules.values()) + list(matching_rules or [])
		syntaxes = list(self.syntaxes.values()) + list(syntaxes or [])
		for subschema in subschemas:
			object_classes += list(subschema.object_classes.values())
			attribute_types += list(subschema.attribute_types.values())
			matching_rules += list(subschema.matching_rules.values())
			syntaxes += list(subschema.syntaxes.values())
		return Subschema(dn, object_classes, attribute_types, matching_rules, syntaxes)

	def lookup_attribute(self, oid_or_name, fail_if_not_found=False):
		if isinstance(oid_or_name, AttributeType):
			if self.attribute_types.get(oid_or_name.oid) != oid_or_name:
				raise Exception()
			return oid_or_name
		if oid_or_name in self.attribute_types:
			return self.attribute_types[oid_or_name]
		result = self.attribute_types_by_unique_name.get(oid_or_name.lower())
		if result is None and fail_if_not_found:
			raise Exception(f'Attribute "{oid_or_name}" not in schema')
		return result

	def lookup_attribute_list(self, oid_or_name):
		if oid_or_name in self.attribute_types_by_name:
			return list(self.attribute_types_by_name[oid_or_name])
		result = self.lookup_attribute(oid_or_name)
		if result is None:
			return []
		return [result]

	def match_search(self, base_obj, scope, filter_obj):
		return DN.from_str(base_obj) == self.dn and  \
		       scope == ldap.SearchScope.baseObject and \
		       isinstance(filter_obj, ldap.FilterEqual) and \
		       filter_obj.attribute.lower() == 'objectclass' and \
		       filter_obj.value.lower() == b'subschema'

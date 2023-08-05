from ..types import MatchingRule, FilterResult
from ... import rfc4518_stringprep
from . import syntaxes

class GenericMatchingRule(MatchingRule):
	def match_equal(self, attribute_value, assertion_value):
		if attribute_value == assertion_value:
			return FilterResult.TRUE
		else:
			return FilterResult.FALSE

	def match_less(self, attribute_value, assertion_value):
		if attribute_value < assertion_value:
			return FilterResult.TRUE
		else:
			return FilterResult.FALSE

	def match_greater_or_equal(self, attribute_value, assertion_value):
		if attribute_value >= assertion_value:
			return FilterResult.TRUE
		else:
			return FilterResult.FALSE

class StringMatchingRule(MatchingRule):
	def __init__(self, oid, name, syntax, matching_type=rfc4518_stringprep.MatchingType.EXACT_STRING):
		super().__init__(oid, name, syntax)
		self.matching_type = matching_type

	def match_equal(self, attribute_value, assertion_value):
		try:
			attribute_value = rfc4518_stringprep.prepare(attribute_value, self.matching_type)
			assertion_value = rfc4518_stringprep.prepare(assertion_value, self.matching_type)
		except ValueError:
			return FilterResult.UNDEFINED
		if attribute_value == assertion_value:
			return FilterResult.TRUE
		else:
			return FilterResult.FALSE

	def match_less(self, attribute_value, assertion_value):
		try:
			attribute_value = rfc4518_stringprep.prepare(attribute_value, self.matching_type)
			assertion_value = rfc4518_stringprep.prepare(assertion_value, self.matching_type)
		except ValueError:
			return FilterResult.UNDEFINED
		if attribute_value < assertion_value:
			return FilterResult.TRUE
		else:
			return FilterResult.FALSE

	def match_greater_or_equal(self, attribute_value, assertion_value):
		try:
			attribute_value = rfc4518_stringprep.prepare(attribute_value, self.matching_type)
			assertion_value = rfc4518_stringprep.prepare(assertion_value, self.matching_type)
		except ValueError:
			return FilterResult.UNDEFINED
		if attribute_value >= assertion_value:
			return FilterResult.TRUE
		else:
			return FilterResult.FALSE

	def match_substr(self, attribute_value, inital_substring, any_substrings, final_substring):
		try:
			attribute_value = rfc4518_stringprep.prepare(attribute_value, self.matching_type)
			if inital_substring:
				inital_substring = rfc4518_stringprep.prepare(inital_substring, self.matching_type, rfc4518_stringprep.SubstringType.INITIAL)
			any_substrings = [rfc4518_stringprep.prepare(substring, self.matching_type, rfc4518_stringprep.SubstringType.ANY) for substring in any_substrings]
			if final_substring:
				final_substring = rfc4518_stringprep.prepare(final_substring, self.matching_type, rfc4518_stringprep.SubstringType.FINAL)
		except ValueError:
			return FilterResult.UNDEFINED
		if inital_substring:
			if not attribute_value.startswith(inital_substring):
				return FilterResult.FALSE
			attribute_value = attribute_value[len(inital_substring):]
		if final_substring:
			if not attribute_value.endswith(final_substring):
				return FilterResult.FALSE
			attribute_value = attribute_value[:-len(final_substring)]
		for substring in any_substrings:
			index = attribute_value.find(substring)
			if index == -1:
				return FilterResult.FALSE
			attribute_value = attribute_value[index+len(substring):]
		return FilterResult.TRUE

class StringListMatchingRule(MatchingRule):
	def __init__(self, oid, name, syntax, matching_type=rfc4518_stringprep.MatchingType.EXACT_STRING):
		super().__init__(oid, name, syntax)
		self.matching_type = matching_type

	# Values are both lists of str
	def match_equal(self, attribute_value, assertion_value):
		try:
			attribute_value = [rfc4518_stringprep.prepare(line, self.matching_type) for line in attribute_value]
			assertion_value = [rfc4518_stringprep.prepare(line, self.matching_type) for line in assertion_value]
		except ValueError:
			return FilterResult.UNDEFINED
		if attribute_value == assertion_value:
			return FilterResult.TRUE
		else:
			return FilterResult.FALSE

class FirstComponentMatchingRule(MatchingRule):
	def __init__(self, oid, name, syntax, attribute_name):
		super().__init__(oid, name, syntax)
		self.attribute_name = attribute_name

	def match_equal(self, attribute_value, assertion_value):
		if not hasattr(attribute_value, self.attribute_name):
			return None
		if getattr(attribute_value, self.attribute_name)() == assertion_value:
			return FilterResult.TRUE
		else:
			return FilterResult.FALSE

bitStringMatch = GenericMatchingRule('2.5.13.16', name='bitStringMatch', syntax=syntaxes.BitString())
booleanMatch = GenericMatchingRule('2.5.13.13', name='booleanMatch', syntax=syntaxes.Boolean())
caseExactIA5Match = StringMatchingRule('1.3.6.1.4.1.1466.109.114.1', name='caseExactIA5Match', syntax=syntaxes.IA5String(), matching_type=rfc4518_stringprep.MatchingType.EXACT_STRING)
caseExactMatch = StringMatchingRule('2.5.13.5', name='caseExactMatch', syntax=syntaxes.DirectoryString(), matching_type=rfc4518_stringprep.MatchingType.EXACT_STRING)
caseExactOrderingMatch = StringMatchingRule('2.5.13.6', name='caseExactOrderingMatch', syntax=syntaxes.DirectoryString(), matching_type=rfc4518_stringprep.MatchingType.EXACT_STRING)
caseExactSubstringsMatch = StringMatchingRule('2.5.13.7', name='caseExactSubstringsMatch', syntax=syntaxes.SubstringAssertion(), matching_type=rfc4518_stringprep.MatchingType.EXACT_STRING)
caseIgnoreIA5Match = StringMatchingRule('1.3.6.1.4.1.1466.109.114.2', name='caseIgnoreIA5Match', syntax=syntaxes.IA5String(), matching_type=rfc4518_stringprep.MatchingType.CASE_IGNORE_STRING)
caseIgnoreIA5SubstringsMatch = StringMatchingRule('1.3.6.1.4.1.1466.109.114.3', name='caseIgnoreIA5SubstringsMatch', syntax=syntaxes.SubstringAssertion(), matching_type=rfc4518_stringprep.MatchingType.CASE_IGNORE_STRING)
caseIgnoreListMatch = StringListMatchingRule('2.5.13.11', name='caseIgnoreListMatch', syntax=syntaxes.PostalAddress(), matching_type=rfc4518_stringprep.MatchingType.CASE_IGNORE_STRING)
caseIgnoreListSubstringsMatch = StringListMatchingRule('2.5.13.12', name='caseIgnoreListSubstringsMatch', syntax=syntaxes.SubstringAssertion(), matching_type=rfc4518_stringprep.MatchingType.CASE_IGNORE_STRING)
caseIgnoreMatch = StringMatchingRule('2.5.13.2', name='caseIgnoreMatch', syntax=syntaxes.DirectoryString(), matching_type=rfc4518_stringprep.MatchingType.CASE_IGNORE_STRING)
caseIgnoreOrderingMatch = StringMatchingRule('2.5.13.3', name='caseIgnoreOrderingMatch', syntax=syntaxes.DirectoryString(), matching_type=rfc4518_stringprep.MatchingType.CASE_IGNORE_STRING)
caseIgnoreSubstringsMatch = StringMatchingRule('2.5.13.4', name='caseIgnoreSubstringsMatch', syntax=syntaxes.SubstringAssertion(), matching_type=rfc4518_stringprep.MatchingType.CASE_IGNORE_STRING)
directoryStringFirstComponentMatch = FirstComponentMatchingRule('2.5.13.31', name='directoryStringFirstComponentMatch', syntax=syntaxes.DirectoryString(), attribute_name='get_first_component_string')
distinguishedNameMatch = GenericMatchingRule('2.5.13.1', name='distinguishedNameMatch', syntax=syntaxes.DN())
generalizedTimeMatch = GenericMatchingRule('2.5.13.27', name='generalizedTimeMatch', syntax=syntaxes.GeneralizedTime())
generalizedTimeOrderingMatch = GenericMatchingRule('2.5.13.28', name='generalizedTimeOrderingMatch', syntax=syntaxes.GeneralizedTime())
integerFirstComponentMatch = FirstComponentMatchingRule('2.5.13.29', name='integerFirstComponentMatch', syntax=syntaxes.INTEGER(), attribute_name='get_first_component_integer')
integerMatch = GenericMatchingRule('2.5.13.14', name='integerMatch', syntax=syntaxes.INTEGER())
integerOrderingMatch = GenericMatchingRule('2.5.13.15', name='integerOrderingMatch', syntax=syntaxes.INTEGER())
# Optional and implementation-specific, we simply never match
keywordMatch = MatchingRule('2.5.13.33', name='keywordMatch', syntax=syntaxes.DirectoryString())
numericStringMatch = StringMatchingRule('2.5.13.8', name='numericStringMatch', syntax=syntaxes.NumericString(), matching_type=rfc4518_stringprep.MatchingType.NUMERIC_STRING)
numericStringOrderingMatch = StringMatchingRule('2.5.13.9', name='numericStringOrderingMatch', syntax=syntaxes.NumericString(), matching_type=rfc4518_stringprep.MatchingType.NUMERIC_STRING)
numericStringSubstringsMatch = StringMatchingRule('2.5.13.10', name='numericStringSubstringsMatch', syntax=syntaxes.SubstringAssertion(), matching_type=rfc4518_stringprep.MatchingType.NUMERIC_STRING)
objectIdentifierFirstComponentMatch = FirstComponentMatchingRule('2.5.13.30', name='objectIdentifierFirstComponentMatch', syntax=syntaxes.OID(), attribute_name='get_first_component_oid')
objectIdentifierMatch = StringMatchingRule('2.5.13.0', name='objectIdentifierMatch', syntax=syntaxes.OID(), matching_type=rfc4518_stringprep.MatchingType.CASE_IGNORE_STRING)
octetStringMatch = GenericMatchingRule('2.5.13.17', name='octetStringMatch', syntax=syntaxes.OctetString())
octetStringOrderingMatch = GenericMatchingRule('2.5.13.18', name='octetStringOrderingMatch', syntax=syntaxes.OctetString())
telephoneNumberMatch = StringMatchingRule('2.5.13.20', name='telephoneNumberMatch', syntax=syntaxes.TelephoneNumber(), matching_type=rfc4518_stringprep.MatchingType.TELEPHONE_NUMBER)
telephoneNumberSubstringsMatch = StringMatchingRule('2.5.13.21', name='telephoneNumberSubstringsMatch', syntax=syntaxes.SubstringAssertion(), matching_type=rfc4518_stringprep.MatchingType.TELEPHONE_NUMBER)
uniqueMemberMatch = GenericMatchingRule('2.5.13.23', name='uniqueMemberMatch', syntax=syntaxes.NameAndOptionalUID())
# Optional and implementation-specific, we simply never match
wordMatch = MatchingRule('2.5.13.32', name='wordMatch', syntax=syntaxes.DirectoryString())

ALL = (
	bitStringMatch,
	booleanMatch,
	caseExactIA5Match,
	caseExactMatch,
	caseExactOrderingMatch,
	caseExactSubstringsMatch,
	caseIgnoreIA5Match,
	caseIgnoreIA5SubstringsMatch,
	caseIgnoreListMatch,
	caseIgnoreListSubstringsMatch,
	caseIgnoreMatch,
	caseIgnoreOrderingMatch,
	caseIgnoreSubstringsMatch,
	directoryStringFirstComponentMatch,
	distinguishedNameMatch,
	generalizedTimeMatch,
	generalizedTimeOrderingMatch,
	integerFirstComponentMatch,
	integerMatch,
	integerOrderingMatch,
	#keywordMatch,
	numericStringMatch,
	numericStringOrderingMatch,
	numericStringSubstringsMatch,
	objectIdentifierFirstComponentMatch,
	objectIdentifierMatch,
	octetStringMatch,
	octetStringOrderingMatch,
	telephoneNumberMatch,
	telephoneNumberSubstringsMatch,
	uniqueMemberMatch,
	#wordMatch,
)

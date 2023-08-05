
# pylint: disable=wildcard-import,unused-wildcard-import,unused-import

from ..types import AttributeType
from ..rfc4524.attribute_types import *
from ..rfc3112.attribute_types import authPassword, ALL as RFC3112_ALL
from . import syntaxes, matching_rules

uidNumber = AttributeType('1.3.6.1.1.1.1.0', name='uidNumber', desc='An integer uniquely identifying a user in an administrative domain', equality=matching_rules.integerMatch, ordering=matching_rules.integerOrderingMatch, syntax=syntaxes.INTEGER(), single_value=True)
gidNumber = AttributeType('1.3.6.1.1.1.1.1', name='gidNumber', desc='An integer uniquely identifying a group in an administrative domain', equality=matching_rules.integerMatch, ordering=matching_rules.integerOrderingMatch, syntax=syntaxes.INTEGER(), single_value=True)
gecos = AttributeType('1.3.6.1.1.1.1.2', name='gecos', desc='The GECOS field; the common name', equality=matching_rules.caseIgnoreMatch, substr=matching_rules.caseIgnoreSubstringsMatch, syntax=syntaxes.DirectoryString(), single_value=True)
homeDirectory = AttributeType('1.3.6.1.1.1.1.3', name='homeDirectory', desc='The absolute path to the home directory', equality=matching_rules.caseExactIA5Match, syntax=syntaxes.IA5String(), single_value=True)
loginShell = AttributeType('1.3.6.1.1.1.1.4', name='loginShell', desc='The path to the login shell', equality=matching_rules.caseExactIA5Match, syntax=syntaxes.IA5String(), single_value=True)
shadowLastChange = AttributeType('1.3.6.1.1.1.1.5', name='shadowLastChange', equality=matching_rules.integerMatch, ordering=matching_rules.integerOrderingMatch, syntax=syntaxes.INTEGER(), single_value=True)
shadowMin = AttributeType('1.3.6.1.1.1.1.6', name='shadowMin', equality=matching_rules.integerMatch, ordering=matching_rules.integerOrderingMatch, syntax=syntaxes.INTEGER(), single_value=True)
shadowMax = AttributeType('1.3.6.1.1.1.1.7', name='shadowMax', equality=matching_rules.integerMatch, ordering=matching_rules.integerOrderingMatch, syntax=syntaxes.INTEGER(), single_value=True)
shadowWarning = AttributeType('1.3.6.1.1.1.1.8', name='shadowWarning', equality=matching_rules.integerMatch, ordering=matching_rules.integerOrderingMatch, syntax=syntaxes.INTEGER(), single_value=True)
shadowInactive = AttributeType('1.3.6.1.1.1.1.9', name='shadowInactive', equality=matching_rules.integerMatch, ordering=matching_rules.integerOrderingMatch, syntax=syntaxes.INTEGER(), single_value=True)
shadowExpire = AttributeType('1.3.6.1.1.1.1.10', name='shadowExpire', equality=matching_rules.integerMatch, ordering=matching_rules.integerOrderingMatch, syntax=syntaxes.INTEGER(), single_value=True)
shadowFlag = AttributeType('1.3.6.1.1.1.1.11', name='shadowFlag', equality=matching_rules.integerMatch, ordering=matching_rules.integerOrderingMatch, syntax=syntaxes.INTEGER(), single_value=True)
memberUid = AttributeType('1.3.6.1.1.1.1.12', name='memberUid', equality=matching_rules.caseExactMatch, syntax=syntaxes.DirectoryString())
memberNisNetgroup = AttributeType('1.3.6.1.1.1.1.13', name='memberNisNetgroup', equality=matching_rules.caseExactMatch, syntax=syntaxes.DirectoryString())
nisNetgroupTriple = AttributeType('1.3.6.1.1.1.1.14', name='nisNetgroupTriple', desc='Netgroup triple', equality=matching_rules.caseIgnoreMatch, substr=matching_rules.caseIgnoreSubstringsMatch, syntax=syntaxes.DirectoryString())
ipServicePort = AttributeType('1.3.6.1.1.1.1.15', name='ipServicePort', desc='Service port number', equality=matching_rules.integerMatch, ordering=matching_rules.integerOrderingMatch, syntax=syntaxes.INTEGER(), single_value=True)
ipServiceProtocol = AttributeType('1.3.6.1.1.1.1.16', name='ipServiceProtocol', desc='Service protocol name', equality=matching_rules.caseIgnoreMatch, syntax=syntaxes.DirectoryString())
ipProtocolNumber = AttributeType('1.3.6.1.1.1.1.17', name='ipProtocolNumber', desc='IP protocol number', equality=matching_rules.integerMatch, ordering=matching_rules.integerOrderingMatch, syntax=syntaxes.INTEGER(), single_value=True)
oncRpcNumber = AttributeType('1.3.6.1.1.1.1.18', name='oncRpcNumber', desc='ONC RPC number', equality=matching_rules.integerMatch, ordering=matching_rules.integerOrderingMatch, syntax=syntaxes.INTEGER(), single_value=True)
ipHostNumber = AttributeType('1.3.6.1.1.1.1.19', name='ipHostNumber', desc='IPv4 addresses as a dotted decimal omitting leading zeros or IPv6 addresses as defined in RFC2373', equality=matching_rules.caseIgnoreIA5Match, syntax=syntaxes.IA5String())
ipNetworkNumber = AttributeType('1.3.6.1.1.1.1.20', name='ipNetworkNumber', desc='IP network omitting leading zeros, eg. 192.168', equality=matching_rules.caseIgnoreIA5Match, syntax=syntaxes.IA5String(), single_value=True)
ipNetmaskNumber = AttributeType('1.3.6.1.1.1.1.21', name='ipNetmaskNumber', desc='IP netmask omitting leading zeros, eg. 255.255.255.0', equality=matching_rules.caseIgnoreIA5Match, syntax=syntaxes.IA5String(), single_value=True)
macAddress = AttributeType('1.3.6.1.1.1.1.22', name='macAddress', desc='MAC address in maximal, colon separated hex notation, eg. 00:00:92:90:ee:e2', equality=matching_rules.caseIgnoreIA5Match, syntax=syntaxes.IA5String())
bootParameter = AttributeType('1.3.6.1.1.1.1.23', name='bootParameter', desc='rpc.bootparamd parameter', equality=matching_rules.caseExactIA5Match, syntax=syntaxes.IA5String())
bootFile = AttributeType('1.3.6.1.1.1.1.24', name='bootFile', desc='Boot image name', equality=matching_rules.caseExactIA5Match, syntax=syntaxes.IA5String())
nisMapName = AttributeType('1.3.6.1.1.1.1.26', name='nisMapName', desc='Name of a generic NIS map', equality=matching_rules.caseIgnoreMatch, syntax=syntaxes.DirectoryString(64))
nisMapEntry = AttributeType('1.3.6.1.1.1.1.27', name='nisMapEntry', desc='A generic NIS entry', equality=matching_rules.caseExactMatch, syntax=syntaxes.DirectoryString(1024), single_value=True)
nisPublicKey = AttributeType('1.3.6.1.1.1.1.28', name='nisPublicKey', desc='NIS public key', equality=matching_rules.octetStringMatch, syntax=syntaxes.OctetString(), single_value=True)
nisSecretKey = AttributeType('1.3.6.1.1.1.1.29', name='nisSecretKey', desc='NIS secret key', equality=matching_rules.octetStringMatch, syntax=syntaxes.OctetString(), single_value=True)
nisDomain = AttributeType('1.3.6.1.1.1.1.30', name='nisDomain', desc='NIS domain', equality=matching_rules.caseIgnoreIA5Match, syntax=syntaxes.IA5String(256))
automountMapName = AttributeType('1.3.6.1.1.1.1.31', name='automountMapName', desc='automount Map Name', equality=matching_rules.caseExactMatch, syntax=syntaxes.DirectoryString(), single_value=True)
automountKey = AttributeType('1.3.6.1.1.1.1.32', name='automountKey', desc='Automount Key value', equality=matching_rules.caseExactMatch, syntax=syntaxes.DirectoryString(), single_value=True)
automountInformation = AttributeType('1.3.6.1.1.1.1.33', name='automountInformation', desc='Automount information', equality=matching_rules.caseExactMatch, syntax=syntaxes.DirectoryString(), single_value=True)

ALL = ALL + RFC3112_ALL + (
	uidNumber,
	gidNumber,
	gecos,
	homeDirectory,
	loginShell,
	shadowLastChange,
	shadowMin,
	shadowMax,
	shadowWarning,
	shadowInactive,
	shadowExpire,
	shadowFlag,
	memberUid,
	memberNisNetgroup,
	nisNetgroupTriple,
	ipServicePort,
	ipServiceProtocol,
	ipProtocolNumber,
	oncRpcNumber,
	ipHostNumber,
	ipNetworkNumber,
	ipNetmaskNumber,
	macAddress,
	bootParameter,
	bootFile,
	nisMapName,
	nisMapEntry,
	nisPublicKey,
	nisSecretKey,
	nisDomain,
	automountMapName,
	automountKey,
	automountInformation,
)


# pylint: disable=wildcard-import,unused-wildcard-import

from ..types import ObjectClass, ObjectClassKind
from ..rfc3112.object_classes import ALL as RFC3112_ALL
from ..rfc4524.object_classes import *
from . import attribute_types

posixAccount = ObjectClass('1.3.6.1.1.1.2.0', name='posixAccount', sup=top, kind=ObjectClassKind.AUXILIARY, desc='Abstraction of an account with POSIX attributes', must=[attribute_types.cn, attribute_types.uid, attribute_types.uidNumber, attribute_types.gidNumber, attribute_types.homeDirectory], may=[attribute_types.authPassword, attribute_types.userPassword, attribute_types.loginShell, attribute_types.gecos, attribute_types.description])
shadowAccount = ObjectClass('1.3.6.1.1.1.2.1', name='shadowAccount', sup=top, kind=ObjectClassKind.AUXILIARY, desc='Additional attributes for shadow passwords', must=[attribute_types.uid], may=[attribute_types.authPassword, attribute_types.userPassword, attribute_types.description, attribute_types.shadowLastChange, attribute_types.shadowMin, attribute_types.shadowMax, attribute_types.shadowWarning, attribute_types.shadowInactive, attribute_types.shadowExpire, attribute_types.shadowFlag])
posixGroup = ObjectClass('1.3.6.1.1.1.2.2', name='posixGroup', sup=top, kind=ObjectClassKind.AUXILIARY, desc='Abstraction of a group of accounts', must=[attribute_types.gidNumber], may=[attribute_types.authPassword, attribute_types.userPassword, attribute_types.memberUid, attribute_types.description])
ipService = ObjectClass('1.3.6.1.1.1.2.3', name='ipService', sup=top, kind=ObjectClassKind.STRUCTURAL, desc='Abstraction an Internet Protocol service.  Maps an IP port and protocol (such as tcp or udp) to one or more names; the distinguished value of the cn attribute denotes the service\'s canonical name', must=[attribute_types.cn, attribute_types.ipServicePort, attribute_types.ipServiceProtocol], may=[attribute_types.description])
ipProtocol = ObjectClass('1.3.6.1.1.1.2.4', name='ipProtocol', sup=top, kind=ObjectClassKind.STRUCTURAL, desc='Abstraction of an IP protocol. Maps a protocol number to one or more names. The distinguished value of the cn attribute denotes the protocol canonical name', must=[attribute_types.cn, attribute_types.ipProtocolNumber], may=[attribute_types.description])
oncRpc = ObjectClass('1.3.6.1.1.1.2.5', name='oncRpc', sup=top, kind=ObjectClassKind.STRUCTURAL, desc='Abstraction of an Open Network Computing (ONC) [RFC1057] Remote Procedure Call (RPC) binding.  This class maps an ONC RPC number to a name.  The distinguished value of the cn attribute denotes the RPC service canonical name', must=[attribute_types.cn, attribute_types.oncRpcNumber], may=[attribute_types.description])
ipHost = ObjectClass('1.3.6.1.1.1.2.6', name='ipHost', sup=top, kind=ObjectClassKind.AUXILIARY, desc='Abstraction of a host, an IP device. The distinguished value of the cn attribute denotes the host\'s canonical name. Device SHOULD be used as a structural class', must=[attribute_types.cn, attribute_types.ipHostNumber], may=[attribute_types.authPassword, attribute_types.userPassword, attribute_types.l, attribute_types.description, attribute_types.manager])
ipNetwork = ObjectClass('1.3.6.1.1.1.2.7', name='ipNetwork', sup=top, kind=ObjectClassKind.STRUCTURAL, desc='Abstraction of a network. The distinguished value of the cn attribute denotes the network canonical name', must=[attribute_types.ipNetworkNumber], may=[attribute_types.cn, attribute_types.ipNetmaskNumber, attribute_types.l, attribute_types.description, attribute_types.manager])
nisNetgroup = ObjectClass('1.3.6.1.1.1.2.8', name='nisNetgroup', sup=top, kind=ObjectClassKind.STRUCTURAL, desc='Abstraction of a netgroup. May refer to other netgroups', must=[attribute_types.cn], may=[attribute_types.nisNetgroupTriple, attribute_types.memberNisNetgroup, attribute_types.description])
nisMap = ObjectClass('1.3.6.1.1.1.2.9', name='nisMap', sup=top, kind=ObjectClassKind.STRUCTURAL, desc='A generic abstraction of a NIS map', must=[attribute_types.nisMapName], may=[attribute_types.description])
nisObject = ObjectClass('1.3.6.1.1.1.2.10', name='nisObject', sup=top, kind=ObjectClassKind.STRUCTURAL, desc='An entry in a NIS map', must=[attribute_types.cn, attribute_types.nisMapEntry, attribute_types.nisMapName])
ieee802Device = ObjectClass('1.3.6.1.1.1.2.11', name='ieee802Device', sup=top, kind=ObjectClassKind.AUXILIARY, desc='A device with a MAC address; device SHOULD be used as a structural class', may=[attribute_types.macAddress])
bootableDevice = ObjectClass('1.3.6.1.1.1.2.12', name='bootableDevice', sup=top, kind=ObjectClassKind.AUXILIARY, desc='A device with boot parameters; device SHOULD be used as a structural class', may=[attribute_types.bootFile, attribute_types.bootParameter])
nisKeyObject = ObjectClass('1.3.6.1.1.1.2.14', name='nisKeyObject', sup=top, kind=ObjectClassKind.AUXILIARY, desc='An object with a public and secret key', must=[attribute_types.cn, attribute_types.nisPublicKey, attribute_types.nisSecretKey], may=[attribute_types.uidNumber, attribute_types.description])
nisDomainObject = ObjectClass('1.3.6.1.1.1.2.15', name='nisDomainObject', sup=top, kind=ObjectClassKind.AUXILIARY, desc='Associates a NIS domain with a naming context', must=[attribute_types.nisDomain])
automountMap = ObjectClass('1.3.6.1.1.1.2.16', name='automountMap', sup=top, kind=ObjectClassKind.STRUCTURAL, must=[attribute_types.automountMapName], may=[attribute_types.description])
automount = ObjectClass('1.3.6.1.1.1.2.17', name='automount', sup=top, kind=ObjectClassKind.STRUCTURAL, desc='Automount information', must=[attribute_types.automountKey, attribute_types.automountInformation], may=[attribute_types.description])
groupOfMembers = ObjectClass('1.3.6.1.1.1.2.18', name='groupOfMembers', sup=top, kind=ObjectClassKind.STRUCTURAL, desc='A group with members (DNs)', must=[attribute_types.cn], may=[attribute_types.businessCategory, attribute_types.seeAlso, attribute_types.owner, attribute_types.ou, attribute_types.o, attribute_types.description, attribute_types.member])

ALL = ALL + RFC3112_ALL + (
	posixAccount,
	shadowAccount,
	posixGroup,
	ipService,
	ipProtocol,
	oncRpc,
	ipHost,
	ipNetwork,
	nisNetgroup,
	nisMap,
	nisObject,
	ieee802Device,
	bootableDevice,
	nisKeyObject,
	nisDomainObject,
	automountMap,
	automount,
	groupOfMembers,
)

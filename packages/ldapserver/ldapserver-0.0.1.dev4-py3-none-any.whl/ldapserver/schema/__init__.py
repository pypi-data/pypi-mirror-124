from .types import *
from . import rfc4517, rfc4512, rfc4519, rfc4524, rfc3112, rfc2307bis, rfc2079, rfc2252, rfc2798, rfc4523, rfc1274

# Core LDAP Schema
RFC4519_SUBSCHEMA = Subschema('cn=Subschema', rfc4519.object_classes.ALL, rfc4519.attribute_types.ALL, rfc4519.matching_rules.ALL, rfc4519.matching_rules.ALL)

# COSINE LDAP/X.500 Schema
RFC4524_SUBSCHEMA = Subschema('cn=Subschema', rfc4524.object_classes.ALL, rfc4524.attribute_types.ALL, rfc4524.matching_rules.ALL, rfc4524.matching_rules.ALL)

# inetOrgPerson Schema
RFC2798_SUBSCHEMA = Subschema('cn=Subschema', rfc2798.object_classes.ALL, rfc2798.attribute_types.ALL, rfc2798.matching_rules.ALL, rfc2798.matching_rules.ALL)

# Extended RFC2307 (NIS) Schema
RFC2307BIS_SUBSCHEMA = Subschema('cn=Subschema', rfc2307bis.object_classes.ALL, rfc2307bis.attribute_types.ALL, rfc2307bis.matching_rules.ALL, rfc2307bis.matching_rules.ALL)

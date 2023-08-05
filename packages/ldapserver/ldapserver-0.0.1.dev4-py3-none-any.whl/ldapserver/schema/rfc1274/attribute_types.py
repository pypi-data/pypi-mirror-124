from ..types import AttributeType
from . import syntaxes

audio = AttributeType('0.9.2342.19200300.100.1.55', name='audio', desc='audio (u-law)', syntax=syntaxes.OctetString(25000))
photo = AttributeType('0.9.2342.19200300.100.1.7', name='photo', desc='photo (G3 fax)', syntax=syntaxes.OctetString(25000))

ALL = (
	audio,
	photo,
)

from ..types import ObjectClass, ObjectClassKind
from . import attribute_types

authPasswordObject = ObjectClass('1.3.6.1.4.1.4203.1.4.7', name='authPasswordObject', desc='authentication password mix in class', kind=ObjectClassKind.AUXILIARY,  may=[attribute_types.authPassword])

ALL = (
	authPasswordObject,
)

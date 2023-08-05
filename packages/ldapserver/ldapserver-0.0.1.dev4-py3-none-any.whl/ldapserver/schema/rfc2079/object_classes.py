from ..types import ObjectClass, ObjectClassKind
from ..rfc4512.object_classes import top
from . import attribute_types

labeledURIObject = ObjectClass('1.3.6.1.4.1.250.3.15', name='labeledURIObject', desc='object that contains the URI attribute type', sup=top, kind=ObjectClassKind.AUXILIARY, may=[attribute_types.labeledURI])

ALL = (
	labeledURIObject,
)

""" Contains conversion logic between Mongoengine Fields and Graphene Types """

from singledispatch import singledispatch

from graphene import (
    String, Boolean, Int, Float, List,
    ID, Dynamic, Enum, Field
)

from graphene.types.json import JSONString
from graphene.types.datetime import DateTime

from mongoengine.fields import (
    # Done
    ObjectIdField,
    BooleanField, StringField, IntField, LongField, FloatField, DecimalField,
    URLField, EmailField, 
    DateTimeField, ComplexDateTimeField,
    
    # Todo
    SequenceField, UUIDField,
    EmbeddedDocumentField,
    DynamicField,
    ListField, SortedListField,  DictField, MapField,
    EmbeddedDocumentListField,
    ReferenceField, CachedReferenceField,
    LazyReferenceField,
    GenericEmbeddedDocumentField,  GenericLazyReferenceField, GenericReferenceField,
    BinaryField,
    FileField,
    ImageField,
    GeoPointField, PolygonField, PointField,
    LineStringField,
    MultiPointField, MultiLineStringField, MultiPolygonField,  GeoJsonBaseField
)

from .fields import create_connection_field

from .utils import (
    get_field_description, is_field_required
)

# pylint: disable=W0622

# def convert_sqlalchemy_relationship(relationship, registry):
#     direction = relationship.direction
#     model = relationship.mapper.entity

#     def dynamic_type():
#         _type = registry.get_type_for_model(model)
#         if not _type:
#             return None
#         if direction == interfaces.MANYTOONE or not relationship.uselist:
#             return Field(_type)
#         elif direction in (interfaces.ONETOMANY, interfaces.MANYTOMANY):
#             if _type._meta.connection:
#                 return createConnectionField(_type)
#             return Field(List(_type))

#     return Dynamic(dynamic_type)


def convert_mongoengine_field(field, registry=None):
    """ Shorcut method to :convert_mongoengine_type: """
    return convert_mongoengine_type(field, registry)

def get_data_from_field(field):
    """ Extracts Field data for Graphene type construction """
    return {
        'description': get_field_description(field),
        'required': is_field_required(field)
    }

@singledispatch
def convert_mongoengine_type(field, registry=None):
    """ Generic Mongoengine Field to Graphene Type converter """
    raise Exception(f"Don't know how to convert the Mongoengine field {field} ({type})")


@convert_mongoengine_type.register(ObjectIdField)
def convert_field_to_id(field, registry=None):
    """ Converts Mongoengine fields to Graphene ID type """
    return ID(**get_data_from_field(field))


@convert_mongoengine_type.register(StringField)
@convert_mongoengine_type.register(URLField)
@convert_mongoengine_type.register(EmailField)
def convert_field_to_string(field, registry=None):
    """ Converts Mongoengine fields to Graphene String type """
    return String(**get_data_from_field(field))


@convert_mongoengine_type.register(DateTimeField)
@convert_mongoengine_type.register(ComplexDateTimeField)
def convert_field_to_datetime(field, registry=None):
    """ Converts Mongoengine fields to Graphene DateTime type """
    return DateTime(**get_data_from_field(field))


@convert_mongoengine_type.register(IntField)
@convert_mongoengine_type.register(LongField)
def convert_field_to_int_or_id(field, registry=None):
    """ Converts Mongoengine fields to Graphene Int type """
    return Int(**get_data_from_field(field))


@convert_mongoengine_type.register(BooleanField)
def convert_field_to_boolean(field, registry=None):
    """ Converts Mongoengine fields to Graphene Boolean type """
    return Boolean(**get_data_from_field(field))


@convert_mongoengine_type.register(FloatField)
@convert_mongoengine_type.register(DecimalField)
def convert_field_to_float(field, registry=None):
    """ Converts Mongoengine fields to Graphene Float type """
    return Float(**get_data_from_field(field))


# @convert_mongoengine_type.register(ScalarListType)
# def convert_scalar_list_to_list(type, column, registry=None):
#     return List(String, description=get_column_doc(column))

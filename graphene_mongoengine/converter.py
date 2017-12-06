""" Contains conversion logic between Mongoengine Fields and Graphene Types """

from singledispatch import singledispatch

from graphene import (
    String, Boolean, Int, Float, List,
    ID, Dynamic, Field
)

from graphene.types.json import JSONString
from graphene.types.datetime import DateTime

from mongoengine.fields import (
    ObjectIdField,
    BooleanField, StringField, IntField, LongField, FloatField, DecimalField,
    URLField, EmailField,
    DateTimeField, ComplexDateTimeField,
    SequenceField, UUIDField,
    DynamicField, DictField, MapField,
    GeoPointField, PolygonField, PointField, LineStringField,
    MultiPointField, MultiLineStringField, MultiPolygonField,
    EmbeddedDocumentField,
    ListField, SortedListField,
    EmbeddedDocumentListField,
    ReferenceField, CachedReferenceField, LazyReferenceField,
    GenericEmbeddedDocumentField, GenericLazyReferenceField, GenericReferenceField,
    BinaryField, FileField, ImageField
)

from .fields import create_connection_field

from .utils import (
    get_field_description, field_is_document_list, field_is_required
)

# pylint: disable=W0622


def convert_mongoengine_field(field, registry=None):
    """ Wrapper method for :convert_mongoengine_type: """
    return convert_mongoengine_type(field, registry)


def get_data_from_field(field, **kwargs):
    """ Extracts Field data for Graphene type construction """
    return {
        'description': get_field_description(field, **kwargs),
        'required': field_is_required(field)
    }


@singledispatch
def convert_mongoengine_type(field, registry=None):
    """ Generic Mongoengine Field to Graphene Type converter """
    raise Exception(
        f"Don't know how to convert the Mongoengine field {field} ({type})")


@convert_mongoengine_type.register(ObjectIdField)
def convert_field_to_id(field, registry=None):
    """ Converts Mongoengine fields to Graphene ID type """
    return ID(**get_data_from_field(field))


@convert_mongoengine_type.register(StringField)
@convert_mongoengine_type.register(URLField)
@convert_mongoengine_type.register(EmailField)
@convert_mongoengine_type.register(SequenceField)
@convert_mongoengine_type.register(UUIDField)
def convert_field_to_string(field, registry=None):
    """ Converts Mongoengine fields to Graphene String type """
    return String(**get_data_from_field(field))


@convert_mongoengine_type.register(DateTimeField)
@convert_mongoengine_type.register(ComplexDateTimeField)
def convert_field_to_datetime(field, registry=None):
    """ Converts Mongoengine fields to Graphene DateTime type """
    return DateTime(**get_data_from_field(field))


@convert_mongoengine_type.register(IntField)
def convert_field_to_int_or_id(field, registry=None):
    """ Converts Mongoengine fields to Graphene Int type """
    return Int(**get_data_from_field(field))


@convert_mongoengine_type.register(BooleanField)
def convert_field_to_boolean(field, registry=None):
    """ Converts Mongoengine fields to Graphene Boolean type """
    return Boolean(**get_data_from_field(field))


@convert_mongoengine_type.register(FloatField)
@convert_mongoengine_type.register(DecimalField)
@convert_mongoengine_type.register(LongField)
def convert_field_to_float(field, registry=None):
    """ Converts Mongoengine fields to Graphene Float type """
    return Float(**get_data_from_field(field))


@convert_mongoengine_type.register(DynamicField)
@convert_mongoengine_type.register(DictField)
@convert_mongoengine_type.register(MapField)
@convert_mongoengine_type.register(GeoPointField)
@convert_mongoengine_type.register(PolygonField)
@convert_mongoengine_type.register(PointField)
@convert_mongoengine_type.register(LineStringField)
@convert_mongoengine_type.register(MultiPointField)
@convert_mongoengine_type.register(MultiLineStringField)
@convert_mongoengine_type.register(MultiPolygonField)
def convert_field_to_jsonstring(field, registry=None):
    """ Converts Mongoengine fields to Graphene JSONString type """
    return JSONString(**get_data_from_field(field))


@convert_mongoengine_type.register(GenericEmbeddedDocumentField)
@convert_mongoengine_type.register(GenericLazyReferenceField)
@convert_mongoengine_type.register(GenericReferenceField)
def convert_field_to_jsonstring(field, registry=None):
    """ Converts Mongoengine fields to Graphene JSONString type.
    Generic fields can have any document type, so the best that can be done is
    to convert them to JSONString
    """
    return JSONString(**get_data_from_field(field))


@convert_mongoengine_type.register(ReferenceField)
@convert_mongoengine_type.register(LazyReferenceField)
@convert_mongoengine_type.register(CachedReferenceField)
@convert_mongoengine_type.register(EmbeddedDocumentField)
def convert_field_to_object(field, registry=None):
    """ Converts Mongoengine fields to Graphene Object type """
    field_data = get_data_from_field(field)

    def type_factory():
        """ Lazy type factory """
        doc_type = registry.get_type_for_document(field.document_type)
        if not doc_type:
            return None
        return Field(doc_type, **field_data)

    return Dynamic(type_factory)


@convert_mongoengine_type.register(ListField)
@convert_mongoengine_type.register(SortedListField)
def convert_field_to_list(list_field, registry=None):
    """ Converts Mongoengine fields to Graphene List type """

    if field_is_document_list(list_field):
        return convert_document_list(list_field, registry)
    else:
        if list_field.field is None:
            inner_type = String
        else:
            inner_type = convert_mongoengine_field(list_field.field(), registry).__class__

        return List(inner_type,  **get_data_from_field(list_field))


def convert_document_list(list_field, registry=None):
    """ Converts a MongoEngine List based field wrapping 
    a Document based field to a Graphene List or Connection Field
    """
    document = list_field.field.document_type
    field_data = get_data_from_field(list_field)

    def type_factory():
        """ Lazy type factory """
        doc_type = registry.get_type_for_document(document)
        if not doc_type:
            return None

        if doc_type._meta.connection:
            return create_connection_field(doc_type, **field_data)

        return Field(List(doc_type), **field_data)

    return Dynamic(type_factory)

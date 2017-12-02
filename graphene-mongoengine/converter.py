from singledispatch import singledispatch


from graphene import (
    String, Boolean, Int, Float, List,
    ID, Dynamic, Enum, Field
)

from graphene.types.json import JSONString

from mongoengine.fields import (
    ObjectIdField,
    BooleanField, StringField, IntField, LongField, FloatField, DecimalField,
    URLField, EmailField, SequenceField, UUIDField,
    DateTimeField, ComplexDateTimeField,
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

from .fields import createConnectionField

try:
    from sqlalchemy_utils import (
        ChoiceType, JSONType, ScalarListType, TSVectorType)
except ImportError:
    ChoiceType = JSONType = ScalarListType = TSVectorType = object


def convert_sqlalchemy_relationship(relationship, registry):
    direction = relationship.direction
    model = relationship.mapper.entity

    def dynamic_type():
        _type = registry.get_type_for_model(model)
        if not _type:
            return None
        if direction == interfaces.MANYTOONE or not relationship.uselist:
            return Field(_type)
        elif direction in (interfaces.ONETOMANY, interfaces.MANYTOMANY):
            if _type._meta.connection:
                return createConnectionField(_type)
            return Field(List(_type))

    return Dynamic(dynamic_type)


def convert_sqlalchemy_composite(composite, registry):
    converter = registry.get_converter_for_composite(composite.composite_class)
    if not converter:
        try:
            raise Exception(
                "Don't know how to convert the composite field %s (%s)" %
                (composite, composite.composite_class))
        except AttributeError:
            # handle fields that are not attached to a class yet (don't have a parent)
            raise Exception(
                "Don't know how to convert the composite field %r (%s)" %
                (composite, composite.composite_class))
    return converter(composite, registry)


def _register_composite_class(cls, registry=None):
    if registry is None:
        from .registry import get_global_registry
        registry = get_global_registry()

    def inner(fn):
        registry.register_composite_converter(cls, fn)
    return inner


convert_sqlalchemy_composite.register = _register_composite_class


def convert_mongoengine_field(field, registry=None):
    return convert_mongoengine_type(field.__class__, field, registry)


@singledispatch
def convert_mongoengine_type(type, field, registry=None):
    raise Exception(
        "Don't know how to convert the Mongoengine field %s (%s)" % (field, type))


@convert_mongoengine_type.register(StringField)
@convert_mongoengine_type.register(URLField)
@convert_mongoengine_type.register(EmailField)
def convert_column_to_string(type, column, registry=None):
    return String(description=get_column_doc(column),
                  required=not(is_column_nullable(column)))


@convert_mongoengine_type.register(DateTimeField)
@convert_mongoengine_type.register(ComplexDateTimeField)
def convert_column_to_datetime(type, column, registry=None):
    from graphene.types.datetime import DateTime
    return DateTime(description=get_column_doc(column),
                    required=not(is_column_nullable(column)))


@convert_mongoengine_type.register(types.SmallInteger)
@convert_mongoengine_type.register(types.Integer)
def convert_column_to_int_or_id(type, column, registry=None):
    if column.primary_key:
        return ID(description=get_column_doc(column), required=not (is_column_nullable(column)))
    else:
        return Int(description=get_column_doc(column),
                   required=not (is_column_nullable(column)))


@convert_mongoengine_type.register(types.Boolean)
def convert_column_to_boolean(type, column, registry=None):
    return Boolean(description=get_column_doc(column), required=not(is_column_nullable(column)))


@convert_mongoengine_type.register(types.Float)
@convert_mongoengine_type.register(types.Numeric)
@convert_mongoengine_type.register(types.BigInteger)
def convert_column_to_float(type, column, registry=None):
    return Float(description=get_column_doc(column), required=not(is_column_nullable(column)))


@convert_mongoengine_type.register(ChoiceType)
def convert_column_to_enum(type, column, registry=None):
    name = '{}_{}'.format(column.table.name, column.name).upper()
    return Enum(name, type.choices, description=get_column_doc(column))


@convert_mongoengine_type.register(ScalarListType)
def convert_scalar_list_to_list(type, column, registry=None):
    return List(String, description=get_column_doc(column))


@convert_mongoengine_type.register(postgresql.ARRAY)
def convert_postgres_array_to_list(_type, column, registry=None):
    graphene_type = convert_mongoengine_type(column.type.item_type, column)
    inner_type = type(graphene_type)
    return List(inner_type, description=get_column_doc(column), required=not(is_column_nullable(column)))


@convert_mongoengine_type.register(postgresql.HSTORE)
@convert_mongoengine_type.register(postgresql.JSON)
@convert_mongoengine_type.register(postgresql.JSONB)
def convert_json_to_string(type, column, registry=None):
    return JSONString(description=get_column_doc(column), required=not(is_column_nullable(column)))


@convert_mongoengine_type.register(JSONType)
def convert_json_type_to_string(type, column, registry=None):
    return JSONString(description=get_column_doc(column), required=not(is_column_nullable(column)))

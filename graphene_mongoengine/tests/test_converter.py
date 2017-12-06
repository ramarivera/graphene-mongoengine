from py.test import raises

from graphene import (
    String, Int, Boolean, Float, ID,
    List, Dynamic
)
from graphene.relay import Node
from graphene.types.datetime import DateTime
from graphene.types.json import JSONString

import mongoengine.fields as fields

from ..converter import convert_mongoengine_field
from ..fields import MongoEngineConnectionField
from ..registry import Registry
from ..types import MongoEngineObjectType
from .models import PeriodicTask

DESCRIPTION_TEXT = 'Custom Help Text'

def assert_field_conversion(mongoengine_field, graphene_field, **kwargs):
    field = mongoengine_field(description=DESCRIPTION_TEXT, **kwargs)
    graphene_type = convert_mongoengine_field(field)
    assert isinstance(graphene_type, graphene_field)
    field = graphene_type.Field()
    assert field.description == DESCRIPTION_TEXT
    return field
 
def assert_list_field_conversion(list_type, mongoengine_field, graphene_field, **kwargs):
    field = list_type(field=mongoengine_field, description=DESCRIPTION_TEXT, **kwargs)
    graphene_type = convert_mongoengine_field(field)
    assert isinstance(graphene_type, graphene_field)
    field = graphene_type.Field()
    assert field.description == DESCRIPTION_TEXT
    return field


def test_should_none_raise_exception():
    with raises(Exception) as excinfo:
        convert_mongoengine_field(None)
    assert "Don't know how to convert the Mongoengine field" in str(excinfo.value)


def test_should_not_mongoengine_field_raise_exception():
    with raises(Exception) as excinfo:
        convert_mongoengine_field(str)
    assert "Don't know how to convert the Mongoengine field" in str(excinfo.value)
    assert str(str) in str(excinfo.value)



def test_should_objectid_convert_id():
    assert_field_conversion(fields.ObjectIdField, ID)


def test_should_string_convert_string():
    assert_field_conversion(fields.StringField, String)


def test_should_url_convert_string():
    assert_field_conversion(fields.URLField, String)


def test_should_email_convert_string():
    assert_field_conversion(fields.EmailField, String)


def test_should_uuid_convert_string():
    assert_field_conversion(fields.UUIDField, String)


def test_should_sequence_convert_string():
    assert_field_conversion(fields.SequenceField, String)


def test_should_datetime_convert_datetime():
    assert_field_conversion(fields.DateTimeField, DateTime)


def test_should_complexdatetime_convert_datetime():
    assert_field_conversion(fields.ComplexDateTimeField, DateTime)


def test_should_int_convert_int():
    assert_field_conversion(fields.IntField, Int)


def test_should_long_convert_float():
    assert_field_conversion(fields.LongField, Float)


def test_should_boolean_convert_boolean():
    assert_field_conversion(fields.BooleanField, Boolean)


def test_should_float_convert_float():
    assert_field_conversion(fields.FloatField, Float)


def test_should_decimal_convert_float():
    assert_field_conversion(fields.DecimalField, Float)


def test_should_dynamic_convert_jsonstring():
    assert_field_conversion(fields.DynamicField, JSONString)


def test_should_dict_convert_jsonstring():
    assert_field_conversion(fields.DictField, JSONString)


# def test_should_map_convert_jsonstring():
#     assert_field_conversion(fields.MapField, JSONString)


def test_should_geopoint_convert_jsonstring():
    assert_field_conversion(fields.GeoPointField, JSONString)


def test_should_polygon_convert_jsonstring():
    assert_field_conversion(fields.PolygonField, JSONString)


def test_should_point_convert_jsonstring():
    assert_field_conversion(fields.PointField, JSONString)


def test_should_linestring_convert_jsonstring():
    assert_field_conversion(fields.LineStringField, JSONString)


def test_should_multipoint_convert_jsonstring():
    assert_field_conversion(fields.MultiPointField, JSONString)


def test_should_multilinestring_convert_jsonstring():
    assert_field_conversion(fields.MultiLineStringField, JSONString)


def test_should_multipolygon_convert_jsonstring():
    assert_field_conversion(fields.MultiPolygonField, JSONString)


def test_should_list_int_convert_list_int():
    assert_list_field_conversion(fields.ListField, fields.IntField, List)


def test_should_list_string_convert_list_string():
    assert_list_field_conversion(fields.ListField, fields.StringField, List)


def test_should_list_none_convert_list_string():
    assert_list_field_conversion(fields.ListField, None, List)


def test_should_sortedlist_int_convert_list_int():
    assert_list_field_conversion(fields.SortedListField, fields.IntField, List)


def test_should_sortedlist_string_convert_list_string():
    assert_list_field_conversion(fields.SortedListField, fields.StringField, List)


def test_should_sortedlist_none_convert_list_string():
    assert_list_field_conversion(fields.SortedListField, None, List)


"""@convert_mongoengine_type.register(ReferenceField)
@convert_mongoengine_type.register(LazyReferenceField)
@convert_mongoengine_type.register(CachedReferenceField)
@convert_mongoengine_type.register(EmbeddedDocumentField)
"""

def assert_reference_field_conversion(reference_type, document_type, graphene_field, registry=None, **kwargs):
    registry = registry or Registry()
    field = reference_type(document_type, description=DESCRIPTION_TEXT, **kwargs)
    graphene_type = convert_mongoengine_field(field, registry)
    assert isinstance(graphene_type, graphene_field)
    return graphene_type

def test_should_unregistered_reference_field_convert_dynamic():
    dynamic_field = assert_reference_field_conversion(fields.ReferenceField, PeriodicTask, Dynamic)
    # assert field.description == DESCRIPTION_TEXT
    assert not dynamic_field.get_type()

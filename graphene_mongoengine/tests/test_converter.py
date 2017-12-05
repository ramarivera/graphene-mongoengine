from py.test import raises

from graphene import (
    String, Int, Boolean, Float, ID
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


def assert_field_conversion(mongoengine_field, graphene_field, **kwargs):
    description_text = 'Custom Help Text'
    field = mongoengine_field(description=description_text, **kwargs)
    graphene_type = convert_mongoengine_field(field)
    assert isinstance(graphene_type, graphene_field)
    field = graphene_type.Field()
    assert field.description == description_text
    return field


def test_should_objectid_convert_id():
    assert_field_conversion(fields.ObjectIdField, ID)


def test_should_string_convert_string():
    assert_field_conversion(fields.StringField, String)


def test_should_url_convert_string():
    assert_field_conversion(fields.URLField, String)


def test_should_email_convert_string():
    assert_field_conversion(fields.EmailField, String)


def test_should_datetime_convert_datetime():
    assert_field_conversion(fields.DateTimeField, DateTime)


def test_should_complexdatetime_convert_datetime():
    assert_field_conversion(fields.ComplexDateTimeField, DateTime)


def test_should_int_convert_int():
    assert_field_conversion(fields.IntField, Int)


def test_should_long_convert_int():
    assert_field_conversion(fields.LongField, Int)


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



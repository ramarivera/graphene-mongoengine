from functools import partial

from mongoengine import QuerySet

from graphene.relay import ConnectionField
from graphene.relay.connection import PageInfo
from graphql_relay.connection.arrayconnection import connection_from_list_slice

from .utils import get_query

# pylint: disable=C0103, W0603, W0622, W0212

class MongoEngineConnectionField(ConnectionField):

    @property
    def document(self):
        """ Returns MongoEngine document for this Connection Field """
        return self.type._meta.node._meta.document

    @classmethod
    def get_query(cls, document, info, **args):
        """ Returns a document queryset specified by the queryset_attr keyword argument"""
        if 'queryset_attr' in args:
            return get_query(document, info.context, queryset_attr=args.get('queryset_attr'))
        else:
            return get_query(document, info.context)
            
    @property
    def type(self):
        """ Returns Connection Type for this field"""

        from .types import MongoEngineObjectType
        connection_type = super(ConnectionField, self).type

        assert issubclass(connection_type, MongoEngineObjectType), (
            "MongoEngineConnectionField only accepts MongoEngineObjectType types"
        )

        assert connection_type._meta.connection, f"The type {connection_type.__name__} doesn't have a connection"

        return connection_type._meta.connection

    @classmethod
    def connection_resolver(cls, resolver, connection, document, root, info, **args):
        """ Returns a Graphql Connection object """

        iterable = resolver(root, info, **args)

        if iterable is None:
            iterable = cls.get_query(document, info, **args)

        if isinstance(iterable, QuerySet):
            length = iterable.count()
        else:
            length = len(iterable)

        connection = connection_from_list_slice(
            iterable,
            args,
            slice_start=0,
            list_length=length,
            list_slice_length=length,
            connection_type=connection,
            pageinfo_type=PageInfo,
            edge_type=connection.Edge,
        )
        connection.iterable = iterable
        connection.length = length

        return connection

    def get_resolver(self, parent_resolver):
        return partial(self.connection_resolver, parent_resolver, self.type, self.document)


__connection_factory = MongoEngineConnectionField


def create_connection_field(type, **kwargs):
    """ Creates a :MongoEngineConnectionField: for a given type"""
    return __connection_factory(type, **kwargs)


def register_connection_field_factory(factory_method):
    """ Registers a new factory method for connection fields """
    global __connection_factory
    __connection_factory = factory_method


def unregister_connection_field_factory():
    """ Resets default connection field factory """
    global __connection_factory
    __connection_factory = MongoEngineConnectionField

from collections import OrderedDict

from graphene import Field  # , annotate, ResolveInfo
from graphene.relay import Connection, Node
from graphene.types.objecttype import ObjectType, ObjectTypeOptions
from graphene.types.utils import yank_fields_from_attrs

from mongoengine import DoesNotExist

from .converter import convert_mongoengine_field

from .registry import Registry, get_global_registry

from .utils import get_document_fields, is_mongoengine_document, get_query

# pylint: disable=W0622,C0103

def construct_fields(document, registry, only_fields, exclude_fields):
    
    fields = OrderedDict()
    document_fields = get_document_fields(document)

    for name, field in document_fields.items():
        
        is_not_in_only = only_fields and name not in only_fields
        is_excluded = name in exclude_fields
        if is_not_in_only or is_excluded:
            continue

        converted_field = convert_mongoengine_field(field, registry)

        print(name)
        fields[name] = converted_field

    # # Get all the columns for the relationships on the model
    # for relationship in inspected_model.relationships:
    #     is_not_in_only = only_fields and relationship.key not in only_fields
    #     # is_already_created = relationship.key in options.fields
    #     is_excluded = relationship.key in exclude_fields  # or is_already_created
    #     if is_not_in_only or is_excluded:
    #         # We skip this field if we specify only_fields and is not
    #         # in there. Or when we exclude this field in exclude_fields
    #         continue
    #     converted_relationship = convert_sqlalchemy_relationship(relationship, registry)
    #     name = relationship.key
    #     fields[name] = converted_relationship

    return fields


class MongoEngineObjectTypeOptions(ObjectTypeOptions):
    document = None  # type: Document
    registry = None  # type: Registry
    connection = None  # type: Type[Connection]
    id = None  # type: str


class MongoEngineObjectType(ObjectType):
    
    @classmethod
    def __init_subclass_with_meta__(cls, document=None, registry=None, skip_registry=False,
                                    only_fields=(), exclude_fields=(), connection=None,
                                    use_connection=None, interfaces=(), id=None, **options):

        assert is_mongoengine_document(document), (
            f"You need to pass a valid MongoEngine Document in {cls.__name__}.Meta, "
            f"received '{document}'."
        )

        if not registry:
            registry = get_global_registry()

        assert isinstance(registry, Registry), (
            f'The attribute registry in {cls.__name__} needs to be an instance of '
            f'Registry, received "{registry}".'
        )

        mongoengine_fields = yank_fields_from_attrs(
            construct_fields(document, registry, only_fields, exclude_fields),
            _as=Field,
        )

        if use_connection is None and interfaces:
            use_connection = any((issubclass(interface, Node) for interface in interfaces))

        if use_connection and not connection:
            # We create the connection automatically
            connection = Connection.create_type(f'{cls.__name__}Connection', node=cls)

        if connection is not None:
            assert issubclass(connection, Connection), (
                f'The connection must be a Connection. Received {connection.__name__}'
            )

        _meta = MongoEngineObjectTypeOptions(cls)
        _meta.document = document
        _meta.registry = registry
        _meta.fields = mongoengine_fields
        _meta.connection = connection
        _meta.id = id or 'id'

        super(MongoEngineObjectType, cls).__init_subclass_with_meta__(
            _meta=_meta,
            interfaces=interfaces,
            **options
        )

        if not skip_registry:
            registry.register(cls)

    @classmethod
    def is_type_of(cls, root, info):
        if isinstance(root, cls):
            return True
        if not is_mongoengine_document(root):
            raise Exception(f'Received incompatible instance "{root}".')

        return isinstance(root, cls._meta.document)

    @classmethod
    def get_query(cls, info):
        """ Gets QuerySet for this type's document """
        document = cls._meta.document
        return get_query(document, info.context)

    @classmethod
    def get_node(cls, info, id):
        """ Returns document to wrap in Node """
        try:
            return cls.get_query(info).get(id)
        except DoesNotExist:
            return None
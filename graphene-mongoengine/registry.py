""" Contains :Registry: class and related utilities """

# pylint: disable=W0212,W0603,C0103

class Registry(object):
    """ Holds mappings between MongoEngine Document types
        and Graphene MongoEngineObjectType classes
    """

    def __init__(self):
        self._registry = {}
        self._registry_documents = {}

    def register(self, cls):
        """ Register a class for a given Document """

        from .types import MongoEngineObjectType

        assert issubclass(cls, MongoEngineObjectType), (
            'Only classes of type MongoEngineObjectType can be registered, '
            'received "{cls.__name__}"'
        )

        assert cls._meta.registry == self, 'Registry for a Document have to match.'

        self._registry[cls._meta.document] = cls

    def get_type_for_document(self, document):
        """ Returns registered class for a given Document """
        return self._registry.get(document)


registry = None


def get_global_registry():
    """ Returns a globally shared :Registry: object """
    global registry
    if not registry:
        registry = Registry()
    return registry


def reset_global_registry():
    """ Resets globally shared :Registry: """
    global registry
    registry = None

""" Utils for MongoEngine integration with Graphene """

import inspect

from mongoengine.document import (
    Document, DynamicDocument,
    EmbeddedDocument, DynamicEmbeddedDocument
)

from mongoengine.fields import (
    EmbeddedDocumentField,
    ListField, SortedListField,
    EmbeddedDocumentListField,
    ReferenceField, CachedReferenceField, LazyReferenceField,
    GenericEmbeddedDocumentField, GenericLazyReferenceField, GenericReferenceField,
)


def get_query(document, context, queryset_attr='objects'):
    query = getattr(document, queryset_attr, None)
    if query is None:
        # session = get_session(context)
        # if not session:
        raise Exception('A queryset in the document is required for querying.')
    return query


def get_document_fields(document):
    """ Returns a dict with a :Document: fields,
    which keys are the Fields name as defined in the Document """
    return getattr(document, '_fields', {})


def is_mongoengine_document(document):
    """ Checks whether document is a MongoEngine document """
    document_classes = (
        Document, EmbeddedDocument,
        DynamicDocument, DynamicEmbeddedDocument
    )
    if not inspect.isclass(document):
        document_class = document.__class__
    else:
        document_class = document
    return issubclass(document_class, document_classes)


def field_is_required(field):
    """ Returns true if the field is required (e.g. not nullable) """
    return getattr(field, 'required', False)


def field_is_nullable(field):
    """ Returns true if the field is nullable"""
    return not field_is_required(field)


def get_field_type(field):
    """ Gets field type """
    return field.__class__


def get_field_description(field, description_keyword='description'):
    """ Gets field description if available, using the description_keyword"""
    return getattr(field, description_keyword, '')


def field_is_document_list(field):
    """ Returns True if the field is a :ListField: subclass
    whose inner field is a Document field
    """

    document_fields = (
        EmbeddedDocumentField, ReferenceField,
        CachedReferenceField, LazyReferenceField
    )

    if issubclass(field.__class__, (ListField)):
        if field.field is not None:
            return isinstance(field.field, document_fields)

    return False




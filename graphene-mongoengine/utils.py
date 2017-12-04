""" Utils for MongoEngine integration with Graphene """

from mongoengine.document import (
    Document, DynamicDocument,
    EmbeddedDocument, DynamicEmbeddedDocument
)

def get_query(document, context, queryset_attr='objects'):
    query = getattr(document, queryset_attr, None)
    if not query:
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
    return isinstance(document, document_classes)

def is_field_required(field):
    """ Returns true if the field is required (e.g. not nullable) """
    return field.required

def is_field_nullable(field):
    """ Returns true if the field is nullable"""
    return not is_field_required(field)

def get_field_type(field):
    """ Gets field type """
    return field.__class__

def get_field_description(field, description_keyword='description'):
    """ Gets field description if available, using the description_keyword"""
    return getattr(field, description_keyword, '')




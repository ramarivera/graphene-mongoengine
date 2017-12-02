from sqlalchemy.exc import ArgumentError
from sqlalchemy.orm import class_mapper, object_mapper
from sqlalchemy.orm.exc import UnmappedClassError, UnmappedInstanceError


def get_session(context):
    return context.get('session')


def get_query(model, context):
    query = getattr(model, 'query', None)
    if not query:
        session = get_session(context)
        if not session:
            raise Exception('A query in the model Base or a session in the schema is required for querying.\n'
                            'Read more http://graphene-python.org/docs/sqlalchemy/tips/#querying')
        query = session.query(model)
    return query


def is_mapped_class(cls):
    try:
        class_mapper(cls)
    except (ArgumentError, UnmappedClassError):
        return False
    else:
        return True


def is_mapped_instance(cls):
    try:
        object_mapper(cls)
    except (ArgumentError, UnmappedInstanceError):
        return False
    else:
        return True

class DocumentInspectionData:
    
    def __init__(self, document):
        self.collection = ''
        self.document_type = document.__class__

        self._process_fields(get_document_fields(document))

    def _process_fields(self, document_fields):
        pass
        

def get_document_fields(document):
    return getattr(document, '_fields', {})


def inspect_mongoengine_document(document):
    return DocumentInspectionData(document)

def is_field_required(field):
    pass

def is_field_nullable(field):
    pass

def get_field_type(field):
    pass


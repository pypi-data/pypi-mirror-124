from dataclasses import dataclass
from roughrider.predicate.errors import ConstraintError
from roughrider.predicate.validators import Validator, Or


@dataclass
class Document:
    id: str
    body: str = ''
    content_type: str = 'text/plain'


def non_empty_document(item):
    """Implementation of a validator/predicate
    """
    if not item.body:
        raise ConstraintError('Body is empty.')


class ContentType(Validator):

    def __init__(self, content_type):
        self.ct = content_type

    def __call__(self, item):
        if item.content_type != self.ct:
            raise ConstraintError(
                f'Expected {self.ct}, got {item.content_type}.')


validator = Or((
    ContentType('text/plain'),
    Or((ContentType('text/html'), non_empty_document))
))
document = Document(id='test', content_type='application/json')
validator(document)  # raises ConstraintsErrors

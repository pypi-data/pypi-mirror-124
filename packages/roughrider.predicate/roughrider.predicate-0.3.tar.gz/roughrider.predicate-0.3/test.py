import timeit
from dataclasses import dataclass
from roughrider.predicate.errors import ConstraintError
from roughrider.predicate.validators import Or
from roughrider.predicate.types import Predicate
from roughrider.predicate.utils import resolve_constraints


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


def non_test_document(item):
    """Implementation of a validator/predicate
    """
    if item.id.startswith('test'):
        raise ConstraintError("The document shouldn't be a test.")


class ContentType(Predicate):

    def __init__(self, content_type):
        self.ct = content_type

    def __call__(self, item):
        if item.content_type != self.ct:
            raise ConstraintError(
                f'Expected {self.ct}, got {item.content_type}.')


validators = (
    non_test_document,
    non_empty_document,
    Or((ContentType('text/html'), ContentType('text/plain')))
)


def resolve():
    resolve_constraints(validators, Document(
        id='test', content_type='application/json'
    ))

    resolve_constraints(validators, Document(
        id='test', content_type='text/html'
    ))

    resolve_constraints(validators, Document(
        id='somedoc', content_type='text/plain'
    ))



duration = timeit.Timer(resolve).timeit(number=100000)
print(duration)

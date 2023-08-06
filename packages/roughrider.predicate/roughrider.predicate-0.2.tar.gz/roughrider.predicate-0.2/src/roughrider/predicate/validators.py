from abc import ABC, abstractmethod
from typing import Iterable, Tuple, Optional, Callable, Union
from roughrider.predicate.errors import ConstraintError, ConstraintsErrors


class Validator(ABC):
    """A validator.
    """
    description: Optional[str]

    @abstractmethod
    def __call__(self, *args, **namespace) -> None:
        """Raises a roughrider.predicate.ConstraintError if the validation failed.
        """


Constraint = Union[Validator, Callable[..., None]]


class Or(Tuple[Constraint], Validator):

    def __call__(self, *args, **namespace):
        errors = []
        for validator in self:
            try:
                validator(*args, **namespace)
                return
            except ConstraintError as exc:
                errors.append(exc)
            except ConstraintsErrors as exc:
                errors.extend(exc.errors)

        raise ConstraintsErrors(*errors)


def resolve_validators(
        validators: Iterable[Constraint], *args, **namespace
) -> Optional[ConstraintsErrors]:
    errors = []
    for validator in validators:
        try:
            validator(*args, **namespace)
        except ConstraintError as exc:
            errors.append(exc)
        except ConstraintsErrors as exc:
            errors.extend(exc.errors)
    if errors:
        return ConstraintsErrors(*errors)

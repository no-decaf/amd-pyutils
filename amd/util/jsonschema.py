"""A JSON Schema validator that uses Draft 7 and handles defaults and date types.

Timezones are required for all datetimes. Validation will fail without a timezone.
"""

from copy import deepcopy
from datetime import date, datetime
from functools import partial
from typing import Any, Callable, Dict, Iterable, List, Optional, Tuple, Type

from jsonschema import Draft7Validator, FormatChecker
from jsonschema._types import TypeChecker
from jsonschema.exceptions import ValidationError
from jsonschema.validators import extend

from amd.util.datetime import is_aware, utcnow
from amd.util.dict import find


def make_strict(schema: Dict[str, Any]) -> Dict[str, Any]:
    """Make a strict JSON Schema with custom types converted to string types.

    Converts custom date and datetime types to formatted string types.

    :param schema: A JSON Schema that may contain custom types.

    :return: A strict JSON Schema with no custom types.
    """
    # Do not mutate the input schema.
    schema = deepcopy(schema)

    subschemas = []
    for type_ in ("date", "datetime"):
        subschemas.extend(find(schema, {"type": type_}))

    for subschema in subschemas:
        if subschema["type"] == "date":
            subschema["format"] = "date"
        else:
            subschema["format"] = "date-time"
        subschema["type"] = "string"

        # Remove the utcnow default value, since it's a function placeholder that
        # doesn't apply to a formatted string type.
        if subschema.get("default") == "utcnow":
            del subschema["default"]

    return schema


def validate(
    instance: Any, schema: Dict[str, Any]
) -> Tuple[Dict[str, Any], List[Dict[str, Any]]]:
    """Validate JSON Schema Draft 7, set defaults, and return errors.

    :param instance: The instance to validate.
    :param schema: The schema to use for validation.

    :return: A tuple with a copy of the instance with its default values set, and a list
             of errors.
    """
    # The validator sets defaults on the instance. Do not mutate the input instance.
    instance_copy = deepcopy(instance)
    validator = _Validator(schema, format_checker=FormatChecker())
    errors = list(validator.iter_errors(instance_copy))

    return (
        instance_copy,
        [
            {
                "instance": i.instance,
                "message": i.message,
                "path": list(i.absolute_path),
                "schema": i.schema,
            }
            for i in errors
        ],
    )


def _extend_validator() -> Type[Draft7Validator]:
    """Extend the Draft 7 validator with custom type checkers and custom validation.

    :return: A class definition for a custom Draft 7 JSON Schema validator.
    """
    custom_type_checks = {"date": _is_date, "datetime": _is_datetime}
    extended_type_checker = Draft7Validator.TYPE_CHECKER.redefine_many(
        custom_type_checks
    )
    extended_validator = extend(Draft7Validator, type_checker=extended_type_checker)

    # Ensure the original validate function is passed to validate with defaults.
    validate_properties = extended_validator.VALIDATORS["properties"]
    custom_validate_properties = partial(
        _validate_properties_with_defaults, validate_properties
    )

    return extend(extended_validator, {"properties": custom_validate_properties})


def _is_date(_: Optional[TypeChecker], instance: Any) -> bool:
    """Check whether an instance is a date.

    :param _: The unused type checker.
    :param instance: The instance to check the type of.

    :return: True if the instance is a date, otherwise False.
    """
    return isinstance(instance, date)


def _is_datetime(_: Optional[TypeChecker], instance: Any) -> bool:
    """Check whether an instance is a datetime. Does not accept naive datetimes.

    :param _: The unused type checker.
    :param instance: The instance to check the type of.

    :return: True if the instance is a timezone-aware datetime, otherwise False.
    """
    return isinstance(instance, datetime) and is_aware(instance)


def _validate_properties_with_defaults(
    validate_properties: Callable[
        [Draft7Validator, Dict[str, Any], Dict[str, Any], Dict[str, Any]],
        Iterable[ValidationError],
    ],
    validator: Draft7Validator,
    properties: Dict[str, Any],
    instance: Dict[str, Any],
    schema: Dict[str, Any],
) -> None:
    """Set default values and validate the properties of an instance.

    Called automatically during validation.

    :param validate_properties: The property validation function to use.
    :param validator: The validator to use.
    :param properties: The properties to validate.
    :param instance: The instance to validate.
    :param schema: The schema to use for validation.
    """
    for prop, subschema in properties.items():
        if prop in instance and instance[prop] is None and "default" in subschema:
            if subschema["type"] == "datetime" and subschema["default"] == "utcnow":
                instance[prop] = utcnow()
            else:
                instance[prop] = subschema["default"]

    for error in validate_properties(validator, properties, instance, schema):
        yield error


_Validator: Draft7Validator = _extend_validator()
"""The custom validator to use with the validate method."""

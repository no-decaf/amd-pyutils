"""Functions for working with Flask applications for JSON-only APIs."""

import json as stdlib_json
from collections.abc import Iterable
from copy import deepcopy
from functools import wraps
from typing import Any, Callable, Dict, List, Optional, Union

from flask import Blueprint, Flask, Response, abort, make_response, request
from prometheus_flask_exporter import PrometheusMetrics
from prometheus_flask_exporter.multiprocess import GunicornPrometheusMetrics
from werkzeug.exceptions import HTTPException

from amd.util import doc, json
from amd.util.jsonschema import make_strict
from amd.util.jsonschema import validate as _validate

try:
    import importlib.resources as import_resources
except ImportError:
    # Try importlib_resources which is backported to Python < 3.7.
    import importlib_resources as import_resources

OPEN_API: Dict[str, Optional[Union[bytes, str]]] = {
    "redoc_html": None,
    "spec_json": None,
    "swagger_html": None,
}
"""Contains OpenAPI HTML and JSON data."""


def load_body() -> Union[Dict[str, Any], List[Any]]:
    """Parse the request body with a JSON loader.

    Handles date types and unicode.

    :return: A dictionary or list with the request body.
    """
    return json.loads(request.get_data())


def load_querystring() -> Dict[str, Any]:
    """Parse the querystring and handle dates, query params, and unicode.

    :return: A dictionary with querystring parameters.
    """
    args = request.args.to_dict()

    # Handle special parameters for querying.
    if "filter" in args:
        # Filter is given an underscore because it is often passed as a keyword
        # argument and "filter" masks Python's built-in function.
        args["filter_"] = json.loads(args["filter"])
        del args["filter"]
    if "limit" in args:
        args["limit"] = int(args["limit"])
    if "sort" in args:
        args["sort"] = args["sort"].split(",")

    # Serialize to JSON and back again to parse date strings into Python
    # objects.
    return json.loads(json.dumps(args))


def make_json_response(obj: Any) -> Response:
    """Make a readable JSON response that is compliant with the JSON:API spec.

    Handles date types and unicode.
    This should be the only function used to return JSON from a Flask route.

    JSON:API Specification: https://jsonapi.org/

    The Flask convention is to use:
        from flask import jsonify
        return jsonify({"key": val})

    This approach is used instead of the Flask convention to avoid the extra
    work of implementing a custom JSON Encoder and Decoder for Flask. The
    amd.util.json module implements "dumps" and "loads" but no other json
    functions. Overriding flask.json.JSONDecoder would require implementing
    numerous other functions to ensure every use case is handled. Since the
    primary use case for microservice APIs just involves handling JSON data that
    is RFC 8259 compliant, this is a simple way of supporting JSON APIs. We can
    always build a more thorough implementation in the future if we choose.

    Reference:
        https://github.com/pallets/flask/blob/master/flask/json/__init__.py
        https://pythonhosted.org/itsdangerous/
        https://github.com/pallets/itsdangerous/blob/master/src/itsdangerous/_json.py
        https://tools.ietf.org/html/rfc8259

    :param obj: The object to convert to the body of the JSON response.

    :return: A Flask response.
    """
    # Ensure the data key is present if none of the top-level keys are present.
    if not isinstance(obj, dict) or all(
        i not in obj for i in ("data", "errors", "meta")
    ):
        obj = {"data": obj}

    json_data = json.readable(obj)
    response = make_response(json_data)
    response.mimetype = "application/vnd.api+json"

    return response


def make_schema_response(schema: Any) -> Response:
    """Make a response with strict JSON Schema that complies with JSON:API.

    :param schema: The JSON Schema object to convert to the body of the JSON
                   response.

    :return: A Flask response.
    """
    strict_schema = make_strict(schema)

    return make_json_response(strict_schema)


def register_error_handlers(app: Union[Blueprint, Flask]) -> None:
    """Register custom error handlers which return JSON responses.

    :param app: The Flask application or blueprint to modify.
    """
    app.register_error_handler(400, _custom400)
    app.register_error_handler(404, _custom404)
    app.register_error_handler(500, _custom500)


def register_openapi(
    app: Union[Blueprint, Flask], specfile: str = "spec.json"
) -> None:
    """Register OpenAPI endpoints. Assigns the root URL.

    :param app: The Flask application or blueprint to modify.
    :param specfile: The path to the spec file containing OpenAPI JSON. This
                     defaults to spec.json in the folder where Flask is running.
    """
    url_prefix = app.url_prefix if hasattr(app, "url_prefix") else ""

    OPEN_API["redoc_html"] = import_resources.read_text(
        doc, "redoc.html"
    ).replace("{URL_PREFIX}", url_prefix)
    OPEN_API["swagger_html"] = import_resources.read_text(
        doc, "swagger.html"
    ).replace("{URL_PREFIX}", url_prefix)

    with open(specfile, "rb") as inf:
        OPEN_API["spec_json"] = inf.read()

    app.add_url_rule(
        "/", endpoint="index", methods=["GET"], view_func=_get_index
    )
    app.add_url_rule(
        "/spec", endpoint="spec", methods=["GET"], view_func=_get_spec_index
    )
    app.add_url_rule(
        "/swagger",
        endpoint="swagger",
        methods=["GET"],
        view_func=_get_swagger_index,
    )


def register_prometheus(app: Union[Blueprint, Flask], debug: bool) -> None:
    """Register Prometheus endpoints. Assumes Gunicorn is used for production.

    :param app: The Flask application or blueprint to modify.
    :param debug: Whether the Flask application is running in debug mode.
    """
    if debug:
        # Running in debug mode.
        PrometheusMetrics(app)
    else:
        # Running with Gunicorn.
        GunicornPrometheusMetrics(app)


def validate(schema: Dict[str, Any]) -> Callable[[Any], Any]:
    """Wrap a Flask endpoint and validate the body, path, and querystring.

    Converts custom JSON Schema to a strict schema before validating.

    The schema must describe request data with this structure.
        {
            "request_body": request_body_schema,
            "request_path": request_path_schema,
            "request_query": request_query_schema,
        }

    :param schema: The schema to use for validation.

    :return: A function wrapper.
    """

    # noqa: D202
    def inner_wrapper(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            body = request.get_data()
            path = request.view_args
            query = request.args.to_dict()

            request_data = {}
            if body:
                # Strict JSON schema validates date and datetime values as
                # string types with a format. Use the json module from the
                # standard library to load JSON without parsing dates.
                request_data["request_body"] = stdlib_json.loads(body)
            if path:
                request_data["request_path"] = deepcopy(path)
            if query:
                request_data["request_query"] = deepcopy(query)

            strict_schema = make_strict(schema)
            _, err = _validate(request_data, strict_schema)

            if err:
                abort(400, err)

            return func(*args, **kwargs)

        return wrapper

    return inner_wrapper


def _custom400(error: HTTPException) -> Response:
    """Send a JSON response with error data that is JSON:API compliant.

    :param error: The Flask HTTP exception.

    :return: A Flask response.
    """
    errors = (
        error.description
        if isinstance(error.description, Iterable)
        else [error.description]
    )
    response = make_json_response({"errors": errors})
    response.status_code = 400

    return response


def _custom404(_: HTTPException) -> Response:
    """Send an empty JSON response to the client.

    :param _: The unused Flask HTTP exception.

    :return: A Flask response.
    """
    response = make_response("")
    response.mimetype = "application/json"
    response.status_code = 404

    return response


def _custom500(_: HTTPException) -> Response:
    """Send a JSON response with an error message that is JSON:API compliant.

    :param _: The unused Flask HTTP exception.

    :return: A Flask response.
    """
    response = make_json_response(
        {"errors": ["An unexpected error has occurred."]}
    )
    response.status_code = 500

    return response


def _get_index() -> Response:
    """Send a ReDoc HTML response to the client.

    :return: A Flask response.
    """
    return make_response(OPEN_API["redoc_html"])


def _get_spec_index() -> Response:
    """Send an OpenAPI specification to the client as JSON.

    :return: A Flask response.
    """
    response = make_response(OPEN_API["spec_json"])
    response.mimetype = "application/json"

    return response


def _get_swagger_index() -> Response:
    """Send a Swagger UI HTML response to the client.

    :return: A Flask response.
    """
    return make_response(OPEN_API["swagger_html"])

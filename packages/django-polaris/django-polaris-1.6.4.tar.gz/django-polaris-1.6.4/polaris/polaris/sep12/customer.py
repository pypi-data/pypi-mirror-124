from typing import Dict, Optional

from django.utils.translation import gettext as _
from django.core.validators import URLValidator
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.decorators import api_view, renderer_classes, parser_classes
from rest_framework.renderers import JSONRenderer, BrowsableAPIRenderer
from rest_framework.parsers import JSONParser, MultiPartParser, FormParser

from polaris import settings
from polaris.utils import (
    extract_sep9_fields,
    render_error_response,
    make_memo,
    getLogger,
    SEP_9_FIELDS,
)
from polaris.sep10.utils import validate_sep10_token
from polaris.integrations import registered_customer_integration as rci


logger = getLogger(__name__)


class CustomerAPIView(APIView):
    renderer_classes = [JSONRenderer, BrowsableAPIRenderer]
    parser_classes = [MultiPartParser, FormParser, JSONParser]

    @staticmethod
    @validate_sep10_token()
    def get(account: str, _client_domain: Optional[str], request: Request) -> Response:
        if request.GET.get("account") and account != request.GET.get("account"):
            return render_error_response(
                _("The account specified does not match authorization token"),
                status_code=403,
            )
        elif request.GET.get("id") and (
            request.GET.get("account")
            or request.GET.get("memo")
            or request.GET.get("memo_type")
        ):
            return render_error_response(
                _(
                    "requests with 'id' cannot also have 'account', 'memo', or 'memo_type'"
                )
            )

        try:
            # validate memo and memo_type
            make_memo(request.GET.get("memo"), request.GET.get("memo_type"))
        except ValueError:
            return render_error_response(_("invalid 'memo' for 'memo_type'"))

        try:
            response_data = rci.get(
                {
                    "id": request.GET.get("id"),
                    "sep10_client_account": account,
                    "account": request.GET.get("account"),
                    "memo": request.GET.get("memo"),
                    "memo_type": request.GET.get("memo_type"),
                    "type": request.GET.get("type"),
                    "lang": request.GET.get("lang"),
                }
            )
        except ValueError as e:
            return render_error_response(str(e), status_code=400)
        except ObjectDoesNotExist as e:
            return render_error_response(str(e), status_code=404)

        try:
            validate_response_data(response_data)
        except ValueError:
            logger.exception(
                "An exception was raised validating GET /customer response"
            )
            return render_error_response(
                _("unable to process request."), status_code=500
            )

        return Response(response_data)

    @staticmethod
    @validate_sep10_token()
    def put(account: str, _client_domain: Optional[str], request: Request) -> Response:
        if request.data.get("id"):
            if not isinstance(request.data.get("id"), str):
                return render_error_response(_("bad ID value, expected str"))
            elif (
                request.data.get("account")
                or request.data.get("memo")
                or request.data.get("memo_type")
            ):
                return render_error_response(
                    _(
                        "requests with 'id' cannot also have 'account', 'memo', or 'memo_type'"
                    )
                )
        elif account != request.data.get("account"):
            return render_error_response(
                _("The account specified does not match authorization token"),
                status_code=403,
            )

        try:
            # validate memo and memo_type
            make_memo(request.data.get("memo"), request.data.get("memo_type"))
        except ValueError:
            return render_error_response(_("invalid 'memo' for 'memo_type'"))

        try:
            customer_id = rci.put(
                {
                    "id": request.data.get("id"),
                    "account": account,
                    "memo": request.data.get("memo"),
                    "memo_type": request.data.get("memo_type"),
                    "type": request.data.get("type"),
                    **extract_sep9_fields(request.data),
                }
            )
        except ValueError as e:
            return render_error_response(str(e), status_code=400)
        except ObjectDoesNotExist as e:
            return render_error_response(str(e), status_code=404)

        if not isinstance(customer_id, str):
            logger.error(
                "Invalid customer ID returned from put() integration. Must be str."
            )
            return render_error_response(_("unable to process request"))

        return Response({"id": customer_id}, status=202)


@api_view(["PUT"])
@renderer_classes([JSONRenderer, BrowsableAPIRenderer])
@parser_classes([MultiPartParser, FormParser, JSONParser])
@validate_sep10_token()
def callback(account: str, _client_domain: Optional[str], request: Request) -> Response:
    if request.data.get("id"):
        if not isinstance(request.data.get("id"), str):
            return render_error_response(_("bad ID value, expected str"))
        elif (
            request.data.get("account")
            or request.data.get("memo")
            or request.data.get("memo_type")
        ):
            return render_error_response(
                _(
                    "requests with 'id' cannot also have 'account', 'memo', or 'memo_type'"
                )
            )
    elif account != request.data.get("account"):
        return render_error_response(
            _("The account specified does not match authorization token"),
            status_code=403,
        )

    try:
        # validate memo and memo_type
        make_memo(request.data.get("memo"), request.data.get("memo_type"))
    except ValueError:
        return render_error_response(_("invalid 'memo' for 'memo_type'"))

    callback_url = request.data.get("url")
    if not callback_url:
        return render_error_response(_("callback 'url' required"))
    schemes = ["https"] if not settings.LOCAL_MODE else ["https", "http"]
    try:
        URLValidator(schemes=schemes)(request.data.get("url"))
    except ValidationError:
        return render_error_response(_("'url' must be a valid URL"))

    try:
        rci.callback(
            {
                "id": request.data.get("id"),
                "account": account,
                "memo": request.data.get("memo"),
                "memo_type": request.data.get("memo_type"),
                "url": callback_url,
            }
        )
    except ValueError as e:
        return render_error_response(str(e), status_code=400)
    except ObjectDoesNotExist as e:
        return render_error_response(str(e), status_code=404)
    except NotImplementedError:
        return render_error_response(_("not implemented"), status_code=501)

    return Response({"success": True})


@api_view(["DELETE"])
@renderer_classes([JSONRenderer, BrowsableAPIRenderer])
@parser_classes([MultiPartParser, FormParser, JSONParser])
@validate_sep10_token()
def delete(
    account_from_auth: str,
    _client_domain: Optional[str],
    request: Request,
    account: str,
) -> Response:
    if account_from_auth != account:
        return render_error_response(_("account not found"), status_code=404)
    try:
        make_memo(request.data.get("memo"), request.data.get("memo_type"))
    except ValueError:
        return render_error_response(_("invalid 'memo' for 'memo_type'"))
    try:
        rci.delete(account, request.data.get("memo"), request.data.get("memo_type"))
    except ObjectDoesNotExist:
        return render_error_response(_("account not found"), status_code=404)
    else:
        return Response({"status": "success"}, status=200)


@api_view(["PUT"])
@renderer_classes([JSONRenderer, BrowsableAPIRenderer])
@parser_classes([MultiPartParser, FormParser, JSONParser])
@validate_sep10_token()
def put_verification(account: str, _client_domain: Optional[str], request) -> Response:
    if not request.data.get("id") or not isinstance(request.data.get("id"), str):
        return render_error_response(_("bad ID value, expected str"))
    for key, value in request.data.items():
        if key == "id":
            continue
        sep9_field, verification = key.rsplit("_", 1)
        if verification != "verification" or sep9_field not in SEP_9_FIELDS:
            return render_error_response(
                _(
                    "all request attributes other than 'id' must be a SEP-9 field followed "
                    "by '_verification'"
                )
            )

    try:
        response_data = rci.put_verification(account, dict(request.data))
    except ObjectDoesNotExist:
        return render_error_response(_("customer not found"), status_code=404)
    except ValueError as e:
        return render_error_response(str(e), status_code=400)
    except NotImplementedError:
        return render_error_response(_("not implemented"), status_code=501)

    try:
        validate_response_data(response_data)
    except ValueError:
        logger.exception(
            "An exception was raised validating PUT /customer/verification response"
        )
        return render_error_response(_("unable to process request."), status_code=500)

    return Response(response_data)


def validate_response_data(data: Dict):
    attrs = ["fields", "id", "message", "status", "provided_fields"]
    if not data:
        raise ValueError("empty response from SEP-12 get() integration")
    elif any(f not in attrs for f in data):
        raise ValueError(
            f"unexpected attribute included in GET /customer response. "
            f"Accepted attributes: {attrs}"
        )
    elif "id" in data and not isinstance(data["id"], str):
        raise ValueError("customer IDs must be strings")
    accepted_statuses = ["ACCEPTED", "PROCESSING", "NEEDS_INFO", "REJECTED"]
    if not data.get("status") or data.get("status") not in accepted_statuses:
        raise ValueError("invalid status in SEP-12 GET /customer response")
    elif (
        any([f.get("optional") is False for f in data.get("fields", {}).values()])
        and data.get("status") == "ACCEPTED"
    ):
        raise ValueError(
            "all required 'fields' must be provided before a customer can be 'ACCEPTED'"
        )
    if data.get("fields"):
        validate_fields(data.get("fields"))
    if data.get("provided_fields"):
        validate_fields(data.get("provided_fields"), provided=True)
    if data.get("message") and not isinstance(data["message"], str):
        raise ValueError(
            "invalid message value in SEP-12 GET /customer response, should be str"
        )


def validate_fields(fields: Dict, provided=False):
    if not isinstance(fields, Dict):
        raise ValueError(
            "invalid fields type in SEP-12 GET /customer response, should be dict"
        )
    if len(extract_sep9_fields(fields)) < len(fields):
        raise ValueError("SEP-12 GET /customer response fields must be from SEP-9")
    accepted_field_attrs = [
        "type",
        "description",
        "choices",
        "optional",
        "status",
        "error",
    ]
    accepted_types = ["string", "binary", "number", "date"]
    accepted_statuses = [
        "ACCEPTED",
        "PROCESSING",
        "REJECTED",
        "VERIFICATION_REQUIRED",
    ]
    for key, value in fields.items():
        if not set(value.keys()).issubset(set(accepted_field_attrs)):
            raise ValueError(
                f"unexpected attribute in '{key}' object in SEP-12 GET /customer response, "
                f"accepted values: {', '.join(accepted_field_attrs)}"
            )
        if not value.get("type") or value.get("type") not in accepted_types:
            raise ValueError(
                f"bad type value for '{key}' in SEP-12 GET /customer response"
            )
        elif not (
            value.get("description") and isinstance(value.get("description"), str)
        ):
            raise ValueError(
                f"bad description value for '{key}' in SEP-12 GET /customer response"
            )
        elif value.get("choices") and not isinstance(value.get("choices"), list):
            raise ValueError(
                f"bad choices value for '{key}' in SEP-12 GET /customer response"
            )
        elif value.get("optional") and not isinstance(value.get("optional"), bool):
            raise ValueError(
                f"bad optional value for '{key}' in SEP-12 GET /customer response"
            )
        elif not provided and value.get("status"):
            raise ValueError(
                f"'{key}' object in 'fields' object cannot have a 'status' property"
            )
        elif (
            provided
            and value.get("status")
            and value.get("status") not in accepted_statuses
        ):
            raise ValueError(
                f"bad field status value for '{key}' in SEP-12 GET /customer response"
            )
        elif not provided and value.get("error"):
            raise ValueError(
                f"'{key}' object in 'fields' object cannot have 'error' property"
            )
        elif (
            provided and value.get("error") and not isinstance(value.get("error"), str)
        ):
            raise ValueError(
                f"bad error value for '{key}' in SEP-12 GET /customer response"
            )

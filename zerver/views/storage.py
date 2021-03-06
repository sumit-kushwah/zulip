from typing import Dict, List, Optional

from django.http import HttpRequest, HttpResponse

from zerver.decorator import REQ, has_request_variables
from zerver.lib.bot_storage import (
    StateError,
    get_bot_storage,
    get_keys_in_bot_storage,
    remove_bot_storage,
    set_bot_storage,
)
from zerver.lib.response import json_error, json_success
from zerver.lib.validator import check_dict, check_list, check_string
from zerver.models import UserProfile


@has_request_variables
def update_storage(
    request: HttpRequest,
    user_profile: UserProfile,
    storage: Dict[str, str] = REQ(json_validator=check_dict([], value_validator=check_string)),
) -> HttpResponse:
    try:
        set_bot_storage(user_profile, list(storage.items()))
    except StateError as e:  # nocoverage
        return json_error(str(e))
    return json_success()


@has_request_variables
def get_storage(
    request: HttpRequest,
    user_profile: UserProfile,
    keys: Optional[List[str]] = REQ(json_validator=check_list(check_string), default=None),
) -> HttpResponse:
    keys = keys or get_keys_in_bot_storage(user_profile)
    try:
        storage = {key: get_bot_storage(user_profile, key) for key in keys}
    except StateError as e:
        return json_error(str(e))
    return json_success({"storage": storage})


@has_request_variables
def remove_storage(
    request: HttpRequest,
    user_profile: UserProfile,
    keys: Optional[List[str]] = REQ(json_validator=check_list(check_string), default=None),
) -> HttpResponse:
    keys = keys or get_keys_in_bot_storage(user_profile)
    try:
        remove_bot_storage(user_profile, keys)
    except StateError as e:
        return json_error(str(e))
    return json_success()

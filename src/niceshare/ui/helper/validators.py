import re
from typing import Final, Callable

from email_validator import validate_email, EmailNotValidError
from nicegui.observables import ObservableDict

from niceshare.helper.config import settings
from niceshare.helper.i18n import i18n

""" Form Value Validation Module (Email Adress, Phone Number, Web URL)"""

INPUT_VALIDATION: Final[dict[str, Callable[[str], bool]]] = {i18n.get("form.please_fill_field"): lambda v: len(v) > 0}
IMG_URL_REGEX: re.Pattern = re.compile(
    r"^(?P<url>(?P<domain>https?://[-a-zA-Z0-9@:%._\+~#=]+)(?P<path>(?P<subfolders>(?:/[-a-zA-Z0-9@:%._\+~#=]+)*/)?/?(?P<filename>[^\s/]+?\.(?P<ext>jpg|jpeg|png|gif|bmp|tiff|webp))))",
re.IGNORECASE)
URL_REGEX: re.Pattern = re.compile(r"^(https):\/\/[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}(/[^\s]*)?$")


def validate_mail(key: str, email: str, request: ObservableDict):
    """Email Validation

    Args:
        key (str): #TODO
        email (str): The Email Adress to validate
        request (ObservableDict): #TODO 

    """

    try:
        request.update({key: validate_email(email, check_deliverability=True, strict=True).normalized})
        return None
    except EmailNotValidError as e:
        return e.args[0]

def validate_number(key: str, donation: str, request: ObservableDict):
    """Phone Number Validation

    Args:
        key (str): #TODO
        donation (str): #TODO 
        request (ObservableDict): #TODO 

    """

    #TODO cast to int outside and only accept int for donation 

    try:
        request.update({key: int(donation)})
        return None
    except ValueError:
        return i18n.get("form.number_invalid")

def validate_url(url: str, data:dict[str, str]):
    """URL Validation

    Args:
        key (str): #TODO
        data (dict[str, str]): #TODO

    """

    try:
        url = URL_REGEX.match(url).string
        data[settings.columns.get("url")] = url
        return None
    except AttributeError:
        return i18n.get("admin.url_invalid")

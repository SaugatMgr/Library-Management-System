import uuid
import datetime
import base64
import mimetypes

from rest_framework.exceptions import NotAcceptable

from django.core.files.base import ContentFile
from django.core.mail import send_mail
from django.conf import settings


def generate_error(message, code=None):
    error = {"message": message}
    if code:
        error["code"] = code
    return {"error": error}


def get_instance_by_attr(model, attr_name, attr_value):
    """
    Retrieves the instance of a model according to the provided attribute name and value

    Args:
                model (django.db.models.Model): represents from which model class the instance will be retrieved
                attr_name (str): attribute name of the instance
                attr_value : value of the attribute

    Returns:
                instance of model if exists otherwise error
    """
    try:
        instance = model.objects.get(**{attr_name: attr_value})
        return instance
    except model.DoesNotExist:
        raise NotAcceptable(
            generate_error(
                message=f"model {model.__name__} with {attr_name} {attr_value} does not exist."
            )
        )


def to_internal_value(data):
    """
    function to convert base64 file representation to corresponding file content
    """
    try:
        format, base64_content = data.split(";base64,")
        decoded_base64_content = base64.b64decode(base64_content)
        file_extension = format.split("/")[-1]
        unique_file_name = generate_unique_file_name()
        final_file_name = "%s.%s" % (unique_file_name, file_extension)
        corresponding_file = ContentFile(decoded_base64_content, name=final_file_name)

        return corresponding_file
    except Exception as error:
        return str(error)


def generate_unique_file_name(profile=None, cover=None):
    current_date_time = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    unique_identifier = uuid.uuid4().hex[:8]
    unique_suffix = f"{current_date_time}_{unique_identifier}"

    if profile:
        return f"profile_pic_{unique_suffix}"
    elif cover:
        return f"book_cover_{unique_suffix}"
    else:
        return f"file_{unique_suffix}"


def send_otp_to_email(email, otp):
    subject = "OTP CODE"
    message = f"Your OTP code is {otp}"
    from_email = settings.EMAIL_HOST_USER
    recipient_list = [email]

    send_mail(subject, message, from_email, recipient_list)


def compare_resource_type_with_uploaded_file(file_name, resource_type):
    """
    compares the resource type of digital resource with the uploaded file type
    """
    mime_type, _ = mimetypes.guess_type(file_name)
    expected_mime_types = {
        "video": ["video/mp4", "video/x-msvideo", "video/mpeg"],
        "audio": ["audio/mpeg", "audio/x-wav", "audio/mp4"],
        "pdf": ["application/pdf"],
        "interactive": ["application/x-shockwave-flash", "text/html"],
    }
    return mime_type, mime_type in expected_mime_types.get(resource_type, [])

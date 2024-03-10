import uuid
import datetime
import base64

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


def generate_unique_file_name():
    current_date_time = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    unique_identifier = uuid.uuid4().hex[:8]

    return f"profile_pic_{current_date_time}_{unique_identifier}"


def send_otp_to_email(email, otp):
    subject = "OTP CODE"
    message = f"Your OTP code is {otp}"
    from_email = settings.EMAIL_HOST_USER
    recipient_list = [email]

    send_mail(subject, message, from_email, recipient_list)

import uuid
import datetime
import base64

from django.core.files.base import ContentFile


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

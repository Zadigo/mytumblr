import datetime
import secrets

def upload_video_path(instance, filename):
    _, extension = filename.split('.')
    new_file_name = secrets.token_hex(5)
    return f'uploads/user_{instance.user.id}/{new_file_name}.{extension}'

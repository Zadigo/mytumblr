import datetime

def upload_video_path(instance, filename):
    # current_date = datetime.datetime.now().date()
    # formatted_date = f'{current_date.year}{current_date.month}{current_date.day}'
    return f'uploads/user_{instance.user.id}/{filename}'

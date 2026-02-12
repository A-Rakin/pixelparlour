import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///gallery.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Upload settings
    UPLOADED_PHOTOS_DEST = 'static/uploads/photos'
    THUMBNAIL_DEST = 'static/uploads/thumbnails'

    # Image settings
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size
    THUMBNAIL_SIZE = (300, 300)
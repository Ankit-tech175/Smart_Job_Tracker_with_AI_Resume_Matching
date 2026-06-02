import os

from dotenv import load_dotenv


# Load environment variables
load_dotenv()


BASE_DIR = os.path.abspath(
    os.path.dirname(__file__)
)


class Config:

    # Security Keys
    SECRET_KEY = os.getenv(
        "SECRET_KEY"
    )

    JWT_SECRET_KEY = os.getenv(
        "JWT_SECRET_KEY"
    )

    # Database Configuration
    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URL"
    )

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Upload Configuration
    UPLOAD_FOLDER = os.path.join(
        BASE_DIR,
        "uploads"
    )

    ALLOWED_EXTENSIONS = {
        "pdf",
        "doc",
        "docx"
    }
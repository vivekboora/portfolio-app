import os
from dotenv import load_dotenv

# Load variables from a local .env file if present (used for local dev).
# On Render, environment variables are set in the dashboard instead.
basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, ".env"))


def _build_db_uri():
    """
    Builds the SQLAlchemy database URI.

    Preferred: set DATABASE_URL directly (this is what Render / Aiven
    connection strings usually look like already):
        mysql+pymysql://user:password@host:port/dbname

    Fallback: build it from individual DB_* variables.
    """
    database_url = os.environ.get("DATABASE_URL")
    if database_url:
        # Aiven sometimes provides "mysql://..." - SQLAlchemy needs the
        # pymysql driver spelled out explicitly.
        if database_url.startswith("mysql://"):
            database_url = database_url.replace("mysql://", "mysql+pymysql://", 1)
        return database_url

    db_user = os.environ.get("DB_USER", "root")
    db_password = os.environ.get("DB_PASSWORD", "")
    db_host = os.environ.get("DB_HOST", "localhost")
    db_port = os.environ.get("DB_PORT", "3306")
    db_name = os.environ.get("DB_NAME", "portfolio")

    return f"mysql+pymysql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret-key-change-this-in-production")

    SQLALCHEMY_DATABASE_URI = _build_db_uri()
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Aiven MySQL requires SSL. The CA certificate should be downloaded
    # from the Aiven console and its path set via SSL_CA_PATH (defaults
    # to a "ca.pem" file placed in the project root).
    SSL_CA_PATH = os.environ.get("SSL_CA_PATH", os.path.join(basedir, "ca.pem"))
    if os.environ.get("DB_USE_SSL", "true").lower() == "true" and os.path.exists(SSL_CA_PATH):
        SQLALCHEMY_ENGINE_OPTIONS = {
            "connect_args": {"ssl": {"ca": SSL_CA_PATH}},
            "pool_pre_ping": True,
            "pool_recycle": 280,
        }
    else:
        SQLALCHEMY_ENGINE_OPTIONS = {
            "pool_pre_ping": True,
            "pool_recycle": 280,
        }

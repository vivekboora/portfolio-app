import os
import base64
from dotenv import load_dotenv

# Load variables from a local .env file if present (used for local dev).
# On Render, environment variables are set in the dashboard instead.
basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, ".env"))


def _materialize_ca_cert():
    """
    If CA_CERT_BASE64 is set (a single-line base64-encoded copy of the
    Aiven CA certificate), decode it and write it out as ca.pem.

    This sidesteps a common problem on hosts like Render where pasting a
    multi-line PEM certificate into a text box in the dashboard corrupts
    the newlines/characters, causing "PEM lib" / "NO_CERTIFICATE_OR_CRL_FOUND"
    SSL errors. A single-line base64 string can't be corrupted the same way.
    """
    b64 = os.environ.get("CA_CERT_BASE64")
    if not b64:
        return
    target_path = os.environ.get("SSL_CA_PATH", os.path.join(basedir, "ca.pem"))
    try:
        cert_bytes = base64.b64decode(b64)
        with open(target_path, "wb") as f:
            f.write(cert_bytes)
    except Exception as exc:  # noqa: BLE001
        # Fail loudly at startup rather than silently connecting without SSL.
        raise RuntimeError(f"Failed to decode CA_CERT_BASE64 into {target_path}: {exc}")


_materialize_ca_cert()


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

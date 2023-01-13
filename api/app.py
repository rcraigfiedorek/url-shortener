import os
import random
import string
from datetime import datetime

from apiflask import APIFlask
from flask import redirect

from api.schemas import SubmitUrlInput, UrlStatsOutput
from database import UrlModel, db

app = APIFlask(
    __name__,
    title="URL Shortener API",
    version="0.0.1",
)

for postgres_config_var in (
    "POSTGRES_HOST",
    "POSTGRES_PORT",
    "POSTGRES_USER",
    "POSTGRES_PASSWORD",
    "POSTGRES_DB",
):
    if postgres_config_var not in os.environ:
        raise RuntimeError(
            "Database configuration environment variable not set:"
            f" {postgres_config_var}"
        )
app.config.from_mapping(
    SQLALCHEMY_DATABASE_URI="postgresql+pg8000://%s:%s@%s:%s/%s"
    % (
        os.getenv("POSTGRES_USER"),
        os.getenv("POSTGRES_PASSWORD"),
        os.getenv("POSTGRES_HOST"),
        os.getenv("POSTGRES_PORT"),
        os.getenv("POSTGRES_DB"),
    )
)

db.init_app(app)

with app.app_context():
    db.create_all()


@app.post("/submit")
@app.input(SubmitUrlInput, location="json")
@app.output(UrlStatsOutput, status_code=201)
@app.doc(responses=[400])
def submit_url(data):
    """
    Register a shortened URL
    """
    if "shortcode" not in data:
        data["shortcode"] = "".join(
            random.choices(string.ascii_lowercase + string.digits, k=6)
        )

    url = UrlModel(
        shortcode=data["shortcode"].casefold(),
        url=data["url"],
        created_at=datetime.utcnow(),
        access_count=0,
    )
    db.session.add(url)
    db.session.commit()
    return url


@app.get("/<shortcode>")
@app.doc(responses=[301, 302, 404])
def get_url(shortcode: str):
    """
    Access a registered shortened URL
    """
    url = UrlModel.query.get_or_404(shortcode.casefold())
    url.accessed_at = datetime.utcnow()
    url.access_count += 1
    db.session.commit()
    return redirect(url.url)


@app.get("/<shortcode>/stats")
@app.output(UrlStatsOutput)
@app.doc(responses=[404])
def get_url_stats(shortcode: str):
    """
    Get stats for a registered shortened URL
    """
    return UrlModel.query.get_or_404(shortcode)

from database.connection import db


class UrlModel(db.Model):
    __tablename__ = "url"

    shortcode = db.Column(db.String(64), primary_key=True)
    url = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False)
    accessed_at = db.Column(db.DateTime, nullable=True)
    access_count = db.Column(db.Integer, nullable=False)

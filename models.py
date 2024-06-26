"""Models for Cupcake app."""
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


def connect_db(app):
    """Connect to database."""

    db.app = app
    db.init_app(app)


class Cupcake(db.Model):
    """Cupcake model."""

    __tablename__ = "cupcakes"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    flavor = db.Column(db.String(50), nullable=False)
    size = db.Column(db.String(30), nullable=False)
    image = db.Column(db.Text,nullable=False, default = "https://tinyurl.com/demo-cupcake")
    rating = db.Column(db.Float, nullable=False)
    
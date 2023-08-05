import sqlalchemy as sa

from .db import db


class DbTestModel(db.ModelBase):
    __tablename__ = 'test'

    id = sa.Column(sa.Integer(), primary_key=True, index=True)
    string_field = sa.Column(sa.String(), index=True, nullable=False)
    integer_field = sa.Column(sa.Integer(), index=True, nullable=False)

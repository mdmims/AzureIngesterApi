import logging
import uuid
import re
import sqlalchemy
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()
log = logging.getLogger('sqlalchemy')


def generate_uuid():
    return str(uuid.uuid4())


def get_engine_type():
    return db.session.bind.dialect.name


class DataAssetType(db.Model):
    __tablename__ = 'asset_type'

    id = db.Column(db.Integer, nullable=False, primary_key=True)
    name = db.Column(db.String(250), nullable=False, unique=True)
    description = db.Column(db.String(4000))

    def __repr__(self):
        return f'{self.name}'

    @staticmethod
    def retrieve_all_data_asset_types():
        return DataAssetType.query.all()

    @staticmethod
    def retrieve_data_asset_type_by_id(asset_type_id):
        return DataAssetType.query.filter_by(id=asset_type_id).first()


class DataAsset(db.Model):
    __tablename__ = 'asset'

    id = db.Column(db.String(40), nullable=False, primary_key=True, default=generate_uuid)
    type_id = db.Column(db.Integer, db.ForeignKey(DataAssetType.id), nullable=False)


def run_sql_script(sql_file, bind=None):
    with open(sql_file, 'r') as f:
        content = f.read()
    statements = content.split(';')
    for sql in statements:
        if len(sql.strip()) > 0:
            sql = re.sub(r'--.*\n', ' ', sql, flags=re.MULTILINE)
            sql = sql.strip().replace('\n', ' ')
            if bind:
                bind.execute(sqlalchemy.sql.text(sql))
            else:
                db.engine.execute(sqlalchemy.sql.text(sql))

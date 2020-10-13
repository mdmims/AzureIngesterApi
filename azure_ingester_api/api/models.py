import csv
import logging
import re
import uuid
from dataclasses import dataclass, field

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
log = logging.getLogger('sqlalchemy')


def generate_uuid():
    return str(uuid.uuid4())


def get_engine_type():
    return db.session.bind.dialect.name


class AssetType(db.Model):
    __tablename__ = 'asset_type'

    id = db.Column(db.Integer, nullable=False, primary_key=True)
    name = db.Column(db.String(250), nullable=False, unique=True)
    description = db.Column(db.String(4000))

    def __repr__(self):
        return f'{self.name}'

    @staticmethod
    def retrieve_all_asset_types():
        return AssetType.query.all()

    @staticmethod
    def retrieve_data_asset_type_by_id(asset_type_id):
        return AssetType.query.filter_by(id=asset_type_id).first()

    @staticmethod
    def retrieve_data_asset_type_id_by_name(asset_type_name):
        left_wildcard = right_wildcard = ""
        match = re.match(r'(\*?)([\w -]+)(\*?)', str(asset_type_name))
        if match:
            left_wildcard = match.group(1)
            asset_type_name = match.group(2)
            right_wildcard = match.group(3)
        asset_type = AssetType.query.filter_by(name=asset_type_name).first()
        if asset_type:
            return left_wildcard + str(asset_type.id) + right_wildcard
        return None


class Asset(db.Model):
    __tablename__ = 'asset'

    id = db.Column(db.String(40), nullable=False, primary_key=True, autoincrement=True)
    type_id = db.Column(db.Integer, db.ForeignKey(AssetType.id), nullable=False)
    name = db.Column(db.String(200), nullable=False)


class DataTransform(db.Model):
    __tablename__ = 'transform_type'

    id = db.Column(db.Integer(), nullable=False, primary_key=True)
    name = db.Column(db.String(40), nullable=False, unique=True)
    description = db.Column(db.String(250))

    def __repr__(self):
        return f'{self.name}'


@dataclass(frozen=False)
class StatusResponse:
    status: str = "OK"
    code: int = 200
    messages: list = field(default_factory=list)


@dataclass(frozen=True)
class Result:
    asset_type: str


class DataAssetTypeResponse(StatusResponse):
    def __init__(self, asset_type, **args):
        super().__init__(**args)
        self.result = Result(asset_type=asset_type)


def run_sql_script(sql_file, bind=None):
    with open(sql_file, 'r') as f:
        content = f.read()
    statements = content.split(';')
    for sql in statements:
        if len(sql.strip()) > 0:
            sql = re.sub(r'--.*\n', ' ', sql, flags=re.MULTILINE)
            sql = sql.strip().replace('\n', ' ')
            if bind:
                bind.execute(SQLAlchemy.sql.text(sql))
            else:
                db.engine.execute(SQLAlchemy.sql.text(sql))


def replace_empty(d):
    for k, v in d.items():
        if v == '':
            d[k] = None
    return d


def insert_data_from_csv(filename, table, bind=None):
    with open(filename, newline='', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)
        records = [dict(replace_empty(o)) for o in reader]
        if bind:
            bind.execute(table.insert().values(records))
        else:
            db.engine.execute(table.insert().values(records))

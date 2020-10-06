import factory
from azure_ingester_api.app import db
from azure_ingester_api.healthz.models import HelloWorld


class HelloWorldFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = HelloWorld
        sqlalchemy_session = db.session

    id = factory.Sequence(lambda n: n)
    saying = factory.Sequence(lambda n: f'Hello, World {n}')

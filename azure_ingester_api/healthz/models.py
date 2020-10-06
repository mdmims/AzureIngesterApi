from azure_ingester_api.app import db


class HelloWorld(db.Model):
    __tablename__ = 'helloworld'

    id = db.Column(db.Integer, primary_key=True)
    saying = db.Column(db.String, nullable=False)

    @staticmethod
    def retrieve_all():
        return HelloWorld.query.all()

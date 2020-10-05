from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from azure_ingester_api.app import create_app, db
import os


app = create_app(os.environ.get('API_ENVIRONMENT'))

migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)


if __name__ == '__main__':
    manager.run()

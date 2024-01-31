from flask_migrate import Migrate
from your_flask_app import app, db  # Replace 'your_flask_app' with the actual name of your Flask app

migrate = Migrate(app, db)

if __name__ == '__main__':
    app.run()


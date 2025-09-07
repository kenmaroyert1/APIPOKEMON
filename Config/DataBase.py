from flask_sqlalchemy import SQLAlchemy
import os
from dotenv import load_dotenv

load_dotenv()

db = SQLAlchemy()

def get_database_url():
    username = os.getenv('DBUSERNAME')
    password = os.getenv('DBPASSWORD')
    host = os.getenv('DBHOST')
    port = os.getenv('DBPORT')
    database = os.getenv('DBNAME')
    
    return f"mysql+mysqlconnector://{username}:{password}@{host}:{port}/{database}"

def init_db(app):
    app.config['SQLALCHEMY_DATABASE_URI'] = get_database_url()
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)
    
    with app.app_context():
        db.create_all()
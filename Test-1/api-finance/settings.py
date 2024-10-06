import os
import base64
import logging
import mysql.connector

from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_serialize import FlaskSerializeMixin
from flask_apscheduler import APScheduler

from flask_jwt_extended import JWTManager, create_access_token

from config import ProductionConfig, DevelopmentConfig

""" Initiation Flask """
app = Flask(__name__, static_folder='storage')

""" Load config """
if os.environ.get('FLASK_ENV') == 'development':
    config = DevelopmentConfig()
else:
    config = ProductionConfig()
app.config.from_object(config)

""" Initiation App Scheduller """
scheduler = APScheduler()
scheduler.init_app(app)

""" Setup JWT """
app.config['JWT_SECRET_KEY'] = 'Dfg4beGytBSjWlOKxISH'
jwt = JWTManager(app)

""" Initiation SQL for ORM """
db = SQLAlchemy(app)
FlaskSerializeMixin.db = db

logger = logging.getLogger(__name__)


""" Function get connection for Query RAW """
def get_connection():
	return mysql.connector.connect(
        host=config.DB_HOST, 
        database=config.DB_NAME, 
        user=config.DB_USER, 
        password=config.DB_PASS, 
        use_pure=True, 
        allow_local_infile=True
    )

""" Set scheduller """
import transfer_scheduller as Transfer
scheduler.add_job(id='Scheduled Task Transfer', func=Transfer.transfer_amount, trigger='interval', seconds=15)

# Start the scheduler
scheduler.start()
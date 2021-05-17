from app import create_app
from flask_config import ProdConfig

app = create_app(config=ProdConfig)

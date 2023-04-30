from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, registry

from .config import config


engine = create_engine(config["db_url"], pool_size=10)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

mapper_registry = registry()

Base = mapper_registry.generate_base()
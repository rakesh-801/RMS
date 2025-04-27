from app.database import engine, Base
from app.models import JobDescription, Candidate, Resume
import logging

logging.basicConfig()
logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)

def init_db():
    print("Dropping existing tables...")
    Base.metadata.drop_all(engine)
    
    print("Creating tables...")
    Base.metadata.create_all(engine)
    
    # Verify
    from sqlalchemy import inspect
    inspector = inspect(engine)
    print("Created tables:", inspector.get_table_names())

if __name__ == "__main__":
    init_db()
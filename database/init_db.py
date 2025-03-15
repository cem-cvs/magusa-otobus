from models.base import engine, Base

def init_database():
    print("Initializing database on Neon PostgreSQL...")
    Base.metadata.create_all(bind=engine)  # Create tables if they don't exist

if __name__ == "__main__":
    init_database()

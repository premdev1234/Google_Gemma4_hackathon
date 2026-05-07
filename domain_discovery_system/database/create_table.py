from domain_discovery_system.database.connection import Base, engine

# IMPORTANT:
# Import models so SQLAlchemy registers tables
import domain_discovery_system.database.models


def create_tables():

    print("Creating tables...")

    Base.metadata.create_all(bind=engine)

    print("Tables created successfully!")


if __name__ == "__main__":
    create_tables()

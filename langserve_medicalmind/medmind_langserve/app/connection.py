from sqlalchemy import create_engine

def get_database_connection():
    # Create a SQLAlchemy engine to connect to the SQLite database
    engine = create_engine(
        "sqlite:///C:\\Users\\mtalh\\OneDrive\\Desktop\\ML\\Xavor\\bootcamp\\langserve_medicalmind\\mimic3.db")

    # Connect to the engine
    connection = engine

    return connection

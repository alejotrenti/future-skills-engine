from src.utils.database import engine

with engine.connect() as conn:
    print("Conexion exitosa a Neon")
from sqlmodel import SQLModel, create_engine, Session
from dotenv import load_dotenv
import os

# Carrega variáveis de ambiente
load_dotenv()

# Configuração do banco
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///cybershield.db")

engine = create_engine(
    DATABASE_URL, 
    echo=False, 
    connect_args={"check_same_thread": False}
)

def create_db_and_tables():
    """Cria todas as tabelas no banco de dados"""
    SQLModel.metadata.create_all(engine)
    print("✅ Tabelas criadas ou já existentes.")

def get_session():
    """Dependency para obter sessão do banco"""
    with Session(engine) as session:
        yield session
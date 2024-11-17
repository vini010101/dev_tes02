from sqlalchemy import create_engine, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Configurações do banco de dados
DATABASE_CONFIG = {
    "host": "mysql",
    "user": "vini",
    "password": "885402",
    "database": "blog"
}

# Conexão com o banco de dados usando o MySQL
SQLALCHEMY_DATABASE_URL = (
    f"mysql+mysqlconnector://{DATABASE_CONFIG['user']}:{DATABASE_CONFIG['password']}"
    f"@{DATABASE_CONFIG['host']}/{DATABASE_CONFIG['database']}"
)


# Criando o engine do SQLAlchemy
engine = create_engine(SQLALCHEMY_DATABASE_URL, echo=True)

# Criando a base de dados do SQLAlchemy
Base = declarative_base()

# Criando a sessão
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Função para obter uma sessão de banco de dados
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

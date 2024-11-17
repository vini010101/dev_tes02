from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, Session
from datetime import datetime
# Base para os modelos
Base = declarative_base()

# Definição do modelo User
class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)

    # Relacionamento com a tabela 'posts' usando o nome correto da tabela
    posts = relationship("Post", back_populates="user")

class Post(Base):
    __tablename__ = 'posts'

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'))  # Chave estrangeira para User
    created_at = Column(DateTime, default=datetime.now) 
    
    user = relationship("User", back_populates="posts")  # Relacionamento com User
    
    def __repr__(self):
        return f"<Post(id={self.id}, title={self.title}, created_at={self.created_at})>"
    
    

def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()



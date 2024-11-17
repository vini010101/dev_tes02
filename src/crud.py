from sqlalchemy.orm import Session
from .entity import Post, User
from .schemas import PostCreate
from typing import List


def create_post(db: Session, post: PostCreate, user_id: int):
    db_post = Post(title=post.title, description=post.description, user_id=user_id)
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return db_post


def delete_all_posts(db: Session):
    
    # Deleta todos os posts
    db.query(Post).delete()
    db.commit()
    return {"message": "All posts deleted successfully"}




def get_posts(db: Session) -> List[Post]:
    return db.query(Post).all()


def get_user_by_email(db: Session, email: str):
    try:
        return db.query(User).filter(User.email == email).first()
    except Exception as e:
        print(f"Erro ao buscar usuário: {e}")
        raise


def create_post(db: Session, post_data: PostCreate):
    new_post = Post(**post_data.dict())
    db.add(new_post)
    db.commit()  
    db.refresh(new_post)
    return new_post




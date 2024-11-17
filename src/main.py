from fastapi import FastAPI, HTTPException, Form, status, Depends
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError 
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from starlette.requests import Request
import bcrypt
from . import crud
from .database import get_db  # Função para obter uma sessão do banco de dados
from typing import List, Dict
from .schemas import PostResponse, PostCreate
from .crud import get_posts, get_user_by_email, delete_all_posts
from datetime import datetime
from .entity import Post, User
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)
logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)

app = FastAPI()

# Servindo arquivos estáticos da pasta "frontend"
app.mount("/frontend", StaticFiles(directory="frontend"), name="frontend")

templates = Jinja2Templates(directory="frontend")

# Função para criar o usuário padrão
def create_default_user(db: Session):
    email = "teste@gmail.com"
    password = "1234"
    
    # Verificar se o usuário já existe no banco
    existing_user = crud.get_user_by_email(db, email=email)
    if not existing_user:
        # Hash da senha
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        
        # Criar o usuário no banco
        user = User(email=email, password=hashed_password)
        db.add(user)
        db.commit()
        db.refresh(user)
        print(f"Usuário {email} criado com sucesso.")
    else:
        print(f"O usuário {email} já existe.")

@app.get("startup")
async def startup():
    # Durante a inicialização do site é criado o usuário padrão
    db = next(get_db())  # Obtém a sessão do banco de dados
    create_default_user(db)


@app.get("/", response_class=HTMLResponse)
async def inicial(request: Request):
    try:
        return templates.TemplateResponse("index.html", {"request": request})
    except Exception as e:
        print("Erro ao carregar página inicial:", e)
        raise HTTPException(status_code=500, detail="Erro ao carregar página inicial")


@app.get("/posts", response_class=HTMLResponse)
async def posts_page(request: Request):
    try:
        return templates.TemplateResponse("posts.html", {"request": request})
    except Exception as e:
        print("Erro ao carregar página de posts:", e)
        raise HTTPException(status_code=500, detail="Erro ao carregar posts")


@app.post("/api/login")
async def login(email: str = Form(...), password: str = Form(...), db: Session = Depends(get_db)):
    try:
        # Buscar o usuário pelo e-mail
        user = get_user_by_email(db, email=email)

        # Verificar se o usuário foi encontrado
        if not user:
            raise HTTPException(status_code=404, detail="E-mail não encontrado.")

        # Verificar se a senha está correta comparando com o hash
        if not bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
            raise HTTPException(status_code=401, detail="Senha incorreta.")

        # Se tudo estiver certo, redireciona o usuário
        return RedirectResponse(url="/posts", status_code=303)
    except SQLAlchemyError as e:
        
        # Captura erros do SQLAlchemy
        db.rollback()  # Garantir que a transação seja revertida
        print(f"Erro de banco de dados: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Erro de banco de dados: {str(e)}")
    except Exception as e:
        
        # Captura qualquer outro erro
        print(f"Erro ao realizar login: {e}")
        raise HTTPException(status_code=500, detail="Erro ao realizar login")

@app.post("/api/create-post")
async def create_post(post: PostCreate, db: Session = Depends(get_db)):
    new_post = Post(
        title=post.title,
        description=post.description,
        user_id=6  # Associar diretamente ao único usuário
    )
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return {
        "message": "Post criado com sucesso!",
        "data": {"id": new_post.id, "title": new_post.title, "description": new_post.description}
    }

@app.get("/api/posts", response_model=List[PostResponse])
async def get_posts_endpoint(db: Session = Depends(get_db)):
    try:
        # Recuperar todos os posts
        posts = get_posts(db)
        return posts
    except Exception as e:
        print(f"Erro ao buscar posts: {e}")
        raise HTTPException(status_code=500, detail="Erro ao buscar posts")
    
@app.delete("/posts/all")
async def delete_all_posts(db: Session = Depends(get_db)):
    try:
        db.query(Post).delete()  # Deleta todos os registros na tabela Post
        db.commit()
        return {"message": "Todos os posts foram deletados com sucesso."}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Erro ao deletar posts: {e}")

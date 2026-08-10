from fastapi import Depends, FastAPI, HTTPException
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from pydantic import BaseModel
from typing import Optional
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
import secrets


# Caso seja online, apontar para um banco de dados.
DATABASE_URL = "sqlite:///./tarefas.db"

# Configuração do SQLAlchemy Local
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


app = FastAPI()

USUARIO = "admin"
SENHA = "admin"

security = HTTPBasic()

dicionario_tarefas = {}

class TarefaDB(Base):
    __tablename__ = "tarefas"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, index=True)
    descricao = Column(String, index=True)
    concluida = Column(Integer)

class Tarefas(BaseModel):
    nome: str
    descricao: str
    concluida: int

Base.metadata.create_all(bind=engine)

def sessao_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def autenticar_usuario(credentials: HTTPBasicCredentials = Depends(security)):
    usuario_correto = secrets.compare_digest(credentials.username, USUARIO)
    senha_correta = secrets.compare_digest(credentials.password, SENHA)

    if not (usuario_correto and senha_correta):
        raise HTTPException(
            status_code=401,
            detail="Usuário ou senha inválidos.",
            headers={"WWW-Authenticate": "Basic"},
        )


@app.post("/adiciona")
def adicionar_tarefa(tarefas: Tarefas, db: Session = Depends(sessao_db), credentials: HTTPBasicCredentials = Depends(autenticar_usuario)):
    db_tarefa = db.query(TarefaDB).filter(TarefaDB.nome == tarefas.nome, TarefaDB.descricao == tarefas.descricao).first()
    if db_tarefa:
        raise HTTPException(status_code=400, detail="Tarefa já existe no banco de dados.")

    nova_tarefa = TarefaDB(nome=tarefas.nome, descricao=tarefas.descricao, concluida=tarefas.concluida)
    db.add(nova_tarefa)
    db.commit()
    db.refresh(nova_tarefa)
    return {"mensagem": "Tarefa adicionada com sucesso!"}


    
@app.get("/tarefas")
def listar_tarefas(page: int = 1, per_page: int = 10, db: Session = Depends(sessao_db), credentials: HTTPBasicCredentials = Depends(autenticar_usuario)):
    if page < 1 or per_page < 1:
        raise HTTPException(status_code=400, detail="Parâmetros de paginação inválidos.")

    tarefas = db.query(TarefaDB).offset((page - 1) * per_page).limit(per_page).all()
    
    if not tarefas:
        return {"mensagem": "Nenhuma tarefa encontrada."}
    
    total_tarefas = db.query(TarefaDB).count()

    return {"tarefas": [{"id": tarefa.id, "nome": tarefa.nome, "descricao": tarefa.descricao, "concluida": tarefa.concluida} for tarefa in tarefas], "total_tarefas": total_tarefas, "pagina_atual": page, "tarefas_por_pagina": per_page}

    
@app.put("/atualiza/{id}")
def put_tarefa(id: int, tarefas: Tarefas, db: Session = Depends(sessao_db),credentials: HTTPBasicCredentials = Depends(autenticar_usuario)):
    tarefa_existente = db.query(TarefaDB).filter(TarefaDB.id == id).first()
    if not tarefa_existente:
        raise HTTPException(status_code=404, detail="Tarefa não encontrada.")
    
    tarefa_existente.nome = tarefas.nome
    tarefa_existente.descricao = tarefas.descricao
    tarefa_existente.concluida = tarefas.concluida

    db.commit()
    db.refresh(tarefa_existente)

    return {"mensagem": "Tarefa atualizada com sucesso!"}

    
@app.delete("/deletar/{id}")
def remover_tarefa(id: int, db: Session = Depends(sessao_db), credentials: HTTPBasicCredentials = Depends(autenticar_usuario)):
    tarefa_existente = db.query(TarefaDB).filter(TarefaDB.id == id).first()
    if not tarefa_existente:
        raise HTTPException(status_code=404, detail="Tarefa não encontrada no banco de dados.")

    db.delete(tarefa_existente)
    db.commit()
    return {"mensagem": "Tarefa removida com sucesso!"}
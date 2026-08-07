from fastapi import Depends, FastAPI, HTTPException
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from pydantic import BaseModel
from typing import Optional

app = FastAPI()

USUARIO = "admin"
SENHA = "admin"

security = HTTPBasic()

tarefas = {}

class Tarefa(BaseModel):
    nome: str
    descricao: str
    concluida: bool = False

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
def adicionar_tarefa(id: int, Tarefa: Tarefa, credentials: HTTPBasicCredentials = Depends(autenticar_usuario)):
    if id in tarefas:
        raise HTTPException(status_code=400, detail="Já existe uma tarefa com este ID.")
    else:
        tarefas[id] = Tarefa.model_dump()
        return {"mensagem": "Tarefa adicionada com sucesso!"}

    
@app.get("/tarefas")
def listar_tarefas(page: int = 1, per_page: int = 10, credentials: HTTPBasicCredentials = Depends(autenticar_usuario)):
    if page < 1 or per_page < 1:
        raise HTTPException(status_code=400, detail="Parâmetros de paginação inválidos.")
    if not tarefas:
        return {"mensagem": "Nenhuma tarefa encontrada."}
    start = (page - 1) * per_page
    end = start + per_page

    paginadastarefas = [
        {"id": id, "nome": tarefa_data["nome"], "descricao": tarefa_data["descricao"], "concluida": tarefa_data["concluida"]}
        for id, tarefa_data in list(tarefas.items())[start:end]
    ]

    return {"tarefas": paginadastarefas, "total_tarefas": len(tarefas), "pagina_atual": page, "tarefas_por_pagina": per_page}

    
@app.put("/atualiza/{id}")
def put_tarefa(id: int, Tarefa: Tarefa, credentials: HTTPBasicCredentials = Depends(autenticar_usuario)):
    concluir_tarefa = tarefas.get(id)
    if not concluir_tarefa:
        raise HTTPException(status_code=404, detail="Tarefa não encontrada.")
    else:
        tarefas[id] = Tarefa.model_dump()
        return {"mensagem": "Tarefa atualizada com sucesso!"}

    
@app.delete("/deletar/{id}")
def remover_tarefa(id: int, credentials: HTTPBasicCredentials = Depends(autenticar_usuario)):
    if id not in tarefas:
        raise HTTPException(status_code=404, detail="Tarefa não encontrada.")
    else:
        del tarefas[id]
        return {"mensagem": "Tarefa removida com sucesso!"}
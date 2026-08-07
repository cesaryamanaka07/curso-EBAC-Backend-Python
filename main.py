from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional

app = FastAPI()

tarefas = {}

class Tarefa(BaseModel):
    nome: str
    descricao: str
    concluida: bool = False


@app.post("/adiciona")
def adicionar_tarefa(id: int, Tarefa: Tarefa):
    if id in tarefas:
        raise HTTPException(status_code=400, detail="Já existe uma tarefa com este ID.")
    else:
        tarefas[id] = Tarefa.model_dump()
        return {"mensagem": "Tarefa adicionada com sucesso!"}

    
@app.get("/tarefas")
def listar_tarefas():
    if not tarefas:
        return {"message": "Nenhuma tarefa encontrada."}
    else:
        return {"tarefas": tarefas}

@app.put("/atualiza/{id}")
def put_tarefa(id: int, Tarefa: Tarefa):
    concluir_tarefa = tarefas.get(id)
    if not concluir_tarefa:
        raise HTTPException(status_code=404, detail="Tarefa não encontrada.")
    else:
        tarefas[id] = Tarefa.model_dump()
        return {"mensagem": "Tarefa atualizada com sucesso!"}

    
@app.delete("/deletar/{id}")
def remover_tarefa(id: int):
    if id not in tarefas:
        raise HTTPException(status_code=404, detail="Tarefa não encontrada.")
    else:
        del tarefas[id]
        return {"mensagem": "Tarefa removida com sucesso!"}
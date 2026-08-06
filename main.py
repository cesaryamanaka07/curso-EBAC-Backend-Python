from fastapi import FastAPI, HTTPException, Query

app = FastAPI()

tarefas = {}

@app.post("/adiciona")
def adicionar_tarefa(id: int, nome: str, descricao: str, concluida: str = Query(default= "não concluída")):
    if id in tarefas:
        raise HTTPException(status_code=400, detail="Já existe uma tarefa com este ID.")
    else:
        tarefas[id] = {"id": id, "nome": nome, "descricao": descricao, "concluida": concluida}
        return {"mensagem": "Tarefa adicionada com sucesso!"}

    
@app.get("/tarefas")
def listar_tarefas():
    if not tarefas:
        return {"message": "Nenhuma tarefa encontrada."}
    else:
        return {"tarefas": tarefas}

@app.put("/atualiza/{id}")
def put_tarefa(id: int, nome: str = Query(default=""), descricao: str = Query(default=""), concluida: str = Query(default="")):
    concluir_tarefa = tarefas.get(id)
    if not concluir_tarefa:
        raise HTTPException(status_code=404, detail="Tarefa não encontrada.")
    else:
        if nome:
            concluir_tarefa["nome"] = nome
        if descricao:
            concluir_tarefa["descricao"] = descricao
        if concluida:
            concluir_tarefa["concluida"] = concluida
        return {"mensagem": "Tarefa atualizada com sucesso!"}

    
@app.delete("/deletar/{id}")
def remover_tarefa(id: int):
    if id not in tarefas:
        raise HTTPException(status_code=404, detail="Tarefa não encontrada.")
    else:
        del tarefas[id]
        return {"mensagem": "Tarefa removida com sucesso!"}
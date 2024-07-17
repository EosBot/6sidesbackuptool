import os
from fastapi import Depends, FastAPI, HTTPException, Security
from fastapi.security.api_key import APIKeyHeader
from pydantic import BaseModel
from typing import List, Optional, Dict, Union, Tuple, Annotated
from dotenv import load_dotenv
from .celery import celery_app
from .tasks import (
    init_backup_task, create_backup_task, extract_backup_task,
    check_backup_task, rename_backup_task, list_backup_task,
    diff_backup_task, delete_backup_task, prune_backup_task,
    compact_backup_task, recreate_backup_task, info_backup_task,
    change_passphrase_task, export_tar_task, with_lock_task,
    break_lock_task, serve_task, config_task
)

# Carregar variáveis de ambiente do arquivo .env
load_dotenv()

API_KEY = os.getenv("API_KEY")
API_KEY_NAME = "access_token"

# Função para validar a API key
def validate_api_key(api_key: str = Security(APIKeyHeader(name=API_KEY_NAME, auto_error=True))) -> str: a
    if api_key != API_KEY:
        raise HTTPException(
            status_code=403,
            detail="Could not validate credentials"
        )
    return api_key

app = FastAPI()

class InitBackupModel(BaseModel):
    repository: str
    options: Optional[Dict[str, str]] = None

class CreateBackupModel(BaseModel):
    archive: str
    paths: List[str]
    options: Optional[Dict[str, str]] = None

class ExtractBackupModel(BaseModel):
    archive: str
    paths: Optional[List[str]] = None
    options: Optional[Dict[str, str]] = None

class CheckBackupModel(BaseModel):
    repository_or_archive: str
    options: Optional[Dict[str, str]] = None

class RenameBackupModel(BaseModel):
    archive: str
    newname: str
    options: Optional[Dict[str, str]] = None

class ListBackupModel(BaseModel):
    repository_or_archive: str
    paths: Optional[List[str]] = None
    options: Optional[Dict[str, str]] = None

class DiffBackupModel(BaseModel):
    repo_archive: str
    archive: str
    paths: Optional[List[str]] = None
    options: Optional[Dict[str, str]] = None

class DeleteBackupModel(BaseModel):
    repository_or_archive: str
    archives: Optional[List[str]] = None
    options: Optional[Dict[str, str]] = None

class PruneBackupModel(BaseModel):
    repository: str
    options: Optional[Dict[str, str]] = None

class CompactBackupModel(BaseModel):
    repository: str
    options: Optional[Dict[str, str]] = None

class RecreateBackupModel(BaseModel):
    archive: str
    options: Optional[Dict[str, str]] = None

class InfoBackupModel(BaseModel):
    repository_or_archive: str
    options: Optional[Dict[str, str]] = None

class ChangePassphraseModel(BaseModel):
    repository: str
    options: Optional[Dict[str, str]] = None

class ExportTarModel(BaseModel):
    archive: str
    file: str
    paths: Optional[List[str]] = None
    options: Optional[Dict[str, str]] = None

class WithLockModel(BaseModel):
    repository: str
    command: str
    args: Optional[List[Union[str, int]]] = None
    options: Optional[Dict[str, str]] = None

class BreakLockModel(BaseModel):
    repository: str
    options: Optional[Dict[str, str]] = None

class ServeBackupModel(BaseModel):
    options: Optional[Dict[str, str]] = None

class ConfigBackupModel(BaseModel):
    repository: str
    changes: Optional[List[Union[str, Tuple[str, str]]]] = None
    options: Optional[Dict[str, str]] = None

CommonsDep = Annotated[str, Depends(validate_api_key)]

@app.post("/init")
async def init_backup(
    backup: InitBackupModel, 
    commons: CommonsDep
):
    """
    Inicializa um repositório.
    """
    try:
        task = init_backup_task.apply_async(args=[backup.repository, backup.options or {}])
        return {"task_id": task.id, "status": "Task started"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/create")
async def create_backup(
    backup: CreateBackupModel, 
    commons: CommonsDep
):
    """
    Cria um novo arquivo de backup.
    """
    try:
        task = create_backup_task.apply_async(args=[backup.archive, backup.paths, backup.options or {}])
        return {"task_id": task.id, "status": "Task started"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/extract")
async def extract_backup(
    backup: ExtractBackupModel, 
    commons: CommonsDep
):
    """
    Extrai arquivos de um backup.
    """
    try:
        task = extract_backup_task.apply_async(args=[backup.archive, backup.paths or [], backup.options or {}])
        return {"task_id": task.id, "status": "Task started"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/check")
async def check_backup(
    backup: CheckBackupModel, 
    commons: CommonsDep
):
    """
    Verifica a consistência de um repositório ou arquivo.
    """
    try:
        task = check_backup_task.apply_async(args=[backup.repository_or_archive, backup.options or {}])
        return {"task_id": task.id, "status": "Task started"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/rename")
async def rename_backup(
    backup: RenameBackupModel, 
    commons: CommonsDep
):
    """
    Renomeia um arquivo de backup.
    """
    try:
        task = rename_backup_task.apply_async(args=[backup.archive, backup.newname, backup.options or {}])
        return {"task_id": task.id, "status": "Task started"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/list")
async def list_backup(
    backup: ListBackupModel, 
    commons: CommonsDep
):
    """
    Lista o conteúdo de um repositório ou arquivo.
    """
    try:
        task = list_backup_task.apply_async(args=[backup.repository_or_archive, backup.paths or [], backup.options or {}])
        return {"task_id": task.id, "status": "Task started"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/diff")
async def diff_backup(
    backup: DiffBackupModel, 
    commons: CommonsDep
):
    """
    Mostra as diferenças entre dois arquivos de backup.
    """
    try:
        task = diff_backup_task.apply_async(args=[backup.repo_archive, backup.archive, backup.paths or [], backup.options or {}])
        return {"task_id": task.id, "status": "Task started"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/delete")
async def delete_backup(
    backup: DeleteBackupModel, 
    commons: CommonsDep
):
    """
    Exclui um arquivo ou repositório de backup.
    """
    try:
        task = delete_backup_task.apply_async(args=[backup.repository_or_archive, backup.archives or [], backup.options or {}])
        return {"task_id": task.id, "status": "Task started"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/prune")
async def prune_backup(
    backup: PruneBackupModel, 
    commons: CommonsDep
):
    """
    Prune arquivos em um repositório.
    """
    try:
        task = prune_backup_task.apply_async(args=[backup.repository, backup.options or {}])
        return {"task_id": task.id, "status": "Task started"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/compact")
async def compact_backup(
    backup: CompactBackupModel, 
    commons: CommonsDep
):
    """
    Compacta segmentos em um repositório.
    """
    try:
        task = compact_backup_task.apply_async(args=[backup.repository, backup.options or {}])
        return {"task_id": task.id, "status": "Task started"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/recreate")
async def recreate_backup(
    backup: RecreateBackupModel, 
    commons: CommonsDep
):
    """
    Modifica arquivos existentes em um repositório.
    """
    try:
        task = recreate_backup_task.apply_async(args=[backup.archive, backup.options or {}])
        return {"task_id": task.id, "status": "Task started"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/info")
async def info_backup(
    backup: InfoBackupModel, 
    commons: CommonsDep
):
    """
    Mostra informações detalhadas sobre um repositório ou arquivo.
    """
    try:
        task = info_backup_task.apply_async(args=[backup.repository_or_archive, backup.options or {}])
        return {"task_id": task.id, "status": "Task started"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/change-passphrase")
async def change_passphrase(
    backup: ChangePassphraseModel, 
    commons: CommonsDep
):
    """
    Altera a senha de um repositório.
    """
    try:
        task = change_passphrase_task.apply_async(args=[backup.repository, backup.options or {}])
        return {"task_id": task.id, "status": "Task started"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/export-tar")
async def export_tar(
    backup: ExportTarModel, 
    commons: CommonsDep
):
    """
    Exporta um arquivo de backup como um tarball.
    """
    try:
        task = export_tar_task.apply_async(args=[backup.archive, backup.file, backup.paths or [], backup.options or {}])
        return {"task_id": task.id, "status": "Task started"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/with-lock")
async def with_lock(
    backup: WithLockModel, 
    commons: CommonsDep
):
    """
    Executa um comando enquanto mantém um bloqueio no repositório.
    """
    try:
        task = with_lock_task.apply_async(args=[backup.repository, backup.command, backup.args or [], backup.options or {}])
        return {"task_id": task.id, "status": "Task started"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/break-lock")
async def break_lock(
    backup: BreakLockModel, 
    commons: CommonsDep
):
    """
    Força a remoção de um bloqueio no repositório.
    """
    try:
        task = break_lock_task.apply_async(args=[backup.repository, backup.options or {}])
        return {"task_id": task.id, "status": "Task started"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/serve")
async def serve_backup(
    backup: ServeBackupModel, 
    commons: CommonsDep
):
    """
    Inicia um servidor de repositório.
    """
    try:
        task = serve_task.apply_async(args=[backup.options or {}])
        return {"task_id": task.id, "status": "Task started"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/config")
async def config_backup(
    backup: ConfigBackupModel, 
    commons: CommonsDep
):
    """
    Altera a configuração de um repositório.
    """
    try:
        task = config_task.apply_async(args=[backup.repository, backup.changes or [], backup.options or {}])
        return {"task_id": task.id, "status": "Task started"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/tasks/{task_id}")
async def get_task_status(task_id: str):
    task = celery_app.AsyncResult(task_id)
    if task.state == 'PENDING':
        response = {
            'state': task.state,
            'status': 'Pending...'
        }
    elif task.state != 'FAILURE':
        response = {
            'state': task.state,
            'result': task.result
        }
        if task.state == 'SUCCESS':
            response['status'] = 'Task completed'
    else:
        response = {
            'state': task.state,
            'status': str(task.info),  # This is the exception raised
        }
    return response

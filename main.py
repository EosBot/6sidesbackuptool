import os
from dotenv import load_dotenv
from borgapi import BorgAPI
from fastapi import Depends, FastAPI, HTTPException, Security
from fastapi.security import APIKeyHeader
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Annotated, Union, Tuple, List, Dict, Optional


load_dotenv()

API_KEY = os.getenv("API_KEY")
API_KEY_NAME = os.getenv("API_KEY_NAME")

async def APIKeyValidator(api_key: str = Security(APIKeyHeader(name=API_KEY_NAME, auto_error=True))):
    if api_key != API_KEY:
        raise HTTPException(status_code=403,detail="Could not validate credentials")
    return api_key

app = FastAPI()

origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


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


@app.post("/init")
async def init_backup(backup: InitBackupModel, commons: Annotated[str, Depends(APIKeyValidator)]):
    """
    Inicializa um repositório.
    """
    try:
        api = BorgAPI(defaults={}, options={})
        result = api.init(backup.repository, **(backup.options or {}))
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/create")
async def create_backup(backup: CreateBackupModel, commons: Annotated[str, Depends(APIKeyValidator)]):
    """
    Cria um novo arquivo de backup.
    """
    try:
        api = BorgAPI(defaults={}, options={})
        result = api.create(backup.archive, *backup.paths, **(backup.options or {}))
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/extract")
async def extract_backup(backup: ExtractBackupModel, commons: Annotated[str, Depends(APIKeyValidator)]):
    """
    Extrai arquivos de um backup.
    """
    try:
        api = BorgAPI(defaults={}, options={})
        result = api.extract(backup.archive, *(backup.paths or []), **(backup.options or {}))
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/check")
async def check_backup(backup: CheckBackupModel, commons: Annotated[str, Depends(APIKeyValidator)]):
    """
    Verifica a consistência de um repositório ou arquivo.
    """
    try:
        api = BorgAPI(defaults={}, options={})
        result = api.check(backup.repository_or_archive, **(backup.options or {}))
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/rename")
async def rename_backup(backup: RenameBackupModel, commons: Annotated[str, Depends(APIKeyValidator)]):
    """
    Renomeia um arquivo de backup.
    """
    try:
        api = BorgAPI(defaults={}, options={})
        result = api.rename(backup.archive, backup.newname, **(backup.options or {}))
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/list")
async def list_backup(backup: ListBackupModel, commons: Annotated[str, Depends(APIKeyValidator)]):
    """
    Lista o conteúdo de um repositório ou arquivo.
    """
    try:
        api = BorgAPI(defaults={}, options={})
        result = api.list(backup.repository_or_archive, *(backup.paths or []), **(backup.options or {}))
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/diff")
async def diff_backup(backup: DiffBackupModel, commons: Annotated[str, Depends(APIKeyValidator)]):
    """
    Mostra as diferenças entre dois arquivos de backup.
    """
    try:
        api = BorgAPI(defaults={}, options={})
        result = api.diff(backup.repo_archive, backup.archive, *(backup.paths or []), **(backup.options or {}))
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/delete")
async def delete_backup(backup: DeleteBackupModel, commons: Annotated[str, Depends(APIKeyValidator)]):
    """
    Exclui um arquivo ou repositório de backup.
    """
    try:
        api = BorgAPI(defaults={}, options={})
        result = api.delete(backup.repository_or_archive, *(backup.archives or []), **(backup.options or {}))
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/prune")
async def prune_backup(backup: PruneBackupModel, commons: Annotated[str, Depends(APIKeyValidator)]):
    """
    Prune arquivos em um repositório.
    """
    try:
        api = BorgAPI(defaults={}, options={})
        result = api.prune(backup.repository, **(backup.options or {}))
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/compact")
async def compact_backup(backup: CompactBackupModel, commons: Annotated[str, Depends(APIKeyValidator)]):
    """
    Compacta segmentos em um repositório.
    """
    try:
        api = BorgAPI(defaults={}, options={})
        result = api.compact(backup.repository, **(backup.options or {}))
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/recreate")
async def recreate_backup(backup: RecreateBackupModel, commons: Annotated[str, Depends(APIKeyValidator)]):
    """
    Modifica arquivos existentes em um repositório.
    """
    try:
        api = BorgAPI(defaults={}, options={})
        result = api.recreate(backup.archive, **(backup.options or {}))
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/info")
async def info_backup(backup: InfoBackupModel, commons: Annotated[str, Depends(APIKeyValidator)]):
    """
    Mostra informações detalhadas sobre um repositório ou arquivo.
    """
    try:
        api = BorgAPI(defaults={}, options={})
        result = api.info(backup.repository_or_archive, **(backup.options or {}))
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/change-passphrase")
async def change_passphrase(backup: ChangePassphraseModel, commons: Annotated[str, Depends(APIKeyValidator)]):
    """
    Altera a senha de um repositório.
    """
    try:
        api = BorgAPI(defaults={}, options={})
        result = api.key_change_passphrase(backup.repository, **(backup.options or {}))
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/export-tar")
async def export_tar(backup: ExportTarModel, commons: Annotated[str, Depends(APIKeyValidator)]):
    """
    Exporta um arquivo de backup como um tarball.
    """
    try:
        api = BorgAPI(defaults={}, options={})
        result = api.export_tar(backup.archive, backup.file, *(backup.paths or []), **(backup.options or {}))
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/with-lock")
async def with_lock(backup: WithLockModel, commons: Annotated[str, Depends(APIKeyValidator)]):
    """
    Executa um comando enquanto mantém um bloqueio no repositório.
    """
    try:
        api = BorgAPI(defaults={}, options={})
        result = api.with_lock(backup.repository, backup.command, *(backup.args or []), **(backup.options or {}))
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/break-lock")
async def break_lock(backup: BreakLockModel, commons: Annotated[str, Depends(APIKeyValidator)]):
    """
    Força a remoção de um bloqueio no repositório.
    """
    try:
        api = BorgAPI(defaults={}, options={})
        result = api.break_lock(backup.repository, **(backup.options or {}))
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/serve")
async def serve_backup(backup: ServeBackupModel, commons: Annotated[str, Depends(APIKeyValidator)]):
    """
    Inicia um servidor de repositório.
    """
    try:
        api = BorgAPI(defaults={}, options={})
        result = api.serve(**(backup.options or {}))
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/config")
async def config_backup(backup: ConfigBackupModel, commons: Annotated[str, Depends(APIKeyValidator)]):
    """
    Altera a configuração de um repositório.
    """
    try:
        api = BorgAPI(defaults={}, options={})
        result = api.config(backup.repository, *(backup.changes or []), **(backup.options or {}))
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
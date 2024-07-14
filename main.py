from .borgapi import BorgAPI
from fastapi import FastAPI
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI()


class init_bak(BaseModel):
    repository: str
    #encryption: str
    options: Optional[str] = None

class create_bak(BaseModel):
    archive: str
    paths: List[str]
    options: Optional[str] = None

class extract_bak(BaseModel):
    archive: str
    paths: Optional[str] = None
    options: Optional[str] = None

class check_bak(BaseModel):
    repository_or_archive: str
    options: Optional[str] = None

class rename_bak(BaseModel):
    archive: str
    newname: str
    options: Optional[str] = None

class list_bak(BaseModel):
    repository_or_archive: str
    paths: Optional[str] = None
    options: Optional[str] = None

class diff_bak(BaseModel):
    repo_archive: str
    archive: str
    paths: Optional[str] = None
    options: Optional[str] = None

class delete_bak(BaseModel):
    repository_or_archive: str
    archives: Optional[str] = None
    options: Optional[str] = None


@app.post("/init")
async def init_backup(backup: init_bak):
    try:
        api = BorgAPI(defaults={}, options={})
        result = api.init(backup.repository, backup.options, make_parent_dirs=True, encryption="none", json=True)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/create")
async def create_backup(backup: create_bak):
    try:
        api = BorgAPI(defaults={}, options={})
        result = api.create(backup.archive, backup.paths, backup.options, json=True)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/extract")
async def extract_backup(backup: extract_bak):
    try:
        api = BorgAPI(defaults={}, options={})
        result = api.extract(backup.archive, backup.paths, backup.options, json=True)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/check")
async def check_backup(backup: check_bak):
    try:
        api = BorgAPI(defaults={}, options={})
        result = api.check(backup.archive, backup.newname, backup.options, json=True)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/rename")
async def rename_backup(backup: rename_bak):
    try:
        api = BorgAPI(defaults={}, options={})
        result = api.rename(backup.archive, backup.options, json=True)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/list")
async def list_backup(backup: list_bak):
    try:
        api = BorgAPI(defaults={}, options={})
        result = api.list(backup.repository_or_archive, backup.paths, backup.options, json=True)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/diff")
async def diff_backup(backup: diff_bak):
    try:
        api = BorgAPI(defaults={}, options={})
        result = api.diff(backup.repo_archive, backup.archive, backup.paths, backup.options, json=True)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/delete")
async def delete_backup(backup: delete_bak):
    try:
        api = BorgAPI(defaults={}, options={})
        result = api.delete(backup.repository_or_archive, backup.archives, backup.options, json=True)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
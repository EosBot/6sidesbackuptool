from celery_config import celery_app
from borgapi import BorgAPI

@celery_app.task
def init_backup_task(repository: str, options: dict):
    api = BorgAPI(defaults={}, options={})
    return api.init(repository, **options)

@celery_app.task
def create_backup_task(archive: str, paths: list, options: dict):
    api = BorgAPI(defaults={}, options={})
    return api.create(archive, *paths, **options)

@celery_app.task
def extract_backup_task(archive: str, paths: list, options: dict):
    api = BorgAPI(defaults={}, options={})
    return api.extract(archive, *paths, **options)

@celery_app.task
def check_backup_task(repository_or_archive: str, options: dict):
    api = BorgAPI(defaults={}, options={})
    return api.check(repository_or_archive, **options)

@celery_app.task
def rename_backup_task(archive: str, newname: str, options: dict):
    api = BorgAPI(defaults={}, options={})
    return api.rename(archive, newname, **options)

@celery_app.task
def list_backup_task(repository_or_archive: str, paths: list, options: dict):
    api = BorgAPI(defaults={}, options={})
    return api.list(repository_or_archive, *paths, **options)

@celery_app.task
def diff_backup_task(repo_archive: str, archive: str, paths: list, options: dict):
    api = BorgAPI(defaults={}, options={})
    return api.diff(repo_archive, archive, *paths, **options)

@celery_app.task
def delete_backup_task(repository_or_archive: str, archives: list, options: dict):
    api = BorgAPI(defaults={}, options={})
    return api.delete(repository_or_archive, *archives, **options)

@celery_app.task
def prune_backup_task(repository: str, options: dict):
    api = BorgAPI(defaults={}, options={})
    return api.prune(repository, **options)

@celery_app.task
def compact_backup_task(repository: str, options: dict):
    api = BorgAPI(defaults={}, options={})
    return api.compact(repository, **options)

@celery_app.task
def recreate_backup_task(archive: str, options: dict):
    api = BorgAPI(defaults={}, options={})
    return api.recreate(archive, **options)

@celery_app.task
def info_backup_task(repository_or_archive: str, options: dict):
    api = BorgAPI(defaults={}, options={})
    return api.info(repository_or_archive, **options)

@celery_app.task
def change_passphrase_task(repository: str, options: dict):
    api = BorgAPI(defaults={}, options={})
    return api.key_change_passphrase(repository, **options)

@celery_app.task
def export_tar_task(archive: str, file: str, paths: list, options: dict):
    api = BorgAPI(defaults={}, options={})
    return api.export_tar(archive, file, *paths, **options)

@celery_app.task
def with_lock_task(repository: str, command: str, args: list, options: dict):
    api = BorgAPI(defaults={}, options={})
    return api.with_lock(repository, command, *args, **options)

@celery_app.task
def break_lock_task(repository: str, options: dict):
    api = BorgAPI(defaults={}, options={})
    return api.break_lock(repository, **options)

@celery_app.task
def serve_task(options: dict):
    api = BorgAPI(defaults={}, options={})
    return api.serve(**options)

@celery_app.task
def config_task(repository: str, changes: list, options: dict):
    api = BorgAPI(defaults={}, options={})
    return api.config(repository, *changes, **options)

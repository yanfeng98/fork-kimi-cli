from __future__ import annotations

import json
from hashlib import md5
from pathlib import Path

from kaos import get_current_kaos
from kaos.local import local_kaos
from kaos.path import KaosPath
from pydantic import BaseModel, Field

from kimi_cli.share import get_share_dir
from kimi_cli.utils.logging import logger


def get_metadata_file() -> Path:
    return get_share_dir() / "kimi.json"


class WorkDirMeta(BaseModel):
    path: str
    kaos: str = local_kaos.name
    last_session_id: str | None = None

    @property
    def sessions_dir(self) -> Path:
        path_md5: str = md5(self.path.encode(encoding="utf-8")).hexdigest()
        dir_basename: str = path_md5 if self.kaos == local_kaos.name else f"{self.kaos}_{path_md5}"
        session_dir: Path = get_share_dir() / "sessions" / dir_basename
        session_dir.mkdir(parents=True, exist_ok=True)
        return session_dir


class Metadata(BaseModel):
    work_dirs: list[WorkDirMeta] = Field(default_factory=list[WorkDirMeta])
    thinking: bool = False

    def get_work_dir_meta(self, path: KaosPath) -> WorkDirMeta | None:
        for wd in self.work_dirs:
            if wd.path == str(path) and wd.kaos == get_current_kaos().name:
                return wd
        return None

    def new_work_dir_meta(self, path: KaosPath) -> WorkDirMeta:
        wd_meta: WorkDirMeta = WorkDirMeta(path=str(path), kaos=get_current_kaos().name)
        self.work_dirs.append(wd_meta)
        return wd_meta


def load_metadata() -> Metadata:
    metadata_file: Path = get_metadata_file()
    logger.debug("Loading metadata from file: {file}", file=metadata_file)
    if not metadata_file.exists():
        logger.debug("No metadata file found, creating empty metadata")
        return Metadata()
    with open(metadata_file, encoding="utf-8") as f:
        data = json.load(f)
        return Metadata(**data)


def save_metadata(metadata: Metadata):
    metadata_file = get_metadata_file()
    logger.debug("Saving metadata to file: {file}", file=metadata_file)
    with open(metadata_file, "w", encoding="utf-8") as f:
        json.dump(metadata.model_dump(), f, indent=2, ensure_ascii=False)

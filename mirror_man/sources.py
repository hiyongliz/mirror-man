from __future__ import annotations

import logging
import shutil
import subprocess
from datetime import datetime
from pathlib import Path

logger = logging.getLogger(__name__)


def backup_file(file_path: str) -> str:
    """Backup a file with a timestamped suffix. Returns the backup path."""
    backup_path = f"{file_path}.{datetime.now().strftime('%Y%m%d%H%M%S')}.bak"
    shutil.copy(file_path, backup_path)
    logger.info("Backup created at %s", backup_path)
    return backup_path


def set_apt_sources(source: str, file_path: str = "/etc/apt/sources.list") -> None:
    """Backup and overwrite APT sources list."""
    backup_file(file_path)
    Path(file_path).write_text(source, encoding="utf-8")
    logger.info("APT sources updated: %s", file_path)


def set_yum_repos(base_repo_url: str, epel_repo_url: str) -> None:
    """Backup and replace YUM repository files."""
    base_repo_path = "/etc/yum.repos.d/CentOS-Base.repo"
    epel_repo_path = "/etc/yum.repos.d/epel.repo"

    if Path(base_repo_path).exists():
        backup_file(base_repo_path)
    if Path(epel_repo_path).exists():
        backup_file(epel_repo_path)

    subprocess.run(
        ["curl", "-fsSL", "-o", base_repo_path, base_repo_url], check=True
    )
    subprocess.run(
        ["curl", "-fsSL", "-o", epel_repo_path, epel_repo_url], check=True
    )

    subprocess.run(
        [
            "sed", "-i",
            "-e", "/mirrors.cloud.aliyuncs.com/d",
            "-e", "/mirrors.aliyuncs.com/d",
            base_repo_path,
        ],
        check=False,
    )

    subprocess.run(["yum", "clean", "all"], check=True)
    subprocess.run(["yum", "makecache"], check=True)
    logger.info("YUM repositories updated")

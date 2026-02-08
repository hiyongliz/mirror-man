from __future__ import annotations

from pathlib import Path
from unittest.mock import patch

from mirror_man.sources import backup_file, set_apt_sources


class TestBackupFile:
    def test_creates_backup(self, tmp_path: Path) -> None:
        src = tmp_path / "sources.list"
        src.write_text("original content")
        backup_path = backup_file(str(src))
        assert Path(backup_path).exists()
        assert Path(backup_path).read_text() == "original content"
        assert backup_path.endswith(".bak")

    def test_preserves_original(self, tmp_path: Path) -> None:
        src = tmp_path / "sources.list"
        src.write_text("original content")
        backup_file(str(src))
        assert src.read_text() == "original content"

    def test_missing_file_raises(self, tmp_path: Path) -> None:
        missing = tmp_path / "nonexistent"
        try:
            backup_file(str(missing))
            assert False, "Should have raised FileNotFoundError"
        except FileNotFoundError:
            pass


class TestSetAptSources:
    def test_writes_source_content(self, tmp_path: Path) -> None:
        src = tmp_path / "sources.list"
        src.write_text("old content")
        new_content = "deb https://mirrors.aliyun.com/ubuntu/ jammy main"
        set_apt_sources(new_content, file_path=str(src))
        assert src.read_text() == new_content

    def test_creates_backup_before_write(self, tmp_path: Path) -> None:
        src = tmp_path / "sources.list"
        src.write_text("old content")
        with patch("mirror_man.sources.backup_file") as mock_backup:
            set_apt_sources("new content", file_path=str(src))
            mock_backup.assert_called_once_with(str(src))

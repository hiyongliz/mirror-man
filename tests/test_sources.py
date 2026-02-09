from __future__ import annotations

from pathlib import Path
from unittest.mock import call, patch

from mirror_man.sources import backup_file, set_apt_sources, set_yum_repos


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


class TestSetYumRepos:
    @patch("mirror_man.sources.subprocess.run")
    @patch("mirror_man.sources.backup_file")
    @patch("mirror_man.sources.Path")
    def test_backs_up_existing_files(
        self, mock_path_cls: patch, mock_backup: patch, mock_run: patch
    ) -> None:
        mock_path_cls.return_value.exists.return_value = True
        set_yum_repos("http://base.url", "http://epel.url")
        assert mock_backup.call_count == 2

    @patch("mirror_man.sources.subprocess.run")
    @patch("mirror_man.sources.backup_file")
    @patch("mirror_man.sources.Path")
    def test_skips_backup_when_files_missing(
        self, mock_path_cls: patch, mock_backup: patch, mock_run: patch
    ) -> None:
        mock_path_cls.return_value.exists.return_value = False
        set_yum_repos("http://base.url", "http://epel.url")
        mock_backup.assert_not_called()

    @patch("mirror_man.sources.subprocess.run")
    @patch("mirror_man.sources.backup_file")
    @patch("mirror_man.sources.Path")
    def test_calls_curl_sed_yum(
        self, mock_path_cls: patch, mock_backup: patch, mock_run: patch
    ) -> None:
        mock_path_cls.return_value.exists.return_value = False
        set_yum_repos("http://base.url", "http://epel.url")
        run_calls = mock_run.call_args_list
        assert run_calls[0] == call(
            ["curl", "-fsSL", "-o", "/etc/yum.repos.d/CentOS-Base.repo", "http://base.url"],
            check=True,
        )
        assert run_calls[1] == call(
            ["curl", "-fsSL", "-o", "/etc/yum.repos.d/epel.repo", "http://epel.url"],
            check=True,
        )
        assert run_calls[2].args[0][0] == "sed"
        assert run_calls[3] == call(["yum", "clean", "all"], check=True)
        assert run_calls[4] == call(["yum", "makecache"], check=True)

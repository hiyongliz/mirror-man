from __future__ import annotations

from unittest.mock import patch

from typer.testing import CliRunner

from mirror_man.cli import app
from mirror_man.os_info import OSInfo

runner = CliRunner()


class TestVersion:
    def test_version_flag(self) -> None:
        result = runner.invoke(app, ["--version"])
        assert result.exit_code == 0
        assert "mirror-man version:" in result.output


class TestAliyun:
    def test_ubuntu_supported(self) -> None:
        fake_os = OSInfo(id="ubuntu", version_id="22.04", pretty_name="Ubuntu 22.04.3 LTS")
        with (
            patch("mirror_man.cli.detect_os", return_value=fake_os),
            patch("mirror_man.cli.set_apt_sources") as mock_set,
        ):
            result = runner.invoke(app, ["aliyun"])
            assert result.exit_code == 0
            assert "Successfully switched" in result.output
            mock_set.assert_called_once()

    def test_ubuntu_unsupported_version(self) -> None:
        fake_os = OSInfo(id="ubuntu", version_id="18.04", pretty_name="Ubuntu 18.04 LTS")
        with patch("mirror_man.cli.detect_os", return_value=fake_os):
            result = runner.invoke(app, ["aliyun"])
            assert result.exit_code == 1
            assert "not found" in result.output

    def test_centos_supported(self) -> None:
        fake_os = OSInfo(id="centos", version_id="7", pretty_name="CentOS Linux 7")
        with (
            patch("mirror_man.cli.detect_os", return_value=fake_os),
            patch("mirror_man.cli.set_yum_repos") as mock_set,
        ):
            result = runner.invoke(app, ["aliyun"])
            assert result.exit_code == 0
            assert "Successfully switched" in result.output
            mock_set.assert_called_once()

    def test_centos_unsupported_version(self) -> None:
        fake_os = OSInfo(id="centos", version_id="6", pretty_name="CentOS Linux 6")
        with patch("mirror_man.cli.detect_os", return_value=fake_os):
            result = runner.invoke(app, ["aliyun"])
            assert result.exit_code == 1
            assert "not found" in result.output

    def test_unsupported_os(self) -> None:
        fake_os = OSInfo(id="arch", version_id="rolling", pretty_name="Arch Linux")
        with patch("mirror_man.cli.detect_os", return_value=fake_os):
            result = runner.invoke(app, ["aliyun"])
            assert result.exit_code == 1
            assert "Unsupported" in result.output

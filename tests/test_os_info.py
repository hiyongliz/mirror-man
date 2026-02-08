from __future__ import annotations

from pathlib import Path

from mirror_man.os_info import OSInfo, detect_os


class TestOSInfo:
    def test_mirror_key_ubuntu(self) -> None:
        info = OSInfo(id="ubuntu", version_id="22.04", pretty_name="Ubuntu 22.04.3 LTS")
        assert info.mirror_key == "ubuntu_2204"

    def test_mirror_key_ubuntu_2404(self) -> None:
        info = OSInfo(id="ubuntu", version_id="24.04", pretty_name="Ubuntu 24.04 LTS")
        assert info.mirror_key == "ubuntu_2404"

    def test_mirror_key_centos(self) -> None:
        info = OSInfo(id="centos", version_id="7", pretty_name="CentOS Linux 7")
        assert info.mirror_key == "centos_7"

    def test_mirror_key_unknown(self) -> None:
        info = OSInfo(id="unknown", version_id="", pretty_name="Unknown OS")
        assert info.mirror_key == "unknown_"

    def test_frozen(self) -> None:
        info = OSInfo(id="ubuntu", version_id="22.04", pretty_name="Ubuntu 22.04")
        try:
            info.id = "centos"  # type: ignore[misc]
            assert False, "Should have raised FrozenInstanceError"
        except AttributeError:
            pass


class TestDetectOS:
    def test_ubuntu(self, tmp_path: Path) -> None:
        os_release = tmp_path / "os-release"
        os_release.write_text(
            'PRETTY_NAME="Ubuntu 22.04.3 LTS"\n'
            "NAME=Ubuntu\n"
            'VERSION_ID="22.04"\n'
            "ID=ubuntu\n"
        )
        info = detect_os(os_release)
        assert info.id == "ubuntu"
        assert info.version_id == "22.04"
        assert info.pretty_name == "Ubuntu 22.04.3 LTS"
        assert info.mirror_key == "ubuntu_2204"

    def test_centos(self, tmp_path: Path) -> None:
        os_release = tmp_path / "os-release"
        os_release.write_text(
            'PRETTY_NAME="CentOS Linux 7 (Core)"\n'
            "NAME=CentOS Linux\n"
            'VERSION_ID="7"\n'
            "ID=centos\n"
        )
        info = detect_os(os_release)
        assert info.id == "centos"
        assert info.version_id == "7"
        assert info.mirror_key == "centos_7"

    def test_file_not_found(self, tmp_path: Path) -> None:
        missing = tmp_path / "nonexistent"
        info = detect_os(missing)
        assert info.id == "unknown"
        assert info.version_id == ""
        assert info.pretty_name == "Unknown OS"

    def test_missing_fields(self, tmp_path: Path) -> None:
        os_release = tmp_path / "os-release"
        os_release.write_text("NAME=SomeOS\n")
        info = detect_os(os_release)
        assert info.id == "unknown"
        assert info.version_id == ""
        assert info.pretty_name == "Unknown OS"

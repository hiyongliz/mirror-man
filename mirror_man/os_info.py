from __future__ import annotations

import logging
from dataclasses import dataclass
from pathlib import Path

logger = logging.getLogger(__name__)

OS_RELEASE_PATH = Path("/etc/os-release")


@dataclass(frozen=True)
class OSInfo:
    id: str
    version_id: str
    pretty_name: str

    @property
    def mirror_key(self) -> str:
        """Generate a normalized key for mirror data lookup.

        Examples: 'ubuntu_2204', 'centos_7'
        """
        normalized_version = self.version_id.replace(".", "")
        return f"{self.id}_{normalized_version}"


def detect_os(os_release_path: Path = OS_RELEASE_PATH) -> OSInfo:
    """Parse /etc/os-release to detect the current OS."""
    fields: dict[str, str] = {}
    try:
        text = os_release_path.read_text(encoding="utf-8")
        for line in text.splitlines():
            if "=" in line:
                key, _, value = line.partition("=")
                fields[key.strip()] = value.strip().strip('"')
    except FileNotFoundError:
        logger.warning("File not found: %s", os_release_path)

    return OSInfo(
        id=fields.get("ID", "unknown"),
        version_id=fields.get("VERSION_ID", ""),
        pretty_name=fields.get("PRETTY_NAME", "Unknown OS"),
    )

import typer
import shutil
from datetime import datetime
from mirror_data import apt_sources


app = typer.Typer()
__VERSION__ = "0.1.0"


def version_callback(value: bool):
    if value:
        typer.echo(__VERSION__)


def get_os():
    """Get the current operating system."""
    with open("/etc/os-release") as f:
        os_info = f.read()
    for line in os_info.splitlines():
        if line.startswith("PRETTY_NAME="):
            return line.split("=")[1].strip('"')


def backup(file_path: str):
    """Backup the current apt sources."""
    backup_path = f"{file_path}.{datetime.now().strftime('%Y%m%d%H%M%S')}.bak"
    shutil.copy(file_path, backup_path)
    print(f"Backup created at {backup_path}")


def set_apt_sources(source: str):
    """Set the apt sources to the specified source."""
    file_path = "/etc/apt/sources.list"
    backup(file_path)
    with open(file_path, "w") as f:
        f.write(source)


@app.command()
def aliyun():
    # TODO: Implement Aliyun functionality
    os = get_os()
    if os.startswith("Ubuntu"):
        set_apt_sources(apt_sources[os.lower().replace(" ", "_").replace(".", "")[:11]])


@app.command()
def huaweiyun():
    # TODO: Implement Huawei Cloud functionality
    print("Huawei Cloud functionality is not yet implemented.")


def main():
    print("Hello from mirror-man!")


if __name__ == "__main__":
    app()

# Mirror Man

Mirror Man is a command-line tool to manage software mirror sources for your Linux distribution. It simplifies the process of switching between different mirror sources, helping you to get faster package downloads.

## Features

*   Backup your current mirror sources before making changes.
*   Switch to Aliyun mirror sources for Ubuntu and CentOS.
*   Planned support for Huawei Cloud and other mirror sources.
*   Dynamic versioning for easier maintenance.
*   Uses `uv` for faster builds and dependency management.

## Installation

### Using pip

```bash
pip install mirror-man
```

### Using uv (Recommended)

```bash
uv pip install mirror-man
```

### Development Installation

To install the package in development mode using `uv`:

```bash
uv pip install -e .
```

## Usage

To switch to the Aliyun mirror source, run the following command:

```bash
mirror-man aliyun
```

This will automatically detect your operating system and configure the appropriate Aliyun mirror source. Your existing sources file will be backed up with a timestamp.

### Version

To check the version of `mirror-man`:

```bash
mirror-man --version
```

### Supported Operating Systems

*   Ubuntu 22.04
*   Ubuntu 24.04
*   CentOS 7

## Development

### Using Makefile

The project includes a `Makefile` to simplify common development tasks:

*   `make clean`: Remove build artifacts.
*   `make build`: Build the package (sdist and wheel).
*   `make install`: Install the package in the current environment.
*   `make uninstall`: Uninstall the package from the current environment.
*   `make dev-install`: Install the package in editable mode for development.
*   `make publish`: Publish the package to PyPI (requires twine).

These commands use `uv` for faster builds and dependency management.

## Contributing

Contributions are welcome! Please feel free to submit a pull request or open an issue.

## License

This project is licensed under the MIT License.

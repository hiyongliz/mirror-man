# Makefile for Mirror Man

# Variables
UV := uv
BUILD_DIR := dist
SDIST := $(BUILD_DIR)/*.tar.gz
WHEEL := $(BUILD_DIR)/*.whl

# Phony targets
.PHONY: help clean build install uninstall dev-install publish

# Default target
help:
	@echo "Available targets:"
	@echo "  clean       - Remove build artifacts"
	@echo "  build       - Build the package (sdist and wheel)"
	@echo "  install     - Install the package in the current environment"
	@echo "  uninstall   - Uninstall the package from the current environment"
	@echo "  dev-install - Install the package in editable mode for development"
	@echo "  publish     - Publish the package to PyPI (requires twine)"

# Clean build artifacts
clean:
	$(UV) clean
	@echo "Build artifacts removed."

# Build the package
build: clean
	$(UV) build
	@echo "Package built successfully."

# Install the package
install: build
	$(UV) pip install $(WHEEL)
	@echo "Package installed."

# Uninstall the package
uninstall:
	$(UV) pip uninstall -y mirror-man
	@echo "Package uninstalled."

# Install in development mode
dev-install:
	$(UV) pip install -e .
	@echo "Package installed in development mode."

# Publish to PyPI
publish: build
	twine upload $(SDIST) $(WHEEL)
	@echo "Package published to PyPI."

# Publish to TestPyPI
publish-test: build
	twine upload --repository-url https://test.pypi.org/legacy/ $(SDIST) $(WHEEL)
	@echo "Package published to TestPyPI."

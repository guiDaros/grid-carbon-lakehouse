"""Grid Carbon Lakehouse: batch lakehouse for hourly grid and weather data."""

from importlib.metadata import version

# Single source of truth is `[project].version` in pyproject.toml.
__version__ = version("gridcarbon")

__all__ = ["__version__"]

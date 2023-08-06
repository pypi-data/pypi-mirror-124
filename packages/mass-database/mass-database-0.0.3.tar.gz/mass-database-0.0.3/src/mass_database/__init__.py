"""TODO DOCSTRING."""
import re
from collections import OrderedDict
from pathlib import Path

from mass_manager.mass_manager import MassManager


_BASE_DIR = Path(__file__).resolve().parent.parent.parent

MassManager.mass_dependencies = OrderedDict(
    {
        "mass_manager": "MASS-manager",
        "mass_database": "MASSdb",
        "mass": "MASSpy",
    }
)

MASSMANAGER = MassManager()
MASSMANAGER.main_directory = _BASE_DIR

__version__ = "0.0.3"

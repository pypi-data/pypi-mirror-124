import toml
from pathlib import Path
__root__ = Path(__file__).parent.parent.parent
__version__ = toml.load(__root__.joinpath('pyproject.toml'))['tool']['poetry']['version']

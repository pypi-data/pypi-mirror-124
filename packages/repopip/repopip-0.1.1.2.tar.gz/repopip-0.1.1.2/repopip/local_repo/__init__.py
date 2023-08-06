from pathlib import Path
import os

try:
    os.makedirs(Path(os.environ['HOME']).resolve().joinpath('.static', 'simple'))
except OSError:
    pass

SIMPLE_PATH = Path(os.environ['HOME']).resolve().joinpath('.static', 'simple')

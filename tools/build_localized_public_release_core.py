from pathlib import Path
import runpy
ROOT=Path(__file__).resolve().parents[1]
globals().update(runpy.run_path(str(ROOT/'tools'/'temporary.txt')))

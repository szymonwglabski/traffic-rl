from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SUMO_DIR = ROOT / "sumo"
CFG = str(SUMO_DIR / "sim.sumocfg")
ROUTES_DIR = SUMO_DIR / "routes"
MODELS_DIR = ROOT / "models"
RESULTS_DIR = ROOT / "results"
IMG_DIR = ROOT / "img"


def route(kind, seed):
    return str(ROUTES_DIR / f"routes_{kind}_{seed}.rou.xml")
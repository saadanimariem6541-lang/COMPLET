import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DB_PATH = os.path.join(
    BASE_DIR,      # backend/
    "..",          # gestion_acess_vehicules/
    "data",        # data/
    "acces.db"     # acces.db
)
from modules.db_manager import DBManager
from modules.ui_builder import GUIBuilder

db = DBManager("test.sqlite")

gui = GUIBuilder(db.select("USERS", "Username", "ACCESS_LEVEL=1"),db)
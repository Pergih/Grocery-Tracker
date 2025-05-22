# main.py
import crud

crud.create_tables()
crud.add_product("Eggs", "Dairy")
print(crud.get_all_products())

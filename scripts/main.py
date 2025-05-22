import crud

crud.create_tables()
crud.add_brands("Continente")
crud.add_canonical_product("Arroz")
print(crud.get_all_brands())

import crud
from datetime import date

crud.create_tables()
brand_id = crud.add_brand("Continente")
canonical_product_id = crud.add_canonical_product("Arroz")
product_id = crud.add_product("Arroz Carolino", brand_id, canonical_product_id, "https://www.continente.pt/produto/arroz-carolino-continente-4738050.html")
crud.add_price(product_id, 1.25, "€/kg", date.today().isoformat())

print(crud.get_all_brands())
print(crud.get_all_products())

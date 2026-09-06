from typing import Any, Dict, Iterable, List

from seeder.context import Context
from seeder.db import Table
from seeder.paths import load_resource

# keys of a product fixture that are relations, not columns of the products table
PRODUCT_RELATIONS = ("categories", "brands", "variants", "images")

# same, for one entry of "variants"
VARIANT_RELATIONS = ("pricing", "images")

# optional tables: seeded when the migration for them exists, skipped otherwise
IMAGES_TABLE = "product_images"


def columns_of(fixture: Dict[str, Any], relations: Iterable[str]) -> Dict[str, Any]:
    """The part of a fixture that maps onto table columns."""
    return {k: v for k, v in fixture.items() if k not in relations}


class ProductsSeeder:
    """resources/products.json - regenerate it with resources/gen_products.py.

    One fixture carries the product row, its category / brand links, its variants,
    the pricing of every variant and its images. Plain columns are never listed
    here: whatever the fixture holds and the table has is written (see seeder.db),
    so a new product or variant column needs no change in this file.
    """

    def name(self) -> str:
        return "products"

    def seed(self, ctx: Context):
        products = load_resource("products.json")
        cursor = ctx.cursor()

        categories = ctx.tables("categories").lookup(cursor)
        brands = ctx.tables("brands").lookup(cursor)
        if not categories:
            raise RuntimeError(f"{ctx.tables('categories')} is empty, seed categories before products")
        if not brands:
            raise RuntimeError(f"{ctx.tables('brands')} is empty, seed brands before products")

        images = ctx.tables(IMAGES_TABLE)
        counted = {"variants": 0, "prices": 0, "images": 0}

        for p in products:
            product_id = ctx.tables("products").insert(cursor, columns_of(p, PRODUCT_RELATIONS))

            self._link(cursor, ctx.tables("product_categories"), "category_id", product_id,
                       self._resolve(categories, p.get("categories", []), "category", p["title"]))
            self._link(cursor, ctx.tables("product_brands"), "brand_id", product_id,
                       self._resolve(brands, p.get("brands", []), "brand", p["title"]))

            counted["variants"] += self._variants(ctx, cursor, product_id, p.get("variants", []), counted)

            if images.exists():
                counted["images"] += images.insert_many(
                    cursor,
                    [{"product_id": product_id, **image} for image in p.get("images", [])],
                )

        ctx.commit()

        print(f"Inserted {len(products)} products, {counted['variants']} variants, "
              f"{counted['prices']} prices")
        if images.exists():
            print(f"Inserted {counted['images']} images")
        else:
            print(f"Skipped images: table {images} does not exist")

    def _variants(self, ctx: Context, cursor, product_id: int, variants: List[Dict[str, Any]],
                  counted: Dict[str, int]) -> int:
        pricing = ctx.tables("product_pricing")
        images = ctx.tables(IMAGES_TABLE)

        for v in variants:
            variant_id = ctx.tables("product_variants").insert(
                cursor,
                {"product_id": product_id, **columns_of(v, VARIANT_RELATIONS)},
            )

            if v.get("pricing"):
                pricing.insert(cursor, {"variant_id": variant_id, **v["pricing"]}, returning=None)
                counted["prices"] += 1

            if images.exists() and v.get("images"):
                counted["images"] += images.insert_many(
                    cursor,
                    [{"product_id": product_id, "variant_id": variant_id, **image} for image in v["images"]],
                )

        return len(variants)

    def _resolve(self, known: Dict[str, Any], titles: List[str], kind: str, product_title: str) -> List[Any]:
        ids = []
        for title in titles:
            if title not in known:
                raise RuntimeError(f"unknown {kind} '{title}' for product '{product_title}'")
            ids.append(known[title])
        return ids

    def _link(self, cursor, table: Table, column: str, product_id: int, ids: List[Any]):
        table.insert_many(cursor, [{"product_id": product_id, column: i} for i in ids])

    def clear(self, ctx: Context):
        cursor = ctx.cursor()
        # variants, pricing and the category / brand links go away by ON DELETE CASCADE
        ctx.tables(IMAGES_TABLE).delete_all(cursor)
        ctx.tables("products").delete_all(cursor)
        ctx.commit()

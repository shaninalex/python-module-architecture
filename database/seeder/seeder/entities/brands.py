from seeder.context import Context
from seeder.paths import load_resource


class BrandsSeeder:
    """resources/brands.json holds one object per brand.

    Columns the brands table does not have yet (a logo, a slug) are ignored, so the
    fixture can run ahead of the migration.
    """

    def name(self) -> str:
        return "brands"

    def seed(self, ctx: Context):
        brands = load_resource("brands.json")
        cursor = ctx.cursor()
        inserted = ctx.tables("brands").insert_many(cursor, brands)
        ctx.commit()
        print(f"Inserted {inserted} brands")

    def clear(self, ctx: Context):
        cursor = ctx.cursor()
        ctx.tables("brands").delete_all(cursor)
        ctx.commit()

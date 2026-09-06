# Seeder

Fills the database with mock shoes: categories, brands, products, variants and prices.

```bash
# from the repository root
uv sync --all-packages

# re-roll the fixtures (optional, products.json is committed)
uv run --package seeder python database/seeder/resources/gen_products.py

# wipe the catalog data and seed it again
uv run --package seeder python -m seeder \
    --config ./database/seeder/config.yaml \
    start
```

`config.yaml` holds the connection and the schema the tables live in (`public` here).

## Layout

```
resources/            fixtures - plain JSON, no code
  brands.json         [{ "title": ... }]
  categories.json     [{ "title": ..., "children": [...] }]
  attributes.json     value pools used by the generator only
  products.json       generated, see gen_products.py
  gen_products.py     regenerates products.json with faker
seeder/
  db.py               Table / Tables - the schema aware insert helpers
  entities/           one seeder per aggregate: brands, categories, products
  seeder.py           registry + executor (clear in reverse, then seed)
```

## Adding a field

Inserts never name their columns. `Table.insert` takes a dict and drops the keys the
table has no column for, so:

1. add the key to the fixture (`resources/*.json`, or to `gen_products.py`),
2. add the column in a migration.

The seeder picks it up on the next run - no change in `seeder/entities/`. Until the
migration lands, the extra key is simply ignored, so the fixture may run ahead of the
schema.

Keys that are *not* columns are relations, and those are listed in
`seeder/entities/products.py`:

* `PRODUCT_RELATIONS` - `categories`, `brands`, `variants`, `images`
* `VARIANT_RELATIONS` - `pricing`, `images`

A variant's `pricing` object is spread into the `product_pricing` row, so a second
price column (`special_price`, `cost`) only needs the key and the migration.

## Images

`gen_products.py` already writes an `images` list for every product:

```json
{ "path": "/images/products/atlas-oxford-pro-1.jpg", "position": 1, "role": "main" }
```

There is no table for them yet. Create `product_images` with the columns you want -
`product_id`, optional `variant_id`, and any of `path` / `position` / `role` - and the
products seeder starts filling it on the next run. Without that table it prints
`Skipped images: table public.product_images does not exist` and carries on.
The same holds for a variant level gallery: fill `variants[].images` in the generator.

## Notes

* product titles never contain the brand - the brand is a `product_brands` link;
* `products.title`, `product_variants.sku` and `barcode` are UNIQUE, the generator
  keeps them unique across a run;
* the generator is seeded (`SEED` in `gen_products.py`), so the same fixtures come out
  every time - bump it to get a different catalog.

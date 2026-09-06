"""Generate the products / product_variants fixtures for the shoe store.

Run it to re-roll products.json:  python3 database/seeder/resources/gen_products.py

Output shape (see seeder/entities/products.py for how it is consumed):
    title, categories[] (categories.title), brands[] (brands.title),
    short_description, description, images[], variants[{title, description, sku,
    barcode, pricing{}, images[]}]

Two rules worth keeping in mind while editing this file:

* the product title never contains the brand - the brand lives in the
  product_brands link only;
* anything added to a fixture that is not a relation is treated as a column, so
  a new key here is seeded as soon as a migration adds the column of that name.
"""
import json
import os
import random

from faker import Faker

SEED = 20260906
random.seed(SEED)
Faker.seed(SEED)
fake = Faker("en_US")

ROOT = os.path.dirname(os.path.abspath(__file__))


def load(name):
    with open(os.path.join(ROOT, name), encoding="utf-8") as f:
        return json.load(f)


BRANDS = [b["title"] for b in load("brands.json")]
ATTRS = load("attributes.json")
CATEGORY_TREE = load("categories.json")

COLORS = list(ATTRS["color"].keys())
MATERIALS = list(ATTRS["material"].keys())
SOLES = list(ATTRS["sole"].keys())
CLOSURES = list(ATTRS["closure"].keys())
WIDTHS = list(ATTRS["width"].keys())
SEASONS = list(ATTRS["season"].keys())

PARENT_OF = {}


def _index_parents(nodes, parent=None):
    for node in nodes:
        PARENT_OF[node["title"]] = parent
        _index_parents(node.get("children", []), node["title"])


_index_parents(CATEGORY_TREE)

# --- what each leaf category sells -------------------------------------------------

SHOE_CATS = [
    "men sneakers", "men boots", "men loafers", "men sandals", "men formal", "men running",
    "women sneakers", "women boots", "women heels", "women ballet flats", "women sandals",
    "women running",
    "kids sneakers", "kids boots", "kids sandals", "kids school shoes",
    "trail running", "training", "football boots", "basketball", "hiking",
]
ACCESSORY_CATS = ["laces", "insoles", "shoe care", "socks"]

CATEGORY_KIND = {c: "shoes" for c in SHOE_CATS}
CATEGORY_KIND.update({c: "accessory" for c in ACCESSORY_CATS})

MEN = [str(n) for n in range(39, 48)]
WOMEN = [str(n) for n in range(35, 43)]
KIDS = [str(n) for n in range(24, 35)]
UNISEX = [str(n) for n in range(38, 47)]

SIZES = {c: UNISEX for c in SHOE_CATS}
SIZES.update({c: MEN for c in SHOE_CATS if c.startswith("men")})
SIZES.update({c: WOMEN for c in SHOE_CATS if c.startswith("women")})
SIZES.update({c: KIDS for c in SHOE_CATS if c.startswith("kids")})

# model names, deliberately brand free
MODELS = {
    "men sneakers": ["Court Low", "Street Runner", "Retro 84", "Daily Trainer", "Canvas Low"],
    "men boots": ["Chelsea", "Ranger", "Workman", "Winter Ridge", "Desert Boot"],
    "men loafers": ["Penny Loafer", "Driver", "Tassel", "Weekend Slip-On"],
    "men sandals": ["Slide", "River Sandal", "Trek Sandal", "Beachline"],
    "men formal": ["Oxford", "Derby", "Brogue", "Monk Strap"],
    "men running": ["Tempo", "Long Run", "Cushion 5", "Race Day", "Marathon Lite"],
    "women sneakers": ["Court Low", "Platform", "Retro 84", "Knit Runner", "Canvas Low"],
    "women boots": ["Chelsea", "Ankle Boot", "Rider", "Winter Ridge", "Combat"],
    "women heels": ["Stiletto", "Block Heel", "Kitten Heel", "Slingback", "Pump"],
    "women ballet flats": ["Ballerina", "Mary Jane", "Square Toe Flat", "Bow Flat"],
    "women sandals": ["Strap Sandal", "Slide", "Espadrille", "Gladiator"],
    "women running": ["Tempo", "Long Run", "Cushion 5", "Race Day", "Studio Run"],
    "kids sneakers": ["First Step", "Playground", "Velcro Runner", "Mini Court"],
    "kids boots": ["Snow Cub", "Rain Boot", "Winter Cub", "Hiker Junior"],
    "kids sandals": ["Beach Cub", "River Junior", "Summer Strap"],
    "kids school shoes": ["School Classic", "Uniform Loafer", "Smart Velcro"],
    "trail running": ["Ridge Trail", "Mud Runner", "Rock Grip", "Ultra Trail"],
    "training": ["Gym Flat", "Cross Trainer", "Lift Zero", "Studio Trainer"],
    "football boots": ["Firm Ground", "Artificial Grass", "Indoor Court", "Soft Ground"],
    "basketball": ["High Top", "Mid Cut", "Post Player", "Guard 3"],
    "hiking": ["Summit Mid", "Alpine GTX", "Backcountry", "Fell Walker"],
    "laces": ["Flat Lace", "Round Lace", "Waxed Lace", "Elastic Lace"],
    "insoles": ["Memory Insole", "Arch Support", "Winter Wool Insole", "Sport Gel Insole"],
    "shoe care": ["Cleaning Kit", "Suede Protector", "Leather Balm", "Water Repellent"],
    "socks": ["Ankle Socks", "Crew Socks", "Running Socks", "Wool Socks"],
}

PREFIXES = ["Aurora", "Nimbus", "Vertex", "Cascade", "Solstice", "Meridian", "Harbor", "Drift",
            "Ember", "Quarry", "Lumen", "Grove", "Atlas", "Cobble", "Vista", "Halcyon", "Nomad",
            "Bracken", "Tundra", "Marlow", "Sable", "Copper", "Willow", "Slate", "Corso",
            "Verano", "Aster", "Cairn", "Basalt", "Juniper", "Onyx", "Pallas", "Rivet", "Sierra"]

EDITIONS = ["", "", "", "II", "III", "Pro", "Lite", "Plus", "GTX", "Classic"]

USE = {
    "shoes": ["city walking", "long days on your feet", "commuting", "weekend trips",
              "training sessions", "everyday wear"],
    "accessory": ["daily use", "seasonal care", "long training weeks", "everyday wear"],
}

SHORT_SHOE = "{model} in {material} on a {sole} sole, {closure} closure."
SHORT_ACCESSORY = "{model} for {use}, sold per pair unless stated otherwise."

LONG_SHOE = (
    "The {model} is built on a {material} upper and a {sole} sole, with a {closure} "
    "closure and a {width} fit. Made for {use} and rated for {season}. "
)
LONG_ACCESSORY = (
    "The {model} is a small upgrade with an obvious effect: made for {use} and easy to "
    "swap in and out. Rated for {season}. "
)

CARE = [
    "Wipe with a damp cloth, dry away from direct heat.",
    "Machine washable at 30 degrees, do not tumble dry.",
    "Store in the box with the shape holder to keep the last.",
    "Re-proof once a season to keep the water repellency.",
]

# --- variants ----------------------------------------------------------------------

LACE_LENGTHS = ["90 cm", "120 cm", "140 cm", "160 cm"]
INSOLE_SIZES = [str(n) for n in range(36, 46)]
SOCK_SIZES = ["S 35-38", "M 39-42", "L 43-46"]
CARE_KINDS = ["150 ml spray", "250 ml foam", "75 ml balm", "brush + cloth"]

PRICE_RANGE = {
    "men sneakers": (69, 165), "men boots": (95, 260), "men loafers": (85, 210),
    "men sandals": (35, 90), "men formal": (110, 290), "men running": (79, 210),
    "women sneakers": (65, 160), "women boots": (95, 250), "women heels": (75, 195),
    "women ballet flats": (55, 140), "women sandals": (35, 95), "women running": (79, 205),
    "kids sneakers": (29, 75), "kids boots": (39, 95), "kids sandals": (22, 55),
    "kids school shoes": (35, 85),
    "trail running": (95, 230), "training": (69, 155), "football boots": (55, 240),
    "basketball": (85, 220), "hiking": (110, 280),
    "laces": (3, 12), "insoles": (7, 29), "shoe care": (5, 24), "socks": (6, 22),
}

used_titles = set()
used_sku = set()
used_barcode = set()


def ean13(seq: int) -> str:
    base = f"482{seq:09d}"[:12]
    total = sum(int(d) * (1 if i % 2 == 0 else 3) for i, d in enumerate(base))
    return base + str((10 - total % 10) % 10)


def slug(s: str, n: int = 3) -> str:
    letters = "".join(ch for ch in s.upper() if ch.isalnum())
    return letters[:n] or "XXX"


def category_code(cat: str, n: int = 4) -> str:
    """Short, collision free code for a category: "men formal" -> "MEFO"."""
    return slug("".join(word[:2] for word in cat.split()), n)


def path_slug(s: str) -> str:
    out = "".join(ch.lower() if ch.isalnum() else "-" for ch in s)
    while "--" in out:
        out = out.replace("--", "-")
    return out.strip("-")


def variant_axes(cat: str):
    """[(suffix, sku_part)] - one entry per variant of a product in this category."""
    if CATEGORY_KIND[cat] == "shoes":
        sizes = random.sample(SIZES[cat], k=random.randint(4, 7))
        colors = random.sample(COLORS, k=random.randint(1, 2))
        return [(f"EU {s} / {c}", f"{s}-{slug(c, 3)}")
                for s in sorted(sizes, key=int) for c in colors]
    if cat == "laces":
        return [(f"{l} / {c}", f"{l.split()[0]}-{slug(c, 3)}")
                for l in random.sample(LACE_LENGTHS, k=random.randint(2, 3))
                for c in random.sample(COLORS, k=2)]
    if cat == "insoles":
        return [(f"EU {s}", f"EU{s}") for s in random.sample(INSOLE_SIZES, k=random.randint(4, 6))]
    if cat == "socks":
        return [(f"{s} / {c}", f"{slug(s, 1)}-{slug(c, 3)}")
                for s in SOCK_SIZES for c in random.sample(COLORS, k=random.randint(1, 2))]
    # shoe care and fallback
    return [(k, slug(k, 4)) for k in random.sample(CARE_KINDS, k=random.randint(2, 3))]


def images(name: str, count: int):
    """Placeholder gallery. No table holds these yet - see database/seeder/README.md."""
    base = path_slug(name)
    return [
        {
            "path": f"/images/products/{base}-{i + 1}.jpg",
            "position": i + 1,
            "role": "main" if i == 0 else "gallery",
        }
        for i in range(count)
    ]


def make_product(cat: str, seq: int):
    brand = random.choice(BRANDS)
    kind = CATEGORY_KIND[cat]
    model = random.choice(MODELS[cat])
    material = random.choice(MATERIALS)
    sole = random.choice(SOLES)
    closure = random.choice(CLOSURES)
    width = random.choice(WIDTHS)
    season = random.choice(SEASONS)
    use = random.choice(USE[kind])

    # the brand is intentionally left out of the title
    title = " ".join(x for x in (random.choice(PREFIXES), model, random.choice(EDITIONS)) if x)
    if title in used_titles:  # products.title is UNIQUE
        title = f"{title} {seq}"
    used_titles.add(title)

    if kind == "shoes":
        short = SHORT_SHOE.format(model=model, material=material, sole=sole, closure=closure)
        lead = LONG_SHOE.format(model=model, material=material, sole=sole, closure=closure,
                                width=width, use=use, season=season)
    else:
        short = SHORT_ACCESSORY.format(model=model, use=use)
        lead = LONG_ACCESSORY.format(model=model, use=use, season=season)

    description = f"{lead}{fake.paragraph(nb_sentences=4)} {random.choice(CARE)}"

    low, high = PRICE_RANGE[cat]
    base_price = round(random.uniform(low, high), 2)

    variants = []
    for i, (suffix, sku_part) in enumerate(variant_axes(cat)):
        sku = f"{slug(brand)}-{category_code(cat)}-{seq:04d}-{sku_part}".upper().replace(" ", "")
        if sku in used_sku:
            sku = f"{sku}-{i}"
        used_sku.add(sku)

        code = ean13(len(used_barcode) + 1)
        used_barcode.add(code)

        variants.append({
            "title": f"{title} {suffix}",
            "description": None if random.random() < 0.6 else f"{title} in {suffix}.",
            "sku": sku,
            "barcode": code,
            "pricing": {
                # sizes at the edge of the run cost a little more to make
                "price": round(base_price + random.choice([0, 0, 0, 5, 10]), 2),
            },
            "images": [],
        })

    categories = [cat]
    parent = PARENT_OF.get(cat)
    if parent and random.random() < 0.7:
        categories.append(parent)

    return {
        "title": title,
        "short_description": short,
        "description": description,
        "categories": categories,
        "brands": [brand],
        "images": images(title, random.randint(2, 4)),
        "variants": variants,
    }

def main():
    COUNTS = {c: 8 for c in SHOE_CATS}
    COUNTS.update({c: 5 for c in ACCESSORY_CATS})

    products = []
    seq = 0
    for category, amount in COUNTS.items():
        for _ in range(amount):
            seq += 1
            products.append(make_product(category, seq))

    random.shuffle(products)

    out = os.path.join(ROOT, "products.json")
    with open(out, "w", encoding="utf-8") as f:
        json.dump(products, f, indent=4, ensure_ascii=False)
        f.write("\n")

    print(f"products: {len(products)}  variants: {sum(len(p['variants']) for p in products)}")
    print(f"unique titles: {len(used_titles)}  skus: {len(used_sku)}  barcodes: {len(used_barcode)}")


if __name__ == "__main__":
    main()
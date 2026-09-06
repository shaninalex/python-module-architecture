import os

# database/seeder
SEEDER_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

RESOURCES_DIR = os.path.join(SEEDER_ROOT, "resources")


def resource(name: str) -> str:
    """Absolute path of a file inside database/seeder/resources."""
    return os.path.join(RESOURCES_DIR, name)


def load_resource(name: str):
    """Parsed JSON fixture from database/seeder/resources."""
    import json

    with open(resource(name), "r", encoding="utf-8") as f:
        return json.load(f)

from typing import Any, Dict, List, Optional

from seeder.context import Context
from seeder.paths import load_resource

# nesting is expressed by this key, everything else on the node is a column
CHILDREN = "children"


class CategorySeeder:
    """resources/categories.json is a list of nodes: {"title": ..., "children": [...]}.

    Any other key on a node is passed straight to the categories table, so adding
    an image or a description to a category is a fixture + migration change only.
    """

    def __init__(self):
        self.counter: int = 0

    def name(self) -> str:
        return "categories"

    def seed(self, ctx: Context):
        cursor = ctx.cursor()
        self.counter = 0
        self._insert_tree(ctx, cursor, load_resource("categories.json"), None)
        ctx.commit()
        print(f"Inserted {self.counter} categories")

    def _insert_tree(self, ctx: Context, cursor, nodes: List[Dict[str, Any]], parent_id: Optional[int]):
        for node in nodes:
            values = {k: v for k, v in node.items() if k != CHILDREN}
            values["parent_id"] = parent_id

            category_id = ctx.tables("categories").insert(cursor, values)
            self.counter += 1

            self._insert_tree(ctx, cursor, node.get(CHILDREN, []), category_id)

    def clear(self, ctx: Context):
        cursor = ctx.cursor()
        ctx.tables("categories").delete_all(cursor)
        ctx.commit()

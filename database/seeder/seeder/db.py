"""Schema aware helpers around a psycopg2 connection.

Every write goes through Table.insert / Table.insert_many, and both accept a plain
dict of column -> value. Keys the table does not have are dropped, so a fixture may
carry more than the current migration knows about.

That is what keeps the seeder cheap to extend: to seed a new column (an image path,
a weight, a slug) add the key to the JSON fixture and the column to a migration -
no entity code changes. Whole tables work the same way: Table.exists() is False
until the migration creates it, and the seeder logs a skip instead of crashing.
"""

from typing import Any, Dict, Iterable, List, Optional, Set


class Table:
    def __init__(self, connection, schema: str, name: str):
        self._connection = connection
        self.schema = schema
        self.name = name
        self._columns: Optional[Set[str]] = None

    def __str__(self) -> str:
        return self.qualified

    @property
    def qualified(self) -> str:
        return f"{self.schema}.{self.name}"

    @property
    def columns(self) -> Set[str]:
        if self._columns is None:
            cursor = self._connection.cursor()
            cursor.execute(
                "select column_name from information_schema.columns "
                "where table_schema = %s and table_name = %s",
                (self.schema, self.name),
            )
            self._columns = {row[0] for row in cursor.fetchall()}
        return self._columns

    def exists(self) -> bool:
        return bool(self.columns)

    def known(self, values: Dict[str, Any]) -> Dict[str, Any]:
        """Drop the keys this table has no column for."""
        return {k: v for k, v in values.items() if k in self.columns}

    def insert(self, cursor, values: Dict[str, Any], returning: Optional[str] = "id"):
        """Insert one row, return the `returning` column (None to skip the fetch)."""
        row = self._row(values)
        sql = f"insert into {self.qualified} ({self._names(row)}) values ({self._marks(row)})"
        if returning:
            sql += f" returning {returning}"
        cursor.execute(sql, list(row.values()))
        return cursor.fetchone()[0] if returning else None

    def insert_many(self, cursor, values: Iterable[Dict[str, Any]]) -> int:
        """Insert rows that all share the same shape. Returns the number of rows."""
        rows: List[Dict[str, Any]] = [self._row(v) for v in values]
        if not rows:
            return 0

        names = list(rows[0].keys())
        for row in rows:
            if list(row.keys()) != names:
                raise RuntimeError(
                    f"{self.qualified}: insert_many needs rows with identical columns, "
                    f"got {names} and {list(row.keys())}"
                )

        cursor.executemany(
            f"insert into {self.qualified} ({', '.join(names)}) "
            f"values ({', '.join(['%s'] * len(names))})",
            [[row[n] for n in names] for row in rows],
        )
        return len(rows)

    def delete_all(self, cursor):
        if not self.exists():
            return
        cursor.execute(f"delete from {self.qualified};")

    def lookup(self, cursor, key: str = "title", value: str = "id") -> Dict[str, Any]:
        """{title: id} map, used to resolve fixture references."""
        cursor.execute(f"select {key}, {value} from {self.qualified};")
        return dict(cursor.fetchall())

    def _row(self, values: Dict[str, Any]) -> Dict[str, Any]:
        if not self.exists():
            raise RuntimeError(f"table {self.qualified} does not exist")
        row = self.known(values)
        if not row:
            raise RuntimeError(
                f"{self.qualified}: none of {sorted(values)} match a column of the table"
            )
        return row

    @staticmethod
    def _names(row: Dict[str, Any]) -> str:
        return ", ".join(row.keys())

    @staticmethod
    def _marks(row: Dict[str, Any]) -> str:
        return ", ".join(["%s"] * len(row))


class Tables:
    """Table factory bound to the schema from the config."""

    def __init__(self, connection, schema: str):
        self._connection = connection
        self._schema = schema
        self._cache: Dict[str, Table] = {}

    def __call__(self, name: str) -> Table:
        if name not in self._cache:
            self._cache[name] = Table(self._connection, self._schema, name)
        return self._cache[name]

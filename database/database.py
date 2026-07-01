import sqlite3
from contextlib import contextmanager
from typing import Any

from app.schemas import ShipmentCreate, ShipmentUpdate


class Database:
    def connect(self) -> None:
        self.conn = sqlite3.connect(
            "sqlite.db",
            check_same_thread=False,
        )
        self.conn.row_factory = sqlite3.Row
        self.cur = self.conn.cursor()

    def create_table(self) -> None:
        self.cur.execute("""
            CREATE TABLE IF NOT EXISTS shipment (
                id INTEGER PRIMARY KEY,
                content TEXT,
                weight REAL,
                status TEXT
            )
        """)
        self.conn.commit()

    def create(self, shipment: ShipmentCreate) -> int:
        self.cur.execute(
            """
            INSERT INTO shipment (content, weight, status)
            VALUES (:content, :weight, :status)
        """,
            {
                **shipment.model_dump(),
                "status": "placed",
            },
        )

        self.conn.commit()
        return self.cur.lastrowid

    def get(self, shipment_id: int) -> dict[str, Any] | None:
        self.cur.execute(
            "SELECT * FROM shipment WHERE id = ?",
            (shipment_id,),
        )

        row = self.cur.fetchone()
        return dict(row) if row else None

    def get_all(self):
        self.cur.execute("SELECT * FROM shipment")
        return [dict(row) for row in self.cur.fetchall()]

    def update(
        self,
        shipment_id: int,
        shipment: ShipmentUpdate,
    ) -> dict[str, Any] | None:

        values = shipment.model_dump(exclude_none=True)

        if not values:
            return self.get(shipment_id)

        assignments = ", ".join(f"{column} = :{column}" for column in values)

        values["id"] = shipment_id

        self.cur.execute(
            f"""
            UPDATE shipment
            SET {assignments}
            WHERE id = :id
            """,
            values,
        )

        self.conn.commit()
        return self.get(shipment_id)

    def replace(
        self,
        shipment_id: int,
        shipment: ShipmentCreate,
    ) -> dict[str, Any] | None:

        self.cur.execute(
            """
                         UPDATE shipment
                         SET content = :content,
                             weight = :weight,
                             status = :status
                         WHERE id = :id
                         """,
            {
                "id": shipment_id,
                **shipment.model_dump(),
            },
        )

        self.conn.commit()
        return self.get(shipment_id)

    def delete(self, shipment_id: int) -> None:
        self.cur.execute(
            "DELETE FROM shipment WHERE id = ?",
            (shipment_id,),
        )
        self.conn.commit()

    def close(self) -> None:
        self.conn.close()

    def __enter__(self):
        self.connect()
        self.create_table()
        return self

    def __exit__(self, *_):
        self.close()


def get_db():
    with Database() as db:
        yield db


if __name__ == "__main__":
    with Database() as db:
        print(db.get(12701))
        print(db.get(12702))

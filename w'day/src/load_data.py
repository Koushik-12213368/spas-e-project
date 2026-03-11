import os
import sys

import pandas as pd
import pyodbc
from dotenv import load_dotenv


def get_connection_string() -> str:
    """
    Reads connection string from environment.
    Expected: AZURE_SQL_CONNECTION_STRING
    """
    conn_str = os.getenv("AZURE_SQL_CONNECTION_STRING")
    if not conn_str:
        raise RuntimeError("AZURE_SQL_CONNECTION_STRING environment variable is not set")
    return conn_str


def get_connection() -> pyodbc.Connection:
    conn_str = get_connection_string()
    return pyodbc.connect(conn_str)


def apply_schema(cursor) -> None:
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    schema_path = os.path.join(base_dir, "infra", "schema.sql")
    with open(schema_path, "r", encoding="utf-8") as f:
        sql = f.read()
    # Split on GO batches if present
    for statement in [s.strip() for s in sql.split("GO") if s.strip()]:
        cursor.execute(statement)


def load_sales_data(cursor) -> None:
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    csv_path = os.path.join(base_dir, "data", "sample_sales.csv")

    df = pd.read_csv(csv_path, parse_dates=["order_date"])

    # Truncate table to keep data in sync with the CSV
    cursor.execute("IF OBJECT_ID('dbo.Sales', 'U') IS NOT NULL TRUNCATE TABLE dbo.Sales;")

    insert_sql = """
        INSERT INTO Sales (OrderDate, Region, Product, Quantity, UnitPrice)
        VALUES (?, ?, ?, ?, ?)
    """

    for _, row in df.iterrows():
        cursor.execute(
            insert_sql,
            row["order_date"].date(),
            row["region"],
            row["product"],
            int(row["quantity"]),
            float(row["unit_price"]),
        )


def main() -> None:
    load_dotenv()

    with get_connection() as conn:
        cursor = conn.cursor()
        apply_schema(cursor)
        load_sales_data(cursor)
        conn.commit()


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:  # noqa: BLE001
        print(f"Error while loading data: {exc}", file=sys.stderr)
        sys.exit(1)


# ============================================================
# load_db.py  —  Phase 4
# Creates SQLite database, applies schema, loads clean CSVs
# Uses row limits on large relationship files to save disk space
# ============================================================

import os
import sqlite3
import pandas as pd

CLEAN_DIR = os.path.join(os.path.dirname(__file__), '..', 'data', 'clean')
DB_PATH   = os.path.join(os.path.dirname(__file__), '..', 'database', 'patents.db')
SCHEMA    = os.path.join(os.path.dirname(__file__), '..', 'database', 'schema.sql')

# Row limits — set to None for full load, or a number to cap
LIMITS = {
    'clean_patents.csv':         1_000_000,
    'clean_inventors.csv':       1_000_000,
    'clean_companies.csv':       None,        # small file, load all
    'clean_patent_inventor.csv': 1_000_000,
    'clean_patent_assignee.csv': 1_000_000,
    'clean_term_of_grant.csv':   None,        # small file, load all
}


def get_conn():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA journal_mode=OFF")
    conn.execute("PRAGMA synchronous=OFF")
    conn.execute("PRAGMA foreign_keys=OFF")
    return conn


def apply_schema(conn):
    print("  Applying schema ...")
    with open(SCHEMA, 'r') as f:
        conn.executescript(f.read())
    conn.commit()
    print("  Schema applied.")


def load_csv(conn, filename, table):
    path = os.path.join(CLEAN_DIR, filename)
    if not os.path.exists(path):
        print(f"  WARNING: {filename} not found, skipping.")
        return

    row_limit = LIMITS.get(filename)
    limit_str = f"(max {row_limit:,} rows)" if row_limit else "(all rows)"
    print(f"  Loading {filename} -> [{table}] {limit_str} ...")

    chunk_size = 50_000
    total = 0

    for chunk in pd.read_csv(path, dtype=str, chunksize=chunk_size):
        # Apply row limit if set
        if row_limit and total >= row_limit:
            break
        if row_limit:
            remaining = row_limit - total
            chunk = chunk.iloc[:remaining]

        chunk.to_sql(table, conn, if_exists='append', index=False)
        total += len(chunk)
        print(f"    {total:,} rows loaded ...", end='\r')

    conn.commit()
    print(f"  Done: {total:,} rows into [{table}]          ")


def main():
    print("=" * 55)
    print("  Patent Database Loader")
    print("=" * 55)
    print(f"  Database: {os.path.abspath(DB_PATH)}\n")

    conn = get_conn()
    apply_schema(conn)

    load_csv(conn, 'clean_patents.csv',          'patents')
    load_csv(conn, 'clean_inventors.csv',        'inventors')
    load_csv(conn, 'clean_companies.csv',        'companies')
    load_csv(conn, 'clean_patent_inventor.csv',  'patent_inventor')
    load_csv(conn, 'clean_patent_assignee.csv',  'patent_assignee')
    load_csv(conn, 'clean_term_of_grant.csv',    'term_of_grant')

    # Print summary
    print("\n  Summary:")
    tables = ['patents', 'inventors', 'companies',
              'patent_inventor', 'patent_assignee', 'term_of_grant']
    for t in tables:
        count = conn.execute(f"SELECT COUNT(*) FROM {t}").fetchone()[0]
        print(f"    {t:<25} {count:>10,} rows")

    conn.close()
    print("\n  Database ready.")
    print("  Next step: python scripts/report.py")


if __name__ == "__main__":
    main()
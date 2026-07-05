"""Extract INSERT data from the AP SQL file into CSV files."""

import csv
import re
from pathlib import Path

SQL_FILE = Path(__file__).resolve().parent.parent / "create_ap (1) (1).sql"
DATA_DIR = Path(__file__).resolve().parent.parent

INSERT_PATTERN = re.compile(
    r"INSERT\s+(\w+)\s*\(([^)]+)\)\s*VALUES\s*\((.+)\)\s*$",
    re.IGNORECASE,
)


def parse_value(raw: str):
    raw = raw.strip()
    if raw.upper() == "NULL":
        return None
    if raw.startswith("N'") and raw.endswith("'"):
        return raw[2:-1].replace("''", "'")
    if raw.startswith("'") and raw.endswith("'"):
        return raw[1:-1].replace("''", "'")
    if raw.startswith("CAST(N'") and " AS Date)" in raw:
        return raw.split("CAST(N'")[1].split("' AS Date)")[0]
    try:
        if "." in raw:
            return float(raw)
        return int(raw)
    except ValueError:
        return raw


def extract_inserts(sql_text: str) -> dict[str, list[dict]]:
    tables: dict[str, list[dict]] = {}
    for line in sql_text.splitlines():
        line = line.strip()
        if not line.startswith("INSERT "):
            continue
        match = INSERT_PATTERN.match(line)
        if not match:
            continue
        table, cols_raw, vals_raw = match.groups()
        columns = [c.strip() for c in cols_raw.split(",")]
        values = []
        current = []
        in_string = False
        for char in vals_raw + ",":
            if char == "'" and (not current or current[-1] != "\\"):
                in_string = not in_string
                current.append(char)
            elif char == "," and not in_string:
                values.append("".join(current).strip())
                current = []
            else:
                current.append(char)
        row = dict(zip(columns, [parse_value(v) for v in values]))
        tables.setdefault(table, []).append(row)
    return tables


def write_csv(table_name: str, rows: list[dict], out_dir: Path) -> None:
    if not rows:
        return
    out_dir.mkdir(parents=True, exist_ok=True)
    path = out_dir / f"{table_name}.csv"
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)
    print(f"Wrote {len(rows)} rows -> {path}")


def main() -> None:
    sql_text = SQL_FILE.read_text(encoding="utf-16")
    tables = extract_inserts(sql_text)
    for name, rows in sorted(tables.items()):
        write_csv(name, rows, DATA_DIR)


if __name__ == "__main__":
    main()

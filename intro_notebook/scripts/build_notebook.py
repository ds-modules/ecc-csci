#!/usr/bin/env python3
"""Generate intro.ipynb for SQL → Pandas/Polars bridge course."""

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "intro.ipynb"


def md(source: str, tags=None):
    return {
        "cell_type": "markdown",
        "metadata": {"tags": tags or []},
        "source": source if isinstance(source, list) else [source],
    }


def code(source: str, tags=None):
    return {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {"tags": tags or []},
        "outputs": [],
        "source": source if isinstance(source, list) else [source],
    }


def solution_block(source: str, label: str = "Solution") -> str:
    return (
        "<details>\n"
        f"<summary><strong>{label}:</strong></summary>\n\n"
        f"```python\n{source.rstrip()}\n```\n\n"
        "</details>"
    )


def practice_question(prompt: str, solution: str, placeholder: str = "# Your code here\n"):
    cells.append(md(f"{prompt}\n\n{solution_block(solution)}"))
    cells.append(code(placeholder))


HR = '<hr style="border: 2px solid #003262">'
HR_GOLD = '<hr style="border: 2px solid #C9B676">'


def section_start(number: int, title: str) -> None:
    """Divider + heading in their own cell above section content."""
    cells.append(md(f"{HR}\n\n## {number}. {title}"))


cells = []

# --- Section 1: Welcome ---
cells.append(md("# Introduction to Jupyter, Python, Pandas, and Polars for SQL Students"))
cells.append(md(f"{HR}\n\n{HR_GOLD}\n\n## 1. Welcome"))
cells.append(md(
    "You've spent about eight weeks learning **SQL** — how to retrieve data with "
    "`SELECT`, filter with `WHERE`, summarize with `GROUP BY`, and combine tables with `JOIN`.\n\n"
    "This notebook will bridge your SQL knowledge into Python data analysis using **Pandas** and **Polars**.\n\n"
    "We use the **AP (Accounts Payable)** database from your SQL course — vendors, invoices, "
    "payment terms, and general-ledger accounts — stored as CSV files in this project folder."
))

cells.append(md(
    "## Learning Objectives\n\n"
    "By the end of this notebook, you should be able to:\n\n"
    "- Navigate and run cells in a Jupyter notebook\n"
    "- Load tabular data into **DataFrames** with Pandas and Polars\n"
    "- Translate common SQL operations into Pandas syntax\n"
    "- Translate the same operations into Polars syntax\n"
    "- Explain why Python is commonly used **after** SQL in data workflows"
))

cells.append(md(
    "> **How to use this notebook:** Read each short section, run the code cell immediately "
    "below it, and try the practice question before expanding the **Solution** section to check your work."
))

# --- Section 2: Jupyter Basics ---
section_start(2, "Jupyter Notebook Basics")
cells.append(md(
    "A **Jupyter notebook** mixes explanatory text (Markdown) with runnable **code cells**. "
    "Each cell runs independently, which makes exploration easy.\n\n"
    "| Cell type | Purpose |\n"
    "|-----------|----------|\n"
    "| **Markdown** | Headings, explanations, tables (like this cell) |\n"
    "| **Code** | Python you can run and re-run |\n\n"
    "**Running a cell:** Click a cell and press `Shift + Enter` (runs and moves down) or "
    "`Ctrl/Cmd + Enter` (runs in place).\n\n"
    "**Restart & Run All:** `Kernel → Restart & Run All` re-runs every cell from the top — "
    "useful after editing earlier cells.\n\n"
    "**Useful shortcuts:**\n"
    "- `A` — insert cell above (command mode)\n"
    "- `B` — insert cell below\n"
    "- `D, D` — delete cell\n"
    "- `M` — change cell to Markdown\n"
    "- `Y` — change cell to Code"
))

cells.append(md("**Exercise:** Run the cell below. You should see a greeting printed."))
cells.append(code('print("Hello from Jupyter! You ran your first cell.")'))

# --- Section 3: Python Essentials ---
section_start(3, "Python Essentials (Just Enough)")
cells.append(md(
    "We only cover Python concepts you'll use in this notebook. No loops, classes, or file writing."
))

cells.append(md("## Variables\n\nA **variable** stores a value under a name."))
cells.append(code("x = 10\ny = 3.5\nname = \"AP Database\"\nprint(x, y, name)"))

cells.append(md("## Strings and Lists\n\n**Strings** hold text. **Lists** hold ordered collections."))
cells.append(code(
    'vendor = "Federal Express Corporation"\nstates = ["CA", "WI", "TN"]\nprint(vendor.upper())\nprint(len(states))\nprint(states[0])'
))

cells.append(md("## Basic Math"))
cells.append(code("invoice_total = 3813.33\ntax = invoice_total * 0.08\nprint(invoice_total + tax)\nprint(invoice_total / 2)"))

cells.append(md("## Built-in Functions\n\n`print()`, `len()`, and `type()` appear often:"))
cells.append(code('print(type(invoice_total))\nprint(len("Invoices"))'))

cells.append(md(
    "## Importing Libraries\n\n"
    "> **Kernel check:** If imports fail, use **Kernel → Change Kernel** and select "
    "**Python (ecc-csci)** or your project's `.venv` interpreter — not the system Python.\n\n"
    "**Pandas** and **Polars** are imported with standard aliases:"
))
cells.append(code("import pandas as pd\nimport polars as pl\nimport numpy as np\n\nprint(pd.__version__)"))

practice_question(
    "**Practice:** Create a variable `terms_days = 30` and print its type.\n\n"
    "*Write your answer in the cell below.*",
    "terms_days = 30\nprint(type(terms_days))",
)

# --- Section 4: DataFrames ---
section_start(4, "Introducing DataFrames")
cells.append(md(
    "In SQL, data lives in **tables**. In Python, the equivalent is a **DataFrame** — "
    "a table with **rows**, **columns**, **column names**, and **data types**.\n\n"
    "```\n"
    "Database Table  →  DataFrame\n"
    "     row          →  row (observation)\n"
    "   column         →  column (variable)\n"
    "```\n\n"
    "Our dataset comes from the AP database (`Vendors`, `Invoices`, `Terms`, `GLAccounts`, etc.), "
    "exported to CSV files in this folder."
))

cells.append(md("## Load with Pandas"))
cells.append(code(
    'vendors_pd = pd.read_csv("Vendors.csv")\n'
    'invoices_pd = pd.read_csv("Invoices.csv")\n'
    'terms_pd = pd.read_csv("Terms.csv")\n'
    'vendors_pd.head()'
))

cells.append(md("## Load with Polars"))
cells.append(code(
    'vendors_pl = pl.read_csv("Vendors.csv")\n'
    'invoices_pl = pl.read_csv("Invoices.csv")\n'
    'terms_pl = pl.read_csv("Terms.csv")\n'
    'vendors_pl.head()'
))

cells.append(md("## Inspecting a DataFrame"))
cells.append(code(
    'print("Shape (rows, columns):", vendors_pd.shape)\n'
    'print("Columns:", list(vendors_pd.columns))\n'
    'vendors_pd.dtypes'
))

practice_question(
    "**Practice:** Load `GLAccounts.csv` into a Pandas DataFrame called `gl_pd` and display its first 5 rows.",
    'gl_pd = pd.read_csv("GLAccounts.csv")\ngl_pd.head()',
)

# --- Section 5: SQL Review ---
section_start(5, "SQL Review (Quick Refresher)")
cells.append(md(
    "This is a **refresher**, not a re-teach. We'll use the AP schema throughout.\n\n"
    "**Key tables:**\n"
    "- `Vendors` — companies we pay (`VendorID`, `VendorName`, `VendorState`, …)\n"
    "- `Invoices` — bills received (`InvoiceID`, `VendorID`, `InvoiceTotal`, `TermsID`, …)\n"
    "- `Terms` — payment terms (`TermsID`, `TermsDescription`, `TermsDueDays`)\n"
    "- `GLAccounts` — chart of accounts (`AccountNo`, `AccountDescription`)\n\n"
    "| SQL clause | What it does | AP example |\n"
    "|------------|--------------|------------|\n"
    "| `SELECT` | Choose columns | vendor names |\n"
    "| `FROM` | Choose table | `Vendors` |\n"
    "| `WHERE` | Filter rows | invoices over 10,000 |\n"
    "| `ORDER BY` | Sort results | largest invoices first |\n"
    "| `GROUP BY` | Group rows | count vendors per state |\n"
    "| `COUNT`, `AVG`, `MIN`, `MAX` | Summarize | average invoice total |\n"
    "| `JOIN` | Combine tables | invoices + vendor names |\n\n"
    "**Example SQL** (from the AP database):\n\n"
    "```sql\n"
    "SELECT VendorName, VendorState\n"
    "FROM Vendors\n"
    "WHERE VendorState = 'CA'\n"
    "ORDER BY VendorName;\n"
    "```\n\n"
    "```sql\n"
    "SELECT TermsID, AVG(InvoiceTotal) AS AvgTotal\n"
    "FROM Invoices\n"
    "GROUP BY TermsID;\n"
    "```\n\n"
    "```sql\n"
    "SELECT v.VendorName, i.InvoiceTotal\n"
    "FROM Invoices i\n"
    "JOIN Vendors v ON i.VendorID = v.VendorID\n"
    "WHERE i.InvoiceTotal > 20000;\n"
    "```"
))

# --- Section 6: SQL → Pandas ---
section_start(6, "SQL → Pandas")
cells.append(md(
    "For each SQL concept: **SQL → Pandas → explanation → practice**.\n\n"
    "We'll use `vendors_pd` and `invoices_pd` loaded earlier."
))

# SELECT columns
cells.append(md(
    "## Selecting Columns (`SELECT`)\n\n"
    "**SQL:**\n"
    "```sql\n"
    "SELECT VendorName, VendorCity FROM Vendors;\n"
    "```\n\n"
    "**Pandas:** Use double brackets `[[]]` or `.loc` to select columns."
))
cells.append(code("vendors_pd[[\"VendorName\", \"VendorCity\"]].head()"))
practice_question(
    "**Practice:** Select `InvoiceID`, `InvoiceTotal`, and `VendorID` from `invoices_pd` (first 5 rows).",
    'invoices_pd[["InvoiceID", "InvoiceTotal", "VendorID"]].head()',
)

# WHERE filter
cells.append(md(
    "## Filtering Rows (`WHERE`)\n\n"
    "**SQL:**\n"
    "```sql\n"
    "SELECT * FROM Invoices WHERE InvoiceTotal > 10000;\n"
    "```\n\n"
    "**Pandas:** Boolean indexing — pass a condition inside `[]`."
))
cells.append(code("invoices_pd[invoices_pd[\"InvoiceTotal\"] > 10000].head()"))
practice_question(
    "**Practice:** Show vendors in California (`VendorState == 'CA'`). Display `VendorName` and `VendorCity`.",
    'vendors_pd[vendors_pd["VendorState"] == "CA"][["VendorName", "VendorCity"]].head()',
)

# SORT
cells.append(md(
    "## Sorting (`ORDER BY`)\n\n"
    "**SQL:**\n"
    "```sql\n"
    "SELECT VendorName, InvoiceTotal\n"
    "FROM Invoices i JOIN Vendors v ...\n"
    "ORDER BY InvoiceTotal DESC;\n"
    "```\n\n"
    "**Pandas:** `.sort_values()` with `ascending=False` for descending."
))
cells.append(code('invoices_pd.sort_values("InvoiceTotal", ascending=False).head()'))
practice_question(
    "**Practice:** Sort `vendors_pd` by `VendorName` alphabetically. Show the first 5 rows.",
    'vendors_pd.sort_values("VendorName").head()',
)

# New columns
cells.append(md(
    "## Creating New Columns\n\n"
    "**SQL:**\n"
    "```sql\n"
    "SELECT InvoiceTotal, PaymentTotal,\n"
    "       InvoiceTotal - PaymentTotal AS BalanceDue\n"
    "FROM Invoices;\n"
    "```\n\n"
    "**Pandas:** Assign to a new column name with `df[\"new_col\"] = ...`"
))
cells.append(code(
    'sample = invoices_pd[["InvoiceTotal", "PaymentTotal"]].copy()\n'
    'sample["BalanceDue"] = sample["InvoiceTotal"] - sample["PaymentTotal"]\n'
    'sample.head()'
))
practice_question(
    "**Practice:** Add a column `IsLarge` to a copy of `invoices_pd` that is `True` when `InvoiceTotal > 5000`.",
    'inv_copy = invoices_pd.copy()\n'
    'inv_copy["IsLarge"] = inv_copy["InvoiceTotal"] > 5000\n'
    'inv_copy[["InvoiceID", "InvoiceTotal", "IsLarge"]].head()',
)

# Aggregates
cells.append(md(
    "## Aggregate Functions (`COUNT`, `AVG`, `MIN`, `MAX`)\n\n"
    "**SQL:**\n"
    "```sql\n"
    "SELECT AVG(InvoiceTotal), MAX(InvoiceTotal), MIN(InvoiceTotal)\n"
    "FROM Invoices;\n"
    "```\n\n"
    "**Pandas:** Call `.mean()`, `.max()`, `.min()`, `.count()` on a column."
))
cells.append(code(
    'print("Average:", invoices_pd["InvoiceTotal"].mean())\n'
    'print("Max:", invoices_pd["InvoiceTotal"].max())\n'
    'print("Min:", invoices_pd["InvoiceTotal"].min())\n'
    'print("Count:", invoices_pd["InvoiceTotal"].count())'
))
practice_question(
    "**Practice:** What is the average `TermsDueDays` in `terms_pd`?",
    'terms_pd["TermsDueDays"].mean()',
)

# GROUP BY
cells.append(md(
    "## Group By (`GROUP BY`)\n\n"
    "**SQL:**\n"
    "```sql\n"
    "SELECT VendorState, COUNT(*) AS NumVendors\n"
    "FROM Vendors\n"
    "GROUP BY VendorState\n"
    "ORDER BY NumVendors DESC;\n"
    "```\n\n"
    "**Pandas:** `.groupby(\"col\").agg(...)` or `.groupby(\"col\")[\"col2\"].mean()`"
))
cells.append(code(
    'vendors_pd.groupby("VendorState").size().sort_values(ascending=False).head(10)'
))
cells.append(code(
    'invoices_pd.groupby("TermsID")["InvoiceTotal"].agg(["count", "mean", "max"]).round(2)'
))
practice_question(
    "**Practice:** Group `invoices_pd` by `VendorID` and compute the sum of `InvoiceTotal`. Sort descending, show top 5.",
    'invoices_pd.groupby("VendorID")["InvoiceTotal"].sum().sort_values(ascending=False).head()',
)

# DISTINCT
cells.append(md(
    "## Distinct (`DISTINCT` / `SELECT DISTINCT`)\n\n"
    "**SQL:**\n"
    "```sql\n"
    "SELECT DISTINCT VendorState FROM Vendors;\n"
    "```\n\n"
    "**Pandas:** `.drop_duplicates()` or `.unique()` on a column."
))
cells.append(code('sorted(vendors_pd["VendorState"].unique())'))
cells.append(code('vendors_pd[["VendorState"]].drop_duplicates().sort_values("VendorState").head(10)'))
practice_question(
    "**Practice:** How many distinct `TermsID` values appear in `invoices_pd`?",
    'invoices_pd["TermsID"].nunique()',
)

# HEAD / LIMIT
cells.append(md(
    "## Head / Limit (`TOP` / `LIMIT`)\n\n"
    "**SQL:**\n"
    "```sql\n"
    "SELECT TOP 5 VendorName FROM Vendors ORDER BY VendorName;\n"
    "```\n\n"
    "**Pandas:** `.head(n)` returns the first *n* rows (after sorting if needed)."
))
cells.append(code('vendors_pd.sort_values("VendorName").head(5)[["VendorName"]]'))
practice_question(
    "**Practice:** Show the 3 invoices with the highest `InvoiceTotal`.",
    'invoices_pd.nlargest(3, "InvoiceTotal")[["InvoiceID", "InvoiceTotal"]]',
)

# JOIN
cells.append(md(
    "## Joins (`JOIN`)\n\n"
    "**SQL:**\n"
    "```sql\n"
    "SELECT v.VendorName, i.InvoiceNumber, i.InvoiceTotal\n"
    "FROM Invoices i\n"
    "INNER JOIN Vendors v ON i.VendorID = v.VendorID;\n"
    "```\n\n"
    "**Pandas:** `pd.merge(left, right, on=\"key\")` or `how=\"inner\"`."
))
cells.append(code(
    'inv_vendors = pd.merge(\n'
    '    invoices_pd,\n'
    '    vendors_pd[["VendorID", "VendorName", "VendorState"]],\n'
    '    on="VendorID",\n'
    '    how="inner"\n'
    ')\n'
    'inv_vendors[["VendorName", "InvoiceNumber", "InvoiceTotal"]].head()'
))
practice_question(
    "**Practice:** Join `invoices_pd` with `terms_pd` on `TermsID`. Show `InvoiceID`, `InvoiceTotal`, and `TermsDescription` for the first 5 rows.",
    'pd.merge(invoices_pd, terms_pd, on="TermsID")[["InvoiceID", "InvoiceTotal", "TermsDescription"]].head()',
)

# --- Section 7: SQL → Polars ---
section_start(7, "SQL → Polars")
cells.append(md(
    "Polars uses a **method-chaining** style that reads similarly to SQL. "
    "It is newer, often **faster on large datasets**, and increasingly used in modern data science "
    "(including newer Berkeley Data Science curriculum).\n\n"
    "Same pattern: SQL → Polars → practice."
))

cells.append(md(
    "## Selecting Columns — `select()`\n\n"
    "```sql\n"
    "SELECT VendorName, VendorState FROM Vendors;\n"
    "```"
))
cells.append(code('vendors_pl.select("VendorName", "VendorState").head()'))
practice_question(
    "**Practice:** Select `InvoiceID` and `InvoiceTotal` from `invoices_pl`.",
    'invoices_pl.select("InvoiceID", "InvoiceTotal").head()',
)

cells.append(md(
    "## Filtering — `filter()`\n\n"
    "```sql\n"
    "SELECT * FROM Invoices WHERE InvoiceTotal > 10000;\n"
    "```"
))
cells.append(code('invoices_pl.filter(pl.col("InvoiceTotal") > 10000).head()'))
practice_question(
    "**Practice:** Filter vendors where `VendorState` is `'TN'`.",
    'vendors_pl.filter(pl.col("VendorState") == "TN")',
)

cells.append(md(
    "## New Columns — `with_columns()`\n\n"
    "```sql\n"
    "SELECT InvoiceTotal - PaymentTotal AS BalanceDue FROM Invoices;\n"
    "```"
))
cells.append(code(
    'invoices_pl.with_columns(\n'
    '    (pl.col("InvoiceTotal") - pl.col("PaymentTotal")).alias("BalanceDue")\n'
    ').select("InvoiceID", "InvoiceTotal", "PaymentTotal", "BalanceDue").head()'
))
practice_question(
    "**Practice:** Add a column `DoubleTotal` = `InvoiceTotal * 2`.",
    'invoices_pl.with_columns(\n'
    '    (pl.col("InvoiceTotal") * 2).alias("DoubleTotal")\n'
    ').select("InvoiceID", "InvoiceTotal", "DoubleTotal").head()',
)

cells.append(md(
    "## Group By — `group_by()` + `agg()`\n\n"
    "```sql\n"
    "SELECT TermsID, AVG(InvoiceTotal) FROM Invoices GROUP BY TermsID;\n"
    "```"
))
cells.append(code(
    'invoices_pl.group_by("TermsID").agg(\n'
    '    pl.col("InvoiceTotal").mean().alias("AvgTotal"),\n'
    '    pl.col("InvoiceID").count().alias("InvoiceCount")\n'
    ')'
))
practice_question(
    "**Practice:** Count vendors per `VendorState`, sorted by count descending.",
    'vendors_pl.group_by("VendorState").agg(\n'
    '    pl.len().alias("NumVendors")\n'
    ').sort("NumVendors", descending=True)',
)

cells.append(md(
    "## Sort — `sort()`\n\n"
    "```sql\n"
    "SELECT * FROM Invoices ORDER BY InvoiceTotal DESC;\n"
    "```"
))
cells.append(code('invoices_pl.sort("InvoiceTotal", descending=True).head(5)'))
practice_question(
    "**Practice:** Sort `terms_pl` by `TermsDueDays` ascending.",
    'terms_pl.sort("TermsDueDays")',
)

cells.append(md(
    "## Distinct — `unique()`\n\n"
    "```sql\n"
    "SELECT DISTINCT VendorState FROM Vendors;\n"
    "```"
))
cells.append(code('vendors_pl.select("VendorState").unique().sort("VendorState")'))
practice_question(
    "**Practice:** Get unique `TermsID` values from `invoices_pl`.",
    'invoices_pl.select("TermsID").unique()',
)

cells.append(md(
    "## Head — `head()`\n\n"
    "```sql\n"
    "SELECT TOP 5 * FROM Vendors;\n"
    "```"
))
cells.append(code('vendors_pl.head(5)'))
practice_question(
    "**Practice:** Show the top 3 rows of `terms_pl`.",
    'terms_pl.head(3)',
)

cells.append(md(
    "## Joins — `join()`\n\n"
    "```sql\n"
    "SELECT v.VendorName, i.InvoiceTotal\n"
    "FROM Invoices i JOIN Vendors v ON i.VendorID = v.VendorID;\n"
    "```"
))
cells.append(code(
    'invoices_pl.join(\n'
    '    vendors_pl.select("VendorID", "VendorName"),\n'
    '    on="VendorID",\n'
    '    how="inner"\n'
    ').select("VendorName", "InvoiceNumber", "InvoiceTotal").head()'
))
practice_question(
    "**Practice:** Join invoices with terms; show `InvoiceID`, `InvoiceTotal`, `TermsDescription`.",
    'invoices_pl.join(terms_pl, on="TermsID").select(\n'
    '    "InvoiceID", "InvoiceTotal", "TermsDescription"\n'
    ').head()',
)

# --- Section 8: Comparison ---
section_start(8, "Pandas vs Polars — Side-by-Side")
cells.append(md(
    "| Operation | SQL | Pandas | Polars |\n"
    "|-----------|-----|--------|--------|\n"
    "| Select columns | `SELECT col1, col2` | `df[[\"col1\", \"col2\"]]` | `df.select(\"col1\", \"col2\")` |\n"
    "| Filter rows | `WHERE col > 10` | `df[df[\"col\"] > 10]` | `df.filter(pl.col(\"col\") > 10)` |\n"
    "| Group & aggregate | `GROUP BY ... AVG()` | `df.groupby(\"col\").mean()` | `df.group_by(\"col\").agg(...)` |\n"
    "| Count | `COUNT(*)` | `df.groupby(...).size()` | `pl.len()` or `.count()` |\n"
    "| Limit rows | `TOP 5` / `LIMIT 5` | `df.head(5)` | `df.head(5)` |\n"
    "| Distinct | `SELECT DISTINCT col` | `df[\"col\"].unique()` | `df.select(\"col\").unique()` |\n"
    "| Join | `JOIN ... ON` | `pd.merge(df1, df2, on=...)` | `df1.join(df2, on=...)` |\n"
    "| Sort | `ORDER BY col DESC` | `df.sort_values(\"col\", ascending=False)` | `df.sort(\"col\", descending=True)` |\n\n"
    "> **When to use which?** Pandas has the largest ecosystem and most tutorials. "
    "Polars is often faster and has a cleaner API for chained transformations. "
    "Both are valuable — learn Pandas first, then add Polars."
))

# --- Section 9: Practice Problems ---
section_start(9, "Practice Problems")
cells.append(md(
    "Use **either Pandas or Polars** (your choice). Work through these in order — "
    "each builds on SQL skills you already have.\n\n"
    "Data files: `Vendors.csv`, `Invoices.csv`, `Terms.csv`, `GLAccounts.csv`, `InvoiceLineItems.csv`"
))

problems = [
    (
        "**Problem 1.** Show only vendor names (`VendorName`) from the Vendors table.",
        'vendors_pd[["VendorName"]].head()\n# Polars: vendors_pl.select("VendorName").head()',
    ),
    (
        "**Problem 2.** Find invoices with `InvoiceTotal` greater than 10,000.",
        'invoices_pd[invoices_pd["InvoiceTotal"] > 10000][["InvoiceID", "InvoiceTotal"]]',
    ),
    (
        "**Problem 3.** Sort invoices by `InvoiceTotal` from highest to lowest. Show the top 10.",
        'invoices_pd.sort_values("InvoiceTotal", ascending=False).head(10)[["InvoiceID", "InvoiceTotal"]]',
    ),
    (
        "**Problem 4.** Find the average `InvoiceTotal` for each `TermsID`.",
        'invoices_pd.groupby("TermsID")["InvoiceTotal"].mean().round(2)',
    ),
    (
        "**Problem 5.** Count how many vendors are in each `VendorState`. Sort by count descending.",
        'vendors_pd.groupby("VendorState").size().sort_values(ascending=False)',
    ),
    (
        "**Problem 6.** Find the single invoice with the highest `InvoiceTotal`. Show `InvoiceID`, `VendorID`, and `InvoiceTotal`.",
        'invoices_pd.loc[invoices_pd["InvoiceTotal"].idxmax(), ["InvoiceID", "VendorID", "InvoiceTotal"]]',
    ),
    (
        "**Problem 7.** Join `Invoices` and `Vendors` to show `VendorName`, `InvoiceNumber`, and `InvoiceTotal` for all invoices.",
        'pd.merge(invoices_pd, vendors_pd[["VendorID", "VendorName"]], on="VendorID")[["VendorName", "InvoiceNumber", "InvoiceTotal"]].head()',
    ),
    (
        "**Problem 8.** How many invoices have a `PaymentDate` of `NULL` (unpaid)? Hint: use `.isna()`.",
        'invoices_pd["PaymentDate"].isna().sum()',
    ),
    (
        "**Problem 9.** For each vendor state, what is the **total** invoice amount? "
        "(Join invoices to vendors first, then group by state.)",
        'pd.merge(invoices_pd, vendors_pd[["VendorID", "VendorState"]], on="VendorID")\n'
        '  .groupby("VendorState")["InvoiceTotal"].sum()\n'
        '  .sort_values(ascending=False)\n'
        '  .head(10)',
    ),
    (
        "**Problem 10.** Load `InvoiceLineItems.csv` and find the average line-item amount (`InvoiceLineItemAmount`) "
        "for each `AccountNo`. Join with `GLAccounts` to show `AccountDescription` too.",
        'line_items = pd.read_csv("InvoiceLineItems.csv")\n'
        'gl = pd.read_csv("GLAccounts.csv")\n'
        'summary = line_items.groupby("AccountNo")["InvoiceLineItemAmount"].mean().reset_index()\n'
        'pd.merge(summary, gl, on="AccountNo").sort_values("InvoiceLineItemAmount", ascending=False).head(10)',
    ),
]

for prob, sol in problems:
    practice_question(prob, sol, "# Your solution here\n")

# --- Section 10: Mini Challenge ---
section_start(10, "Mini Challenge")
cells.append(md(
    "The **AP manager** wants a report showing the **average invoice total for every payment term**, "
    "sorted from **highest average to lowest**, including the term description.\n\n"
    "Expected columns: `TermsDescription`, `AvgInvoiceTotal`\n\n"
    "Complete this using Pandas or Polars in the cell below.\n\n"
    + solution_block(
        '# Pandas solution\n'
        'report = (\n'
        '    pd.merge(invoices_pd, terms_pd, on="TermsID")\n'
        '    .groupby(["TermsID", "TermsDescription"])["InvoiceTotal"]\n'
        '    .mean()\n'
        '    .reset_index(name="AvgInvoiceTotal")\n'
        '    .sort_values("AvgInvoiceTotal", ascending=False)\n'
        ')\n'
        'report'
    )
))
cells.append(code("# Mini challenge — your solution\n"))

# Optional viz
cells.append(md(
    "### Optional: Quick Visualization\n\n"
    "Visualization is not the focus of this notebook, but a simple bar chart can make the challenge "
    "result easier to present."
))
cells.append(code(
    'import matplotlib.pyplot as plt\n\n'
    'plt.figure(figsize=(8, 4))\n'
    'plt.bar(report["TermsDescription"], report["AvgInvoiceTotal"])\n'
    'plt.xticks(rotation=15, ha="right")\n'
    'plt.ylabel("Average Invoice Total ($)")\n'
    'plt.title("Average Invoice Total by Payment Term")\n'
    'plt.tight_layout()\n'
    'plt.show()'
))

# --- Section 11: Why Polars ---
section_start(11, "Why Learn Polars?")
cells.append(md(
    "**Performance.** Polars is written in Rust and uses parallel execution. On datasets with "
    "millions of rows, it is often significantly faster than Pandas.\n\n"
    "**Modern data science.** New tools and courses (including updated Berkeley Data Science "
    "material) are introducing Polars alongside Pandas.\n\n"
    "**Growing adoption.** Companies handling large-scale analytics increasingly evaluate Polars "
    "for ETL and exploratory analysis pipelines.\n\n"
    "**Industry relevance.** SQL remains the language of databases; Pandas remains the most common "
    "Python tabular library; Polars is the fast, modern alternative worth knowing.\n\n"
    "**Practical advice:** Master SQL first (done!). Add Pandas for the Python ecosystem. "
    "Learn Polars when you need speed or cleaner chained expressions. All three skills complement each other."
))

# --- Section 12: Cheat Sheet ---
section_start(12, "Cheat Sheet")
cells.append(md(
    "Bookmark this page — return here when translating SQL to Python.\n\n"
    "| Task | SQL | Pandas | Polars |\n"
    "|------|-----|--------|--------|\n"
    "| Load CSV | *(external)* | `pd.read_csv(\"file.csv\")` | `pl.read_csv(\"file.csv\")` |\n"
    "| Preview rows | `SELECT TOP 5 *` | `df.head()` | `df.head()` |\n"
    "| Select columns | `SELECT a, b` | `df[[\"a\", \"b\"]]` | `df.select(\"a\", \"b\")` |\n"
    "| Filter | `WHERE x > 5` | `df[df[\"x\"] > 5]` | `df.filter(pl.col(\"x\") > 5)` |\n"
    "| Sort | `ORDER BY x DESC` | `df.sort_values(\"x\", ascending=False)` | `df.sort(\"x\", descending=True)` |\n"
    "| New column | `SELECT a + b AS c` | `df[\"c\"] = df[\"a\"] + df[\"b\"]` | `df.with_columns((pl.col(\"a\")+pl.col(\"b\")).alias(\"c\"))` |\n"
    "| Mean | `AVG(x)` | `df[\"x\"].mean()` | `df[\"x\"].mean()` |\n"
    "| Count | `COUNT(*)` | `df.groupby(\"g\").size()` | `df.group_by(\"g\").agg(pl.len())` |\n"
    "| Group + agg | `GROUP BY g` | `df.groupby(\"g\")[\"x\"].mean()` | `df.group_by(\"g\").agg(pl.col(\"x\").mean())` |\n"
    "| Distinct | `SELECT DISTINCT x` | `df[\"x\"].unique()` | `df.select(\"x\").unique()` |\n"
    "| Join | `JOIN b ON a.id = b.id` | `pd.merge(a, b, on=\"id\")` | `a.join(b, on=\"id\")` |\n"
    "| Null check | `WHERE x IS NULL` | `df[\"x\"].isna()` | `pl.col(\"x\").is_null()` |\n"
    "| Row count | `COUNT(*)` | `len(df)` or `df.shape[0]` | `df.height` |\n\n"
    "---\n\n"
    "**Remember:** SQL retrieves data from databases. Pandas and Polars analyze data in Python. "
    "Together, they form the bridge from databases to modern data science."
))

cells.append(md(f"{HR}\n\n{HR_GOLD}"))
cells.append(md("*End of notebook. Restart & Run All to verify everything works from a clean state.*"))

notebook = {
    "nbformat": 4,
    "nbformat_minor": 5,
    "metadata": {
        "kernelspec": {
            "display_name": "Python (ecc-csci)",
            "language": "python",
            "name": "ecc-csci",
        },
        "language_info": {
            "name": "python",
            "pygments_lexer": "ipython3",
        },
    },
    "cells": cells,
}

OUT.write_text(json.dumps(notebook, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
print(f"Wrote {len(cells)} cells to {OUT}")

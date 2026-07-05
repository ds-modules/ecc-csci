# Introduction to Jupyter, Python, Pandas, and Polars for SQL Students

Educational materials for El Camino College CSCI — bridging SQL knowledge into Python data analysis.

## Purpose

The notebook `intro.ipynb` is **not** an introduction to programming. It assumes students have already spent approximately eight weeks learning SQL (`SELECT`, `FROM`, `WHERE`, `GROUP BY`, `JOIN`, aggregate functions, and related topics).

The goal is to show how the same analytical thinking transfers to **Pandas** and **Polars** in Python:

> You've learned how to retrieve data using SQL. Now let's analyze that same data using Python.

The notebook follows a Berkeley Data 8 / Data 100 style: short explanations, runnable examples, and practice questions throughout.

## Intended Audience

- Students coming from an SQL-focused course
- Learners who want to use Python for tabular data analysis without re-learning programming from scratch
- Anyone preparing for data science coursework that uses Jupyter notebooks

## Dataset

The **AP (Accounts Payable)** sample database is provided as SQL in `create_ap (1) (1).sql`. CSV files in the project root were extracted from that script so the notebook runs entirely in Python — no SQL Server required.

| File | Description |
|------|-------------|
| `Vendors.csv` | Vendor master records |
| `Invoices.csv` | Invoice headers |
| `Terms.csv` | Payment terms |
| `GLAccounts.csv` | General ledger accounts |
| `InvoiceLineItems.csv` | Invoice line details |
| `ContactUpdates.csv` | Vendor contact updates |

To regenerate CSVs from the SQL file:

```bash
python scripts/extract_sql_to_csv.py
```

## Software Requirements

- Python 3.10 or newer recommended
- Packages listed in `requirements.txt`

## Setup

```bash
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

## How to Run

1. Activate your virtual environment (see above).
2. Start Jupyter from the project root:

   ```bash
   jupyter notebook intro.ipynb
   ```

   Or with JupyterLab:

   ```bash
   jupyter lab intro.ipynb
   ```

3. Use **Kernel → Change Kernel → Python (ecc-csci)** (or select the `.venv` interpreter in Cursor).
4. Work through each section: read, run code, try practice questions, then expand the collapsible **Solution** sections to check your work.

If you see `ModuleNotFoundError: No module named 'polars'`, the notebook is using the wrong Python environment. From the project root run:

```bash
source .venv/bin/activate
pip install -r requirements.txt
python -m ipykernel install --prefix="$(pwd)/.venv" --name=ecc-csci --display-name="Python (ecc-csci)"
```

Then restart the notebook kernel and select **Python (ecc-csci)**.

## Repository Contents

| Path | Description |
|------|-------------|
| `intro.ipynb` | Main teaching notebook |
| `*.csv` | CSV files extracted from the AP SQL database (project root) |
| `scripts/extract_sql_to_csv.py` | SQL → CSV extraction utility |
| `scripts/build_notebook.py` | Notebook generator (optional maintenance) |
| `requirements.txt` | Python dependencies |

## Regenerating the Notebook

If you edit the notebook structure in `scripts/build_notebook.py`:

```bash
python scripts/build_notebook.py
```

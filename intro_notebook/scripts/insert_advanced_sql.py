#!/usr/bin/env python3
"""Insert Advanced SQL Concepts section into pandas.ipynb and renumber later sections."""

import json
import uuid
from pathlib import Path

NB_PATH = Path(__file__).resolve().parent.parent / "pandas.ipynb"
HR = '<hr style="border: 2px solid #003262">'


def mid():
    return str(uuid.uuid4())[:8]


def md(source: str):
    return {
        "cell_type": "markdown",
        "id": mid(),
        "metadata": {"tags": []},
        "source": [line + "\n" for line in source.split("\n")[:-1]]
        + ([source.split("\n")[-1]] if source.split("\n")[-1] else []),
    }


def md_block(source: str):
    """Markdown cell with proper trailing newlines on each line except last."""
    lines = source.split("\n")
    src = [ln + "\n" for ln in lines[:-1]]
    if lines[-1] != "" or len(lines) == 1:
        src.append(lines[-1])
    else:
        # source ended with newline — last empty already handled
        pass
    if not src:
        src = [""]
    # Ensure last line doesn't force extra issues: match notebook style
    if src and not src[-1].endswith("\n") and len(src) > 1:
        pass
    return {
        "cell_type": "markdown",
        "id": mid(),
        "metadata": {"tags": []},
        "source": src if src[-1:] != [""] or len(src) > 1 else [source],
    }


def code(source: str):
    lines = source.split("\n")
    src = [ln + "\n" for ln in lines[:-1]]
    src.append(lines[-1] if lines[-1] else "")
    if src and src[-1] == "" and len(src) > 1:
        # keep trailing newline style used in notebook: last line often has \n in separate form
        src[-1] = "\n"
        # Actually existing notebook uses: "line\n", "lastline" without trailing on last
        # Rebuild cleaner:
    lines = source.split("\n")
    if len(lines) == 1:
        src = [lines[0]]
    else:
        src = [ln + "\n" for ln in lines[:-1]] + [lines[-1]]
    return {
        "cell_type": "code",
        "execution_count": None,
        "id": mid(),
        "metadata": {"tags": []},
        "outputs": [],
        "source": src,
    }


def practice(prompt: str, solution: str, placeholder: str = "# Your code here\n"):
    text = (
        f"{prompt}\n\n"
        "<details>\n"
        "<summary><strong>Solution:</strong></summary>\n\n"
        f"```python\n{solution.rstrip()}\n```\n\n"
        "</details>"
    )
    return [md_block(text), code(placeholder.rstrip("\n") + "\n" if not placeholder.endswith("\n") else placeholder)]


def section_cells():
    out = []

    out.append(md_block(f"{HR}\n\n## 8. Advanced SQL Concepts in pandas and Polars"))
    out.append(
        md_block(
            "You already mapped basic SQL (`SELECT`, `WHERE`, `GROUP BY`, inner `JOIN`) to DataFrames.\n\n"
            "This section covers **advanced SQL ideas** you likely saw near the end of your SQL course:\n\n"
            "- Outer joins (`LEFT`, `RIGHT`, `FULL`)\n"
            "- Set operations (`UNION`, `UNION ALL`, `INTERSECT`, `EXCEPT`)\n"
            "- Subqueries\n"
            "- Recursive CTEs for hierarchical data\n\n"
            "> **Goal:** See each idea first as **SQL**, then as **pandas**, then as **Polars**, "
            "using small example tables you can inspect by eye."
        )
    )

    # --- Outer joins ---
    out.append(md_block("### Left, Right, and Full Outer Joins"))
    out.append(
        md_block(
            "Inner joins keep only matching keys. Outer joins also keep **unmatched** rows and fill missing side with `NULL`.\n\n"
            "We will use tiny `employees` and `departments` tables — some IDs match, some do not."
        )
    )
    out.append(
        code(
            "employees = pd.DataFrame(\n"
            "    {\n"
            '        "emp_id": [1, 2, 3, 4],\n'
            '        "emp_name": ["Ada", "Lin", "Sam", "Kai"],\n'
            '        "dept_id": [10, 20, 30, 40],  # 40 has no matching department\n'
            "    }\n"
            ")\n"
            "\n"
            "departments = pd.DataFrame(\n"
            "    {\n"
            '        "dept_id": [10, 20, 50],  # 50 has no matching employee\n'
            '        "dept_name": ["Sales", "Engineering", "Legal"],\n'
            "    }\n"
            ")\n"
            "\n"
            "employees_pl = pl.DataFrame(employees.to_dict(orient='list'))\n"
            "departments_pl = pl.DataFrame(departments.to_dict(orient='list'))\n"
            "\n"
            "display(employees)\n"
            "display(departments)"
        )
    )

    out.append(
        md_block(
            "**SQL (conceptual)**\n\n"
            "```sql\n"
            "-- LEFT JOIN: keep all employees; unmatched dept columns are NULL\n"
            "SELECT e.emp_name, d.dept_name\n"
            "FROM employees e\n"
            "LEFT JOIN departments d ON e.dept_id = d.dept_id;\n"
            "\n"
            "-- RIGHT JOIN: keep all departments; unmatched emp columns are NULL\n"
            "SELECT e.emp_name, d.dept_name\n"
            "FROM employees e\n"
            "RIGHT JOIN departments d ON e.dept_id = d.dept_id;\n"
            "\n"
            "-- FULL OUTER JOIN: keep unmatched rows from both sides\n"
            "SELECT e.emp_name, d.dept_name\n"
            "FROM employees e\n"
            "FULL OUTER JOIN departments d ON e.dept_id = d.dept_id;\n"
            "```\n\n"
            "| Join | Keeps unmatched rows from | Why nulls appear |\n"
            "|------|---------------------------|------------------|\n"
            "| `LEFT` | Left table (`employees`) | No matching `departments` row |\n"
            "| `RIGHT` | Right table (`departments`) | No matching `employees` row |\n"
            "| `FULL` | Both tables | Either side has no match |"
        )
    )

    out.append(md_block("**pandas** — `how=\"left\"`, `how=\"right\"`, `how=\"outer\"`"))
    out.append(
        code(
            'print("LEFT JOIN")\n'
            'display(pd.merge(employees, departments, on="dept_id", how="left"))\n'
            "\n"
            'print("RIGHT JOIN")\n'
            'display(pd.merge(employees, departments, on="dept_id", how="right"))\n'
            "\n"
            'print("FULL OUTER JOIN")\n'
            'display(pd.merge(employees, departments, on="dept_id", how="outer"))'
        )
    )

    out.append(md_block("**Polars** — same ideas with `how=` on `.join()`"))
    out.append(
        code(
            'print("LEFT JOIN")\n'
            'display(employees_pl.join(departments_pl, on="dept_id", how="left"))\n'
            "\n"
            'print("RIGHT JOIN")\n'
            'display(employees_pl.join(departments_pl, on="dept_id", how="right"))\n'
            "\n"
            'print("FULL OUTER JOIN")\n'
            'display(employees_pl.join(departments_pl, on="dept_id", how="full", coalesce=True))'
        )
    )

    out.extend(
        practice(
            "**Check Your Understanding (prediction):** Before running code, predict which names appear "
            "with a missing `dept_name` in a **LEFT** join of `employees` to `departments`. "
            "Then verify with pandas.\n\n"
            "*Write your answer in the cell below.*",
            'left_join = pd.merge(employees, departments, on="dept_id", how="left")\n'
            'left_join[left_join["dept_name"].isna()][["emp_name", "dept_id", "dept_name"]]\n'
            '# Kai (dept_id 40) has no matching department, so dept_name is null.',
        )
    )

    # --- Set ops ---
    out.append(md_block("### UNION ALL, UNION, INTERSECT, and EXCEPT"))
    out.append(
        md_block(
            "Set operations combine rows from two result sets with the **same columns**.\n\n"
            "- **`UNION ALL`** — stack all rows; keep duplicates\n"
            "- **`UNION`** — stack rows; **remove duplicates**\n"
            "- **`INTERSECT`** — rows that appear in **both**\n"
            "- **`EXCEPT`** (SQL Server: `EXCEPT`) — rows in the first set **but not** the second\n\n"
            "> **Key difference:** `UNION` drops duplicate rows; `UNION ALL` keeps them. "
            "`UNION ALL` is usually faster when you know duplicates are fine."
        )
    )

    out.append(
        code(
            "fall = pd.DataFrame(\n"
            "    {\n"
            '        "student_id": [1, 2, 3, 4],\n'
            '        "course": ["CSCI", "MATH", "CSCI", "HIST"],\n'
            "    }\n"
            ")\n"
            "\n"
            "spring = pd.DataFrame(\n"
            "    {\n"
            '        "student_id": [3, 4, 4, 5],\n'
            '        "course": ["CSCI", "HIST", "HIST", "CSCI"],  # (4, HIST) repeats; overlaps with fall\n'
            "    }\n"
            ")\n"
            "\n"
            "fall_pl = pl.DataFrame(fall.to_dict(orient='list'))\n"
            "spring_pl = pl.DataFrame(spring.to_dict(orient='list'))\n"
            "\n"
            'print("Fall enrollments")\n'
            "display(fall)\n"
            'print("Spring enrollments")\n'
            "display(spring)"
        )
    )

    out.append(
        md_block(
            "**SQL (conceptual)**\n\n"
            "```sql\n"
            "SELECT student_id, course FROM fall\n"
            "UNION ALL\n"
            "SELECT student_id, course FROM spring;\n"
            "\n"
            "SELECT student_id, course FROM fall\n"
            "UNION\n"
            "SELECT student_id, course FROM spring;\n"
            "\n"
            "SELECT student_id, course FROM fall\n"
            "INTERSECT\n"
            "SELECT student_id, course FROM spring;\n"
            "\n"
            "SELECT student_id, course FROM fall\n"
            "EXCEPT\n"
            "SELECT student_id, course FROM spring;\n"
            "```"
        )
    )

    out.append(md_block("**pandas**"))
    out.append(
        code(
            'union_all = pd.concat([fall, spring], ignore_index=True)\n'
            'union_distinct = pd.concat([fall, spring], ignore_index=True).drop_duplicates()\n'
            'intersect = pd.merge(fall, spring, on=["student_id", "course"], how="inner").drop_duplicates()\n'
            "\n"
            "except_rows = (\n"
            '    pd.merge(fall, spring, on=["student_id", "course"], how="left", indicator=True)\n'
            '    .query(\'_merge == "left_only"\')\n'
            '    .drop(columns="_merge")\n'
            ")\n"
            "\n"
            'print("UNION ALL"); display(union_all)\n'
            'print("UNION"); display(union_distinct)\n'
            'print("INTERSECT"); display(intersect)\n'
            'print("EXCEPT (fall minus spring)"); display(except_rows)'
        )
    )

    out.append(md_block("**Polars**"))
    out.append(
        code(
            "union_all_pl = pl.concat([fall_pl, spring_pl])\n"
            "union_pl = pl.concat([fall_pl, spring_pl]).unique()\n"
            'intersect_pl = fall_pl.join(spring_pl, on=["student_id", "course"], how="inner").unique()\n'
            'except_pl = fall_pl.join(spring_pl, on=["student_id", "course"], how="anti")\n'
            "\n"
            'print("UNION ALL"); display(union_all_pl)\n'
            'print("UNION"); display(union_pl)\n'
            'print("INTERSECT"); display(intersect_pl)\n'
            'print("EXCEPT"); display(except_pl)'
        )
    )

    out.append(
        md_block(
            "| Operation | SQL | Pandas | Polars |\n"
            "|-----------|-----|--------|--------|\n"
            "| Keep all rows (dupes OK) | `UNION ALL` | `pd.concat([a, b])` | `pl.concat([a, b])` |\n"
            "| Stack + distinct | `UNION` | `pd.concat(...).drop_duplicates()` | `pl.concat(...).unique()` |\n"
            "| Rows in both | `INTERSECT` | `pd.merge(..., how=\"inner\")` | `join(..., how=\"inner\")` |\n"
            "| In first, not second | `EXCEPT` | `merge(..., indicator=True)` then keep `left_only` | `join(..., how=\"anti\")` |"
        )
    )

    out.extend(
        practice(
            "**Practice:** Using `fall` and `spring`, create a **UNION ALL** result and count how many rows it has. "
            "Then create a **UNION** result and count those rows. How many duplicates were removed?\n\n"
            "*Write your answer in the cell below.*",
            "all_rows = pd.concat([fall, spring], ignore_index=True)\n"
            "distinct_rows = all_rows.drop_duplicates()\n"
            "print(len(all_rows), len(distinct_rows), len(all_rows) - len(distinct_rows))",
        )
    )

    # --- Subqueries ---
    out.append(md_block("### Subqueries"))
    out.append(
        md_block(
            "In SQL, a **subquery** is a query nested inside another query.\n\n"
            "In Python, that often becomes:\n\n"
            "- an **intermediate DataFrame** (list of keys), or\n"
            "- a **scalar value** (one number), which you then use to filter.\n\n"
            "We will reuse the AP `invoices_pd` / `vendors_pd` tables already loaded."
        )
    )

    out.append(
        md_block(
            "#### Example A — `WHERE ... IN (SELECT ...)`\n\n"
            "**SQL**\n"
            "```sql\n"
            "SELECT VendorName, VendorState\n"
            "FROM Vendors\n"
            "WHERE VendorID IN (\n"
            "    SELECT VendorID\n"
            "    FROM Invoices\n"
            "    WHERE InvoiceTotal > 10000\n"
            ");\n"
            "```\n\n"
            "The subquery finds vendor IDs with a large invoice; the outer query returns those vendors."
        )
    )

    out.append(md_block("**pandas** — clear intermediate variable first"))
    out.append(
        code(
            "large_invoice_vendor_ids = invoices_pd.loc[\n"
            '    invoices_pd["InvoiceTotal"] > 10000, "VendorID"\n'
            "]\n"
            "\n"
            "vendors_with_large_invoices = vendors_pd[\n"
            '    vendors_pd["VendorID"].isin(large_invoice_vendor_ids)\n'
            '][["VendorName", "VendorState"]]\n'
            "\n"
            "vendors_with_large_invoices.head()"
        )
    )

    out.append(md_block("Optional chained style (same idea, harder to debug):"))
    out.append(
        code(
            "(\n"
            "    vendors_pd[\n"
            '        vendors_pd["VendorID"].isin(\n'
            '            invoices_pd.loc[invoices_pd["InvoiceTotal"] > 10000, "VendorID"]\n'
            "        )\n"
            '    ][["VendorName", "VendorState"]]\n'
            ".head())"
        )
    )

    out.append(md_block("**Polars**"))
    out.append(
        code(
            "large_ids_pl = (\n"
            '    invoices_pl.filter(pl.col("InvoiceTotal") > 10000)\n'
            '    .select("VendorID")\n'
            ")\n"
            "\n"
            "(\n"
            "    vendors_pl.join(large_ids_pl, on=\"VendorID\", how=\"semi\")\n"
            '    .select("VendorName", "VendorState")\n'
            ".head())"
        )
    )

    out.append(
        md_block(
            "#### Example B — scalar subquery\n\n"
            "**SQL**\n"
            "```sql\n"
            "SELECT InvoiceID, InvoiceTotal\n"
            "FROM Invoices\n"
            "WHERE InvoiceTotal > (\n"
            "    SELECT AVG(InvoiceTotal) FROM Invoices\n"
            ");\n"
            "```"
        )
    )

    out.append(md_block("**pandas**"))
    out.append(
        code(
            'avg_invoice_total = invoices_pd["InvoiceTotal"].mean()\n'
            "\n"
            "above_average = invoices_pd[\n"
            '    invoices_pd["InvoiceTotal"] > avg_invoice_total\n'
            '][["InvoiceID", "InvoiceTotal"]]\n'
            "\n"
            "print(\"Average InvoiceTotal:\", round(avg_invoice_total, 2))\n"
            "above_average.head()"
        )
    )

    out.append(md_block("**Polars**"))
    out.append(
        code(
            'avg_total_pl = invoices_pl.select(pl.col("InvoiceTotal").mean()).item()\n'
            "\n"
            "(\n"
            '    invoices_pl.filter(pl.col("InvoiceTotal") > avg_total_pl)\n'
            '    .select("InvoiceID", "InvoiceTotal")\n'
            ".head())"
        )
    )

    out.extend(
        practice(
            "**Check Your Understanding:** In one sentence, explain what a SQL subquery usually becomes "
            "when you rewrite it in pandas.\n\n"
            "*Write a short comment or print statement in the cell below.*",
            'print("A SQL subquery usually becomes an intermediate Series/DataFrame of keys, "\n'
            '      "or a scalar value, that you reuse in a later filter/join.")',
        )
    )

    # --- Recursive CTE ---
    out.append(md_block("### Recursive CTEs and Hierarchical Data"))
    out.append(
        md_block(
            "Org charts are **hierarchical**: each employee may report to a manager, who reports to another manager.\n\n"
            "SQL solves this with a **recursive CTE**. **pandas and Polars do not have recursive CTE syntax** — "
            "you express the same idea with a clear loop (or repeated joins) in Python."
        )
    )

    out.append(
        md_block(
            "We will use this instructor-provided Employees data exactly:\n\n"
            "| Column | Meaning |\n"
            "|--------|---------|\n"
            "| `EmployeeID` | Unique employee key |\n"
            "| `LastName`, `FirstName` | Name parts |\n"
            "| `TitleID` | Job title key (not used in the hierarchy walk) |\n"
            "| `ManagerID` | EmployeeID of this person's manager (`NULL` = top of tree) |"
        )
    )

    out.append(
        code(
            "employee_data = [\n"
            '    (1, "Smith", "Cindy", 2, None),\n'
            '    (2, "Jones", "Elmer", 4, 1),\n'
            '    (3, "Simonian", "Ralph", 2, 2),\n'
            '    (4, "Hernandez", "Olivia", 1, 2),\n'
            '    (5, "Aaronsen", "Robert", 2, 3),\n'
            '    (6, "Watson", "Denise", 6, 3),\n'
            '    (7, "Hardy", "Thomas", 5, 2),\n'
            '    (8, "O\'Leary", "Rhea", 4, 2),\n'
            '    (9, "Locario", "Paulo", 6, 1),\n'
            "]\n"
            "\n"
            "employees_hier = pd.DataFrame(\n"
            "    employee_data,\n"
            '    columns=["EmployeeID", "LastName", "FirstName", "TitleID", "ManagerID"],\n'
            ")\n"
            "employees_hier"
        )
    )

    out.append(
        md_block(
            "**Original SQL recursive CTE (from the instructor)**\n\n"
            "```sql\n"
            "WITH EmployeesCTE AS\n"
            "(\n"
            "    -- Base case: employees with no manager (top of hierarchy)\n"
            "    SELECT\n"
            "        EmployeeID,\n"
            "        LastName,\n"
            "        FirstName,\n"
            "        ManagerID,\n"
            "        1 AS Rank\n"
            "    FROM Employees\n"
            "    WHERE ManagerID IS NULL\n"
            "\n"
            "    UNION ALL\n"
            "\n"
            "    -- Recursive case: employees who report to someone already in the CTE\n"
            "    SELECT\n"
            "        e.EmployeeID,\n"
            "        e.LastName,\n"
            "        e.FirstName,\n"
            "        e.ManagerID,\n"
            "        c.Rank + 1 AS Rank\n"
            "    FROM Employees AS e\n"
            "    JOIN EmployeesCTE AS c\n"
            "      ON e.ManagerID = c.EmployeeID\n"
            ")\n"
            "SELECT\n"
            "    Rank,\n"
            "    EmployeeID,\n"
            "    LastName + ', ' + FirstName AS EmployeeName,\n"
            "    ManagerID\n"
            "FROM EmployeesCTE\n"
            "ORDER BY Rank, EmployeeID;\n"
            "```\n\n"
            "- **Base case:** start with rows where `ManagerID IS NULL` and set `Rank = 1`\n"
            "- **Recursive case:** find employees whose `ManagerID` matches an `EmployeeID` already found; "
            "set `Rank = manager Rank + 1`\n"
            "- Repeat until no new reports are found"
        )
    )

    out.append(
        md_block(
            "#### pandas: `build_employee_hierarchy()`\n\n"
            "A beginner-readable `while` loop mirrors the CTE: start at the top, then keep attaching direct reports."
        )
    )

    out.append(
        code(
            "def build_employee_hierarchy(employees_df: pd.DataFrame) -> pd.DataFrame:\n"
            '    """Build Ranked hierarchy like the recursive EmployeesCTE."""\n'
            "    levels = []\n"
            "\n"
            "    # Base case: no manager\n"
            '    current = employees_df[employees_df["ManagerID"].isna()].copy()\n'
            '    current["Rank"] = 1\n'
            "    levels.append(current)\n"
            "\n"
            "    # Recursive case: keep finding direct reports\n"
            "    while True:\n"
            '        managers = current[["EmployeeID", "Rank"]].rename(\n'
            '            columns={"EmployeeID": "ManagerID", "Rank": "ManagerRank"}\n'
            "        )\n"
            "        nxt = employees_df.merge(managers, on=\"ManagerID\", how=\"inner\").copy()\n"
            "        if nxt.empty:\n"
            "            break\n"
            '        nxt["Rank"] = nxt["ManagerRank"] + 1\n'
            '        nxt = nxt.drop(columns=["ManagerRank"])\n'
            "        levels.append(nxt)\n"
            "        current = nxt\n"
            "\n"
            "    hierarchy = pd.concat(levels, ignore_index=True)\n"
            '    hierarchy["EmployeeName"] = hierarchy["LastName"] + ", " + hierarchy["FirstName"]\n'
            "    hierarchy = hierarchy.sort_values([\"Rank\", \"EmployeeID\"]).reset_index(drop=True)\n"
            '    return hierarchy[["Rank", "EmployeeID", "EmployeeName", "ManagerID"]]\n'
            "\n"
            "\n"
            "hierarchy = build_employee_hierarchy(employees_hier)\n"
            "display(hierarchy)\n"
            'print("Ranks present:", sorted(hierarchy["Rank"].unique().tolist()))\n'
            'assert sorted(hierarchy["Rank"].unique().tolist()) == [1, 2, 3, 4]'
        )
    )

    out.append(
        md_block(
            "#### Polars note\n\n"
            "Polars also has **no recursive CTE**. You can run the **same Python `while` loop** and use "
            "Polars only for filters/joins inside each step, or convert with `pl.DataFrame(hierarchy.to_dict(orient="list"))` "
            "after the pandas function finishes.\n\n"
            "Keeping the loop in plain Python is usually clearer for this topic."
        )
    )

    out.append(
        code(
            "# Optional: view the finished hierarchy as a Polars DataFrame\n"
            "hierarchy_pl = pl.DataFrame(hierarchy.to_dict(orient='list'))\n"
            "hierarchy_pl"
        )
    )

    out.extend(
        practice(
            "**Practice:** Add a new employee who reports to **Robert Aaronsen** "
            "(find Robert's `EmployeeID` in the table). "
            "Rebuild the hierarchy and report the new employee's **Rank**.\n\n"
            "Suggested new row: `EmployeeID=10`, `LastName=\"Nguyen\"`, `FirstName=\"Alex\"`, "
            "`TitleID=2`, `ManagerID=<Robert's EmployeeID>`.\n\n"
            "*Write your answer in the cell below.*",
            "robert_id = employees_hier.loc[\n"
            '    (employees_hier["LastName"] == "Aaronsen")\n'
            '    & (employees_hier["FirstName"] == "Robert"),\n'
            '    "EmployeeID",\n'
            "].iloc[0]\n"
            "\n"
            "employees_with_new = pd.concat(\n"
            "    [\n"
            "        employees_hier,\n"
            "        pd.DataFrame(\n"
            "            [{\n"
            '                "EmployeeID": 10,\n'
            '                "LastName": "Nguyen",\n'
            '                "FirstName": "Alex",\n'
            '                "TitleID": 2,\n'
            '                "ManagerID": robert_id,\n'
            "            }]\n"
            "        ),\n"
            "    ],\n"
            "    ignore_index=True,\n"
            ")\n"
            "\n"
            "hierarchy_new = build_employee_hierarchy(employees_with_new)\n"
            'new_rank = hierarchy_new.loc[hierarchy_new["EmployeeID"] == 10, "Rank"].iloc[0]\n'
            'print("Robert EmployeeID:", robert_id)\n'
            'print("Alex Nguyen Rank:", int(new_rank))\n'
            "hierarchy_new.tail()"
        )
    )

    return out


def source_text(cell):
    return "".join(cell.get("source", []))


def main():
    nb = json.loads(NB_PATH.read_text())
    cells = nb["cells"]

    # Update learning objectives if present
    for cell in cells:
        if cell.get("cell_type") != "markdown":
            continue
        text = source_text(cell)
        if text.startswith("## Learning Objectives"):
            if "outer joins" not in text.lower() and "recursive" not in text.lower():
                cell["source"] = [
                    "## Learning Objectives\n",
                    "\n",
                    "By the end of this notebook, you should be able to:\n",
                    "\n",
                    "- Navigate and run cells in a Jupyter notebook\n",
                    "- Load tabular data into **DataFrames** with Pandas and Polars\n",
                    "- Translate common SQL operations into Pandas syntax\n",
                    "- Translate the same operations into Polars syntax\n",
                    "- Use advanced SQL ideas in Python: **outer joins**, **set operations**, **subqueries**, and **hierarchical (recursive) data**\n",
                    "- Explain why Python is commonly used **after** SQL in data workflows",
                ]
            break

    # Find insertion point: before "## 8. Pandas vs Polars"
    insert_at = None
    for i, cell in enumerate(cells):
        text = source_text(cell)
        if "## 8. Pandas vs Polars" in text:
            insert_at = i
            break
    if insert_at is None:
        raise SystemExit("Could not find section 8 insertion point")

    # Skip if already inserted
    already = any("Advanced SQL Concepts" in source_text(c) for c in cells)
    if already:
        print("Advanced SQL section already present — skipping insert")
    else:
        new_cells = section_cells()
        cells[insert_at:insert_at] = new_cells
        print(f"Inserted {len(new_cells)} cells at index {insert_at}")

    # Renumber later section headings if needed
    renames = [
        ("## 8. Pandas vs Polars — Side-by-Side", "## 9. Pandas vs Polars — Side-by-Side"),
        ("## 9. Practice Problems", "## 10. Practice Problems"),
        ("## 10. Mini Challenge", "## 11. Mini Challenge"),
        ("## 11. Why Learn Polars?", "## 12. Why Learn Polars?"),
        ("## 12. Cheat Sheet", "## 13. Cheat Sheet"),
    ]
    for cell in cells:
        if cell.get("cell_type") != "markdown":
            continue
        text = source_text(cell)
        for old, new in renames:
            if old in text and "Advanced SQL" not in text:
                cell["source"] = [s.replace(old, new) for s in cell["source"]]
                break

    # Extend cheat sheet with advanced ops if cheat sheet exists and lacks UNION
    for cell in cells:
        if cell.get("cell_type") != "markdown":
            continue
        text = source_text(cell)
        if "## 13. Cheat Sheet" in text or ("## 12. Cheat Sheet" in text and "Advanced SQL Concepts" not in "".join(source_text(c) for c in cells)):
            pass
        if "Cheat Sheet" in text and "UNION ALL" not in text:
            # append advanced rows before Remember line if present
            extra = (
                "| Left/right/full join | `LEFT/RIGHT/FULL JOIN` | `pd.merge(..., how=...)` | `df.join(..., how=...)` |\n"
                "| Union all | `UNION ALL` | `pd.concat([a, b])` | `pl.concat([a, b])` |\n"
                "| Union distinct | `UNION` | `pd.concat(...).drop_duplicates()` | `pl.concat(...).unique()` |\n"
                "| Intersect | `INTERSECT` | `pd.merge(..., how=\"inner\")` | `join(..., how=\"inner\")` |\n"
                "| Except | `EXCEPT` | `merge(..., indicator=True)` | `join(..., how=\"anti\")` |\n"
                "| Subquery IN | `WHERE x IN (SELECT...)` | `.isin(intermediate)` | `join(..., how=\"semi\")` |\n"
            )
            new_src = []
            for s in cell["source"]:
                if s.startswith("| Row count"):
                    new_src.append(extra)
                if "**Remember:**" in s and "UNION ALL" not in "".join(new_src):
                    # ensure extra added before remember if row count missing
                    if extra not in "".join(new_src):
                        new_src.append(extra)
                new_src.append(s)
            cell["source"] = new_src
            break

    # Comparison table section: add a note pointing to advanced section
    for cell in cells:
        if cell.get("cell_type") != "markdown":
            continue
        text = source_text(cell)
        if "Pandas vs Polars — Side-by-Side" in text and "Outer joins" not in text:
            # The content cell after the heading
            pass
        if text.startswith("| Operation | SQL | Pandas | Polars |") and "FULL JOIN" not in text:
            lines = cell["source"]
            # insert advanced rows before the closing callout if any
            insert_lines = [
                "| Outer join | `LEFT/RIGHT/FULL JOIN` | `pd.merge(..., how=\"left/right/outer\")` | `df.join(..., how=\"left/right/full\")` |\n",
                "| Union / Union all | `UNION` / `UNION ALL` | `concat` (+ `drop_duplicates`) | `concat` (+ `unique`) |\n",
                "| Except | `EXCEPT` | `merge` + `indicator` | `join(..., how=\"anti\")` |\n",
            ]
            new_lines = []
            for s in lines:
                if s.startswith("> **When to use which?"):
                    new_lines.extend(insert_lines)
                    new_lines.append("\n")
                new_lines.append(s)
            cell["source"] = new_lines

    nb["cells"] = cells
    NB_PATH.write_text(json.dumps(nb, indent=1, ensure_ascii=False) + "\n")
    print(f"Wrote {NB_PATH} with {len(cells)} cells")


if __name__ == "__main__":
    main()

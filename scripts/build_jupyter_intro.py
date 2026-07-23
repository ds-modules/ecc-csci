#!/usr/bin/env python3
"""Generate a Jupyter-only intro that prepares students for pandas.ipynb."""

import json
from pathlib import Path

OUT = Path(__file__).resolve().parent.parent / "intro.ipynb"
HR = '<hr style="border: 2px solid #003262">'
HR_GOLD = '<hr style="border: 2px solid #C9B676">'


def md(source: str):
    return {
        "cell_type": "markdown",
        "metadata": {},
        "source": [source],
    }


def code(source: str):
    return {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [source],
    }


def section(number: int, title: str):
    cells.append(md(f"{HR}\n\n## {number}. {title}"))


def practice(prompt: str, solution: str, placeholder: str = "# Your code here\n"):
    """Match pandas.ipynb format: instructions + dropdown Solution in one markdown cell, then a code cell."""
    cells.append(
        md(
            f"{prompt}\n\n"
            "<details>\n"
            "<summary><strong>Solution:</strong></summary>\n\n"
            f"```python\n{solution.rstrip()}\n```\n\n"
            "</details>"
        )
    )
    cells.append(code(placeholder))


cells = []

# Title
cells.append(
    md(
        "# Introduction to Jupyter Notebooks\n"
        "##### Professor: Joanna\n"
        "##### Developed by: Ariana Ghimire"
    )
)

# 1. Welcome
cells.append(md(f"{HR}\n\n{HR_GOLD}\n\n## 1. Welcome"))
cells.append(
    md(
        "This notebook teaches **only Jupyter** — the tool you will use for the rest of this unit.\n\n"
        "You already know **SQL**. Next you will open `pandas.ipynb` and analyze data with Python. "
        "Before that, you need to be comfortable running notebook cells, fixing common mistakes, "
        "and using the same practice format you will see later.\n\n"
        "> *Jupyter is where you write explanations and runnable code in one document.*"
    )
)

cells.append(
    md(
        "## Learning Objectives\n\n"
        "By the end of this notebook, you should be able to do everything Jupyter requires "
        "for `pandas.ipynb`:\n\n"
        "- Open a `.ipynb` file and navigate Markdown vs Code cells\n"
        "- Run cells with `Shift + Enter`\n"
        "- Add, delete, and convert cells with keyboard shortcuts\n"
        "- Write simple Markdown (headings, bold, lists, tables, inline code)\n"
        "- Understand why **cell order** matters\n"
        "- Use **Kernel → Restart & Run All**\n"
        "- Choose the correct Python kernel when imports fail\n"
        "- Run `import` cells and recognize a successful import\n"
        "- Know that CSV files must be in the notebook's working folder\n"
        "- Complete practice questions using the collapsible **Solution** dropdown"
    )
)

cells.append(
    md(
        "> **How to use this notebook:** Read each short section, run the code cell immediately "
        "below it, and try the practice question before expanding the **Solution** section to "
        "check your work."
    )
)

# 2. What is Jupyter
section(2, "What Is a Jupyter Notebook?")
cells.append(
    md(
        "A **Jupyter notebook** mixes:\n\n"
        "- **Text** — instructions and explanations\n"
        "- **Code** — Python you can run\n"
        "- **Output** — results shown under each code cell\n\n"
        "Notebook files end in `.ipynb`. This file and `pandas.ipynb` are both notebooks.\n\n"
        "That format is why notebooks are used in data classes: learn → run → practice → check."
    )
)

# 3. Cells
section(3, "Markdown Cells vs Code Cells")
cells.append(
    md(
        "Everything lives in a **cell**.\n\n"
        "| Cell type | Purpose | How you recognize it |\n"
        "|-----------|---------|----------------------|\n"
        "| **Markdown** | Titles, explanations, tables, practice instructions | Formatted text after you run it |\n"
        "| **Code** | Python you execute | `In [ ]:` on the left |\n\n"
        "In `pandas.ipynb`, lessons are Markdown and examples/practice answers go in Code cells.\n\n"
        "- Click once to **select** a cell\n"
        "- Double-click a Markdown cell to **edit** it\n"
        "- Press `Shift + Enter` to **run** it"
    )
)

cells.append(
    md(
        "**Exercise:** Run the cell below. You should see a greeting printed.\n\n"
        "<details>\n"
        "<summary><strong>Solution:</strong></summary>\n\n"
        "Press `Shift + Enter` while the code cell below is selected. "
        "You should see output under the cell.\n\n"
        "</details>"
    )
)
cells.append(code('print("Hello from Jupyter! You ran your first cell.")'))

# 4. Running cells
section(4, "Running Cells")
cells.append(
    md(
        "These are the run shortcuts you will use constantly in `pandas.ipynb`:\n\n"
        "| Shortcut | What it does |\n"
        "|----------|--------------|\n"
        "| `Shift + Enter` | Run cell and move to the next one |\n"
        "| `Ctrl + Enter` (Windows) / `Cmd + Enter` (Mac) | Run cell and stay on it |\n\n"
        "You can also click the **Run** button in the toolbar.\n\n"
        "Code output always appears **directly under** the cell that produced it."
    )
)

practice(
    "**Practice:** Change the text inside the quotes below to your first name, then run the cell "
    "with `Shift + Enter`.\n\n"
    "*Write your answer in the cell below.*",
    'print("Ariana")',
)

# 5. Edit vs Command mode + shortcuts
section(5, "Edit Mode, Command Mode, and Shortcuts")
cells.append(
    md(
        "Jupyter has two modes:\n\n"
        "- **Edit mode** — cursor is inside the cell; you are typing\n"
        "- **Command mode** — cell is selected, but you are not typing inside it\n\n"
        "| Action | How |\n"
        "|--------|-----|\n"
        "| Enter Edit mode | Press `Enter`, or click inside the cell |\n"
        "| Enter Command mode | Press `Esc` |\n\n"
        "`pandas.ipynb` expects you to use these Command-mode shortcuts:\n\n"
        "| Shortcut | Action |\n"
        "|----------|--------|\n"
        "| `A` | Insert cell **above** |\n"
        "| `B` | Insert cell **below** |\n"
        "| `D`, `D` | Delete selected cell (press D twice) |\n"
        "| `M` | Change cell to **Markdown** |\n"
        "| `Y` | Change cell to **Code** |\n\n"
        "> Tip: Press `Esc` first, then the shortcut."
    )
)

practice(
    "**Practice:** In Command mode, press `B` to add a cell below, press `M` to make it Markdown, "
    "type `## Ready for Pandas`, then run it with `Shift + Enter`.\n\n"
    "*Do this in the notebook UI. The code cell below can hold notes if you want.*",
    "# Example Markdown you would type in the new cell:\n"
    "## Ready for Pandas",
    "# (Optional notes — the real practice is creating a Markdown cell with B then M)\n",
)

# 6. Markdown basics (needed to read pandas.ipynb)
section(6, "Markdown You Will See in Class Notebooks")
cells.append(
    md(
        "`pandas.ipynb` uses Markdown heavily: headings, tables, SQL examples in backticks, "
        "and collapsible Solutions.\n\n"
        "Double-click the next cell to see the source, then run it to see the formatted result."
    )
)
cells.append(
    md(
        "## Sample heading\n\n"
        "**Bold** and *italic*\n\n"
        "- Bullet list item\n\n"
        "Inline code: `SELECT * FROM Vendors`\n\n"
        "| SQL | Jupyter |\n"
        "|-----|---------|\n"
        "| Query data | Run analysis |\n\n"
        "> Blockquotes are used for tips and “how to use this notebook” notes."
    )
)

practice(
    "**Practice:** In a Markdown cell, write:\n"
    "1. A heading with your name\n"
    "2. One bold sentence about SQL\n"
    "3. A bullet list of three SQL keywords you know\n\n"
    "*Create/edit a Markdown cell for this. You can also draft it in the code cell as comments.*",
    "## Ariana\n\n"
    "**I already know how to filter rows with WHERE.**\n\n"
    "- SELECT\n"
    "- JOIN\n"
    "- GROUP BY",
    "# Draft Markdown here as comments if helpful, or use a real Markdown cell above\n",
)

# 7. Practice format used in pandas.ipynb
section(7, "How Practice Questions Work in This Class")
cells.append(
    md(
        "In `pandas.ipynb`, almost every concept ends with the same pattern:\n\n"
        "1. A **Markdown** cell with the question\n"
        "2. A collapsible **Solution** dropdown in that same Markdown cell\n"
        "3. A **Code** cell underneath that says `# Your code here`\n\n"
        "Your job:\n\n"
        "- Try the problem in the code cell first\n"
        "- Only then click **Solution** to check\n\n"
        "Click the triangle / **Solution** label below to see how a dropdown works."
    )
)

practice(
    "**Practice:** Create a variable `weeks = 8` and print it.\n\n"
    "*Write your answer in the cell below.*",
    "weeks = 8\nprint(weeks)",
)

# 8. Execution order
section(8, "Cell Order Matters")
cells.append(
    md(
        "Notebooks remember variables from cells you already ran.\n\n"
        "> If a later cell uses a name from an earlier cell, you must run the earlier cell first.\n\n"
        "This is critical in `pandas.ipynb`: import cells and `read_csv` cells must run "
        "before practice cells that use those DataFrames."
    )
)

cells.append(md("Run these two cells **in order**:"))
cells.append(code('course = "CSCI"\nprint("Saved the course name.")'))
cells.append(code('print("Welcome to", course)'))

cells.append(
    md(
        "If you skip the first cell, the second cell raises `NameError` because `course` "
        "was never defined.\n\n"
        "When things get confusing, use:\n\n"
        "**Kernel → Restart & Run All**\n\n"
        "That clears memory and re-runs every cell from the top — exactly what you should do "
        "before trusting a finished notebook."
    )
)

practice(
    "**Practice:** In one cell, create `tool = \"Jupyter\"`. In the next cell (or the same practice cell), "
    "print a sentence that includes `tool`.\n\n"
    "*Write your answer in the cell below.*",
    'tool = "Jupyter"\nprint("I am learning", tool)',
)

# 9. Kernel
section(9, "The Kernel (Very Important for pandas.ipynb)")
cells.append(
    md(
        "The **kernel** is the Python engine behind your notebook.\n\n"
        "| Action | When to use it |\n"
        "|--------|----------------|\n"
        "| **Interrupt** | A cell is stuck |\n"
        "| **Restart** | Clear all variables |\n"
        "| **Restart & Run All** | Verify the whole notebook top-to-bottom |\n"
        "| **Change Kernel** | Imports fail / wrong Python environment |\n\n"
        "`pandas.ipynb` imports Pandas and Polars. If you see:\n\n"
        "`ModuleNotFoundError: No module named 'polars'`\n\n"
        "your notebook is using the wrong Python. Fix it with:\n\n"
        "**Kernel → Change Kernel → Python (ecc-csci)**\n"
        "(or the `.venv` / class environment your instructor named)\n\n"
        "Then re-run the import cell."
    )
)

practice(
    "**Practice:** Find **Kernel** in the menu and locate these three items: "
    "**Interrupt**, **Restart**, and **Restart & Run All**. "
    "You do not need to restart right now — just confirm you can find them.\n\n"
    "*Type `found` in the cell below when you have located the menu items.*",
    'print("found")',
)

# 10. Imports (Jupyter workflow, not Pandas teaching)
section(10, "Running Import Cells")
cells.append(
    md(
        "Near the start of `pandas.ipynb` you will run a cell like:\n\n"
        "```python\n"
        "import pandas as pd\n"
        "import polars as pl\n"
        "```\n\n"
        "You do **not** need to understand Pandas yet. You do need to know:\n\n"
        "1. Run the import cell with `Shift + Enter`\n"
        "2. If it errors, change the kernel, then run it again\n"
        "3. A successful import usually shows no error (and may print a version number)\n\n"
        "Try a tiny import now:"
    )
)
cells.append(code("import math\nprint(math.pi)"))

practice(
    "**Practice:** Import the built-in `statistics` module and print `statistics.mean([10, 20, 30])`.\n\n"
    "*Write your answer in the cell below.*",
    "import statistics\nprint(statistics.mean([10, 20, 30]))",
)

# 11. Working directory / files
section(11, "Files and Working Directory")
cells.append(
    md(
        "`pandas.ipynb` loads CSV files with names like `Vendors.csv`.\n\n"
        "That works only if:\n\n"
        "- Jupyter was started from the folder that contains those CSVs, **or**\n"
        "- the notebook and CSV files live in the same project folder students are told to use\n\n"
        "If you see `FileNotFoundError`, you are usually in the wrong folder.\n\n"
        "Check your current folder with:"
    )
)
cells.append(code("import os\nprint(os.getcwd())"))

practice(
    "**Practice:** Run a cell that prints the current working directory, then list files in that "
    "directory with `os.listdir('.')` (show just the first 10 names).\n\n"
    "*Write your answer in the cell below.*",
    "import os\nprint(os.getcwd())\nprint(os.listdir('.')[:10])",
)

# 12. Reading errors
section(12, "Reading Common Errors")
cells.append(
    md(
        "You will see errors in `pandas.ipynb`. Read the **last line** first.\n\n"
        "| Error | Usual meaning | What to do |\n"
        "|-------|---------------|------------|\n"
        "| `NameError` | Variable not defined yet | Run earlier cells, or Restart & Run All |\n"
        "| `ModuleNotFoundError` | Wrong Python / package missing | Change kernel / install packages |\n"
        "| `FileNotFoundError` | CSV path / folder is wrong | Check working directory and file names |\n"
        "| `SyntaxError` | Typo in Python code | Fix quotes, parentheses, commas |\n\n"
        "Errors are normal while learning. Fix the cause, then re-run the cell."
    )
)

practice(
    "**Practice:** The cell below is broken on purpose. Fix it so it prints `100`.\n\n"
    "*Edit the code cell below.*",
    "print(100)",
    "print(100\n",
)

# 13. Saving + scrolling / navigation
section(13, "Saving and Moving Around a Long Notebook")
cells.append(
    md(
        "`pandas.ipynb` is long. Useful habits:\n\n"
        "- **Save often** — `Ctrl/Cmd + S`, or rely on Jupyter autosave\n"
        "- Use the **Table of Contents** / sidebar outline if your Jupyter shows one\n"
        "- Jump by scrolling to section headers (`## 6. SQL → Pandas`, etc.)\n"
        "- After big edits, do **Restart & Run All** once\n\n"
        "Do not delete example cells unless your instructor asks you to. "
        "Add your work in the `# Your code here` cells."
    )
)

practice(
    "**Practice:** Save this notebook now (`Ctrl/Cmd + S`). Then type `saved` in the cell below.\n\n"
    "*Write your answer in the cell below.*",
    'print("saved")',
)

# 14. Mini checklist matching pandas workflow
section(14, "Final Jupyter Checklist")
cells.append(
    md(
        "Complete this checklist the same way you will work in `pandas.ipynb`.\n\n"
        "1. Print your first name.\n"
        "2. Create `ready = True` and print it.\n"
        "3. Import `math` and print `math.sqrt(49)`.\n\n"
        "Use the code cell below for all three (or add extra cells with `B`)."
    )
)

practice(
    "**Practice:** Complete the three checklist tasks above.\n\n"
    "*Write your answer in the cell below.*",
    'print("Ariana")\n'
    "ready = True\n"
    "print(ready)\n"
    "import math\n"
    "print(math.sqrt(49))",
)

# 15. What's next
section(15, "You Are Ready for pandas.ipynb")
cells.append(
    md(
        "If you can do the skills in this notebook, you have the Jupyter tools needed for the next file.\n\n"
        "In `intro_notebook/pandas.ipynb` you will:\n\n"
        "- Run setup / import cells at the top\n"
        "- Load CSV files\n"
        "- Follow SQL → Pandas / Polars examples\n"
        "- Solve practices with `# Your code here` and check the **Solution** dropdown\n\n"
        "Before you start that notebook:\n\n"
        "1. Open it from the `intro_notebook` folder\n"
        "2. Select the class kernel if needed\n"
        "3. Use **Restart & Run All** after you finish a section\n\n"
        "Pandas and Polars are taught there — not here."
    )
)

cells.append(md(f"{HR}\n\n{HR_GOLD}"))
cells.append(
    md(
        "*End of notebook. Use **Kernel → Restart & Run All** to confirm everything works "
        "from a clean start.*"
    )
)

notebook = {
    "nbformat": 4,
    "nbformat_minor": 5,
    "metadata": {
        "kernelspec": {
            "display_name": "Python 3",
            "language": "python",
            "name": "python3",
        },
        "language_info": {
            "name": "python",
            "pygments_lexer": "ipython3",
        },
    },
    "cells": cells,
}

OUT.write_text(json.dumps(notebook, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
print(f"Wrote {len(cells)} cells -> {OUT}")
print("Practice dropdowns:", sum(1 for c in cells if "<details>" in "".join(c["source"])))

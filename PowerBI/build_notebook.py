#!/usr/bin/env python3
"""Generate PowerBI_Intro.ipynb — project-based Power BI dashboard course."""

import json
from pathlib import Path

OUT = Path(__file__).resolve().parent / "PowerBI_Intro.ipynb"
HR = '<hr style="border: 2px solid #003262">'
HR_GOLD = '<hr style="border: 2px solid #C9B676">'


def md(source: str):
    lines = source.split("\n")
    src = [ln + "\n" for ln in lines[:-1]] + ([lines[-1]] if lines[-1] != "" else [])
    if not src:
        src = [""]
    return {"cell_type": "markdown", "metadata": {}, "source": src}


def code(source: str):
    lines = source.split("\n")
    src = [ln + "\n" for ln in lines[:-1]] + ([lines[-1]] if lines[-1] != "" else [])
    return {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": src if src else [""],
    }


def section(number, title: str):
    cells.append(md(f"{HR}\n\n## {number}. {title}"))


def part(title: str):
    cells.append(md(f"{HR}\n\n{HR_GOLD}\n\n# {title}"))


def pbi_exercise(prompt: str, solution: str):
    """Power BI Desktop exercise (not Python)."""
    cells.append(
        md(
            f"{prompt}\n\n"
            "<details>\n"
            "<summary><strong>Solution:</strong></summary>\n\n"
            f"{solution.rstrip()}\n\n"
            "</details>"
        )
    )


cells = []

# ---------------------------------------------------------------------------
# Title
# ---------------------------------------------------------------------------
cells.append(
    md(
        "# Power BI with Python: Building Interactive Dashboards\n"
        "##### Professor: Joanna\n"
        "##### Developed by: Ariana Ghimire"
    )
)

# ---------------------------------------------------------------------------
# 0. Introduction
# ---------------------------------------------------------------------------
cells.append(md(f"{HR}\n\n{HR_GOLD}\n\n## 0. Introduction"))
cells.append(
    md(
        "You already know how to prepare data with **SQL** and **pandas** "
        "(see the SQL → Pandas notebook).\n\n"
        "This notebook answers a different question:\n\n"
        "> **Now that I've prepared my data, how do I turn it into an interactive dashboard?**\n\n"
        "**Time split:** spend about **20%** of class time in Jupyter (export a clean CSV) "
        "and about **80%** in **Power BI Desktop** (query, model, DAX, visuals, design).\n\n"
        "This is a **project notebook**, not a Python lecture. Most “exercises” happen in Power BI."
    )
)

cells.append(
    md(
        "### What you'll learn\n\n"
        "By the end of this notebook you'll be able to:\n\n"
        "- Prepare data for Power BI\n"
        "- Export datasets from Python\n"
        "- Import data into Power BI\n"
        "- Understand Power Query vs DAX\n"
        "- Build an interactive dashboard\n"
        "- Create measures and calculated columns\n"
        "- Add slicers and filters\n"
        "- Design a clean dashboard"
    )
)

cells.append(
    md(
        "### Table of Contents\n\n"
        "0. [Introduction](#0-introduction)\n"
        "1. [Why Power BI?](#1-why-power-bi)\n"
        "2. [Preparing Data in Python](#2-preparing-data-in-python)\n"
        "3. [Before Opening Power BI](#3-before-opening-power-bi)\n"
        "4. [Importing Data](#4-importing-data) *(Power Query)*\n"
        "5. [Power Query Basics](#5-power-query-basics)\n"
        "6. [Data Types](#6-data-types)\n"
        "7. [Tables & Relationships](#7-tables--relationships)\n"
        "8. [Star Schema (optional)](#8-star-schema-optional)\n"
        "9. [Calculated Columns](#9-calculated-columns) *(DAX)*\n"
        "10. [Measures](#10-measures)\n"
        "11. [Context](#11-context)\n"
        "12. [Common DAX Functions](#12-common-dax-functions)\n"
        "13–22. [Visualizations](#13-cards)\n"
        "23–25. [Dashboard Design](#23-dashboard-layout)\n"
        "26. [Final Project](#26-final-project)"
    )
)

# ---------------------------------------------------------------------------
# 1. Why Power BI?
# ---------------------------------------------------------------------------
section(1, "Why Power BI?")
cells.append(
    md(
        "Power BI is a **business intelligence (BI)** tool. It turns cleaned tables into "
        "**interactive reports** that managers and teams can click, filter, and explore.\n\n"
        "```\n"
        "SQL Database\n"
        "      ↓\n"
        "Python (pandas)\n"
        "      ↓\n"
        "Clean Dataset\n"
        "      ↓\n"
        "Power BI\n"
        "      ↓\n"
        "Interactive Dashboard\n"
        "```\n\n"
        "| Tool | Best for |\n"
        "|------|----------|\n"
        "| **SQL** | Retrieving and joining data from databases |\n"
        "| **Python (pandas)** | Cleaning, reshaping, feature engineering, automation |\n"
        "| **Power BI** | Interactive visuals, slicers, sharing dashboards with non-coders |\n\n"
        "**Why businesses use BI tools**\n\n"
        "- Non-analysts can explore data without writing code\n"
        "- Filters and slicers answer “what if?” questions live\n"
        "- One published report can replace dozens of static Excel charts\n\n"
        "**When to use each**\n\n"
        "- Use **Python** when the data is messy or you need repeatable prep\n"
        "- Use **Power BI** when the audience needs an interactive dashboard\n"
        "- Do **not** re-clean the same mess every week only inside Power BI if Python already fixed it"
    )
)

# ---------------------------------------------------------------------------
# 2. Preparing Data in Python (SHORT)
# ---------------------------------------------------------------------------
section(2, "Preparing Data in Python")
cells.append(
    md(
        "Keep this section short — you already know pandas.\n\n"
        "We only prep Spotify song data enough to export a clean file for Power BI.\n\n"
        "Dataset: `data.csv` (teaching subset of a public Spotify songs dataset)."
    )
)

cells.append(md("### Load CSV and quick inspection"))
cells.append(
    code(
        "import pandas as pd\n"
        "\n"
        "songs = pd.read_csv(\"data.csv\")\n"
        "print(songs.shape)\n"
        "songs.head()"
    )
)
cells.append(code('songs[["name", "artists", "year", "popularity", "energy", "danceability"]].describe(include="all")'))

cells.append(
    md(
        "### Clean for the dashboard\n\n"
        "- Drop columns Power BI does not need for this project\n"
        "- Keep readable names\n"
        "- Create a `decade` feature (great for bar charts and slicers)\n"
        "- Keep missing values visible so Power Query / DAX decisions are intentional"
    )
)
cells.append(
    code(
        "# Keep a focused set of columns for the dashboard\n"
        "keep = [\n"
        '    "name",\n'
        '    "artists",\n'
        '    "year",\n'
        '    "popularity",\n'
        '    "danceability",\n'
        '    "energy",\n'
        '    "valence",\n'
        '    "tempo",\n'
        '    "explicit",\n'
        "]\n"
        "dashboard = songs[keep].copy()\n"
        "\n"
        "# Feature for Power BI grouping / slicers\n"
        'dashboard["decade"] = (dashboard["year"] // 10) * 10\n'
        "\n"
        "# Optional: tidy artist strings that look like Python lists\n"
        'dashboard["artists"] = (\n'
        '    dashboard["artists"]\n'
        '    .astype(str)\n'
        '    .str.replace(r"^\\[\'|\'\\]$", "", regex=True)\n'
        '    .str.replace("\', \'", ", ")\n'
        ")\n"
        "\n"
        "dashboard = dashboard.rename(\n"
        "    columns={\n"
        '        "name": "Song",\n'
        '        "artists": "Artist",\n'
        '        "year": "Year",\n'
        '        "decade": "Decade",\n'
        '        "popularity": "Popularity",\n'
        '        "danceability": "Danceability",\n'
        '        "energy": "Energy",\n'
        '        "valence": "Valence",\n'
        '        "tempo": "Tempo",\n'
        '        "explicit": "Explicit",\n'
        "    }\n"
        ")\n"
        "\n"
        "dashboard.head()"
    )
)

cells.append(md("### Export CSV for Power BI"))
cells.append(
    code(
        'dashboard.to_csv("dashboard_data.csv", index=False)\n'
        'print("Wrote dashboard_data.csv with", len(dashboard), "rows")\n'
        "dashboard.dtypes"
    )
)
cells.append(
    md(
        "> **Checkpoint:** After you run the cell above, you should have `dashboard_data.csv` "
        "in this folder. Everything from here on happens in **Power BI Desktop**.\n\n"
        "> Tip: You can also keep using `spotify_dashboard.csv` if your instructor provided it — "
        "same idea, slightly different column names. This notebook assumes **`dashboard_data.csv`**."
    )
)

# ---------------------------------------------------------------------------
# 3. Before Opening Power BI
# ---------------------------------------------------------------------------
section(3, "Before Opening Power BI")
cells.append(
    md(
        "Power BI Desktop has a few important areas. Learn the names before you click around.\n\n"
        "| Area | What it is |\n"
        "|------|------------|\n"
        "| **Power Query** | Transform raw tables (rename, types, filter) *before* they load into the model |\n"
        "| **Data View** | Spreadsheet-like view of loaded tables |\n"
        "| **Model View** | Relationships between tables (lines between boxes) |\n"
        "| **Report View** | Where you build visuals and the dashboard canvas |\n\n"
        "**Power Query vs DAX (preview)**\n\n"
        "| | Power Query | DAX |\n"
        "|--|-------------|-----|\n"
        "| When | During import / refresh | After data is loaded |\n"
        "| Job | Shape and clean columns | Calculate columns & measures for visuals |\n"
        "| Feels like | Excel Transform / ETL | Formulas that respect filters |\n\n"
        "> **Screenshot placeholders** (instructor can paste real UI captures):\n"
        ">\n"
        "> 1. Report View with the Visualizations pane\n"
        "> 2. Data View showing a table\n"
        "> 3. Model View with table cards\n"
        "> 4. Power Query Editor ribbon"
    )
)

# ---------------------------------------------------------------------------
# Part II — Power Query
# ---------------------------------------------------------------------------
part("Part II — Power Query")

section(4, "Importing Data")
cells.append(
    md(
        "Open **Power BI Desktop**, then:\n\n"
        "1. **Home → Get data → Text/CSV**\n"
        "2. Select `dashboard_data.csv` from this folder\n"
        "3. Preview the table\n"
        "4. Click **Transform Data** (opens Power Query Editor) — do **not** click Load yet "
        "if you want to clean first\n\n"
        "> If you already clicked Load, you can still open Power Query with "
        "**Home → Transform data**."
    )
)
pbi_exercise(
    "**Power BI exercise:** Import `dashboard_data.csv` and open Power Query. "
    "How many columns do you see?",
    "You should see 10 columns: Song, Artist, Year, Popularity, Danceability, Energy, "
    "Valence, Tempo, Explicit, Decade.",
)

section(5, "Power Query Basics")
cells.append(
    md(
        "In Power Query Editor, practice these transforms on your Spotify table "
        "(or a temporary copy of a column if you want to experiment safely).\n\n"
        "| Skill | Where |\n"
        "|-------|-------|\n"
        "| Rename columns | Double-click header, or right-click → Rename |\n"
        "| Change data types | Click the type icon left of the column name |\n"
        "| Filter rows | Column filter dropdown |\n"
        "| Replace values | Right-click column → Replace Values |\n"
        "| Split columns | Transform → Split Column |\n"
        "| Merge columns | Select columns → Transform → Merge Columns |\n"
        "| Sort | Column dropdown → Sort Ascending / Descending |\n"
        "| Remove duplicates | Home / Transform → Remove Rows → Remove Duplicates |\n"
        "| **Close & Apply** | Home → Close & Apply (loads changes into the model) |\n\n"
        "For this project you may not need every transform — the Python export is already tidy. "
        "Still practice **rename**, **types**, and **Close & Apply** so you can fix future messy CSVs."
    )
)
pbi_exercise(
    "**Power BI exercise:** In Power Query, confirm `Year` and `Decade` are whole numbers "
    "and `Song` / `Artist` are text. Then **Close & Apply**.",
    "Click the ABC/123 icon on each column header and set:\n"
    "- Song, Artist → Text\n"
    "- Year, Decade, Popularity, Explicit → Whole Number\n"
    "- Danceability, Energy, Valence, Tempo → Decimal Number\n\n"
    "Then Home → Close & Apply.",
)

section(6, "Data Types")
cells.append(
    md(
        "Wrong data types break visuals and DAX.\n\n"
        "| Type | Example in this project |\n"
        "|------|-------------------------|\n"
        "| Text | Song, Artist |\n"
        "| Whole Number | Year, Decade, Popularity |\n"
        "| Decimal | Danceability, Energy, Tempo |\n"
        "| Date | *(not in this CSV — but common in other projects)* |\n"
        "| Boolean / True/False | Explicit (0/1 works as whole number too) |\n\n"
        "**Why it matters:** If `Year` is text, sorting may go `1999, 200, 2010…` and averages can fail."
    )
)
pbi_exercise(
    "**Power BI exercise (fix types):** Temporarily set `Popularity` to Text, try to create a "
    "Card with Average of Popularity, note the problem, then fix the type back to Whole Number.",
    "Average needs a numeric column. Change Popularity back to Whole Number "
    "(Power Query or Column tools in Data View), then recreate the card.",
)

# ---------------------------------------------------------------------------
# Part III — Data Model
# ---------------------------------------------------------------------------
part("Part III — Building the Data Model")

section(7, "Tables & Relationships")
cells.append(
    md(
        "Even with **one table**, learn the vocabulary — real projects usually have several tables.\n\n"
        "| Idea | Meaning |\n"
        "|------|---------|\n"
        "| **Fact table** | Events / measurements (here: each song row is a fact) |\n"
        "| **Dimension table** | Lookup attributes (Artist, Decade, Genre…) |\n"
        "| **Primary key** | Unique ID for a row in a dimension |\n"
        "| **Relationship** | Link between tables on a key |\n"
        "| **Many-to-one** | Many fact rows → one dimension row (many songs → one artist) |\n"
        "| **One-to-many** | Same idea from the other direction |\n\n"
        "Open **Model View**. With one table you will only see one box — that is fine for this project."
    )
)

section(8, "Star Schema (optional)")
cells.append(
    md(
        "A **star schema** is a common BI design:\n\n"
        "```\n"
        "          DimArtist\n"
        "              \\\n"
        "    DimDecade — FactSongs — DimYear\n"
        "              /\n"
        "         (other dims)\n"
        "```\n\n"
        "Facts hold measures (popularity, tempo). Dimensions hold labels for filtering and grouping.\n\n"
        "You do **not** need to split the Spotify file for the final project. Knowing the pattern "
        "helps when you later connect SQL tables that are already normalized."
    )
)

# ---------------------------------------------------------------------------
# Part IV — DAX
# ---------------------------------------------------------------------------
part("Part IV — DAX")
cells.append(
    md(
        "**DAX** (Data Analysis Expressions) is the formula language of Power BI.\n\n"
        "| | Calculated column | Measure |\n"
        "|--|-------------------|---------|\n"
        "| Runs | Once per row (stored) | On demand when a visual needs it |\n"
        "| Use for | Categories, flags, row labels | KPIs, totals, averages |\n"
        "| Respects slicers? | Value is fixed per row | Recalculates under filter context |"
    )
)

section(9, "Calculated Columns")
cells.append(
    md(
        "Calculated columns run **once per row**.\n\n"
        "In **Data View** / Table tools → **New column**, try:\n\n"
        "```dax\n"
        "Popularity Category =\n"
        "IF(\n"
        "    Songs[Popularity] >= 70, \"High\",\n"
        "    IF(Songs[Popularity] >= 40, \"Medium\", \"Low\")\n"
        ")\n"
        "```\n\n"
        "Replace `Songs` with your actual table name if Power BI named it `dashboard_data`.\n\n"
        "Other ideas:\n\n"
        "```dax\n"
        "Energy Level =\n"
        "IF(Songs[Energy] >= 0.7, \"High Energy\", \"Lower Energy\")\n"
        "```"
    )
)
pbi_exercise(
    "**Power BI exercise:** Create a calculated column `Popularity Category` "
    "(High / Medium / Low) using the thresholds above.",
    "```dax\n"
    "Popularity Category =\n"
    "IF(\n"
    "    'dashboard_data'[Popularity] >= 70, \"High\",\n"
    "    IF('dashboard_data'[Popularity] >= 40, \"Medium\", \"Low\")\n"
    ")\n"
    "```\n"
    "Use your table's real name if it differs.",
)

section(10, "Measures")
cells.append(
    md(
        "Measures are calculated **on demand** and change when slicers change.\n\n"
        "Create measures with **New measure**:\n\n"
        "```dax\n"
        "Song Count = COUNTROWS('dashboard_data')\n"
        "```\n\n"
        "```dax\n"
        "Avg Popularity = AVERAGE('dashboard_data'[Popularity])\n"
        "```\n\n"
        "```dax\n"
        "Total Popularity = SUM('dashboard_data'[Popularity])\n"
        "```\n\n"
        "```dax\n"
        "Artist Count = DISTINCTCOUNT('dashboard_data'[Artist])\n"
        "```\n\n"
        "```dax\n"
        "Avg Energy = AVERAGE('dashboard_data'[Energy])\n"
        "```\n\n"
        "Put each measure in a **Card** visual to test it."
    )
)
pbi_exercise(
    "**Power BI exercise:** Create at least these measures: `Song Count`, `Avg Popularity`, "
    "`Artist Count`. Add three Cards to the report page.",
    "Use COUNTROWS, AVERAGE, and DISTINCTCOUNT as shown above. "
    "Format Avg Popularity to 1 decimal place (Measure tools → Format).",
)

section(11, "Context")
cells.append(
    md(
        "This is where students usually struggle — and where Power BI becomes powerful.\n\n"
        "**Row context** — formulas that “walk” row by row (typical of calculated columns).\n\n"
        "**Filter context** — the set of rows currently visible because of:\n\n"
        "- Slicers\n"
        "- Visual filters\n"
        "- Cross-filtering from other charts\n"
        "- `CALCULATE` modifications\n\n"
        "**Interactive demo**\n\n"
        "1. Put `Avg Popularity` on a Card\n"
        "2. Add a **Decade** slicer\n"
        "3. Click different decades\n\n"
        "> What happens when you click a slicer?\n"
        "> The filter context shrinks to that decade’s rows, and the measure **recalculates**.\n"
        "> The calculated column `Popularity Category` on each row does **not** rewrite itself — "
        "but visuals that count those categories will only see filtered rows."
    )
)

section(12, "Common DAX Functions")
cells.append(
    md(
        "Small reference (bookmark this):\n\n"
        "| Function | Use |\n"
        "|----------|-----|\n"
        "| `SUM` | Add a numeric column |\n"
        "| `AVERAGE` | Mean of a column |\n"
        "| `COUNTROWS` | Count rows in a table |\n"
        "| `DISTINCTCOUNT` | Count unique values |\n"
        "| `DIVIDE` | Safe division (handles divide-by-zero) |\n"
        "| `CALCULATE` | Change filter context, then evaluate an expression |\n"
        "| `IF` | Conditional logic |\n"
        "| `SWITCH` | Cleaner multi-branch conditions |\n"
        "| `FORMAT` | Display numbers/dates as text |\n\n"
        "Example with `CALCULATE`:\n\n"
        "```dax\n"
        "High Popularity Songs =\n"
        "CALCULATE(\n"
        "    COUNTROWS('dashboard_data'),\n"
        "    'dashboard_data'[Popularity] >= 70\n"
        ")\n"
        "```"
    )
)

# ---------------------------------------------------------------------------
# Part V — Visualizations
# ---------------------------------------------------------------------------
part("Part V — Visualizations")

section(13, "Cards")
cells.append(
    md(
        "**Cards** show a single KPI.\n\n"
        "Good KPIs for this project:\n\n"
        "- Song Count\n"
        "- Avg Popularity\n"
        "- Artist Count\n"
        "- Avg Energy\n"
        "- High Popularity Songs (optional CALCULATE measure)\n\n"
        "Place 5 cards across the top of your page — that will satisfy the final project KPI requirement."
    )
)

section(14, "Bar Charts")
cells.append(
    md(
        "Build **Average Popularity by Decade**:\n\n"
        "1. Clustered bar chart (or column chart)\n"
        "2. Axis: `Decade`\n"
        "3. Values: Average of `Popularity` (or your `Avg Popularity` measure)\n"
        "4. Sort axis by Decade ascending"
    )
)

section(15, "Line Charts")
cells.append(
    md(
        "Build **Song Count by Year**:\n\n"
        "1. Line chart\n"
        "2. X-axis: `Year`\n"
        "3. Y-axis: Count of Song (or `Song Count`)\n\n"
        "Ask: does the sample have more songs in recent years?"
    )
)

section(16, "Scatter Plots")
cells.append(
    md(
        "Build **Energy vs Popularity**:\n\n"
        "1. Scatter chart\n"
        "2. X: `Energy`\n"
        "3. Y: `Popularity`\n"
        "4. Legend (optional): `Popularity Category` or `Explicit`\n"
        "5. Size (optional): `Danceability` or `Tempo`\n\n"
        "Turn on **tooltips** so hovering shows Song and Artist."
    )
)

section(17, "Maps (optional)")
cells.append(
    md(
        "This Spotify sample has **no location fields**, so skip maps for the final project.\n\n"
        "In other datasets, a Map visual needs city/country/latitude-longitude columns."
    )
)

section(18, "Tables & Matrix")
cells.append(
    md(
        "| Visual | Best for |\n"
        "|--------|----------|\n"
        "| **Table** | Flat list of rows (Song, Artist, Popularity) |\n"
        "| **Matrix** | Rows + columns with aggregation (e.g. Decade on rows, Explicit on columns) |\n\n"
        "Try a matrix with `Decade` on rows and Average Popularity as values."
    )
)

section(19, "Slicers")
cells.append(
    md(
        "Add slicers for interactivity:\n\n"
        "- `Decade` (list or dropdown)\n"
        "- `Popularity Category`\n"
        "- `Explicit`\n\n"
        "Slicer settings to try:\n\n"
        "- Dropdown vs List\n"
        "- Single select vs multi-select\n"
        "- **Sync slicers** across pages (View → Sync slicers) if you add a second report page"
    )
)

section(20, "Drill Down")
cells.append(
    md(
        "Hierarchy drill-down is very useful for dates:\n\n"
        "```\n"
        "Year\n"
        " ↓\n"
        "Month\n"
        " ↓\n"
        "Day\n"
        "```\n\n"
        "Our CSV only has `Year` / `Decade`. You can still:\n\n"
        "1. Create a hierarchy: Decade → Year (right-click fields in Data pane → New hierarchy)\n"
        "2. Put the hierarchy on a visual axis\n"
        "3. Use the drill icons on the visual header"
    )
)

section(21, "Cross Filtering")
cells.append(
    md(
        "One of Power BI’s coolest features: **clicking one chart filters another**.\n\n"
        "1. Click a decade bar\n"
        "2. Watch cards, scatter, and line chart update\n\n"
        "Edit interactions: **Format → Edit interactions** to control whether a visual "
        "filters, highlights, or ignores another."
    )
)

section(22, "Tooltips")
cells.append(
    md(
        "Default tooltips show the fields on the visual.\n\n"
        "**Custom tooltips (stretch goal):**\n\n"
        "1. Create a new report page named `Tooltip`\n"
        "2. Page information → allow use as tooltip; set page size to Tooltip\n"
        "3. Add a few cards / a small table\n"
        "4. On your main scatter → Format → Tooltips → Report page → Tooltip"
    )
)

# ---------------------------------------------------------------------------
# Part VI — Dashboard Design
# ---------------------------------------------------------------------------
part("Part VI — Dashboard Design")

section(23, "Dashboard Layout")
cells.append(
    md(
        "Many tutorials ignore design — do not.\n\n"
        "- **Alignment** — snap to grid; line up card tops\n"
        "- **Spacing** — even gaps; avoid overlapping visuals\n"
        "- **White space** — leave breathing room; do not fill every pixel\n"
        "- **Color consistency** — one accent color; avoid rainbow charts\n"
        "- **Titles** — every visual needs a clear title; page needs a dashboard title\n"
        "- **Accessibility** — readable font size; sufficient contrast; do not rely on color alone"
    )
)

section(24, "Choosing the Right Visual")
cells.append(
    md(
        "| Goal | Best visual |\n"
        "|------|-------------|\n"
        "| Trends over time | Line |\n"
        "| Comparison across categories | Bar / Column |\n"
        "| Parts of a whole | Pie / Donut *(use sparingly)* |\n"
        "| Relationship between two numbers | Scatter |\n"
        "| Single KPI | Card |\n"
        "| Detail rows | Table |\n"
        "| Cross-tab summary | Matrix |"
    )
)

section(25, "Dashboard Checklist")
cells.append(
    md(
        "Before you call the dashboard done:\n\n"
        "- [ ] Clear title\n"
        "- [ ] Filters / slicers work\n"
        "- [ ] Numbers formatted (decimals, thousands separators)\n"
        "- [ ] Consistent colors\n"
        "- [ ] No unnecessary visuals\n"
        "- [ ] Cross-filtering behaves as intended\n"
        "- [ ] Readable on a laptop screen (bonus: check Mobile layout view)"
    )
)

# ---------------------------------------------------------------------------
# Part VII — Final Project
# ---------------------------------------------------------------------------
part("Part VII — Final Project")
section(26, "Final Project")
cells.append(
    md(
        "Instead of many tiny exercises, finish **one Spotify dashboard**.\n\n"
        "### Dashboard requirements\n\n"
        "Your report must include:\n\n"
        "| Requirement | Minimum |\n"
        "|-------------|--------|\n"
        "| KPI cards | **5** |\n"
        "| Charts | **4** (include at least one bar, one line, one scatter) |\n"
        "| Slicers | **3** |\n"
        "| Calculated column | **1** |\n"
        "| Measures | **5** |\n"
        "| Formatting | Titles, number formats, aligned layout |\n\n"
        "Suggested layout:\n\n"
        "```\n"
        "+------------------------------------------------------+\n"
        "|  Dashboard title                                      |\n"
        "+------+------+------+------+------+\n"
        "| KPI  | KPI  | KPI  | KPI  | KPI  |\n"
        "+------+------+------+------+------+\n"
        "| Slicers...                                            |\n"
        "+---------------------------+--------------------------+\n"
        "| Bar: Avg Pop by Decade    | Line: Songs by Year      |\n"
        "+---------------------------+--------------------------+\n"
        "| Scatter: Energy vs Pop    | Table or Matrix          |\n"
        "+---------------------------+--------------------------+\n"
        "```"
    )
)

cells.append(
    md(
        "### Reflection questions\n\n"
        "Answer in a Markdown cell here **or** on a text box on the Power BI report:\n\n"
        "1. Which decade had the highest average popularity in your sample?\n"
        "2. Which artist appears most often?\n"
        "3. Did popularity tend to increase over time in this dataset?\n"
        "4. Which chart communicates information best — and why?\n"
        "5. What did you clean in **Python** vs **Power Query** vs **DAX**, and why?"
    )
)
cells.append(
    code(
        "# Optional: answer reflection questions as comments or print statements\n"
        "# YOUR REFLECTIONS HERE\n"
    )
)

cells.append(
    md(
        f"{HR}\n\n{HR_GOLD}\n\n"
        "### Workflow reminder\n\n"
        "```\n"
        "SQL → pandas → dashboard_data.csv → Power BI Desktop → Interactive Dashboard\n"
        "```\n\n"
        "*End of notebook. Run the Python export cells, then spend most of your time in Power BI Desktop.*"
    )
)

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

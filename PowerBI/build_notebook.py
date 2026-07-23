#!/usr/bin/env python3
"""Generate PowerBI_Intro.ipynb — Python prep for Power BI dashboards."""

import json
from pathlib import Path

OUT = Path(__file__).resolve().parent / "PowerBI_Intro.ipynb"
HR = '<hr style="border: 2px solid #003262">'
HR_GOLD = '<hr style="border: 2px solid #C9B676">'


def md(source: str):
    return {"cell_type": "markdown", "metadata": {}, "source": [source]}


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


def practice(prompt: str, solution: str, placeholder: str = "# YOUR CODE HERE\n"):
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
        "# From SQL to Power BI: Preparing Data with Python\n"
        "##### Professor: Joanna\n"
        "##### Developed by: Ariana Ghimire"
    )
)

# 1. Introduction
cells.append(md(f"{HR}\n\n{HR_GOLD}\n\n## 1. Introduction"))
cells.append(
    md(
        "You already know how to **query** data with SQL. In real analytics jobs, that is only the start.\n\n"
        "After data is collected and queried, teams often:\n\n"
        "1. Clean and reshape it in **Python** (pandas / Polars)\n"
        "2. Export a tidy CSV\n"
        "3. Build an interactive **Power BI** dashboard\n\n"
        "This notebook teaches that middle step — preparing Spotify song data for Power BI.\n\n"
        "```\n"
        "SQL Database\n"
        "      ↓\n"
        "SQL Queries\n"
        "      ↓\n"
        "Python (pandas / Polars)\n"
        "      ↓\n"
        "Cleaned Dataset (CSV)\n"
        "      ↓\n"
        "Power BI Dashboard\n"
        "```\n\n"
        "> **Big idea:** SQL retrieves data. Python prepares it. Power BI presents it."
    )
)

cells.append(
    md(
        "## Learning Objectives\n\n"
        "By the end of this notebook, you should be able to:\n\n"
        "- Load and inspect a CSV with pandas\n"
        "- Clean columns, missing values, and dates\n"
        "- Translate SQL `WHERE`, `SELECT`, `ORDER BY`, and `GROUP BY` into pandas (and Polars)\n"
        "- Make a few quick exploration charts in Python\n"
        "- Export a dashboard-ready CSV for Power BI\n"
        "- Sketch the visuals a Power BI dashboard should include"
    )
)

cells.append(
    md(
        "> **How to use this notebook:** Read each short section, run the example cell, "
        "then try the practice. Expand **Solution** only after you try."
    )
)

# 2. Load data
section(2, "Load Data")
cells.append(
    md(
        "We will use a Spotify songs sample in `data.csv` (a smaller teaching subset of a public Spotify dataset).\n\n"
        "Compare loading data in Python to SQL:\n\n"
        "```sql\n"
        "SELECT *\n"
        "FROM songs\n"
        "LIMIT 5;\n"
        "```"
    )
)

cells.append(
    code(
        "import pandas as pd\n"
        "import polars as pl\n"
        "import matplotlib.pyplot as plt\n"
        "\n"
        'songs = pd.read_csv("data.csv")\n'
        "songs.head()"
    )
)

cells.append(code("songs.info()"))
cells.append(code("songs.describe()"))

cells.append(
    md(
        "Discuss what you see:\n\n"
        "- **Rows** — each song is one observation\n"
        "- **Columns** — features like `name`, `artists`, `year`, `popularity`\n"
        "- **Data types** — numbers, text, dates (as strings until we convert them)\n\n"
        "`info()` is like checking column types. `describe()` summarizes numeric columns."
    )
)

practice(
    "**Practice:** Print the number of rows and columns using `.shape`, then list the column names.\n\n"
    "*Write your answer in the cell below.*",
    "print(songs.shape)\nprint(list(songs.columns))",
)

# 3. Basic cleaning
section(3, "Basic Cleaning")
cells.append(
    md(
        "Power BI works best with **clean, focused** tables. Common preprocessing steps:"
    )
)

cells.append(
    md(
        "### Remove unnecessary columns\n\n"
        "The `id` column is useful in a database, but not needed for our dashboard."
    )
)
cells.append(code('songs = songs.drop(columns=["id"])\nsongs.head(2)'))

cells.append(md("### Missing values\n\nCheck how many nulls each column has:"))
cells.append(code("songs.isna().sum()"))

cells.append(
    md(
        "### Convert dates\n\n"
        "`release_date` is currently text. Convert it so year/decade work reliably."
    )
)
cells.append(
    code(
        'songs["release_date"] = pd.to_datetime(songs["release_date"], errors="coerce")\n'
        'songs[["name", "release_date"]].head()'
    )
)

cells.append(
    md(
        "### Create a decade column\n\n"
        "This is something students immediately appreciate in Power BI — decades make great bar charts."
    )
)
cells.append(
    code(
        'songs["decade"] = (songs["year"] // 10) * 10\n'
        'songs[["name", "year", "decade"]].head()'
    )
)

practice(
    "**Practice:** Create a new column `duration_min` that converts `duration_ms` from milliseconds to minutes "
    "(divide by 60000). Show `name` and `duration_min` for the first 5 rows.\n\n"
    "*Write your answer in the cell below.*",
    'songs["duration_min"] = songs["duration_ms"] / 60000\n'
    'songs[["name", "duration_min"]].head()',
)

# 4. Filtering
section(4, "Filtering (SQL → pandas → Polars)")
cells.append(
    md(
        "**SQL**\n"
        "```sql\n"
        "SELECT *\n"
        "FROM songs\n"
        "WHERE popularity > 60;\n"
        "```\n\n"
        "**pandas**"
    )
)
cells.append(code('popular = songs[songs["popularity"] > 60]\npopular[["name", "artists", "popularity"]].head()'))

cells.append(md("**Polars**"))
cells.append(
    code(
        'songs_pl = pl.from_pandas(songs)\n'
        'songs_pl.filter(pl.col("popularity") > 60).select("name", "artists", "popularity").head()'
    )
)

practice(
    "**Practice:** Filter songs where `year >= 2010` and show `name`, `year`, and `popularity` "
    "(first 5 rows).\n\n"
    "*Write your answer in the cell below.*",
    'songs[songs["year"] >= 2010][["name", "year", "popularity"]].head()',
)

# 5. Selecting columns
section(5, "Selecting Columns")
cells.append(
    md(
        "**SQL**\n"
        "```sql\n"
        "SELECT name, artists, popularity\n"
        "FROM songs;\n"
        "```\n\n"
        "**pandas**"
    )
)
cells.append(code('songs[["name", "artists", "popularity"]].head()'))

cells.append(md("**Polars**"))
cells.append(code('songs_pl.select("name", "artists", "popularity").head()'))

practice(
    "**Practice:** Select only `name`, `decade`, `energy`, and `danceability`. Show the first 5 rows.\n\n"
    "*Write your answer in the cell below.*",
    'songs[["name", "decade", "energy", "danceability"]].head()',
)

# 6. Sorting
section(6, "Sorting")
cells.append(
    md(
        "**SQL**\n"
        "```sql\n"
        "SELECT name, popularity\n"
        "FROM songs\n"
        "ORDER BY popularity DESC;\n"
        "```\n\n"
        "**pandas**"
    )
)
cells.append(
    code(
        'songs.sort_values("popularity", ascending=False)[["name", "artists", "popularity"]].head(10)'
    )
)

cells.append(md("**Polars**"))
cells.append(
    code(
        'songs_pl.sort("popularity", descending=True).select("name", "artists", "popularity").head(10)'
    )
)

practice(
    "**Practice:** Sort by `energy` descending and show the top 5 song names and energy values.\n\n"
    "*Write your answer in the cell below.*",
    'songs.sort_values("energy", ascending=False)[["name", "energy"]].head(5)',
)

# 7. GROUP BY
section(7, "GROUP BY (Perfect for Power BI)")
cells.append(
    md(
        "Aggregations you build in Python often become the same summaries Power BI charts display.\n\n"
        "**SQL**\n"
        "```sql\n"
        "SELECT\n"
        "  year,\n"
        "  AVG(popularity) AS avg_popularity\n"
        "FROM songs\n"
        "GROUP BY year;\n"
        "```\n\n"
        "**pandas**"
    )
)
cells.append(code('songs.groupby("year")["popularity"].mean().head(10)'))

cells.append(md("Average popularity by **decade** (great Power BI bar chart):"))
cells.append(
    code(
        'by_decade = songs.groupby("decade")["popularity"].mean().reset_index(name="avg_popularity")\n'
        "by_decade"
    )
)

cells.append(md("**Polars**"))
cells.append(
    code(
        'songs_pl.group_by("decade").agg(\n'
        '    pl.col("popularity").mean().alias("avg_popularity")\n'
        ').sort("decade")'
    )
)

practice(
    "**Practice:** Group by `decade` and compute the average `danceability`. "
    "Sort by decade ascending.\n\n"
    "*Write your answer in the cell below.*",
    'songs.groupby("decade")["danceability"].mean().reset_index(name="avg_danceability").sort_values("decade")',
)

# 8. Simple visualizations
section(8, "Simple Visualizations in Python")
cells.append(
    md(
        "Python is great for **quick exploration**. Power BI is designed for **interactive dashboards**.\n\n"
        "Make only a few charts here — just enough to understand the data before exporting."
    )
)

cells.append(md("### Average popularity by year"))
cells.append(
    code(
        'avg_by_year = songs.groupby("year")["popularity"].mean()\n'
        "avg_by_year.plot(figsize=(10, 4), title=\"Average Popularity by Year\")\n"
        'plt.xlabel("Year")\n'
        'plt.ylabel("Average Popularity")\n'
        "plt.tight_layout()\n"
        "plt.show()"
    )
)

cells.append(md("### Average popularity by decade (bar chart)"))
cells.append(
    code(
        'by_decade.plot(x="decade", y="avg_popularity", kind="bar", legend=False, figsize=(8, 4),\n'
        '              title="Average Popularity by Decade")\n'
        'plt.xlabel("Decade")\n'
        'plt.ylabel("Average Popularity")\n'
        "plt.tight_layout()\n"
        "plt.show()"
    )
)

cells.append(md("### Popularity distribution (histogram)"))
cells.append(
    code(
        'songs["popularity"].plot(kind="hist", bins=20, figsize=(8, 4), title="Popularity Distribution")\n'
        'plt.xlabel("Popularity")\n'
        "plt.tight_layout()\n"
        "plt.show()"
    )
)

cells.append(md("### Top artists by number of songs"))
cells.append(
    code(
        'top_artists = songs["artists"].value_counts().head(10)\n'
        'top_artists.plot(kind="barh", figsize=(8, 5), title="Top 10 Artists by Song Count")\n'
        'plt.xlabel("Number of Songs")\n'
        "plt.tight_layout()\n"
        "plt.show()"
    )
)

cells.append(
    md(
        "> **Remember:** These charts are for exploration. The polished interactive version belongs in Power BI."
    )
)

practice(
    "**Try It Yourself:** Make a line chart of average `energy` by `year`.\n\n"
    "*Write your answer in the cell below.*",
    'songs.groupby("year")["energy"].mean().plot(figsize=(10, 4), title="Average Energy by Year")\n'
    'plt.xlabel("Year")\n'
    'plt.ylabel("Average Energy")\n'
    "plt.tight_layout()\n"
    "plt.show()",
)

# 9. Prepare for Power BI
section(9, "Prepare Data for Power BI")
cells.append(
    md(
        "Create a smaller cleaned dataset with only the columns the dashboard needs."
    )
)
cells.append(
    code(
        "dashboard = songs[\n"
        "    [\n"
        '        "name",\n'
        '        "artists",\n'
        '        "year",\n'
        '        "decade",\n'
        '        "popularity",\n'
        '        "danceability",\n'
        '        "energy",\n'
        '        "valence",\n'
        '        "tempo",\n'
        '        "explicit",\n'
        "    ]\n"
        "].copy()\n"
        "\n"
        "dashboard.head()"
    )
)

cells.append(md("### Export the CSV Power BI will import"))
cells.append(
    code(
        'dashboard.to_csv("spotify_dashboard.csv", index=False)\n'
        'print("Exported spotify_dashboard.csv with", len(dashboard), "rows")'
    )
)

practice(
    "**Practice:** Confirm the export worked by reading `spotify_dashboard.csv` back into a "
    "DataFrame called `check` and printing `check.shape`.\n\n"
    "*Write your answer in the cell below.*",
    'check = pd.read_csv("spotify_dashboard.csv")\nprint(check.shape)',
)

# 10. Open Power BI
section(10, "Open Power BI")
cells.append(
    md(
        "Very short setup:\n\n"
        "1. Open **Power BI Desktop**\n"
        "2. Choose **Get data → Text/CSV**\n"
        "3. Select `spotify_dashboard.csv` from this `PowerBI` folder\n"
        "4. Click **Load**\n\n"
        "You should see columns like `name`, `artists`, `year`, `decade`, `popularity`, "
        "`danceability`, `energy`, `valence`, `tempo`, and `explicit`."
    )
)

# 11. Dashboard challenge
section(11, "Dashboard Challenge")
cells.append(
    md(
        "Recreate these visuals in Power BI using `spotify_dashboard.csv`.\n\n"
        "### Visual 1 — Average popularity by decade\n"
        "- Chart type: **Bar chart**\n"
        "- Axis: `decade`\n"
        "- Values: Average of `popularity`\n\n"
        "### Visual 2 — Songs released each year\n"
        "- Chart type: **Line chart**\n"
        "- Axis: `year`\n"
        "- Values: Count of `name` (or Count of rows)\n\n"
        "### Visual 3 — Popularity vs Energy\n"
        "- Chart type: **Scatter chart**\n"
        "- X axis: `energy`\n"
        "- Y axis: `popularity`\n\n"
        "### Visual 4 — Average Danceability by Decade\n"
        "- Chart type: **Column chart**\n"
        "- Axis: `decade`\n"
        "- Values: Average of `danceability`\n\n"
        "### Visual 5 — Slicers\n"
        "Add slicers for:\n"
        "- `year`\n"
        "- `artists`\n"
        "- `explicit`\n\n"
        "### Visual 6 — Cards (KPIs)\n"
        "Add cards for:\n"
        "- Average `popularity`\n"
        "- Average `energy`\n"
        "- Number of songs (Count of rows)\n\n"
        "> Arrange the page so cards are at the top, slicers on the side, and charts in the center."
    )
)

# 12. Reflection
section(12, "Reflection")
cells.append(
    md(
        "Answer these in a Markdown cell or on paper:\n\n"
        "1. Why clean data in Python instead of only in Power BI?\n"
        "2. Which tasks were easier in Python?\n"
        "3. Which tasks are easier in Power BI?\n"
        "4. When would you use SQL instead of Python or Power BI?\n\n"
        "<details>\n"
        "<summary><strong>Sample answers:</strong></summary>\n\n"
        "1. Python is better for repeatable cleaning, creating columns (like decade), and "
        "handling larger/messy transforms before reporting.\n"
        "2. Bulk cleaning, creating calculated columns, quick group-bys, and exporting a tidy CSV.\n"
        "3. Interactive filters/slicers, polished dashboard layout, and sharing visuals with non-coders.\n"
        "4. When the data still lives in a database and you need to retrieve or join source tables efficiently.\n\n"
        "</details>"
    )
)

cells.append(md(f"{HR}\n\n{HR_GOLD}"))
cells.append(
    md(
        "**Workflow reminder**\n\n"
        "`SQL → pandas/Polars → CSV → Power BI Dashboard`\n\n"
        "*End of notebook. Use **Kernel → Restart & Run All**, then open `spotify_dashboard.csv` in Power BI.*"
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

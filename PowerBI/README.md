# Power BI with Python: Building Interactive Dashboards

Project-based unit: prepare a clean CSV in Jupyter (~20%), then build the interactive dashboard in **Power BI Desktop** (~80%).

## Question this unit answers

> Now that I've prepared my data, how do I turn it into an interactive dashboard?

It does **not** re-teach pandas. Students should already know SQL → pandas from the intro notebook.

## Workflow

```
SQL Database
      ↓
Python (pandas)
      ↓
Clean Dataset (dashboard_data.csv)
      ↓
Power BI Desktop
      ↓
Interactive Dashboard
```

## Files

| File | Description |
|------|-------------|
| `PowerBI_Intro.ipynb` | Project notebook (short Python + Power BI walkthrough) |
| `data.csv` | Spotify teaching sample (~4,000 songs) |
| `dashboard_data.csv` | Created when students run the export cell |
| `spotify_dashboard.csv` | Older export name (optional / legacy) |
| `build_notebook.py` | Regenerates the notebook |

## How to run

```bash
cd PowerBI
jupyter notebook PowerBI_Intro.ipynb
```

1. Run the **Section 2** Python cells to write `dashboard_data.csv`
2. Open **Power BI Desktop**
3. Follow Parts II–VII in the notebook (Power Query → Model → DAX → Visuals → Design → Final Project)

## Final project checklist

- 5 KPI cards
- 4 charts (bar, line, scatter, plus one more)
- 3 slicers
- 1 calculated column
- 5 measures
- Clean layout and formatting

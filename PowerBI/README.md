# Power BI Unit — Python → CSV → Dashboard

Capstone-style notebook that connects SQL skills to a Power BI workflow.

## Workflow

```
SQL Database → SQL Queries → Python (pandas/Polars) → Cleaned CSV → Power BI Dashboard
```

## Files

| File | Description |
|------|-------------|
| `PowerBI_Intro.ipynb` | Teaching notebook |
| `data.csv` | Spotify teaching sample (~4,000 songs, git-friendly size) |
| `spotify_dashboard.csv` | Created when students run the export cell |
| `build_notebook.py` | Regenerates the notebook (optional) |

## How to run

From this folder:

```bash
jupyter notebook PowerBI_Intro.ipynb
```

Then **Kernel → Restart & Run All**. After the export cell runs, open `spotify_dashboard.csv` in Power BI Desktop.

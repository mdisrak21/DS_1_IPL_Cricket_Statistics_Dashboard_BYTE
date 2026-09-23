# AVIP DS Task 1 - IPL Cricket Statistics Dashboard

## Project Overview

This project is completed as part of the B.Y.T.E by Arithmatrix AVIP 2026 Data Science Internship.

The objective is to analyze IPL cricket match and ball-by-ball data and build an interactive dashboard showing important team and player statistics.

## Live Dashboard

Deployed Dashboard:
https://avip-ipl-dashboard-byte.onrender.com/ipl_dashboard.html

The dashboard is deployed using Render and provides interactive Season and Team filters along with IPL cricket statistics visualizations.

## Key Dashboard Features

The dashboard includes:

- Runs per match over time
- Top 10 run scorers
- Top 10 wicket takers
- Team win percentage
- Season filter
- Team filter
- Interactive Plotly visualizations
- Data source and extraction date information

## Dataset

The project uses IPL match-level and ball-by-ball delivery data.

### Data Source

https://github.com/Valkyrie31/EDA-IPL-2008-2024

### Data Files

- `data/matches.csv`
- `data/deliveries.csv`

### Extraction / Documentation Date

2026-09-23

## Project Structure

```text
AVIP_DS_Task1_IPL_Dashboard/
│
├── data/
│   ├── matches.csv
│   ├── deliveries.csv
│   └── README.md
│
├── notebooks/
│   └── task_1_ipl_dashboard.ipynb
│
├── outputs/
│   ├── ipl_dashboard.html
│   ├── runs_per_match.png
│   ├── top_10_run_scorers.png
│   ├── top_10_wicket_takers.png
│   ├── team_win_percentage.png
│   ├── insights_summary.txt
│   └── README.txt
│
├── src/
│   └── build_dashboard.py
│
├── README.md
├── requirements.txt
└── .gitignore
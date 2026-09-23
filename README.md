# AVIP DS Task 1 - IPL / Cricket Statistics Dashboard

This project completes **AVIP 2026 Data Science Basic Task 1 — IPL / Cricket Statistics Dashboard**.

## Task Requirements

- Build an interactive dashboard for IPL / Cricket statistics.
- Include runs per match over time.
- Include top 10 run scorers.
- Include top 10 wicket takers.
- Include team win percentages.
- Provide season and team filters.
- Include a data source note with the source URL and extraction/documentation date.
- Provide a public GitHub repository, README, runnable notebook/dashboard, exported PNG visualizations, and brief insights.

## Dataset

Dataset: IPL / Cricket match and ball-by-ball data.

**Dataset Source:**  
https://github.com/Valkyrie31/EDA-IPL-2008-2024

The project uses two main dataset files:

data/matches.csv
data/deliveries.csv

The dataset contains match-level information and ball-by-ball delivery information used to calculate player and team statistics.

**Extraction / Documentation Date:**  
2026-09-23

## Project Structure

AVIP_DS_Task1_IPL_Dashboard/
├── README.md
├── requirements.txt
├── .gitignore
├── data/
│   ├── README.md
│   ├── matches.csv
│   └── deliveries.csv
├── notebooks/
│   └── task_1_ipl_dashboard.ipynb
├── src/
│   └── build_dashboard.py
└── outputs/
    ├── README.txt
    ├── insights_summary.txt
    ├── ipl_dashboard.html
    ├── runs_per_match.png
    ├── top_10_run_scorers.png
    ├── top_10_wicket_takers.png
    └── team_win_percentage.png

## Run Locally

From the project root:

python -m pip install -r requirements.txt

python src/build_dashboard.py

Then open:

outputs/ipl_dashboard.html

For the Jupyter Notebook:

python -m jupyter notebook

Then open:

notebooks/task_1_ipl_dashboard.ipynb

## Generated Outputs

After running the project:

outputs/ipl_dashboard.html
outputs/runs_per_match.png
outputs/top_10_run_scorers.png
outputs/top_10_wicket_takers.png
outputs/team_win_percentage.png
outputs/insights_summary.txt

## Dashboard Visualizations

The dashboard includes the following required visualizations:

1. **Runs Per Match Over Time**
2. **Top 10 Run Scorers**
3. **Top 10 Wicket Takers**
4. **Team Win Percentage**

The dashboard also provides interactive filtering by:

- Season
- Team

## Data Processing

The workflow:

- loads match-level IPL data;
- loads ball-by-ball delivery data;
- processes match and delivery information;
- calculates runs per match;
- calculates total runs for individual players;
- calculates total wickets for bowlers;
- calculates team wins;
- calculates team win percentages;
- creates the required visualizations;
- exports the charts as PNG files;
- generates an interactive HTML dashboard.

## Key Insights

The analysis provides insights related to:

- Match scoring patterns across IPL seasons.
- Top run-scoring players.
- Top wicket-taking players.
- Team win percentages.
- Team performance across the available IPL data.

Detailed generated insights are available in:

outputs/insights_summary.txt

## Interactive Dashboard

The dashboard provides interactive exploration of IPL statistics through season and team filters.

Users can select different seasons and teams to explore the corresponding statistics and visualizations.

## Conclusion

The IPL / Cricket Statistics Dashboard demonstrates an end-to-end data analysis workflow using match-level and ball-by-ball cricket data.

The project processes IPL data to calculate player and team performance statistics and presents the results through interactive and static visualizations.

The final dashboard is available as a runnable HTML application and has been deployed online for public access.

## Live Demo

🚀 **Live Demo:**  
https://avip-ipl-dashboard-byte.onrender.com/ipl_dashboard.html

## GitHub Repository

📂 **GitHub Repository:**  
https://github.com/mdisrak21/DS_1_IPL_Cricket_Statistics_Dashboard_BYTE

## Technologies

- Python
- Pandas
- NumPy
- Plotly
- Jupyter Notebook
- HTML
- Git
- GitHub
- Render

## Internship

**Program:** B.Y.T.E by Arithmatrix — AVIP 2026

**Domain:** Data Science

**Task:** Basic Task 1 — IPL / Cricket Statistics Dashboard
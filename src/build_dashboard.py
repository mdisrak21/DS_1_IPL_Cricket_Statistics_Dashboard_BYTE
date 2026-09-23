import os
import json
import pandas as pd
import matplotlib.pyplot as plt

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")
OUTPUT_DIR = os.path.join(BASE_DIR, "outputs")

MATCHES_FILE = os.path.join(DATA_DIR, "matches.csv")
DELIVERIES_FILE = os.path.join(DATA_DIR, "deliveries.csv")

SOURCE_URL = "https://github.com/Valkyrie31/EDA-IPL-2008-2024"
EXTRACTION_DATE = "2026-09-23"


def txt(x):
    return "" if pd.isna(x) else str(x).strip()


print("=" * 60)
print("AVIP 2026 - IPL Cricket Statistics Dashboard")
print("=" * 60)

os.makedirs(OUTPUT_DIR, exist_ok=True)

# ============================================================
# 1. LOAD DATA
# ============================================================

print("\n[1/6] Loading datasets...")

matches = pd.read_csv(MATCHES_FILE)
deliveries = pd.read_csv(DELIVERIES_FILE)

matches["season"] = matches["season"].astype(str)
matches["id"] = matches["id"].astype(str)
matches["date"] = pd.to_datetime(matches["date"], errors="coerce")

deliveries["match_id"] = deliveries["match_id"].astype(str)

print(f"Loaded {len(matches):,} matches.")
print(f"Loaded {len(deliveries):,} deliveries.")


# ============================================================
# 2. METRICS
# ============================================================

print("\n[2/6] Computing metrics...")

# ---- Runs per match ----

match_runs = (
    deliveries.groupby("match_id")["total_runs"]
    .sum()
    .reset_index()
)

runs = matches[
    ["id", "season", "date", "team1", "team2"]
].merge(
    match_runs,
    left_on="id",
    right_on="match_id",
    how="left"
)

runs["total_runs"] = runs["total_runs"].fillna(0)
runs["team1"] = runs["team1"].map(txt)
runs["team2"] = runs["team2"].map(txt)


# ---- Top run scorers ----

run_scorers = (
    deliveries.groupby("batter")["batsman_runs"]
    .sum()
    .reset_index()
    .rename(columns={"batsman_runs": "runs"})
    .sort_values("runs", ascending=False)
)


# ---- Wicket takers ----

wickets = deliveries[
    deliveries["player_dismissed"].notna()
].copy()

if "dismissal_kind" in wickets.columns:
    credited = [
        "bowled",
        "caught",
        "caught and bowled",
        "lbw",
        "stumped",
        "hit wicket"
    ]

    wickets = wickets[
        wickets["dismissal_kind"]
        .fillna("")
        .str.lower()
        .isin(credited)
    ]

wicket_takers = (
    wickets.groupby("bowler")
    .size()
    .reset_index(name="wickets")
    .sort_values("wickets", ascending=False)
)


# ---- Team results ----

team_rows = []

for _, row in matches.iterrows():

    winner = txt(row["winner"])
    season = str(row["season"])

    for col in ["team1", "team2"]:

        team = txt(row[col])

        if team:
            team_rows.append({
                "season": season,
                "team": team,
                "won": int(team == winner)
            })

team_results = pd.DataFrame(team_rows)


# ---- Season-specific player statistics ----

season_batters = (
    deliveries[
        ["match_id", "batting_team", "batter", "batsman_runs"]
    ]
    .merge(
        matches[["id", "season"]],
        left_on="match_id",
        right_on="id",
        how="left"
    )
    .groupby(
        ["season", "batting_team", "batter"]
    )["batsman_runs"]
    .sum()
    .reset_index()
    .rename(columns={"batsman_runs": "runs"})
)


season_wickets = (
    wickets[
        ["match_id", "bowling_team", "bowler"]
    ]
    .merge(
        matches[["id", "season"]],
        left_on="match_id",
        right_on="id",
        how="left"
    )
    .groupby(
        ["season", "bowling_team", "bowler"]
    )
    .size()
    .reset_index(name="wickets")
)


seasons = sorted(
    matches["season"].dropna().unique(),
    key=lambda x: str(x)
)

teams = sorted(
    set(matches["team1"].dropna().astype(str))
    | set(matches["team2"].dropna().astype(str))
)

print("Metrics calculated successfully.")


# ============================================================
# 3. STATIC PNG CHARTS
# ============================================================

print("\n[3/6] Creating static charts...")

# Runs
tmp = runs.sort_values("date")

plt.figure(figsize=(12, 5))
plt.plot(
    tmp["date"],
    tmp["total_runs"],
    marker=".",
    linewidth=1
)
plt.title("IPL Total Runs per Match")
plt.xlabel("Match Date")
plt.ylabel("Total Runs")
plt.grid(alpha=0.25)
plt.tight_layout()
plt.savefig(
    os.path.join(OUTPUT_DIR, "runs_per_match.png"),
    dpi=160
)
plt.close()


# Top scorers
top = run_scorers.head(10).sort_values("runs")

plt.figure(figsize=(10, 6))
plt.barh(top["batter"], top["runs"])
plt.title("Top 10 IPL Run Scorers")
plt.xlabel("Runs")
plt.tight_layout()
plt.savefig(
    os.path.join(OUTPUT_DIR, "top_10_run_scorers.png"),
    dpi=160
)
plt.close()


# Top wickets
top = wicket_takers.head(10).sort_values("wickets")

plt.figure(figsize=(10, 6))
plt.barh(top["bowler"], top["wickets"])
plt.title("Top 10 IPL Wicket Takers")
plt.xlabel("Wickets")
plt.tight_layout()
plt.savefig(
    os.path.join(OUTPUT_DIR, "top_10_wicket_takers.png"),
    dpi=160
)
plt.close()


# Win percentage
overall = (
    team_results.groupby("team")
    .agg(
        matches=("won", "size"),
        wins=("won", "sum")
    )
    .reset_index()
)

overall["win_percentage"] = (
    overall["wins"] /
    overall["matches"] *
    100
)

top = (
    overall
    .sort_values("win_percentage", ascending=False)
    .head(10)
    .sort_values("win_percentage")
)

plt.figure(figsize=(10, 6))
plt.barh(
    top["team"],
    top["win_percentage"]
)
plt.title("Team Win Percentage - Top 10")
plt.xlabel("Win Percentage")
plt.xlim(0, 100)
plt.tight_layout()
plt.savefig(
    os.path.join(OUTPUT_DIR, "team_win_percentage.png"),
    dpi=160
)
plt.close()

print("Static charts created.")


# ============================================================
# 4. PREPARE JSON DATA
# ============================================================

print("\n[4/6] Preparing interactive dashboard...")

run_records = []

for _, r in runs.iterrows():

    if pd.isna(r["date"]):
        continue

    run_records.append({
        "season": str(r["season"]),
        "date": r["date"].strftime("%Y-%m-%d"),
        "team1": txt(r["team1"]),
        "team2": txt(r["team2"]),
        "runs": float(r["total_runs"])
    })


payload = {
    "runs": run_records,
    "batters": season_batters.to_dict("records"),
    "wickets": season_wickets.to_dict("records"),
    "results": team_results.to_dict("records"),
    "seasons": [str(x) for x in seasons],
    "teams": [str(x) for x in teams],
    "source": SOURCE_URL,
    "date": EXTRACTION_DATE
}

data_json = json.dumps(payload, default=str)


# ============================================================
# 5. INTERACTIVE HTML
# ============================================================

html = r"""
<!DOCTYPE html>
<html>

<head>

<meta charset="UTF-8">

<title>AVIP 2026 - IPL Statistics Dashboard</title>

<script src="https://cdn.plot.ly/plotly-2.35.2.min.js"></script>

<style>

body {
    font-family: Arial, sans-serif;
    background: #f5f7fa;
    margin: 0;
    color: #172033;
}

.container {
    max-width: 1400px;
    margin: auto;
    padding: 25px;
}

h1 {
    margin-bottom: 5px;
}

.subtitle {
    color: #666;
    margin-bottom: 20px;
}

.controls {
    background: white;
    padding: 18px;
    border-radius: 10px;
    margin-bottom: 20px;
    display: flex;
    gap: 25px;
    box-shadow: 0 2px 10px rgba(0,0,0,.06);
}

.control {
    display: flex;
    flex-direction: column;
    gap: 6px;
}

select {
    padding: 9px;
    min-width: 180px;
}

.grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 18px;
}

.card {
    background: white;
    border-radius: 10px;
    padding: 8px;
    box-shadow: 0 2px 10px rgba(0,0,0,.06);
}

.wide {
    grid-column: 1 / -1;
}

.source {
    background: white;
    padding: 18px;
    margin-top: 20px;
    border-radius: 10px;
    font-size: 13px;
}

@media(max-width:900px) {
    .grid {
        grid-template-columns: 1fr;
    }

    .wide {
        grid-column: auto;
    }
}

</style>

</head>

<body>

<div class="container">

<h1>IPL / Cricket Statistics Dashboard</h1>

<div class="subtitle">
AVIP 2026 — Data Science Basic — Task 1
</div>


<div class="controls">

<div class="control">

<label><b>Season</b></label>

<select id="season">

<option>All Seasons</option>

</select>

</div>


<div class="control">

<label><b>Team</b></label>

<select id="team">

<option>All Teams</option>

</select>

</div>

</div>


<div class="grid">

<div class="card wide">
<div id="runs"></div>
</div>

<div class="card">
<div id="batters"></div>
</div>

<div class="card">
<div id="wickets"></div>
</div>

<div class="card wide">
<div id="wins"></div>
</div>

</div>


<div class="source">

<b>Data Source:</b>

<a id="sourceLink" target="_blank"></a>

<br><br>

<b>Extraction Date:</b>

<span id="extractDate"></span>

</div>

</div>


<script>

const DATA = __DATA__;

const season = document.getElementById("season");
const team = document.getElementById("team");


DATA.seasons.forEach(x => {

    let o = document.createElement("option");

    o.value = x;
    o.textContent = x;

    season.appendChild(o);

});


DATA.teams.forEach(x => {

    let o = document.createElement("option");

    o.value = x;
    o.textContent = x;

    team.appendChild(o);

});


document.getElementById("sourceLink").href = DATA.source;
document.getElementById("sourceLink").textContent = DATA.source;

document.getElementById("extractDate").textContent = DATA.date;


function filterRuns() {

    return DATA.runs.filter(r => {

        let s =
            season.value === "All Seasons" ||
            r.season === season.value;

        let t =
            team.value === "All Teams" ||
            r.team1 === team.value ||
            r.team2 === team.value;

        return s && t;

    }).sort((a,b) =>
        a.date.localeCompare(b.date)
    );
}


function filterBatters() {

    return DATA.batters.filter(r => {

        let s =
            season.value === "All Seasons" ||
            String(r.season) === season.value;

        let t =
            team.value === "All Teams" ||
            r.batting_team === team.value;

        return s && t;

    });

}


function filterWickets() {

    return DATA.wickets.filter(r => {

        let s =
            season.value === "All Seasons" ||
            String(r.season) === season.value;

        let t =
            team.value === "All Teams" ||
            r.bowling_team === team.value;

        return s && t;

    });

}


function renderRuns() {

    let data = filterRuns();

    Plotly.react(
        "runs",
        [{
            x: data.map(x => x.date),
            y: data.map(x => x.runs),
            mode: "lines+markers"
        }],
        {
            title: "Runs per Match Over Time",
            xaxis: {title:"Match Date"},
            yaxis: {title:"Total Runs"},
            margin:{l:60,r:20,t:55,b:55}
        },
        {responsive:true, displaylogo:false}
    );

}


function renderBatters() {

    let rows = {};

    filterBatters().forEach(x => {

        rows[x.batter] =
            (rows[x.batter] || 0) +
            Number(x.runs);

    });


    let data = Object.entries(rows)
        .map(x => ({
            player:x[0],
            runs:x[1]
        }))
        .sort((a,b)=>b.runs-a.runs)
        .slice(0,10)
        .sort((a,b)=>a.runs-b.runs);


    Plotly.react(
        "batters",
        [{
            x:data.map(x=>x.runs),
            y:data.map(x=>x.player),
            type:"bar",
            orientation:"h"
        }],
        {
            title:"Top 10 Run Scorers",
            xaxis:{title:"Runs"},
            margin:{l:120,r:20,t:55,b:55}
        },
        {responsive:true,displaylogo:false}
    );

}


function renderWickets() {

    let rows = {};

    filterWickets().forEach(x => {

        rows[x.bowler] =
            (rows[x.bowler] || 0) +
            Number(x.wickets);

    });


    let data = Object.entries(rows)
        .map(x => ({
            player:x[0],
            wickets:x[1]
        }))
        .sort((a,b)=>b.wickets-a.wickets)
        .slice(0,10)
        .sort((a,b)=>a.wickets-b.wickets);


    Plotly.react(
        "wickets",
        [{
            x:data.map(x=>x.wickets),
            y:data.map(x=>x.player),
            type:"bar",
            orientation:"h"
        }],
        {
            title:"Top 10 Wicket Takers",
            xaxis:{title:"Wickets"},
            margin:{l:120,r:20,t:55,b:55}
        },
        {responsive:true,displaylogo:false}
    );

}


function renderWins() {

    const s = season.value;
    const t = team.value;

    let rows = DATA.results.filter(r => {

        let seasonOK =
            s === "All Seasons" ||
            String(r.season) === s;

        let teamOK =
            t === "All Teams" ||
            r.team === t;

        return seasonOK && teamOK;

    });


    let stats = {};

    rows.forEach(r => {

        if (!stats[r.team]) {

            stats[r.team] = {
                matches:0,
                wins:0
            };

        }

        stats[r.team].matches++;
        stats[r.team].wins += Number(r.won);

    });


    let data = Object.entries(stats)
        .map(x => ({
            team:x[0],
            pct:
                x[1].matches ?
                x[1].wins / x[1].matches * 100 :
                0
        }))
        .sort((a,b)=>a.pct-b.pct);


    Plotly.react(
        "wins",
        [{
            x:data.map(x=>x.pct),
            y:data.map(x=>x.team),
            type:"bar",
            orientation:"h"
        }],
        {
            title:"Team Win Percentage",
            xaxis:{
                title:"Win Percentage (%)",
                range:[0,100]
            },
            margin:{l:130,r:20,t:55,b:55}
        },
        {responsive:true,displaylogo:false}
    );

}


function renderAll() {

    renderRuns();
    renderBatters();
    renderWickets();
    renderWins();

}


season.addEventListener("change", renderAll);
team.addEventListener("change", renderAll);

renderAll();

</script>

</body>

</html>
"""

html = html.replace("__DATA__", data_json)

dashboard_file = os.path.join(
    OUTPUT_DIR,
    "ipl_dashboard.html"
)

with open(
    dashboard_file,
    "w",
    encoding="utf-8"
) as f:
    f.write(html)


# ============================================================
# 6. INSIGHTS
# ============================================================

print("\n[5/6] Creating insights summary...")

highest = runs.loc[
    runs["total_runs"].idxmax()
]

top_run = run_scorers.iloc[0]
top_wicket = wicket_takers.iloc[0]

insights = f"""
AVIP 2026 - Task 1 IPL Dashboard

Data Source:
{SOURCE_URL}

Extraction Date:
{EXTRACTION_DATE}

Dataset:
{len(matches):,} matches
{len(deliveries):,} deliveries

Key Observations:

1. The highest total runs in a match were
   {highest["total_runs"]:.0f} runs.

2. The leading run scorer is
   {top_run["batter"]} with {top_run["runs"]:.0f} runs.

3. The leading wicket taker is
   {top_wicket["bowler"]} with {top_wicket["wickets"]:.0f} credited wickets.

4. The dashboard provides Season and Team filters
   for interactive exploration of the IPL statistics.

Win percentage is calculated as wins divided by
matches played within the selected scope.
"""

with open(
    os.path.join(OUTPUT_DIR, "insights_summary.txt"),
    "w",
    encoding="utf-8"
) as f:
    f.write(insights)


print("\n[6/6] Dashboard complete.")

print("\n" + "=" * 60)
print("SUCCESS! Updated Task 1 dashboard is ready.")
print("=" * 60)

print("\nOpen:")
print(
    os.path.join(
        OUTPUT_DIR,
        "ipl_dashboard.html"
    )
)
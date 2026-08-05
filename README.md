<div align="center">

# ⚽ FIFA World Cup 2026 Analytics

### An interactive Streamlit dashboard for exploring player & team performance across the 2026 tournament

<p>
  <img src="https://img.shields.io/badge/Python-3.11%2B-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python 3.11+">
  <img src="https://img.shields.io/badge/Streamlit-1.58-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white" alt="Streamlit 1.58">
  <img src="https://img.shields.io/badge/pandas-3.0-150458?style=for-the-badge&logo=pandas&logoColor=white" alt="pandas 3.0">
  <img src="https://img.shields.io/badge/NumPy-2.4-013243?style=for-the-badge&logo=numpy&logoColor=white" alt="NumPy 2.4">
  <img src="https://img.shields.io/badge/Matplotlib-3.11-11557C?style=for-the-badge&logo=plotly&logoColor=white" alt="Matplotlib 3.11">
  <img src="https://img.shields.io/badge/Seaborn-0.13-444876?style=for-the-badge" alt="Seaborn 0.13">
</p>

<p>
  <a href="https://your-app-name.streamlit.app">
    <img src="assets/badges/live-demo.svg" alt="Live Demo" height="48">
  </a>
  &nbsp;
  <a href="https://github.com/Ahtsham9116/2026_World_Cup_Analytics">
    <img src="https://img.shields.io/badge/View%20Source-GitHub-181717?style=for-the-badge&logo=github&logoColor=white" alt="View Source on GitHub" height="48">
  </a>
</p>

<sub>👆 Swap the Live Demo link once it's deployed on Streamlit Community Cloud</sub>

</div>

<br>

**1,231 players. 48 teams. One dashboard.** Explore Golden Boot races, dig into a single player's numbers against their positional average, settle Player‑vs‑Player debates with a weighted scoring system, and browse six narrative insights pulled straight out of the exploratory analysis — all without writing a line of code.

## 📑 Table of Contents

- [Features](#-features)
- [Preview](#-preview)
- [Data](#-data)
- [Getting Started](#-getting-started)
- [Project Structure](#-project-structure)
- [Tech Stack](#-tech-stack)
- [Known Limitations](#-known-limitations)
- [Roadmap](#-roadmap)
- [Contributing](#-contributing)
- [License](#-license)

## ✨ Features

The app is organized into five sections, accessible from the sidebar:

| Page | What you can do |
|---|---|
| 🏠 **Home** | Tournament-wide summary (players, teams, goals, assists) with quick links into every other section |
| 🔍 **Explorer** | Look up a single player or team and compare their stats against the positional / tournament average |
| ⚔️ **Head-to-Head** | Compare two players (same position) or two teams side-by-side — a weighted-stat scoring system picks a winner and a radar chart shows the shape of the comparison |
| 🏆 **Leaderboard** | Top‑N rankings for Goals, Assists, xG, Passing Accuracy, Discipline, Forced Turnovers, and Goalkeeper Saves, with an adjustable "Top N" slider |
| 📊 **Insights** | Six curated, narrative findings from the exploratory data analysis, each paired with its supporting chart |

A few details worth calling out:
- The **Discipline leaderboard** doesn't just count cards — it ranks players by a weighted Infraction Score (Yellow = 1 pt, Indirect Red = 2 pts, Red = 3 pts), with a transparency footnote on who narrowly missed the cutoff.
- The **Passing Accuracy leaderboard** filters out small samples (50+ passes minimum) and zooms the x-axis so the tight spread at the top is actually readable, with the truncated axis clearly disclosed.
- **Head-to-Head** comparisons run on a configurable weighted scoring model across Attack, Possession, Defense, Goalkeeping, and Discipline.

## 🖼 Preview

<!--
  Add a screenshot or short GIF of the app here once you have one, e.g.:
  ![Dashboard preview](assets/screenshots/home.png)
  Tip: dragging an image into a GitHub issue/PR comment box gives you a
  hosted URL you can paste directly into this README.
-->

> _Screenshots coming soon — drop one in `assets/screenshots/` and link it here._

## 🗂 Data

Player and team statistics were scraped from FIFA's official player-statistics page (see `notebooks/01_scrape.ipynb`) and cleaned/explored in `notebooks/02_eda_analysis.ipynb`. The cleaned CSVs that power the app live in `assets/DATA/`:

| File | Contents |
|---|---|
| `All_Data.csv` | Combined player-level stats across all categories (1,231 players) |
| `Attacking.csv` | Goals, assists, xG, shots, take-ons |
| `Defending.csv` | Forced turnovers, defensive pressures |
| `Discipline.csv` | Yellow/red cards, fouls, infraction score |
| `Distribution.csv` | Passes, passing accuracy, crosses |
| `Goalkeeping.csv` | Saves, actions inside/outside the box |
| `Golden_Boot.csv` | Goals, assists, minutes played |
| `teams.csv` | Team-level aggregates used in Team Explorer / Team vs Team (48 teams) |

## 🚀 Getting Started

```bash
git clone https://github.com/Ahtsham9116/2026_World_Cup_Analytics.git
cd 2026_World_Cup_Analytics
pip install -r requirements.txt
streamlit run main.py
```

The app expects to be launched from the project root, since data paths (`assets/DATA/...`, `assets/insights/...`) are relative to it.

**Requirements:** Python 3.11+

## 📁 Project Structure

```
.
├── main.py                    # Streamlit app: pages, layout, navigation
├── plots.py                   # Data loading + all chart/comparison logic
├── requirements.txt
├── .streamlit/config.toml     # Theme
├── assets/
│   ├── DATA/                  # Cleaned CSVs used by the app
│   ├── insights/              # Static charts shown on the Insights page
│   └── badges/                # README badge assets
└── notebooks/
    ├── 01_scrape.ipynb        # Selenium scraper for FIFA's stats site
    └── 02_eda_analysis.ipynb  # Cleaning + exploratory analysis
```

## 🛠 Tech Stack

**Python** · **Streamlit** · **streamlit-option-menu** · **pandas** · **NumPy** · **Matplotlib** · **Seaborn**

## ⚠️ Known Limitations

- Insight charts on the Insights page are static images generated in the notebook, not regenerated live from the data.
- A small number of players have no recorded passing attempts; their Passing Accuracy is treated as "no data" (shown as `N/A` / 0 rather than skewing comparisons).

## 🗺 Roadmap

Ideas for future iterations — not commitments, just where this could go next:

- [ ] Regenerate the Insights charts live from the underlying data instead of static images
- [ ] Deploy to Streamlit Community Cloud and wire up the live demo link
- [ ] Add automated tests around the leaderboard and comparison logic
- [ ] Team-level Explorer filters (confederation, group stage vs. knockout)

## 🤝 Contributing

Contributions, issues, and suggestions are welcome.

1. Fork the repo
2. Create a branch (`git checkout -b feature/your-idea`)
3. Commit your changes
4. Open a pull request

## 📄 License

No license has been set yet — until one is added, all rights are reserved by default. Adding an [MIT License](https://choosealicense.com/licenses/mit/) is a common, permissive choice if you'd like others to reuse this work.

---

<div align="center">

**Built by Ahtsham**

<a href="https://github.com/Ahtsham9116">
  <img src="https://img.shields.io/badge/GitHub-Ahtsham9116-181717?style=for-the-badge&logo=github&logoColor=white" alt="GitHub">
</a>
&nbsp;
<a href="https://linkedin.com/in/m-ahtsham-javed">
  <img src="https://img.shields.io/badge/LinkedIn-Connect-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white" alt="LinkedIn">
</a>

<sub>⭐ If this project helped you, consider giving it a star.</sub>

</div>

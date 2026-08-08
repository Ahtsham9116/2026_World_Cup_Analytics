<div align="center">

# ⚽ FIFA World Cup 2026 Analytics

### An interactive Streamlit dashboard for exploring player & team performance across the 2026 tournament

**Built with**

![Python](https://img.shields.io/badge/Python-3776AB?style=flat-square&logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=flat-square&logo=streamlit&logoColor=white)
![pandas](https://img.shields.io/badge/pandas-150458?style=flat-square&logo=pandas&logoColor=white)
![NumPy](https://img.shields.io/badge/NumPy-013243?style=flat-square&logo=numpy&logoColor=white)
![Matplotlib](https://img.shields.io/badge/Matplotlib-11557C?style=flat-square)
![Seaborn](https://img.shields.io/badge/Seaborn-444876?style=flat-square)

**Status**

![Status](https://img.shields.io/badge/status-active-2EA44F?style=flat-square)
![Deployment](https://img.shields.io/badge/deployment-Streamlit%20Community%20Cloud-FF4B4B?style=flat-square&logo=streamlit&logoColor=white)
![License](https://img.shields.io/badge/license-MIT-yellow?style=flat-square)

<br>

<p>
  <a href="https://2026worldcupanalyticsgit-m4kzg439vgtdulyed5u5ge.streamlit.app">
    <img src="assets/badges/live-demo.svg" alt="Live Demo" height="48">
  </a>
  &nbsp;
  <a href="https://github.com/Ahtsham9116/2026_World_Cup_Analytics">
    <img src="assets/badges/github-repo.svg" alt="View on GitHub" height="48">
  </a>
  &nbsp;
  <a href="#-preview">
    <img src="assets/badges/watch-demo.svg" alt="Watch Demo" height="48">
  </a>
</p>

</div>

<br>

**1,231 players. 48 teams. One dashboard.** Explore Golden Boot races, dig into a single player's numbers against their positional average, settle Player‑vs‑Player debates with a weighted scoring system, and browse six narrative insights pulled straight out of the exploratory analysis — all without writing a line of code.

## 📑 Table of Contents

- [Project Highlights](#-project-highlights)
- [Preview](#-preview)
- [Features](#-features)
- [How It Works](#-how-it-works)
- [Data](#-data)
- [Getting Started](#-getting-started)
- [Project Structure](#-project-structure)
- [Tech Stack](#-tech-stack)
- [Known Limitations](#-known-limitations)
- [Challenges](#-challenges)
- [Roadmap](#-roadmap)
- [Team & Contributions](#-team--contributions)
- [Contributing](#-contributing)
- [License](#-license)

## 🏆 Project Highlights

- **End-to-end pipeline** — from a live scrape of FIFA's official stats site to a cleaned dataset to a deployed, public-facing dashboard.
- **1,231 players across 48 teams**, unified into a single combined dataset (`All_Data.csv`) alongside seven category-specific tables.
- **Custom weighted scoring models** for two of the harder analytical problems: a configurable Head-to-Head comparison score (Attack, Possession, Defense, Goalkeeping, Discipline) and an Infraction Score for the Discipline leaderboard, rather than naive stat counts.
- **Five-page interactive app** — Home, Explorer, Head-to-Head, Leaderboard, and Insights — built on Streamlit with a custom-themed sidebar and navigation.
- **Six narrative insights** distilled from the exploratory data analysis, each paired with its supporting chart.
- **Deployed and publicly accessible** on Streamlit Community Cloud — no setup required to try it.

## 🎬 Preview

![FIFA World Cup 2026 Analytics dashboard demo](assets/demo/dashboard-demo.gif)

## ✨ Features

The app is organized into five sections, accessible from the sidebar:

| Page | What you can do |
|---|---|
| 🏠 **Home** | Tournament-wide summary (players, teams, goals, assists) with quick links into every other section |
| 🔍 **Explorer** | Look up a single player or team and compare their stats against the positional / tournament average |
| ⚔️ **Head-to-Head** | Compare two players (same position) or two teams side-by-side — a weighted-stat scoring system picks a winner and a radar chart shows the shape of the comparison |
| 🏆 **Leaderboard** | Top‑N rankings for Goals, Assists, xG, Passing Accuracy, Discipline, Forced Turnovers, and Goalkeeper Saves, with an adjustable "Top N" slider |
| 📊 **Insights** | Six curated, narrative findings from the exploratory data analysis, each paired with its supporting chart |

**Details worth calling out:**

- The **Discipline leaderboard** doesn't just count cards — it ranks players by a weighted Infraction Score (Yellow = 1 pt, Indirect Red = 2 pts, Red = 3 pts), with a transparency footnote on who narrowly missed the cutoff.
- The **Passing Accuracy leaderboard** filters out small samples (50+ passes minimum) and zooms the x-axis so the tight spread at the top is actually readable, with the truncated axis clearly disclosed.
- **Head-to-Head** comparisons run on a configurable weighted scoring model across Attack, Possession, Defense, Goalkeeping, and Discipline.

## 🧭 How It Works

```
FIFA official stats site
        │
        ▼
Selenium scraper           (notebooks/01_scrape.ipynb)
        │
        ▼
Raw player & team stats
        │
        ▼
Cleaning + EDA              (notebooks/02_eda_analysis.ipynb)
        │
        ▼
Cleaned CSVs                (assets/DATA/*.csv)
        │
        ▼
Streamlit app                (main.py + plots.py)
        │
        ▼
Home │ Explorer │ Head-to-Head │ Leaderboard │ Insights
```

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
│   ├── demo/                  # README demo GIF
│   └── badges/                # README button assets
└── notebooks/
    ├── 01_scrape.ipynb        # Selenium scraper for FIFA's stats site
    └── 02_eda_analysis.ipynb  # Cleaning + exploratory analysis
```

## 🛠 Tech Stack

**Python** · **Streamlit** · **streamlit-option-menu** · **pandas** · **NumPy** · **Matplotlib** · **Seaborn**

## ⚠️ Known Limitations

- Insight charts on the Insights page are static images generated in the notebook, not regenerated live from the data.
- A small number of players have no recorded passing attempts; their Passing Accuracy is treated as "no data" (shown as `N/A` / 0 rather than skewing comparisons).

## 🧩 Challenges

A few problems that took real iteration to get right:

- **Scraping a live, dynamic stats site reliably.** FIFA's stats pages render client-side, so `01_scrape.ipynb` uses Selenium with explicit waits and pagination handling instead of a simple HTTP request, to make sure every player row actually loaded before being captured.
- **Inconsistent raw data types.** Several numeric-looking fields (e.g. xG Efficiency) came back from the scrape as strings rather than numbers, which meant every downstream calculation needed an explicit cleaning and type-coercion pass before it could be trusted.
- **Small-sample distortion on the Passing Accuracy leaderboard.** A handful of players with very few pass attempts posted misleadingly perfect accuracy figures. The fix was a minimum-sample threshold (50+ passes) combined with a disclosed, zoomed x-axis so the genuinely tight spread at the top stays readable.
- **Designing a fair Head-to-Head score.** Comparing two players or teams on raw totals favors whoever played more minutes. The comparison logic instead normalizes and weights metrics across Attack, Possession, Defense, Goalkeeping, and Discipline into one configurable score.

## 🗺 Roadmap

Ideas for future iterations — not commitments, just where this could go next:

- [ ] Regenerate the Insights charts live from the underlying data instead of static images
- [ ] Add automated tests around the leaderboard ranking and Head-to-Head scoring logic
- [ ] Team-level Explorer filters (confederation, group stage vs. knockout stage)
- [ ] Cache heavier data loads with `st.cache_data` to speed up navigation between pages
- [ ] CSV export for Head-to-Head comparisons and Leaderboard views

## 🤝 Team & Contributions

This project was built collaboratively, with a clear split between analysis and application work.

| Muhammad Ahtsham Javed | Abdul Manan |
|---|---|
| Data Cleaning | Web Scraping |
| Data Preprocessing | Streamlit Development |
| Exploratory Data Analysis (EDA) | Dashboard Integration |
| Statistical Analysis | Deployment |
| Data Visualization | |

## 🙌 Contributing

Contributions, issues, and suggestions are welcome.

1. Fork the repo
2. Create a branch (`git checkout -b feature/your-idea`)
3. Commit your changes
4. Open a pull request

## 📄 License

This project is licensed under the [MIT License](LICENSE).

---

<div align="center">

**Built by Muhammad Ahtsham Javed**

<a href="https://github.com/Ahtsham9116">
  <img src="https://img.shields.io/badge/GitHub-Ahtsham9116-181717?style=flat-square&logo=github&logoColor=white" alt="GitHub">
</a>
&nbsp;
<a href="https://www.linkedin.com/in/m-ahtsham-javed">
  <img src="https://img.shields.io/badge/LinkedIn-Connect-0A66C2?style=flat-square&logo=linkedin&logoColor=white" alt="LinkedIn">
</a>

<sub>⭐ If this project helped you, consider giving it a star.</sub>

</div>

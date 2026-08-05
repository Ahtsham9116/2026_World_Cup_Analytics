import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns



# Set a consistent, publication-ready visual theme
sns.set_theme(style="whitegrid", context="notebook", palette="deep")
plt.rcParams.update({
    "figure.figsize": (12, 6),
    "font.family": "sans-serif",
    "font.size": 11,
    "axes.titlesize": 16,
    "axes.titleweight": "bold",
    "axes.labelsize": 13,
    "axes.labelweight": "bold",
})

# File paths for all six statistical categories
raw_dir = "assets/DATA/"

# Load each CSV into its own DataFrame
attacking = pd.read_csv(raw_dir + "Attacking.csv")
defending = pd.read_csv(raw_dir + "Defending.csv")
discipline = pd.read_csv(raw_dir + "Discipline.csv")
distribution = pd.read_csv(raw_dir + "Distribution.csv")
goalkeeping = pd.read_csv(raw_dir + "Goalkeeping.csv")
golden_boot = pd.read_csv(raw_dir + "Golden_Boot.csv")
all_data=pd.read_csv(raw_dir+"All_Data.csv")
teams=pd.read_csv(raw_dir+"teams.csv")


MAX_LEADERBOARD=30

global_top_goals = (
    golden_boot.nlargest(MAX_LEADERBOARD, "Goals")[["Player", "Country", "Goals"]]
    .reset_index(drop=True)
)


global_top_assists = (
        attacking.nlargest(MAX_LEADERBOARD, "Assists")[["Player", "Country", "Assists"]]
        .reset_index(drop=True)
    )

global_top_xg= (
    attacking.nlargest(MAX_LEADERBOARD, "xG")[["Player", "Country", "xG"]]
    .reset_index(drop=True)
)

qualified_passers = distribution[distribution["Passes"] >= 50].dropna(subset=["Passing Accuracy (%)"])
global_top_pass = (
    qualified_passers.nlargest(MAX_LEADERBOARD, "Passing Accuracy (%)")[["Player", "Country", "Passing Accuracy (%)"]]
    .reset_index(drop=True)
)

global_least_disciplined = discipline.nlargest(MAX_LEADERBOARD, "Infraction Score")[
    ["Player", "Country", "Position", "Yellow Cards", "Red Cards", "Indirect Red Cards", "Infraction Score"]
]


global_top_turnovers = (
    defending.nlargest(MAX_LEADERBOARD, "Forced Turnovers")
    [["Player", "Country", "Position", "Forced Turnovers"]]
    .reset_index(drop=True)
)

global_top_saves = (
    goalkeeping.nlargest(MAX_LEADERBOARD, "Goalkeeper Saves")
    [["Player", "Goalkeeper Saves"]]
    .reset_index(drop=True)
)


#TOP N GOAL SCORER
def top_goals_plot(n):
    # --- Data prep ---
    top_n_goals = global_top_goals.head(n)

    # --- Plot ---
    fig, ax = plt.subplots(figsize=(12, 7))

    max_goals = top_n_goals["Goals"].max()
    colors = ["#d62728" if v == max_goals else "#1f77b4" for v in top_n_goals["Goals"]]
    labels = [f"{p} ({c})" for p, c in zip(top_n_goals["Player"], top_n_goals["Country"])]

    bars = ax.barh(
        range(len(top_n_goals)),
        top_n_goals["Goals"],
        color=colors,
        edgecolor="black",
        linewidth=0.8,
    )
    ax.set_yticks(range(len(top_n_goals)))
    ax.set_yticklabels(labels, fontsize=11)
    ax.invert_yaxis()

    # Value labels at bar ends
    for bar, val in zip(bars, top_n_goals["Goals"]):
        ax.text(
            bar.get_width() + 0.1,
            bar.get_y() + bar.get_height() / 2,
            str(int(val)),
            va="center",
            fontsize=11,
            fontweight="bold",
        )

    ax.set_title(
        f"Top {n} Goal Scorers\nFIFA WORLD CUP 2026 — Golden Boot Race",
        fontsize=18,
        fontweight="bold",
        pad=20,
    )
    ax.set_xlabel("Goals", fontsize=17, fontweight="bold")

    ax.grid(axis="x", linestyle="--", alpha=0.5)
    ax.set_axisbelow(True)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.set_xlim(0, max_goals + 1)

    fig.tight_layout()
    return fig


#TOP N GOAL SCORER
def top_assists_plot(n):

    ## TOP 10 ASSISTS   
    #--DATA PREP
    #---------

    top_n_assists = global_top_assists.head(n)
    cutoff_value = top_n_assists["Assists"].min()
    total_at_cutoff = (attacking["Assists"] == cutoff_value).sum()
    shown_at_cutoff = (top_n_assists["Assists"] == cutoff_value).sum()
    extra_tied = total_at_cutoff - shown_at_cutoff
    #--------------


    fig, ax = plt.subplots(figsize=(12, 7))

    max_assists = top_n_assists["Assists"].max()
    colors = ["#d62728" if v == max_assists else "#1f77b4" for v in top_n_assists["Assists"]]
    labels = [f"{p} ({c})" for p, c in zip(top_n_assists["Player"], top_n_assists["Country"])]

    bars = ax.barh(
        range(len(top_n_assists)),
        top_n_assists["Assists"],
        color=colors,
        edgecolor="black",
        linewidth=0.8,
    )
    ax.set_yticks(range(len(top_n_assists)))
    ax.set_yticklabels(labels, fontsize=11)
    ax.invert_yaxis()

    for bar, val in zip(bars, top_n_assists["Assists"]):
        ax.text(
        bar.get_width() + 0.08,
        bar.get_y() + bar.get_height() / 2,
        str(val),
        va="center", fontsize=11, fontweight="bold",
        )

    ax.set_title(
        f"Top {n} Players by Assists\nFIFA WORLD CUP 2026",
        fontsize=18, fontweight="bold", pad=20,
    )
    ax.set_xlabel("Assists", fontsize=13, fontweight="bold")

    
    ax.grid(axis="x", linestyle="--", alpha=0.5)
    ax.set_axisbelow(True)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.set_xlim(0, max_assists + 1)

    fig.tight_layout(rect=[0, 0.08, 1, 1])  # reserve space at the bottom for the footnote

    if extra_tied > 0:
        plural = extra_tied != 1
        fig.text(
            0.5, 0.01,
            f"Note: {extra_tied} additional player{'s' if plural else ''} also recorded "
            f"{cutoff_value} assist{'s' if cutoff_value != 1 else ''} but "
            f"{'are' if plural else 'is'} not shown due to the top-{n} cutoff.",
            ha="center", va="bottom",
            fontsize=9, style="italic", color="dimgray",
            bbox=dict(boxstyle="round,pad=0.4", facecolor="white", edgecolor="#cfcfcf", linewidth=0.8),
        )

    return fig


#TOP 10 XGA
def top_xg_plot(n):
    # --- Data prep ---
    top_n_xg = global_top_xg.head(n)

    # --- Plot ---
    fig, ax = plt.subplots(figsize=(12, 7))

    max_xg = top_n_xg["xG"].max()
    colors = ["#d62728" if v == max_xg else "#1f77b4" for v in top_n_xg["xG"]]
    labels = [f"{p} ({c})" for p, c in zip(top_n_xg["Player"], top_n_xg["Country"])]

    bars = ax.barh(
        range(len(top_n_xg)),
        top_n_xg["xG"],
        color=colors,
        edgecolor="black",
        linewidth=0.8,
    )
    ax.set_yticks(range(len(top_n_xg)))
    ax.set_yticklabels(labels, fontsize=11)
    ax.invert_yaxis()

    # Value labels at bar ends
    for bar, val in zip(bars, top_n_xg["xG"]):
        ax.text(
            bar.get_width() + 0.05,
            bar.get_y() + bar.get_height() / 2,
            f"{val:.2f}",
            va="center",
            fontsize=11,
            fontweight="bold",
        )

    ax.set_title(
        f"Top {n} Players by Expected Goals (xG)\nFIFA WORLD CUP 2026",
        fontsize=18,
        fontweight="bold",
        pad=20,
    )
    ax.set_xlabel("Expected Goals (xG)", fontsize=13, fontweight="bold")

    ax.grid(axis="x", linestyle="--", alpha=0.5)
    ax.set_axisbelow(True)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.set_xlim(0, max_xg + 0.5)

    fig.tight_layout()
    return fig


#TOP N PASSING accuracy
def top_pass_plot(n):
    # --- Data prep ---
    top_n_pass = global_top_pass.head(n)

    # --- Plot ---
    fig, ax = plt.subplots(figsize=(12, 7))

    max_acc = top_n_pass["Passing Accuracy (%)"].max()
    min_acc = top_n_pass["Passing Accuracy (%)"].min()
    colors = ["#d62728" if v == max_acc else "#1f77b4" for v in top_n_pass["Passing Accuracy (%)"]]
    labels = [f"{p} ({c})" for p, c in zip(top_n_pass["Player"], top_n_pass["Country"])]

    bars = ax.barh(
        range(len(top_n_pass)),
        top_n_pass["Passing Accuracy (%)"],
        color=colors,
        edgecolor="black",
        linewidth=0.8,
    )
    ax.set_yticks(range(len(top_n_pass)))
    ax.set_yticklabels(labels, fontsize=11)
    ax.invert_yaxis()

    # Zoomed x-axis to make the tight top-10 spread readable (disclosed below)
    # NOTE: based on the fixed top-30 pool (not the currently visible top_n slice),
    # so the axis stays put and bars don't visibly shift/rescale as the Top N slider moves.
    pool_min_acc = global_top_pass["Passing Accuracy (%)"].min()
    x_low = np.floor(pool_min_acc * 2) / 2 - 0.5  # nearest 0.5 below the min, with a buffer
    x_high = max_acc + 0.5
    ax.set_xlim(x_low, x_high)

    for bar, val in zip(bars, top_n_pass["Passing Accuracy (%)"]):
        ax.text(
            bar.get_width() + 0.05,
            bar.get_y() + bar.get_height() / 2,
            f"{val:.1f}%",
            va="center",
            fontsize=11,
            fontweight="bold",
        )

    ax.set_title(
        f"Top {n} Players by Passing Accuracy\nMinimum 50 Passes — FIFA WORLD CUP 2026",
        fontsize=18,
        fontweight="bold",
        pad=20,
    )
    ax.set_xlabel("Passing Accuracy (%)", fontsize=15, fontweight="bold")

    ax.grid(axis="x", linestyle="--", alpha=0.5)
    ax.set_axisbelow(True)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    fig.tight_layout(rect=[0, 0.08, 1, 1])  # reserve space at the bottom for the footnote

    # Disclose the truncated axis — required whenever a baseline isn't 0
    fig.text(
        0.5, 0.01,
        f"Note: x-axis starts at {x_low:.1f}% (not 0) to highlight differences among top performers.",
        ha="center",
        va="bottom",
        fontsize=9,
        style="italic",
        color="gray",
    )

    return fig


#least N disciplined
def least_discipline_plot(n):

    #--- DATA PREP
    top_n_least_disciplined=global_least_disciplined.head(n)
    top = top_n_least_disciplined.reset_index(drop=True)

    # Weighted contribution of each card type -> segments stack to the true score
    top["Yellow Contribution"] = top["Yellow Cards"] * 1
    top["Indirect Contribution"] = top["Indirect Red Cards"] * 2
    top["Red Contribution"] = top["Red Cards"] * 3

    labels = [f"{p} ({c})" for p, c in zip(top["Player"], top["Country"])]

    # ------------------------------------------------------------------
    # Transparency footnote stats — computed from the full `discipline` df
    # ------------------------------------------------------------------
    cutoff_score = top["Infraction Score"].min()
    tied_at_cutoff = discipline[discipline["Infraction Score"] == cutoff_score]
    n_excluded = len(tied_at_cutoff) - (top["Infraction Score"] == cutoff_score).sum()
    top_yellow_excluded = (
        discipline.loc[~discipline["Player"].isin(top["Player"])]
        .nlargest(1, "Yellow Cards")
        .iloc[0]
    )   
    all_have_red = (top["Red Cards"] >= 1).all()

    # ------------------------------------------------------------------
    # Plot
    # ------------------------------------------------------------------
    fig, ax = plt.subplots(figsize=(12, 7))

    y = np.arange(len(top))[::-1]  # highest score plotted at the top
    YELLOW, INDIRECT, RED = "#F0C808", "#D95F02", "#8B0000"

    yellow_vals = top["Yellow Contribution"].values
    indirect_vals = top["Indirect Contribution"].values
    red_vals = top["Red Contribution"].values
    totals = top["Infraction Score"].values

    ax.barh(y, yellow_vals, color=YELLOW, edgecolor="black", linewidth=0.8, label="Yellow Cards")
    ax.barh(y, indirect_vals, left=yellow_vals, color=INDIRECT, edgecolor="black",
        linewidth=0.8, label="Indirect Red Cards")
    ax.barh(y, red_vals, left=yellow_vals + indirect_vals, color=RED, edgecolor="black",
        linewidth=0.8, label="Red Cards")

    for yi, total in zip(y, totals):
        ax.text(total + 0.12, yi, str(int(total)), va="center", ha="left",
                fontsize=11, fontweight="bold")

    ax.set_yticks(y)
    ax.set_yticklabels(labels, fontsize=10)
    ax.set_xlim(0, totals.max() + 1.8)
    ax.set_xlabel(
        "Infraction Score  (bar length = points, not raw card count)",
        fontsize=10.5, fontweight="bold"
    )
    ax.set_title(
        f"Top {n} Least Disciplined Players — Weighted Infraction Score\n"
        "(Yellow = 1 pt, Indirect Red = 2 pt, Red = 3 pt)\nFIFA WORLD CUP 2026",
        fontsize=15, fontweight="bold", pad=18
    )

    ax.grid(axis="x", linestyle="--", alpha=0.5)
    ax.set_axisbelow(True)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    ax.legend(loc="upper center", bbox_to_anchor=(0.5, -0.14), ncol=3, frameon=False, fontsize=10)

    if all_have_red:
        ax.text(
            0.98, 0.30, "All 10 players received\nat least one red card",
            transform=ax.transAxes, ha="right", va="top", fontsize=9.5, fontweight="bold",
            bbox=dict(boxstyle="round", facecolor="white", edgecolor="gray", alpha=0.9)
        )

    ax.text(
        0.98, 0.12,
        f"Note: {n_excluded} additional players also scored {cutoff_score} (Infraction Score) but are\n"
        f"excluded by the top-{n} cutoff — including {top_yellow_excluded['Player']} "
        f"({top_yellow_excluded['Yellow Cards']} yellow cards, 0 reds),\n"
        "formerly ranked #1 by raw yellow-card count.",
        transform=ax.transAxes, ha="right", va="top", fontsize=7.8, style="italic",
        color="dimgray", bbox=dict(boxstyle="round", facecolor="white", edgecolor="gray", alpha=0.9)
    )

    fig.tight_layout(rect=[0, 0.10, 1, 1])  # reserve space at the bottom for the legend
    return fig


#top N forced turnovers
def top_turnovers_plot(n):
    top_n_turnovers = global_top_turnovers.head(n)

    # Colors (same style as Assists chart) — renamed to avoid collision
    # with the `colors` dict used in the Yellow Card chart
    bar_colors = ["#d62728"] + ["#1f77b4"] * (len(top_n_turnovers) - 1)

    fig, ax = plt.subplots(figsize=(12, 7))

    bars = ax.barh(
        range(len(top_n_turnovers)),
        top_n_turnovers["Forced Turnovers"],
        color=bar_colors,
        edgecolor="black",
        linewidth=0.8,
        height=0.72
    )

    # Player labels
    labels = [
        f"{player} ({country})"
        for player, country in zip(
            top_n_turnovers["Player"],
            top_n_turnovers["Country"]
        )
    ]

    ax.set_yticks(range(len(labels)))
    ax.set_yticklabels(labels, fontsize=11)

    ax.invert_yaxis()

    # --- Value labels — pad now scales with the data instead of a fixed 0.15 ---
    max_val = top_n_turnovers["Forced Turnovers"].max()
    label_pad = max_val * 0.015

    for bar, value in zip(bars, top_n_turnovers["Forced Turnovers"]):
        ax.text(
            value + label_pad,
            bar.get_y() + bar.get_height()/2,
            f"{value}",
            va="center",
            ha="left",
            fontsize=11,
            fontweight="bold"
        )

    # Titles
    ax.set_title(
        f"Top {n} Players by Forced Turnovers\nFIFA WORLD CUP 2026",
        fontsize=18,
        fontweight="bold",
        pad=20
    )

    ax.set_xlabel(
        "Forced Turnovers",
        fontsize=16,
        fontweight="bold"
    )

    # Grid (matches Assists chart)
    ax.grid(
        axis="x",
        linestyle="--",
        linewidth=1,
        alpha=0.35
    )

    ax.set_axisbelow(True)

    # Clean look
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    # --- xlim headroom now scales with max value, same pattern as the other charts ---
    ax.set_xlim(0, max_val * 1.15)

    plt.tight_layout(rect=[0, 0.08, 1, 1])  # reserve space at the bottom for the footnote

    # -------------------------------------------------------
    # Footnote — placed OUTSIDE the plot area so it can never
    # overlap a bar, regardless of the underlying values
    # -------------------------------------------------------
    fig.text(
        0.5, 0.01,
        "Note: Oyarzabal (FW) leads the ranking — atypical, since forced turnovers\n"
        "are usually a defensive or midfield strength rather than a forward's.",
        ha="center",
        va="bottom",
        fontsize=10,
        style="italic",
        color="dimgray"
    )


    return fig



# top N goalkeeper saves
def top_saves_plot(n):
    #--DATA PREP
    top_n_saves = global_top_saves.head(n) 
    cutoff_value = top_n_saves["Goalkeeper Saves"].iloc[-1]
    tied_total = (goalkeeping["Goalkeeper Saves"] == cutoff_value).sum()
    tied_shown = (top_n_saves["Goalkeeper Saves"] == cutoff_value).sum()
    extra_tied = tied_total - tied_shown

    # Colors — same convention as the other Top-10 charts
    bar_colors = ["#d62728"] + ["#1f77b4"] * (len(top_n_saves) - 1)

    fig, ax = plt.subplots(figsize=(12, 7))

    bars = ax.barh(
        range(len(top_n_saves)),
        top_n_saves["Goalkeeper Saves"],
        color=bar_colors,
        edgecolor="black",
        linewidth=0.8,
        height=0.72
    )

    ax.set_yticks(range(len(top_n_saves)))
    ax.set_yticklabels(top_n_saves["Player"], fontsize=11)

    ax.invert_yaxis()

    # Value labels — offset scales with the data, same pattern as the other charts
    max_val = top_n_saves["Goalkeeper Saves"].max()
    label_pad = max_val * 0.015

    for bar, value in zip(bars, top_n_saves["Goalkeeper Saves"]):
        ax.text(
            value + label_pad,
            bar.get_y() + bar.get_height()/2,
            f"{value}",
            va="center",
            ha="left",
            fontsize=11,
            fontweight="bold"
        )

    # Title
    ax.set_title(
        f"Top {n} Goalkeepers by Saves\nFIFA World Cup 2026",
        fontsize=20,
        fontweight="bold",
        pad=20
    )

    ax.set_xlabel(
        "Goalkeeper Saves",
        fontsize=15,
        fontweight="bold"
    )

    ax.grid(
        axis="x",
        linestyle="--",
        linewidth=1,
        alpha=0.35
    )

    ax.set_axisbelow(True)

    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    # Headroom scales with the data, same pattern as Forced Turnovers
    ax.set_xlim(0, max_val * 1.15)



    plt.tight_layout(rect=[0, 0.08, 1, 1])  # reserve space at the bottom for the footnote

    # -------------------------------------------------------
    # Footnote — outside the axes, bordered box, matching the
    # Assists / Forced Turnovers chart convention
    # -------------------------------------------------------
    if extra_tied > 0:
        plural = "s" if extra_tied != 1 else ""
        verb = "are" if extra_tied != 1 else "is"
        fig.text(
            0.5, 0.01,
            f"Note: {extra_tied} additional goalkeeper{plural} also recorded "
            f"{cutoff_value} saves but {verb} not shown due to the top-{n} cutoff.",
            ha="center",
            va="bottom",
            fontsize=10,
            style="italic",
            color="dimgray",
            bbox=dict(
                boxstyle="round,pad=0.4",
                facecolor="white",
                edgecolor="#cfcfcf",
                linewidth=0.8
            )
        )


    return fig






def normalize(df, columns, max_values,min_values=0):



    stats = df[columns]

    values = stats.iloc[0] #converting in series

    values = values.astype(float)

    # Players with no recorded attempts (e.g. 0 passes -> NaN passing accuracy) used to leave
    # a NaN in the vector, which made matplotlib silently drop the ENTIRE radar polygon for
    # that player. Treat "no data" as 0 on that single axis instead of hiding the whole shape.
    values = values.fillna(0)

    normalized = (values - min_values) / (max_values - min_values)
    normalized = normalized.fillna(0)  # guards the rare max==min case too

    return normalized.tolist()


def radar_plot(col,name1,name2,data1,data2):

    N = len(col)
    data1=data1.copy()
    data2=data2.copy()    # so the original does not get modified

    angles = np.linspace(0, 2*np.pi, N, endpoint=False).tolist()

    # Polygon close karo
    angles.append(angles[0])
    data1.append(data1[0])
    data2.append(data2[0])

    fig, ax = plt.subplots(
         figsize=(8,8),
         subplot_kw=dict(polar=True)
        )

    #  data1 Plot
    ax.plot(
        angles,
        data1,
        linewidth=2,
        color="royalblue",
        label=name1
    )

    ax.fill(
        angles,
        data1,
        color="royalblue",
        alpha=0.25      # transparency
    )


    #  data2 Plot
    ax.plot(
        angles,
        data2,
        linewidth=2,
        color="crimson",
        label=name2
    )

    ax.fill(
        angles,
        data2,
        color="crimson",
        alpha=0.25      # transparency
    )



    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(col, fontsize=11)

    ax.set_ylim(0,1)

    ax.grid(True)
    ax.spines["polar"].set_visible(False)
    ax.legend(loc="upper right")


    return fig


def comparator(df, name1, name2, columns, weights):

    #the data frame should have identifier at its first column

    row1 = df[df.iloc[:, 0] == name1].iloc[0]
    row2 = df[df.iloc[:, 0] == name2].iloc[0]

    score1 = 0
    score2 = 0

    comparison = {
        "Stats":[],
        name1:[],
        name2:[],
        "Winner":[]
    }

    for stat in columns:

        value1 = row1[stat]
        value2 = row2[stat]

        weight = weights[stat]

        # A missing stat (e.g. a player with 0 passes attempted -> NaN passing accuracy) used to
        # fall through both comparisons below (NaN > / < anything is always False) and land on
        # "Draw" with a blank cell, which looked like an unexplained tie. Make that explicit.
        if pd.isna(value1) or pd.isna(value2):
            stat_winner = "Draw"
            display1 = "N/A" if pd.isna(value1) else value1
            display2 = "N/A" if pd.isna(value2) else value2

        # Positive weight Higher is better
        elif weight >= 0:

            display1, display2 = value1, value2

            if value1 > value2:
                score1 += weight
                stat_winner = name1

            elif value2 > value1:
                score2 += weight
                stat_winner = name2

            else:
                stat_winner = "Draw"

        # Negative weight Lower is better
        else:

            display1, display2 = value1, value2
            actual_weight = abs(weight)

            if value1 < value2:
                score1 += actual_weight
                stat_winner = name1

            elif value2 < value1:
                score2 += actual_weight
                stat_winner = name2

            else:
                stat_winner = "Draw"

        comparison["Stats"].append(stat)
        comparison[name1].append(display1)
        comparison[name2].append(display2)
        comparison["Winner"].append(stat_winner)

    if score1 > score2:
        overall_winner = name1

    elif score2 > score1:
        overall_winner = name2

    else:
        overall_winner = "Draw"

    comparison_df = pd.DataFrame(comparison)

    return overall_winner, score1, score2, comparison_df


def player_vs_player(player1, player2,country1,country2,position):

    stats_columns = {
        "FW": [
            "Goals",
            "Assists",
            "xG",
            "xG Efficiency",
            "Attempts At Goal",
            "Attempts At Goal Conv. Rate (%)",
            "Passing Accuracy (%)",
            "Take-Ons Completed",
            "Infraction Score"
        ],

        "MF": [
            "Goals",
            "Assists",
            "Passes Completed",
            "Passing Accuracy (%)",
            "Crossing Accuracy (%)",
            "Defensive Linebreaks Acc (%)",
            "Switches of Play Acc (%)",
            "Forced Turnovers",
            "Defensive Pressures Applied",
            "Infraction Score"
        ],

        "DF": [
            "Forced Turnovers",
            "Defensive Pressures Applied",
            "Passing Accuracy (%)",
            "Passes Completed",
            "Defensive Linebreaks Acc (%)",
            "Fouls For",
            "Infraction Score"
        ],

        "GK": [
            "Goalkeeper Saves",
            "Total Actions",
            "Passing Accuracy (%)",
            "Passes Completed",
            "Minutes Played",
            "Infraction Score"
        ]
    }

    


    # -------------------------
    # Filter Players
    # -------------------------

    data = all_data[
        (all_data["Player"].isin([player1, player2]))
        &
        (all_data["Position"]==position)
        &
        (all_data["Country"].isin([country1, country2]))
    ].copy()


    #---------------
    # normalizing player data
    #------------

    used_columns = stats_columns[position]

    max_values = all_data[used_columns].max()
    min_values = all_data[used_columns].min()

    player1_normalized = normalize(
        data[data["Player"] == player1],
        used_columns,
        max_values,
        min_values
    )

    player2_normalized = normalize(
        data[data["Player"] == player2],
        used_columns,
        max_values,
        min_values
    )        
    


    weights = {
        # Attack
        "Goals": 5,
        "Assists": 4,
        "xG": 4,
        "xG Efficiency": 3,
        "Attempts At Goal": 2,
        "Attempts At Goal Conv. Rate (%)": 3,
        "Take-Ons Completed": 2,

        # Passing
        "Passes Completed": 3,
        "Passing Accuracy (%)": 2,
        "Crossing Accuracy (%)": 2,
        "Defensive Linebreaks Acc (%)": 3,
        "Switches of Play Acc (%)": 2,

        # Defensive
        "Forced Turnovers": 4,
        "Defensive Pressures Applied": 3,
        "Goalkeeper Saves": 5,
        "Total Actions": 2,
        "Minutes Played": 1,

    # Negative
        "Yellow Cards": -2,
        "Red Cards": -5,
        "Indirect Red Cards": -4,
        "Offsides": -1,
        "Fouls For": -1,
        "Infraction Score": -3,
    }

    score = {
        player1: 0,
        player2: 0
    }



    winner,score[player1],score[player2],table=comparator(data,player1,player2,used_columns,weights)



    g=radar_plot(used_columns,player1,player2,player1_normalized,player2_normalized)

    return (
        g,
        table,
        winner,
        score
    )


def team_vs_team(team1, team2):

    # -------------------------
    # Filter Teams
    # -------------------------

    data = teams[
        teams["Country"].isin([team1, team2])
    ].copy()


    # -------------------------
    # Columns
    # -------------------------

    used_columns = [
        "Attack",
        "Possession",
        "Defense",
        "Goalkeeping",
        "Discipline"
    ]


    # -------------------------
    # Normalize
    # -------------------------

    max_values = teams[used_columns].max()
    min_values = teams[used_columns].min()

    team1_normalized = normalize(
        data[data["Country"] == team1],
        used_columns,
        max_values,
        min_values
    )
    

    team2_normalized = normalize(
        data[data["Country"] == team2],
        used_columns,
        max_values,
        min_values
    )


    # -------------------------
    # Weights
    # -------------------------

    weights = {

        "Attack":5,

        "Possession":4,

        "Defense":5,

        "Goalkeeping":3,

        "Discipline":2

    }


    # -------------------------
    # Compare
    # -------------------------

    score = {
        team1:0,
        team2:0
    }

    winner, score[team1], score[team2], table = comparator(
        data,
        team1,
        team2,
        used_columns,
        weights
    )


    # -------------------------
    # Radar
    # -------------------------

    g = radar_plot(
        used_columns,
        team1,
        team2,
        team1_normalized,
        team2_normalized
    )


    return (
        g,
        table,
        winner,
        score
    )


def player_details(player, country, position):

    # -----------------------------
    # Player
    # -----------------------------

    data = all_data[
        (all_data["Player"] == player)
        &
        (all_data["Country"] == country)
        &
        (all_data["Position"] == position)
    ].copy()

    player_series = data.iloc[0]

    # -----------------------------
    # Reference Players
    # -----------------------------

    reference = all_data[
        (all_data["Position"] == position)
        &
        (all_data["Minutes Played"] >= 90)
    ].copy()


    # -----------------------------
    # Stats Table
    # -----------------------------

    stats_columns = [
        col
        for col in all_data.columns
        if col not in ["Player","Country","Position"]
    ]

    player_stats = (
        player_series[stats_columns]
        .rename("Player")
        .reset_index()
    )

    player_stats.columns = [
        "Stat",
        "Value"
    ]

    # -----------------------------
    # Position Average
    # -----------------------------

    average_series = reference[stats_columns].mean()

    comparison_table = pd.DataFrame({

        "Stat": stats_columns,

        "Player": player_series[stats_columns].values,

        "Average": average_series.values

    })

    # -----------------------------
    # Graph
    # -----------------------------

    graph_columns = {

        "FW": [
            "Goals",
            "Assists",
            "Attempts At Goal",
            "Attempts On Target",
            "xG",
            "Take-Ons Completed"
        ],

        "MF": [
            "Assists",
            "Passes Completed",
            "Passing Accuracy (%)",
            "Crossing Accuracy (%)",
            "Defensive Linebreaks Acc (%)",
            "Switches of Play Acc (%)"
        ],

        "DF": [
            "Forced Turnovers",
            "Defensive Pressures Applied",
            "Passing Accuracy (%)",
            "Passes Completed",
            "Defensive Linebreaks Acc (%)",
            "Fouls For"
        ],

        "GK": [
            "Goalkeeper Saves",
            "Total Actions",
            "Goalkeeper Actions Inside the Penalty Area",
            "Goalkeeper Actions Outside the Penalty Area",
            "Passes Completed",
            "Passing Accuracy (%)"
        ]

        }

    selected_stats = graph_columns[position]

    plot_df = comparison_table[
        comparison_table["Stat"].isin(selected_stats)
    ]

    plot_df = plot_df.melt(

        id_vars="Stat",

        value_vars=["Player","Average"],

        var_name="Type",

        value_name="Value"

    )

    # --- Position-specific colour palette ---
    palette_map = {
        "FW": {"Player": "#D62728", "Average": "#99C2E8"},    # red / light blue
        "MF": {"Player": "#2E86AB", "Average": "#A8D8EA"},    # teal / sky
        "DF": {"Player": "#56B4E9", "Average": "#D6EAF8"},    # blue / ice
        "GK": {"Player": "#E6A817", "Average": "#FDEBD0"},    # gold / cream
    }
    palette = palette_map.get(position, {"Player": "#1f77b4", "Average": "#AEC7E8"})

    g = sns.catplot(
        data=plot_df,
        x="Type",
        y="Value",
        hue="Type",
        col="Stat",
        kind="bar",
        col_wrap=3,
        sharey=False,
        palette=palette,
        height=3.8,
        aspect=0.85,
    )

    # Polish subplots
    for ax in g.axes.flat:
        ax.set_xlabel("")
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
        ax.tick_params(axis="x", labelsize=9)
        ax.tick_params(axis="y", labelsize=8)

    g.figure.suptitle(
        f"{player} — {position} Performance vs Position Average",
        fontsize=16,
        fontweight="bold",
        y=1.02,
    )

    return (
        player_stats,
        g.figure
    )


def team_details(country):

    # -----------------------------
    # Selected Team
    # -----------------------------

    data = teams[
        teams["Country"] == country
    ].copy()

    team_series = data.iloc[0]



    # -----------------------------
    # Stats Table
    # -----------------------------

    stats_columns = [
        col
        for col in teams.columns
        if col != "Country"
    ]

    team_stats = (
        team_series[stats_columns]
        .rename("Team")
        .reset_index()
    )

    team_stats.columns = [
        "Stat",
        "Value"
    ]

    # -----------------------------
    # Tournament Average
    # -----------------------------

    average_series = teams[
        stats_columns
    ].mean()

    comparison_table = pd.DataFrame({

        "Stat": stats_columns,

        "Team": team_series[stats_columns].values,

        "Average": average_series.values

    })

    # -----------------------------
    # Graph
    # -----------------------------

    plot_df = comparison_table.melt(

        id_vars="Stat",

        value_vars=["Team", "Average"],

        var_name="Type",

        value_name="Value"

    )


    graph_columns = [

        "Attack",
        "Possession",
        "Defense",
        "Goalkeeping",
        "Discipline"

    ]

    plot_df = plot_df[
        plot_df["Stat"].isin(graph_columns)
    ]
    

    # --- Team-specific colour palette ---
    palette = {"Team": "#274482", "Average": "#BCC8DC"}

    g = sns.catplot(
        data=plot_df,
        x="Type",
        y="Value",
        hue="Type",
        col="Stat",
        kind="bar",
        col_wrap=3,
        sharey=False,
        palette=palette,
        height=4.2,
        aspect=0.85,
    )

    # Polish subplots
    for ax in g.axes.flat:
        ax.set_xlabel("")
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
        ax.tick_params(axis="x", labelsize=10)
        ax.tick_params(axis="y", labelsize=9)

    g.figure.suptitle(
        f"{country} — Performance vs Tournament Average",
        fontsize=16,
        fontweight="bold",
        y=1.02,
    )

    return (
        team_stats,
        g.figure
    )


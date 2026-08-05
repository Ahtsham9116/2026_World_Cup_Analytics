import streamlit as st
from streamlit_option_menu import option_menu
import matplotlib.pyplot as plt
import plots as p
import re

# ---- Page config ----
st.set_page_config(
    page_title="FIFA World Cup Analytics",
    page_icon="⚽",
    layout="wide"
)

# ---- Global CSS — professional, consistent, no decorative fluff ----
st.markdown("""
<style>

/* ---------- Base spacing & typography ---------- */
.block-container {
    padding-top: 1.75rem;
    padding-bottom: 2rem;
    max-width: 1440px;
}

/* ---------- Sidebar ---------- */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0F172A 0%, #1E293B 100%);
    border-right: 1px solid #334155;
}

/* Option-menu inside sidebar */
div.stOptionMenu button {
    color: #CBD5E1 !important;
    border-radius: 8px !important;
    padding: 10px 14px !important;
    margin-bottom: 4px !important;
    font-size: 15px !important;
    transition: background 0.15s;
}
div.stOptionMenu button:hover {
    background: rgba(255,255,255,0.08) !important;
}
div.stOptionMenu button[aria-pressed="true"],
div.stOptionMenu button:focus-visible {
    background: #274482 !important;
    color: #FFFFFF !important;
}

/* Sidebar title */
section[data-testid="stSidebar"] div[data-testid="stMarkdownContainer"] h1,
section[data-testid="stSidebar"] div[data-testid="stMarkdownContainer"] h2,
section[data-testid="stSidebar"] div[data-testid="stMarkdownContainer"] h3 {
    color: #F8FAFC;
    font-weight: 700;
    letter-spacing: -0.02em;
}

/* ---------- KPI Cards ---------- */
.kpi-card {
    background: #FFFFFF;
    border: 1px solid #E2E8F0;
    border-radius: 12px;
    padding: 24px 20px;
    text-align: center;
    box-shadow: 0 1px 3px rgba(0,0,0,0.06);
    transition: box-shadow 0.2s;
}
.kpi-card:hover {
    box-shadow: 0 4px 12px rgba(0,0,0,0.08);
}
.kpi-label {
    font-size: 13px;
    font-weight: 600;
    color: #64748B;
    text-transform: uppercase;
    letter-spacing: 0.06em;
    margin-bottom: 8px;
}
.kpi-value {
    font-size: 36px;
    font-weight: 800;
    color: #1E293B;
    line-height: 1.1;
}
.kpi-accent {
    width: 40px;
    height: 3px;
    background: #274482;
    margin: 12px auto 0;
    border-radius: 2px;
}

/* ---------- Section headers ---------- */
.section-heading {
    font-size: 24px;
    font-weight: 700;
    color: #0F172A;
    margin-bottom: 18px;
    letter-spacing: -0.01em;
}

/* ---------- Navigation cards (Home page) ---------- */
.nav-card {
    background: #FFFFFF;
    border: 1px solid #E2E8F0;
    border-radius: 12px;
    padding: 24px;
    box-shadow: 0 1px 3px rgba(0,0,0,0.04);
}
.nav-card-title {
    font-size: 17px;
    font-weight: 700;
    color: #0F172A;
    margin-bottom: 6px;
}
.nav-card-desc {
    font-size: 14px;
    color: #64748B;
    line-height: 1.55;
    margin-bottom: 14px;
}

/* ---------- Page titles ---------- */
.page-title {
    font-size: 28px;
    font-weight: 700;
    color: #0F172A;
    letter-spacing: -0.02em;
    margin-top: 8px;
    margin-bottom: 4px;
    line-height: 1.25;
}
.page-subtitle {
    font-size: 15px;
    color: #64748B;
    font-weight: 400;
    margin-top: 4px;
    margin-bottom: 18px;
}

/* ---------- Dataframes ---------- */
[data-testid="stDataFrame"] {
    border-radius: 8px;
}

/* ---------- Buttons (secondary) ---------- */
div.stButton button {
    border-radius: 8px !important;
    font-weight: 500 !important;
    font-size: 14px !important;
    padding: 8px 16px !important;
}

/* ---------- Success/Info boxes ---------- */
div[data-testid="stAlertSuccess"],
div[data-testid="stAlertInfo"] {
    border-radius: 8px !important;
}

/* ---------- Insights tabs ---------- */
.insight-text {
    font-size: 15px;
    color: #334155;
    line-height: 1.7;
}

.insight-heading {
    font-size: 18px;
    font-weight: 700;
    color: #0F172A;
    margin-bottom: 16px;
    padding-bottom: 10px;
    border-bottom: 2px solid #274482;
    letter-spacing: -0.01em;
}

/* ---------- H2H section labels ---------- */
.h2h-player-label {
    font-size: 18px;
    font-weight: 700;
    color: #0F172A;
    margin-top: 8px;
    margin-bottom: 12px;
    letter-spacing: -0.01em;
    line-height: 1.3;
}

/* ---------- Hero text ---------- */
.hero-title {
    font-size: 42px;
    font-weight: 800;
    color: #0F172A;
    letter-spacing: -0.03em;
    line-height: 1.15;
    margin-bottom: 8px;
}
.hero-subtitle {
    font-size: 18px;
    font-weight: 500;
    color: #64748B;
    margin-bottom: 14px;
}
.hero-desc {
    max-width: 720px;
    margin: 0 auto;
    color: #64748B;
    font-size: 16px;
    line-height: 1.6;
}

/* ---------- Divider ---------- */
hr {
    border-color: #E2E8F0 !important;
    margin-top: 12px !important;
    margin-bottom: 12px !important;
}

/* ---------- Caption overrides ---------- */
[data-testid="stCaption"] {
    color: #94A3B8 !important;
    font-size: 13px !important;
}

</style>
""", unsafe_allow_html=True)

# ---- Data ----
countries = p.all_data["Country"].unique()


# ---- Helper: centered plot/image ----
def center(content, kind="plot"):
    left, center, right = st.columns([1, 4, 1])
    with center:
        if kind == "plot":
            st.pyplot(content, use_container_width=True)
            plt.close(content)
        else:
            st.image(content, use_container_width=True)


# ---- Navigation ----
NAV_OPTIONS = ["Home", "Explorer", "Head-to-Head", "Leaderboard", "Insights"]

if "nav_target" not in st.session_state:
    st.session_state.nav_target = None


# ---- Sidebar ----
with st.sidebar:

    # Brand header
    st.markdown("### ⚽ FIFA World Cup")
    st.markdown("<span style='color:#94A3B8;font-size:14px;'>Analytics Dashboard</span>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    manual_index = None
    if st.session_state.nav_target is not None:
        manual_index = NAV_OPTIONS.index(st.session_state.nav_target)
        st.session_state.nav_target = None

    page = option_menu(
        menu_title=None,
        options=NAV_OPTIONS,
        icons=[
            "house",
            "search",
            "people",
            "bar-chart",
            "globe2"
        ],
        default_index=0,
        manual_select=manual_index,
        key="nav_menu"
    )

    st.sidebar.markdown("---")
    st.sidebar.markdown(
        "<span style='color:#64748B;font-size:12px;'>Powered by Streamlit &nbsp;|&nbsp; 2026</span>",
        unsafe_allow_html=True
    )


def go_to(page_name):
    st.session_state.nav_target = page_name
    st.rerun()


# =====================================================================
# PAGE: HOME
# =====================================================================
if page == "Home":

    # Hero section
    col_hero_left, col_hero_center, col_hero_right = st.columns([1, 3, 1])
    with col_hero_center:
        st.markdown(
            f"""
            <div style="text-align:center;padding:30px 0 10px 0;">
                <div class="hero-title">FIFA World Cup 2026</div>
                <div class="hero-subtitle">Statistical Analysis Dashboard</div>
                <p class="hero-desc">
                    Explore player performance, team statistics, leaderboards,
                    head-to-head comparisons and tournament insights through
                    interactive visualizations.
                </p>
            </div>
            """,
            unsafe_allow_html=True
        )

    st.divider()

    # ---- KPI Cards ----
    cards = [
        ("Players", p.all_data.shape[0]),
        ("Teams", countries.shape[0]),
        ("Goals", int(p.all_data["Goals"].sum())),
        ("Assists", int(p.all_data["Assists"].sum())),
    ]

    c1, c2, c3, c4 = st.columns(4)

    for col, (title, value) in zip([c1, c2, c3, c4], cards):
        with col:
            st.markdown(
                f"""
                <div class="kpi-card">
                    <div class="kpi-label">{title}</div>
                    <div class="kpi-value">{value:,}</div>
                    <div class="kpi-accent"></div>
                </div>
                """,
                unsafe_allow_html=True
            )

    st.markdown("<br>", unsafe_allow_html=True)

    # ---- Dashboard Overview ----
    st.markdown('<div class="section-heading">Dashboard Overview</div>', unsafe_allow_html=True)

    c1, c2 = st.columns(2, gap="medium")

    with c1:
        with st.container(border=True):
            st.markdown('<div class="nav-card-title">Explorer</div>', unsafe_allow_html=True)
            st.markdown('<div class="nav-card-desc">Analyze players and teams using advanced tournament statistics, performance metrics and interactive visualizations.</div>', unsafe_allow_html=True)
            if st.button("Open Explorer →", key="go_explorer", use_container_width=True):
                go_to("Explorer")
            st.divider()
            st.markdown('<div class="nav-card-title">Head-to-Head</div>', unsafe_allow_html=True)
            st.markdown('<div class="nav-card-desc">Compare players or national teams side-by-side using statistical summaries and radar charts.</div>', unsafe_allow_html=True)
            if st.button("Open Head-to-Head →", key="go_h2h", use_container_width=True):
                go_to("Head-to-Head")

    with c2:
        with st.container(border=True):
            st.markdown('<div class="nav-card-title">Leaderboards</div>', unsafe_allow_html=True)
            st.markdown('<div class="nav-card-desc">Discover tournament leaders across goals, assists, xG, passing, defending and goalkeeping metrics.</div>', unsafe_allow_html=True)
            if st.button("Open Leaderboard →", key="go_leaderboard", use_container_width=True):
                go_to("Leaderboard")
            st.divider()
            st.markdown('<div class="nav-card-title">Insights</div>', unsafe_allow_html=True)
            st.markdown('<div class="nav-card-desc">Review analytical findings and visual summaries highlighting important patterns from the tournament.</div>', unsafe_allow_html=True)
            if st.button("Open Insights →", key="go_insights", use_container_width=True):
                go_to("Insights")

# =====================================================================
# PAGE: EXPLORER
# =====================================================================
elif page == "Explorer":

    st.markdown('<div class="page-title">Explorer</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-subtitle">Explore player and team performance across the tournament.</div>', unsafe_allow_html=True)

    explorer = st.radio("", ["Player", "Team"], horizontal=True, label_visibility="collapsed")
    st.divider()

    if explorer == "Player":

        c1, c2, c3 = st.columns(3)
        pos = c1.selectbox("Position", ["FW", "MF", "DF", "GK"])
        country = c2.selectbox("Country", countries)
        player = c3.selectbox(
            "Player",
            p.all_data[(p.all_data["Position"] == pos) & (p.all_data["Country"] == country)]["Player"]
        )

        table, fig = p.player_details(player, country, pos)

        st.markdown(f'<div class="page-title" style="font-size:24px;">{player}</div>', unsafe_allow_html=True)
        st.caption(f"{country} • {pos}")

        st.dataframe(table, hide_index=True, use_container_width=True)

        center(fig)
        st.caption("Average values are calculated for players in the same position with more than 90 minutes played.")

    else:

        team = st.selectbox("Country", countries)
        table, fig = p.team_details(team)

        st.markdown(f'<div class="page-title" style="font-size:24px;">{team}</div>', unsafe_allow_html=True)
        st.caption("Team Performance Summary")

        st.dataframe(table, hide_index=True, use_container_width=True)
        center(fig)

# =====================================================================
# PAGE: HEAD-TO-HEAD
# =====================================================================
elif page == "Head-to-Head":

    st.markdown('<div class="page-title">Head-to-Head</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-subtitle">Compare players or national teams side by side.</div>', unsafe_allow_html=True)

    comparison = st.radio("", ["Player vs Player", "Team vs Team"], horizontal=True, label_visibility="collapsed")
    st.divider()

    if comparison == "Player vs Player":

        pos = st.selectbox("Position", ["FW", "MF", "DF", "GK"])

        DEFAULT_P1_COUNTRY = "FRA"
        DEFAULT_P2_COUNTRY = "ARG"

        c1, c2 = st.columns(2)

        with c1:
            st.markdown('<div class="h2h-player-label">Player 1</div>', unsafe_allow_html=True)
            country1 = st.selectbox(
                "Country", countries,
                index=list(countries).index(DEFAULT_P1_COUNTRY) if DEFAULT_P1_COUNTRY in countries else 0,
                key="country1"
            )
            player1 = st.selectbox(
                "Player",
                p.all_data[(p.all_data["Position"] == pos) & (p.all_data["Country"] == country1)]["Player"],
                key="player1"
            )

        with c2:
            st.markdown('<div class="h2h-player-label">Player 2</div>', unsafe_allow_html=True)
            country2 = st.selectbox(
                "Country", countries,
                index=list(countries).index(DEFAULT_P2_COUNTRY) if DEFAULT_P2_COUNTRY in countries else 1,
                key="country2"
            )
            player2 = st.selectbox(
                "Player",
                p.all_data[(p.all_data["Position"] == pos) & (p.all_data["Country"] == country2)]["Player"],
                key="player2"
            )

        st.divider()

        if player1 == player2 and country1 == country2:
            st.info("Choose different players.")
        else:
            fig, table, winner, score = p.player_vs_player(player1, player2, country1, country2, pos)

            st.dataframe(table, hide_index=True, use_container_width=True)

            st.success(
                f"Winner: {winner}\n\n"
                f"{list(score.keys())[0]} : {list(score.values())[0]} | "
                f"{list(score.keys())[1]} : {list(score.values())[1]}"
            )

            center(fig)

    else:

        DEFAULT_T1 = "FRA"
        DEFAULT_T2 = "BRA"

        c1, c2 = st.columns(2)

        country1 = c1.selectbox(
            "Team 1", countries,
            index=list(countries).index(DEFAULT_T1) if DEFAULT_T1 in countries else 0,
            key="team1"
        )
        country2 = c2.selectbox(
            "Team 2", countries,
            index=list(countries).index(DEFAULT_T2) if DEFAULT_T2 in countries else 1,
            key="team2"
        )

        st.divider()

        if country1 == country2:
            st.info("Choose different teams.")
        else:
            fig, table, winner, score = p.team_vs_team(country1, country2)

            st.dataframe(table, hide_index=True, use_container_width=True)

            st.success(
                f"Winner: {winner}\n\n"
                f"{list(score.keys())[0]} : {list(score.values())[0]} | "
                f"{list(score.keys())[1]} : {list(score.values())[1]}"
            )
            center(fig)

# =====================================================================
# PAGE: LEADERBOARD
# =====================================================================
elif page == "Leaderboard":

    st.markdown('<div class="page-title">Leaderboard</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-subtitle">Rankings across all major statistical categories.</div>', unsafe_allow_html=True)

    top = st.slider("Top N", 5, 30, 10)
    tabs = st.tabs(["Goals", "Assists", "xG", "Passing", "Discipline", "Turnovers", "Saves"])
    funcs = [
        p.top_goals_plot,
        p.top_assists_plot,
        p.top_xg_plot,
        p.top_pass_plot,
        p.least_discipline_plot,
        p.top_turnovers_plot,
        p.top_saves_plot,
    ]

    for t, f in zip(tabs, funcs):
        with t:
            center(f(top))

# =====================================================================
# PAGE: INSIGHTS
# =====================================================================
else:

    INSIGHTS_DIR = "assets/insights/"

    st.markdown('<div class="page-title">Insights</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-subtitle">Analytical findings and visual summaries from the tournament.</div>', unsafe_allow_html=True)

    insights = [
        (
            "graph1.png",
            """
**Analysis:** The xG distribution is heavily right-skewed with extreme zero-inflation. The median (0.02) is far below the mean (0.21), confirming that most players generated negligible expected goals. The distribution follows a power-law pattern typical of elite sports: a small number of elite attackers (led by Mbappé at 6.54) account for a disproportionate share of total xG. This has direct implications for player valuation — the gap between the top 5% and the rest is enormous.
""",
        ),
        (
            "graph2.png",
            """
**Analysis:** The scatter plot reveals a moderate positive correlation (r ≈ 0.48) between minutes played and goals among forwards and midfielders — more playing time generally yields more goals, but the relationship is far from deterministic. The wide vertical spread at all minute levels shows that shot quality and finishing ability vary enormously even among players with similar playing time. Mbappé's outlier position (most minutes, most goals) reflects both his playing time and exceptional finishing.
""",
        ),
        (
            "graph3.png",
            """
**Analysis:** This chart shows something intuitive once you see it: players who only touch the ball a little (50–150 passes) have wildly inconsistent accuracy — anywhere from 50% to 97%. But players who pass constantly (400+ passes) all land in a tight, elite band of 87–97%. Why? It's the same reason a coin flipped 5 times can look "unfair," but flipped 500 times always settles near 50/50 — small samples are noisy, and a player's *true* skill only shows up once they've had enough chances to prove it. That's also why the overall link between volume and accuracy looks only moderate (r = 0.36) — it's not that more passing *causes* better accuracy, it's that the extremes fade out as sample size grows. Rodri is the standout case: 799 passes at 93.5% accuracy — he didn't just pass a lot, he stayed elite while doing it, at a volume nobody else in the tournament came close to. The practical takeaway for scouting: never trust an accuracy number on its own — always check how many passes it's based on. Below ~50 passes, a single bad ball can swing a player's "accuracy" by 10+ points.
""",
        ),
        (
            "graph4.png",
            """
**Analysis:** The chart shows how yellow card frequency varies by position. Goalkeepers (GK) typically receive the fewest cards, while defenders (DF) and midfielders (MF) average higher due to their involvement in physical challenges. The error bars show that within each position group, there's considerable variation — some players accumulate many cards while most in the same position get none. This suggests individual temperament and playing style matter more than position alone.
""",
        ),
        (
            "graph5.png",
            """
**Analysis:** The strong positive correlation (r = 0.80) between defensive pressures and forced turnovers is one of the most robust findings in this analysis. The scatter plot shows a clear linear trend with consistent spread around the regression line. This has direct business value: coaches can use press intensity as a proxy metric for ball-winning effectiveness during player evaluation, even without direct turnover data. The relationship holds across all positions, suggesting it's a universal football principle rather than position-specific.
""",
        ),
        (
            "graph6.png",
            """
**Analysis:** The near-perfect correlation (r ≈ 0.95) between total actions and saves is expected — keepers facing more shots will mechanically accumulate both stats. The more interesting metric is **save rate** (saves / total actions), which ranges from ~8% to ~15% across the top keepers. Orlando Gill's outlier position reflects Paraguay's defensive strategy: his team allowed many shots, giving him both high total actions and high save counts. For goalkeeper evaluation, save rate and actions-inside-box ratio are more informative than raw save counts.
""",
        ),
    ]

    tabs = st.tabs([f"Insight {i+1}" for i in range(len(insights))])

    for tab, (filename, analysis) in zip(tabs, insights):
        with tab:
            img_path = INSIGHTS_DIR + filename
            center(img_path, kind="image")

            dl_col, zoom_col = st.columns([1, 3])
            with dl_col:
                with open(img_path, "rb") as f:
                    st.download_button(
                        "⬇ Save chart",
                        data=f.read(),
                        file_name=filename,
                        mime="image/png",
                        key=f"dl_{filename}"
                    )
            with zoom_col:
                st.caption("Tip: hover the chart and click the ⛶ icon in its top-right corner to view it full-screen/zoomed in.")

            # Split "**Analysis:** ..." into a styled heading + body
            raw = analysis.strip()
            if raw.startswith("**Analysis:**"):
                after_marker = raw[len("**Analysis:**"):].strip()
                # Prefer a real sentence boundary: punctuation followed by whitespace and a capital letter.
                match = re.search(r'([.!?])\s+(?=[A-Z])', after_marker)
                split_at = match.end() - 1 if match else None
                if split_at is not None:
                    heading_text = after_marker[:split_at + 1].strip()
                    body_text = after_marker[split_at + 1:].strip()
                    st.markdown(
                        f'<div class="insight-heading">{heading_text}</div>',
                        unsafe_allow_html=True
                    )
                    st.markdown(
                        f'<div class="insight-text">{body_text}</div>',
                        unsafe_allow_html=True
                    )
                else:
                    st.markdown(f'<div class="insight-text">{raw}</div>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="insight-text">{raw}</div>', unsafe_allow_html=True)

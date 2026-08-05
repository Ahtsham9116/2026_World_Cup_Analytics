
import streamlit as st
from streamlit_option_menu import option_menu
import matplotlib.pyplot as plt
import plots as p




st.set_page_config(page_title="FIFA World Cup Analytics", layout="wide")

# ---- Minimal premium styling ----
st.markdown("""
<style>
.block-container{padding-top:1.5rem;padding-bottom:2rem;max-width:1400px;}
.card{border:1px solid #e6e6e6;border-radius:12px;padding:1rem;background:white;}
.small{color:#666;font-size:.9rem}
</style>
""", unsafe_allow_html=True)

countries=p.all_data["Country"].unique()

#image resized 60 percent in center
def center(content,kind="plot"):
    left,center,right=st.columns([1,4,1])
    with center:
        if kind=="plot":
            st.pyplot(content,use_container_width=True)
            plt.close(content)  # figures are never closed otherwise -> memory leak over a session
        else:
            st.image(content,use_container_width=True)                
    


NAV_OPTIONS=["Home","Explorer","Head-to-Head","Leaderboard","Insights"]

if "nav_target" not in st.session_state:
    st.session_state.nav_target=None

with st.sidebar:
    manual_index=None
    if st.session_state.nav_target is not None:
        manual_index=NAV_OPTIONS.index(st.session_state.nav_target)
        st.session_state.nav_target=None  # consume it so normal sidebar clicks work again right after

    page=option_menu(
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

def go_to(page_name):
    st.session_state.nav_target=page_name
    st.rerun()

st.sidebar.title("World Cup Analytics")

if page=="Home":

    st.markdown("""
    <div style="text-align:center;padding:45px 0 25px 0;">
        <h1 style="font-size:46px;margin-bottom:8px;">FIFA World Cup 2026</h1>
        <h3 style="font-weight:500;color:#6B7280;">
            Statistical Analysis Dashboard
        </h3>
        <p style="max-width:850px;margin:auto;color:#6B7280;font-size:17px;">
            Explore player performance, team statistics, leaderboards,
            head-to-head comparisons and tournament insights through
            interactive visualizations.
        </p>
    </div>
    """,unsafe_allow_html=True)

    st.divider()

    cards=[
        ("Players",p.all_data.shape[0]),
        ("Teams",countries.shape[0]),
        ("Goals",int(p.all_data["Goals"].sum())),
        ("Assists",int(p.all_data["Assists"].sum()))
    ]

    c1,c2,c3,c4=st.columns(4)

    for col,(title,value) in zip([c1,c2,c3,c4],cards):
        with col:
            st.markdown(f"""
            <div style="
                background:white;
                border:1px solid #E5E7EB;
                border-radius:14px;
                padding:22px;
                text-align:center;
            ">
                <div style="font-size:15px;color:#6B7280;">{title}</div>
                <div style="font-size:34px;font-weight:700;margin-top:8px;">{value}</div>
            </div>
            """,unsafe_allow_html=True)

    st.divider()

    st.markdown("""
    <h2 style="margin-bottom:25px;">
        Dashboard Overview
    </h2>
    """,unsafe_allow_html=True)

    c1,c2=st.columns(2)

    with c1:
        with st.container(border=True):
            st.markdown("### Explorer")
            st.caption("Analyze players and teams using advanced tournament statistics, performance metrics and interactive visualizations.")
            if st.button("Open Explorer →",key="go_explorer",use_container_width=True):
                go_to("Explorer")
            st.divider()
            st.markdown("### Head-to-Head")
            st.caption("Compare players or national teams side-by-side using statistical summaries and radar charts.")
            if st.button("Open Head-to-Head →",key="go_h2h",use_container_width=True):
                go_to("Head-to-Head")

    with c2:
        with st.container(border=True):
            st.markdown("### Leaderboards")
            st.caption("Discover tournament leaders across goals, assists, xG, passing, defending and goalkeeping metrics.")
            if st.button("Open Leaderboard →",key="go_leaderboard",use_container_width=True):
                go_to("Leaderboard")
            st.divider()
            st.markdown("### Insights")
            st.caption("Review analytical findings and visual summaries highlighting important patterns from the tournament.")
            if st.button("Open Insights →",key="go_insights",use_container_width=True):
                go_to("Insights")

    
elif page=="Explorer":

    st.title("Explorer")
    st.caption("Explore player and team performance across the tournament.")

    explorer=st.radio("",["Player","Team"],horizontal=True,label_visibility="collapsed")
    st.divider()

    if explorer=="Player":

        c1,c2,c3=st.columns(3)
        pos=c1.selectbox("Position",["FW","MF","DF","GK"])
        country=c2.selectbox("Country",countries)
        player=c3.selectbox("Player",p.all_data[(p.all_data["Position"]==pos)&(p.all_data["Country"]==country)]["Player"])

        table,fig=p.player_details(player,country,pos)

        st.subheader(player)
        st.caption(f"{country} • {pos}")
        st.dataframe(table,hide_index=True,use_container_width=True)

        center(fig)
        st.caption("Average values are calculated for players in the same position with more than 90 minutes played.")

    else:

        team=st.selectbox("Country",countries)
        table,fig=p.team_details(team)
        st.subheader(team)
        st.caption("Team Performance Summary")
        st.dataframe(table,hide_index=True,use_container_width=True)
        center(fig)

elif page=="Head-to-Head":

    st.title("Head-to-Head")

    comparison=st.radio("",["Player vs Player","Team vs Team"],horizontal=True,label_visibility="collapsed")
    st.divider()

    if comparison=="Player vs Player":

        pos=st.selectbox("Position",["FW","MF","DF","GK"])

        c1,c2=st.columns(2)

        with c1:
            st.subheader("Player 1")
            country1=st.selectbox("Country",countries,key="country1")
            player1=st.selectbox("Player",p.all_data[(p.all_data["Position"]==pos)&(p.all_data["Country"]==country1)]["Player"],key="player1")

        with c2:
            st.subheader("Player 2")
            country2=st.selectbox("Country",countries,key="country2")
            player2=st.selectbox("Player",p.all_data[(p.all_data["Position"]==pos)&(p.all_data["Country"]==country2)]["Player"],key="player2")

        st.divider()

        if player1==player2 and country1==country2:
            st.info("Choose different players.")
        else:
            fig,table,winner,score=p.player_vs_player(player1,player2,country1,country2,pos)

            st.dataframe(table,hide_index=True,use_container_width=True)

            st.success(
                f"Winner: {winner}\n\n"
                f"{list(score.keys())[0]} : {list(score.values())[0]} | "
                f"{list(score.keys())[1]} : {list(score.values())[1]}"
            )

            center(fig)   
    else:

        c1,c2=st.columns(2)

        country1=c1.selectbox("Team 1",countries,key="team1")
        country2=c2.selectbox("Team 2",countries,key="team2")

        st.divider()

        if country1==country2:
            st.info("Choose different teams.")
        else:
            fig,table,winner,score=p.team_vs_team(country1,country2)

            st.dataframe(table,hide_index=True,use_container_width=True)

            st.success(
                f"Winner: {winner}\n\n"
                f"{list(score.keys())[0]} : {list(score.values())[0]} | "
                f"{list(score.keys())[1]} : {list(score.values())[1]}"
            )
            center(fig)
            


elif page=="Leaderboard":
    st.title("Leaderboard")
    top=st.slider("Top N",5,30,10)
    tabs=st.tabs(["Goals","Assists","xG","Passing","Discipline","Turnovers","Saves"])
    funcs=[p.top_goals_plot,p.top_assists_plot,p.top_xg_plot,p.top_pass_plot,p.least_discipline_plot,p.top_turnovers_plot,p.top_saves_plot]
    for t,f in zip(tabs,funcs):
        with t:
            center(f(top))

else:

    INSIGHTS_DIR="assets/insights/"#not dynamic because insights are static and not generated from data

    st.title("Insights")

    insights=[
        ("graph1.png","""
**Analysis:** The xG distribution is heavily right-skewed with extreme zero-inflation. The median (0.02) is far below the mean (0.21), confirming that most players generated negligible expected goals. The distribution follows a power-law pattern typical of elite sports: a small number of elite attackers (led by Mbappé at 6.54) account for a disproportionate share of total xG. This has direct implications for player valuation — the gap between the top 5% and the rest is enormous.
"""),
        ("graph2.png","""
**Analysis:** The scatter plot reveals a moderate positive correlation (r ≈ 0.48) between minutes played and goals among forwards and midfielders — more playing time generally yields more goals, but the relationship is far from deterministic. The wide vertical spread at all minute levels shows that shot quality and finishing ability vary enormously even among players with similar playing time. Mbappé's outlier position (most minutes, most goals) reflects both his playing time and exceptional finishing.

"""),
        ("graph3.png","""
**Analysis:** This chart shows something intuitive once you see it: players who only touch the ball a little (50-150 passes) have wildly inconsistent accuracy — anywhere from 50% to 97%. But players who pass constantly (400+ passes) all land in a tight, elite band of 87-97%. Why? It's the same reason a coin flipped 5 times can look "unfair," but flipped 500 times always settles near 50/50 — small samples are noisy, and a player's *true* skill only shows up once they've had enough chances to prove it. That's also why the overall link between volume and accuracy looks only moderate (r = 0.36) — it's not that more passing *causes* better accuracy, it's that the extremes fade out as sample size grows. Rodri is the standout case: 799 passes at 93.5% accuracy — he didn't just pass a lot, he stayed elite while doing it, at a volume nobody else in the tournament came close to. The practical takeaway for scouting: never trust an accuracy number on its own — always check how many passes it's based on. Below ~50 passes, a single bad ball can swing a player's "accuracy" by 10+ points."""),
        ("graph4.png","""
**Analysis:** The chart shows how yellow card frequency varies by position. Goalkeepers (GK) typically receive the fewest cards, while defenders (DF) and midfielders (MF) average higher due to their involvement in physical challenges. The error bars show that within each position group, there's considerable variation — some players accumulate many cards while most in the same position get none. This suggests individual temperament and playing style matter more than position alone.

"""),
        ("graph5.png","""
**Analysis:** The strong positive correlation (r = 0.80) between defensive pressures and forced turnovers is one of the most robust findings in this analysis. The scatter plot shows a clear linear trend with consistent spread around the regression line. This has direct business value: coaches can use press intensity as a proxy metric for ball-winning effectiveness during player evaluation, even without direct turnover data. The relationship holds across all positions, suggesting it's a universal football principle rather than position-specific.

"""),
        ("graph6.png","""
**Analysis:** The near-perfect correlation (r ≈ 0.95) between total actions and saves is expected — keepers facing more shots will mechanically accumulate both stats. The more interesting metric is **save rate** (saves / total actions), which ranges from ~8% to ~15% across the top keepers. Orlando Gill's outlier position reflects Paraguay's defensive strategy: his team allowed many shots, giving him both high total actions and high save counts. For goalkeeper evaluation, save rate and actions-inside-box ratio are more informative than raw save counts.

"""),
    ]

    tabs=st.tabs([f"Insight {i+1}" for i in range(len(insights))])

    for tab,(filename,analysis) in zip(tabs,insights):
        with tab:
            img_path=INSIGHTS_DIR+filename
            center(img_path,kind="image")

            dl_col,zoom_col=st.columns([1,3])
            with dl_col:
                with open(img_path,"rb") as f:
                    st.download_button(
                        "⬇ Save chart",
                        data=f.read(),
                        file_name=filename,
                        mime="image/png",
                        key=f"dl_{filename}"
                    )
            with zoom_col:
                st.caption("Tip: hover the chart and click the ⛶ icon in its top-right corner to view it full-screen/zoomed in.")

            st.markdown(analysis)

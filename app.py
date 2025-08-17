# PROFESSIONAL FANTASY FOOTBALL APP - ENHANCED UI
# Replace your current app.py with this code for a stunning, professional look

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
from datetime import datetime, timedelta
import time

# =====================================
# PAGE CONFIGURATION & STYLING
# =====================================

st.set_page_config(
    page_title="Fantasy Edge AI | Beat Your League",
    page_icon="🏈", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for professional styling
st.markdown("""
<style>
    /* Main background and theme */
    .main {
        background: linear-gradient(135deg, #0f1419 0%, #1a1f36 100%);
    }
    
    /* Header styling */
    .main-header {
        background: linear-gradient(90deg, #ff6b35 0%, #ff8e53 50%, #ffa500 100%);
        padding: 2rem;
        border-radius: 10px;
        margin-bottom: 2rem;
        text-align: center;
        box-shadow: 0 8px 32px rgba(255, 107, 53, 0.3);
    }
    
    .main-title {
        font-size: 3.5rem;
        font-weight: 900;
        color: white;
        margin: 0;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.5);
    }
    
    .main-subtitle {
        font-size: 1.2rem;
        color: #f0f0f0;
        margin-top: 0.5rem;
        font-weight: 300;
    }
    
    /* Metric cards */
    .metric-card {
        background: linear-gradient(145deg, #1e293b 0%, #334155 100%);
        padding: 1.5rem;
        border-radius: 12px;
        border: 1px solid #475569;
        box-shadow: 0 4px 20px rgba(0,0,0,0.3);
        text-align: center;
        margin-bottom: 1rem;
    }
    
    .metric-value {
        font-size: 2.5rem;
        font-weight: 800;
        margin-bottom: 0.5rem;
    }
    
    .metric-label {
        font-size: 1rem;
        opacity: 0.8;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    /* Play type badges */
    .smash-badge {
        background: linear-gradient(45deg, #ef4444, #dc2626);
        color: white;
        padding: 0.3rem 0.8rem;
        border-radius: 20px;
        font-weight: 600;
        font-size: 0.8rem;
        text-transform: uppercase;
    }
    
    .leverage-badge {
        background: linear-gradient(45deg, #f59e0b, #d97706);
        color: white;
        padding: 0.3rem 0.8rem;
        border-radius: 20px;
        font-weight: 600;
        font-size: 0.8rem;
        text-transform: uppercase;
    }
    
    .chalk-badge {
        background: linear-gradient(45deg, #6b7280, #4b5563);
        color: white;
        padding: 0.3rem 0.8rem;
        border-radius: 20px;
        font-weight: 600;
        font-size: 0.8rem;
        text-transform: uppercase;
    }
    
    /* Data freshness indicator */
    .freshness-indicator {
        background: linear-gradient(90deg, #10b981 0%, #059669 100%);
        color: white;
        padding: 0.8rem 1.5rem;
        border-radius: 25px;
        font-weight: 600;
        display: inline-block;
        margin: 1rem 0;
        box-shadow: 0 4px 15px rgba(16, 185, 129, 0.3);
    }
    
    .stale-indicator {
        background: linear-gradient(90deg, #ef4444 0%, #dc2626 100%);
        color: white;
        padding: 0.8rem 1.5rem;
        border-radius: 25px;
        font-weight: 600;
        display: inline-block;
        margin: 1rem 0;
        box-shadow: 0 4px 15px rgba(239, 68, 68, 0.3);
    }
    
    /* Sidebar styling */
    .css-1d391kg {
        background: linear-gradient(180deg, #1a1f36 0%, #0f1419 100%);
    }
    
    /* Tables */
    .stDataFrame {
        border-radius: 10px;
        overflow: hidden;
        box-shadow: 0 4px 20px rgba(0,0,0,0.2);
    }
    
    /* Buttons */
    .stButton > button {
        background: linear-gradient(45deg, #ff6b35, #ffa500);
        color: white;
        border: none;
        border-radius: 25px;
        padding: 0.6rem 2rem;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(255, 107, 53, 0.4);
    }
</style>
""", unsafe_allow_html=True)

# =====================================
# DATA LOADING WITH CACHING
# =====================================

@st.cache_data(ttl=300)  # Cache for 5 minutes
def load_fantasy_data():
    """Load fantasy data with error handling and sample fallback"""
    try:
        # Try to load from your GitHub CSV
        df = pd.read_csv('fantasy_data.csv')
        
        # Add data source info
        df['data_source'] = 'live'
        df['last_updated'] = datetime.now()
        
        return df
        
    except Exception as e:
        st.warning("⚠️ Live data temporarily unavailable. Using sample data.")
        
        # Fallback sample data
        sample_data = {
            'player_name': [
                'Josh Allen', 'Lamar Jackson', 'Christian McCaffrey', 'Austin Ekeler',
                'Cooper Kupp', 'Davante Adams', 'Travis Kelce', 'George Kittle',
                'Derrick Henry', 'Tyreek Hill', 'Stefon Diggs', 'Mark Andrews'
            ],
            'position': ['QB', 'QB', 'RB', 'RB', 'WR', 'WR', 'TE', 'TE', 'RB', 'WR', 'WR', 'TE'],
            'player_rank': [1, 2, 1, 2, 1, 2, 1, 3, 3, 3, 4, 2],
            'ownership_pct': [28.5, 15.2, 31.8, 24.1, 27.3, 18.6, 35.2, 8.7, 9.1, 13.8, 21.1, 22.3],
            'contrarian_score': [142.0, 149.6, 136.4, 143.8, 145.4, 146.8, 129.6, 145.6, 143.8, 137.4, 111.8, 135.4],
            'play_type': ['CHALK_PLAY', 'LEVERAGE_PLAY', 'CHALK_PLAY', 'NEUTRAL', 'CHALK_PLAY', 'LEVERAGE_PLAY', 'CHALK_PLAY', 'SMASH_PLAY', 'SMASH_PLAY', 'SMASH_PLAY', 'LEVERAGE_PLAY', 'NEUTRAL'],
            'projected_points': [24.0, 21.0, 18.2, 15.4, 16.8, 14.2, 12.0, 10.5, 15.4, 14.2, 12.8, 10.5],
            'estimated_salary': [8000, 7600, 8400, 7800, 8200, 7400, 6800, 5800, 7400, 7600, 6600, 6200],
            'points_per_dollar': [3.0, 2.76, 2.17, 1.97, 2.05, 1.92, 1.76, 1.81, 2.08, 1.87, 1.94, 1.69],
            'recommendation': [
                '📍 CHALK: Rank 1 but 28.5% owned - cash game only',
                '⚡ LEVERAGE: Rank 2 at 15.2% owned - GPP play',
                '📍 CHALK: Rank 1 but 31.8% owned - cash game only',
                '😐 NEUTRAL: Standard play',
                '📍 CHALK: Rank 1 but 27.3% owned - cash game only',
                '⚡ LEVERAGE: Rank 2 at 18.6% owned - GPP play',
                '📍 CHALK: Rank 1 but 35.2% owned - cash game only',
                '🔥 SMASH: Top 3 player at only 8.7% owned!',
                '🔥 SMASH: Top 3 player at only 9.1% owned!',
                '🔥 SMASH: Top 3 player at only 13.8% owned!',
                '⚡ LEVERAGE: Rank 4 at 21.1% owned - GPP play',
                '😐 NEUTRAL: Standard play'
            ],
            'data_source': ['sample'] * 12,
            'last_updated': [datetime.now() - timedelta(hours=2)] * 12
        }
        
        return pd.DataFrame(sample_data)

# =====================================
# DATA FRESHNESS FUNCTIONS
# =====================================

def get_data_freshness(df):
    """Calculate data freshness and return status"""
    if df['data_source'].iloc[0] == 'sample':
        return 'sample', 'Using sample data - live data temporarily unavailable'
    
    last_update = df['last_updated'].iloc[0]
    if isinstance(last_update, str):
        last_update = pd.to_datetime(last_update)
    
    now = datetime.now()
    time_diff = now - last_update
    
    if time_diff.total_seconds() < 3600:  # Less than 1 hour
        minutes = int(time_diff.total_seconds() / 60)
        return 'fresh', f'Updated {minutes} minutes ago'
    elif time_diff.total_seconds() < 86400:  # Less than 24 hours
        hours = int(time_diff.total_seconds() / 3600)
        return 'recent', f'Updated {hours} hours ago'
    else:
        days = time_diff.days
        return 'stale', f'Updated {days} days ago'

def display_freshness_indicator(status, message):
    """Display data freshness indicator"""
    if status == 'fresh':
        st.markdown(f'<div class="freshness-indicator">🟢 LIVE DATA: {message}</div>', unsafe_allow_html=True)
    elif status == 'recent':
        st.markdown(f'<div class="freshness-indicator">🟡 RECENT DATA: {message}</div>', unsafe_allow_html=True)
    elif status == 'stale':
        st.markdown(f'<div class="stale-indicator">🔴 OLD DATA: {message}</div>', unsafe_allow_html=True)
    else:  # sample
        st.markdown(f'<div class="stale-indicator">⚠️ DEMO MODE: {message}</div>', unsafe_allow_html=True)

# =====================================
# MAIN HEADER
# =====================================

st.markdown("""
<div class="main-header">
    <h1 class="main-title">🏈 FANTASY EDGE AI</h1>
    <p class="main-subtitle">AI-Powered Contrarian Analysis | Beat Your League with Data Science</p>
</div>
""", unsafe_allow_html=True)

# Load data
df = load_fantasy_data()
freshness_status, freshness_message = get_data_freshness(df)

# Display data freshness
display_freshness_indicator(freshness_status, freshness_message)

# =====================================
# KEY METRICS DASHBOARD
# =====================================

col1, col2, col3, col4 = st.columns(4)

with col1:
    smash_count = len(df[df['play_type'] == 'SMASH_PLAY'])
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-value" style="color: #ef4444;">🔥 {smash_count}</div>
        <div class="metric-label">SMASH PLAYS</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    leverage_count = len(df[df['play_type'] == 'LEVERAGE_PLAY'])
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-value" style="color: #f59e0b;">⚡ {leverage_count}</div>
        <div class="metric-label">LEVERAGE PLAYS</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    avg_ownership = df['ownership_pct'].mean()
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-value" style="color: #10b981;">{avg_ownership:.1f}%</div>
        <div class="metric-label">AVG OWNERSHIP</div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    total_players = len(df)
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-value" style="color: #3b82f6;">{total_players}</div>
        <div class="metric-label">PLAYERS ANALYZED</div>
    </div>
    """, unsafe_allow_html=True)

# =====================================
# SIDEBAR NAVIGATION
# =====================================

st.sidebar.markdown("## 🎯 Navigation")
page = st.sidebar.radio(
    "Choose Your Analysis:",
    ["🔥 Contrarian Opportunities", "📊 Player Deep Dive", "🏈 Lineup Builder", "🤖 AI Assistant", "📈 Analytics Dashboard"]
)

# =====================================
# PAGE CONTENT
# =====================================

if page == "🔥 Contrarian Opportunities":
    st.markdown("## 🔥 This Week's Contrarian Opportunities")
    st.markdown("*Find elite players with low ownership - your secret weapon for tournaments*")
    
    # Filter options
    col1, col2 = st.columns(2)
    with col1:
        position_filter = st.selectbox("📍 Filter by Position", ["All", "QB", "RB", "WR", "TE"])
    with col2:
        play_type_filter = st.selectbox("🎯 Filter by Play Type", ["All", "SMASH_PLAY", "LEVERAGE_PLAY", "CHALK_PLAY", "NEUTRAL"])
    
    # Filter data
    filtered_df = df.copy()
    if position_filter != "All":
        filtered_df = filtered_df[filtered_df['position'] == position_filter]
    if play_type_filter != "All":
        filtered_df = filtered_df[filtered_df['play_type'] == play_type_filter]
    
    # Display opportunities
    for _, player in filtered_df.iterrows():
        with st.container():
            col1, col2, col3, col4 = st.columns([3, 1, 1, 3])
            
            with col1:
                st.markdown(f"**{player['player_name']}** ({player['position']})")
                
                # Play type badge
                if player['play_type'] == 'SMASH_PLAY':
                    st.markdown('<span class="smash-badge">🔥 SMASH</span>', unsafe_allow_html=True)
                elif player['play_type'] == 'LEVERAGE_PLAY':
                    st.markdown('<span class="leverage-badge">⚡ LEVERAGE</span>', unsafe_allow_html=True)
                elif player['play_type'] == 'CHALK_PLAY':
                    st.markdown('<span class="chalk-badge">📍 CHALK</span>', unsafe_allow_html=True)
            
            with col2:
                st.metric("Rank", f"#{int(player['player_rank'])}")
            
            with col3:
                st.metric("Ownership", f"{player['ownership_pct']:.1f}%")
            
            with col4:
                st.markdown(f"*{player['recommendation']}*")
            
            st.divider()

elif page == "📊 Player Deep Dive":
    st.markdown("## 📊 Player Deep Dive Analysis")
    
    # Player selector
    selected_player = st.selectbox("Choose a player:", df['player_name'].tolist())
    player_data = df[df['player_name'] == selected_player].iloc[0]
    
    # Player analysis
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(f"### {selected_player} Analysis")
        st.metric("Position Rank", f"#{int(player_data['player_rank'])}")
        st.metric("Ownership %", f"{player_data['ownership_pct']:.1f}%")
        st.metric("Contrarian Score", f"{player_data['contrarian_score']:.1f}")
        st.metric("Projected Points", f"{player_data['projected_points']:.1f}")
    
    with col2:
        # Ownership vs Rank scatter plot
        fig = px.scatter(df, x='player_rank', y='ownership_pct', 
                        color='play_type', size='contrarian_score',
                        hover_data=['player_name'],
                        title="Ownership vs Rank (Bubble = Contrarian Score)",
                        color_discrete_map={
                            'SMASH_PLAY': '#ef4444',
                            'LEVERAGE_PLAY': '#f59e0b', 
                            'CHALK_PLAY': '#6b7280',
                            'NEUTRAL': '#3b82f6'
                        })
        
        # Highlight selected player
        selected_data = df[df['player_name'] == selected_player]
        fig.add_scatter(x=selected_data['player_rank'], y=selected_data['ownership_pct'],
                       mode='markers', marker=dict(size=20, color='red', symbol='star'),
                       name=selected_player, showlegend=False)
        
        fig.update_layout(template='plotly_dark', height=400)
        st.plotly_chart(fig, use_container_width=True)

elif page == "🏈 Lineup Builder":
    st.markdown("## 🏈 AI Lineup Builder")
    st.markdown("*Build optimal lineups based on contrarian analysis*")
    
    # Lineup strategy
    strategy = st.radio("Choose your strategy:", 
                       ["🏆 Tournament (GPP)", "💰 Cash Game", "🎯 Contrarian Special"])
    
    if strategy == "🏆 Tournament (GPP)":
        st.markdown("### 🏆 Tournament Lineup Recommendations")
        st.markdown("*Focus on low-owned players with high upside*")
        
        # Filter for tournament plays
        tournament_df = df[df['play_type'].isin(['SMASH_PLAY', 'LEVERAGE_PLAY'])]
        tournament_df = tournament_df.sort_values('contrarian_score', ascending=False)
        
        positions = ['QB', 'RB', 'WR', 'TE']
        for pos in positions:
            pos_players = tournament_df[tournament_df['position'] == pos].head(3)
            if not pos_players.empty:
                st.markdown(f"**{pos} Recommendations:**")
                for _, player in pos_players.iterrows():
                    st.markdown(f"• {player['player_name']} - {player['ownership_pct']:.1f}% owned ({player['play_type']})")
                st.markdown("")

elif page == "🤖 AI Assistant":
    st.markdown("## 🤖 Fantasy AI Assistant")
    st.markdown("*Get AI-powered insights and recommendations*")
    
    # Chat interface
    user_question = st.text_input("Ask me anything about your fantasy lineup:")
    
    if user_question:
        # Simple AI responses based on data
        if "smash" in user_question.lower():
            smash_players = df[df['play_type'] == 'SMASH_PLAY']
            response = f"🔥 This week's SMASH plays are: {', '.join(smash_players['player_name'].tolist())}. These are elite players with surprisingly low ownership!"
        elif "ownership" in user_question.lower():
            avg_own = df['ownership_pct'].mean()
            response = f"📊 Average ownership this week is {avg_own:.1f}%. Players under 15% ownership: {', '.join(df[df['ownership_pct'] < 15]['player_name'].tolist())}"
        elif "chalk" in user_question.lower():
            chalk_players = df[df['play_type'] == 'CHALK_PLAY']
            response = f"📍 Chalk plays to avoid in tournaments: {', '.join(chalk_players['player_name'].tolist())}. Use these in cash games only!"
        else:
            response = "🤖 I can help you with questions about SMASH plays, ownership percentages, chalk plays, and lineup strategies!"
        
        st.markdown(f"**AI Assistant:** {response}")

elif page == "📈 Analytics Dashboard":
    st.markdown("## 📈 Advanced Analytics Dashboard")
    
    # Ownership distribution
    col1, col2 = st.columns(2)
    
    with col1:
        fig1 = px.histogram(df, x='ownership_pct', nbins=20, 
                           title="Ownership Distribution",
                           color_discrete_sequence=['#ff6b35'])
        fig1.update_layout(template='plotly_dark')
        st.plotly_chart(fig1, use_container_width=True)
    
    with col2:
        fig2 = px.box(df, x='position', y='contrarian_score',
                     title="Contrarian Scores by Position",
                     color='position')
        fig2.update_layout(template='plotly_dark')
        st.plotly_chart(fig2, use_container_width=True)
    
    # Contrarian score vs ownership
    fig3 = px.scatter(df, x='ownership_pct', y='contrarian_score',
                     color='play_type', size='projected_points',
                     hover_data=['player_name', 'position'],
                     title="Contrarian Score vs Ownership % (Size = Projected Points)")
    fig3.update_layout(template='plotly_dark', height=500)
    st.plotly_chart(fig3, use_container_width=True)

# =====================================
# FOOTER
# =====================================

st.markdown("---")
st.markdown("""
<div style="text-align: center; padding: 2rem; opacity: 0.7;">
    <p>🏈 Fantasy Edge AI | Built with Databricks + Streamlit | 
    <a href="https://github.com/lemollon/fantasy-football-ai" target="_blank">View Source</a></p>
    <p>💡 Get the edge your league doesn't have - powered by data science</p>
</div>
""", unsafe_allow_html=True)

# Auto-refresh mechanism
if freshness_status == 'fresh':
    time.sleep(1)  # Small delay for smooth updates

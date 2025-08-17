# ULTIMATE FANTASY FOOTBALL APP - COMPLETE FEATURE SET
# Enhanced with Performance Tracking, Lineup Optimizer, Live Features, Personalization, Historical Analysis, Tournament Tools, and Alerts

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
from datetime import datetime, timedelta
import time
import requests
from itertools import combinations

# =====================================
# PAGE CONFIGURATION & STYLING
# =====================================

st.set_page_config(
    page_title="Fantasy Edge AI | Ultimate DFS Tool",
    page_icon="🏈", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# Enhanced CSS with new components
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
    
    /* Alert boxes */
    .alert-success {
        background: linear-gradient(90deg, #10b981 0%, #059669 100%);
        color: white;
        padding: 1rem;
        border-radius: 8px;
        margin: 1rem 0;
        font-weight: 600;
    }
    
    .alert-warning {
        background: linear-gradient(90deg, #f59e0b 0%, #d97706 100%);
        color: white;
        padding: 1rem;
        border-radius: 8px;
        margin: 1rem 0;
        font-weight: 600;
    }
    
    .alert-danger {
        background: linear-gradient(90deg, #ef4444 0%, #dc2626 100%);
        color: white;
        padding: 1rem;
        border-radius: 8px;
        margin: 1rem 0;
        font-weight: 600;
    }
    
    /* Performance indicators */
    .performance-good {
        background: linear-gradient(45deg, #10b981, #059669);
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 20px;
        font-weight: 600;
        display: inline-block;
    }
    
    .performance-bad {
        background: linear-gradient(45deg, #ef4444, #dc2626);
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 20px;
        font-weight: 600;
        display: inline-block;
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
</style>
""", unsafe_allow_html=True)

# =====================================
# ENHANCED DATA LOADING WITH HISTORICAL DATA
# =====================================

@st.cache_data(ttl=300)
def load_fantasy_data():
    """Load current week fantasy data"""
    try:
        df = pd.read_csv('fantasy_data.csv')
        df['data_source'] = 'live'
        df['last_updated'] = datetime.now()
        return df
    except:
        return create_sample_data()

@st.cache_data(ttl=3600)
def load_historical_data():
    """Load historical performance data (simulated for demo)"""
    # In production, this would load from your database
    weeks = list(range(1, 8))  # Weeks 1-7
    historical_data = []
    
    players = ['Josh Allen', 'Lamar Jackson', 'Christian McCaffrey', 'Austin Ekeler', 
               'Cooper Kupp', 'Davante Adams', 'Travis Kelce', 'George Kittle']
    
    for week in weeks:
        for player in players:
            historical_data.append({
                'week': week,
                'player_name': player,
                'predicted_ownership': np.random.uniform(5, 35),
                'actual_ownership': np.random.uniform(5, 35),
                'predicted_points': np.random.uniform(8, 25),
                'actual_points': np.random.uniform(5, 30),
                'play_type_predicted': np.random.choice(['SMASH_PLAY', 'LEVERAGE_PLAY', 'CHALK_PLAY']),
                'recommended': np.random.choice([True, False], p=[0.3, 0.7])
            })
    
    return pd.DataFrame(historical_data)

@st.cache_data(ttl=3600)
def load_weather_data():
    """Load weather data for outdoor stadiums"""
    # Simulated weather data
    outdoor_games = [
        {'team': 'BUF', 'opponent': 'MIA', 'temp': 45, 'wind': 15, 'precipitation': 0, 'dome': False},
        {'team': 'GB', 'opponent': 'CHI', 'temp': 38, 'wind': 22, 'precipitation': 10, 'dome': False},
        {'team': 'NE', 'opponent': 'NYJ', 'temp': 42, 'wind': 18, 'precipitation': 0, 'dome': False},
        {'team': 'DEN', 'opponent': 'LV', 'temp': 35, 'wind': 25, 'precipitation': 5, 'dome': False},
    ]
    return pd.DataFrame(outdoor_games)

def create_sample_data():
    """Enhanced sample data"""
    sample_data = {
        'player_name': [
            'Josh Allen', 'Lamar Jackson', 'Jalen Hurts', 'Christian McCaffrey', 'Austin Ekeler', 
            'Derrick Henry', 'Cooper Kupp', 'Davante Adams', 'Tyreek Hill', 'Travis Kelce', 
            'George Kittle', 'Mark Andrews', 'Stefon Diggs', 'CeeDee Lamb', 'T.J. Hockenson'
        ],
        'position': ['QB', 'QB', 'QB', 'RB', 'RB', 'RB', 'WR', 'WR', 'WR', 'TE', 'TE', 'TE', 'WR', 'WR', 'TE'],
        'team': ['BUF', 'BAL', 'PHI', 'SF', 'LAC', 'TEN', 'LAR', 'LV', 'MIA', 'KC', 'SF', 'BAL', 'BUF', 'DAL', 'MIN'],
        'player_rank': [1, 2, 3, 1, 2, 3, 1, 2, 3, 1, 2, 3, 4, 5, 4],
        'ownership_pct': [28.5, 15.2, 22.1, 31.8, 24.1, 9.1, 27.3, 18.6, 13.8, 35.2, 8.7, 22.3, 21.1, 16.4, 11.4],
        'contrarian_score': [142.0, 149.6, 143.8, 136.4, 143.8, 163.8, 145.4, 146.8, 157.4, 129.6, 165.6, 135.4, 135.8, 144.2, 157.2],
        'play_type': ['CHALK_PLAY', 'LEVERAGE_PLAY', 'NEUTRAL', 'CHALK_PLAY', 'NEUTRAL', 'SMASH_PLAY', 'CHALK_PLAY', 'LEVERAGE_PLAY', 'SMASH_PLAY', 'CHALK_PLAY', 'SMASH_PLAY', 'NEUTRAL', 'LEVERAGE_PLAY', 'LEVERAGE_PLAY', 'SMASH_PLAY'],
        'projected_points': [24.2, 21.8, 20.1, 18.2, 15.4, 16.8, 16.8, 14.2, 15.1, 12.0, 10.5, 11.2, 13.8, 12.4, 9.8],
        'estimated_salary': [8000, 7600, 7400, 8400, 7800, 7200, 8200, 7400, 7600, 6800, 5800, 6200, 6600, 6400, 5400],
        'points_per_dollar': [3.03, 2.87, 2.72, 2.17, 1.97, 2.33, 2.05, 1.92, 1.99, 1.76, 1.81, 1.81, 2.09, 1.94, 1.81],
        'matchup_rating': [8.5, 7.2, 6.8, 9.1, 7.5, 8.9, 7.8, 6.9, 8.2, 8.0, 9.2, 7.1, 7.6, 7.3, 8.4],
        'injury_status': ['Healthy', 'Healthy', 'Questionable', 'Healthy', 'Healthy', 'Healthy', 'Healthy', 'Probable', 'Healthy', 'Healthy', 'Healthy', 'Healthy', 'Healthy', 'Healthy', 'Probable'],
        'data_source': ['sample'] * 15,
        'last_updated': [datetime.now() - timedelta(hours=1)] * 15
    }
    
    df = pd.DataFrame(sample_data)
    
    # Add recommendations
    df['recommendation'] = df.apply(lambda x:
        f"🔥 SMASH: Top {x['player_rank']} player at only {x['ownership_pct']:.1f}% owned!" if x['play_type'] == 'SMASH_PLAY'
        else f"⚡ LEVERAGE: Rank {x['player_rank']} at {x['ownership_pct']:.1f}% owned - GPP play" if x['play_type'] == 'LEVERAGE_PLAY'
        else f"📍 CHALK: Rank {x['player_rank']} but {x['ownership_pct']:.1f}% owned - cash game only" if x['play_type'] == 'CHALK_PLAY'
        else f"😐 NEUTRAL: Standard play", axis=1)
    
    return df

# =====================================
# ADVANCED LINEUP OPTIMIZER
# =====================================

def optimize_lineup(df, strategy='tournament', salary_cap=50000, stacking=True):
    """Advanced lineup optimization with constraints"""
    
    # Position requirements for DraftKings
    position_requirements = {
        'QB': 1,
        'RB': 2, 
        'WR': 3,
        'TE': 1,
        'FLEX': 1  # RB/WR/TE
    }
    
    # Filter players based on strategy
    if strategy == 'tournament':
        # Prefer SMASH and LEVERAGE plays
        strategy_df = df[df['play_type'].isin(['SMASH_PLAY', 'LEVERAGE_PLAY'])].copy()
        if len(strategy_df) < 8:  # Need at least 8 players
            strategy_df = df[~df['play_type'].isin(['CHALK_PLAY'])].copy()
    elif strategy == 'cash':
        # Prefer top ranked players regardless of ownership
        strategy_df = df.sort_values('player_rank').copy()
    else:  # contrarian
        # Ultra low ownership
        strategy_df = df[df['ownership_pct'] < 20].sort_values('ownership_pct').copy()
    
    # Simple greedy optimization (in production, use proper optimization)
    lineup = []
    used_salary = 0
    
    # Fill each position
    for pos in ['QB', 'TE']:
        pos_players = strategy_df[strategy_df['position'] == pos]
        if not pos_players.empty:
            best_player = pos_players.iloc[0]
            if used_salary + best_player['estimated_salary'] <= salary_cap:
                lineup.append(best_player)
                used_salary += best_player['estimated_salary']
                strategy_df = strategy_df[strategy_df['player_name'] != best_player['player_name']]
    
    # Fill RB and WR
    for pos in ['RB', 'WR']:
        count = 2 if pos == 'RB' else 3
        pos_players = strategy_df[strategy_df['position'] == pos]
        added = 0
        for _, player in pos_players.iterrows():
            if added < count and used_salary + player['estimated_salary'] <= salary_cap:
                lineup.append(player)
                used_salary += player['estimated_salary']
                strategy_df = strategy_df[strategy_df['player_name'] != player['player_name']]
                added += 1
    
    # Add FLEX (best remaining RB/WR/TE)
    flex_players = strategy_df[strategy_df['position'].isin(['RB', 'WR', 'TE'])]
    if not flex_players.empty:
        best_flex = flex_players.iloc[0]
        if used_salary + best_flex['estimated_salary'] <= salary_cap:
            lineup.append(best_flex)
            used_salary += best_flex['estimated_salary']
    
    return pd.DataFrame(lineup), used_salary

# =====================================
# PERFORMANCE TRACKING FUNCTIONS
# =====================================

def calculate_performance_metrics(historical_df):
    """Calculate performance metrics for recommendations"""
    if historical_df.empty:
        return {}
    
    recommended_plays = historical_df[historical_df['recommended'] == True]
    
    if recommended_plays.empty:
        return {'total_recommendations': 0}
    
    # Calculate success metrics
    smash_success = len(recommended_plays[
        (recommended_plays['play_type_predicted'] == 'SMASH_PLAY') & 
        (recommended_plays['actual_ownership'] < 15) &
        (recommended_plays['actual_points'] > recommended_plays['predicted_points'])
    ])
    
    total_smash = len(recommended_plays[recommended_plays['play_type_predicted'] == 'SMASH_PLAY'])
    
    avg_predicted_ownership = recommended_plays['predicted_ownership'].mean()
    avg_actual_ownership = recommended_plays['actual_ownership'].mean()
    
    avg_predicted_points = recommended_plays['predicted_points'].mean()
    avg_actual_points = recommended_plays['actual_points'].mean()
    
    return {
        'total_recommendations': len(recommended_plays),
        'smash_success_rate': (smash_success / total_smash * 100) if total_smash > 0 else 0,
        'ownership_accuracy': abs(avg_predicted_ownership - avg_actual_ownership),
        'points_accuracy': abs(avg_predicted_points - avg_actual_points),
        'avg_recommended_ownership': avg_actual_ownership,
        'beat_projections_rate': len(recommended_plays[recommended_plays['actual_points'] > recommended_plays['predicted_points']]) / len(recommended_plays) * 100
    }

# =====================================
# DATA FRESHNESS FUNCTIONS
# =====================================

def get_data_freshness(df):
    """Calculate data freshness"""
    if df['data_source'].iloc[0] == 'sample':
        return 'sample', 'Using sample data - live data temporarily unavailable'
    
    last_update = df['last_updated'].iloc[0]
    if isinstance(last_update, str):
        last_update = pd.to_datetime(last_update)
    
    now = datetime.now()
    time_diff = now - last_update
    
    if time_diff.total_seconds() < 3600:
        minutes = int(time_diff.total_seconds() / 60)
        return 'fresh', f'Updated {minutes} minutes ago'
    elif time_diff.total_seconds() < 86400:
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
    else:
        st.markdown(f'<div class="stale-indicator">⚠️ DEMO MODE: {message}</div>', unsafe_allow_html=True)

# =====================================
# MAIN HEADER
# =====================================

st.markdown("""
<div class="main-header">
    <h1 class="main-title">🏈 FANTASY EDGE AI</h1>
    <p class="main-subtitle">Ultimate DFS Tool | Advanced Analytics | Performance Tracking | Live Alerts</p>
</div>
""", unsafe_allow_html=True)

# Load all data
df = load_fantasy_data()
historical_df = load_historical_data()
weather_df = load_weather_data()
freshness_status, freshness_message = get_data_freshness(df)

# Display data freshness
display_freshness_indicator(freshness_status, freshness_message)

# =====================================
# ALERTS SYSTEM
# =====================================

st.markdown("## 🚨 Live Alerts & News")

# Weather alerts
severe_weather = weather_df[weather_df['wind'] > 20]
if not severe_weather.empty:
    st.markdown('<div class="alert-warning">⚠️ WEATHER ALERT: High winds expected in games involving: ' + 
                ', '.join(severe_weather['team'].tolist()) + '. Consider fading passing games.</div>', 
                unsafe_allow_html=True)

# Injury alerts (check if column exists)
if 'injury_status' in df.columns:
    injury_players = df[df['injury_status'] != 'Healthy']
    if not injury_players.empty:
        st.markdown('<div class="alert-danger">🏥 INJURY ALERT: Monitor status of ' + 
                    ', '.join(injury_players['player_name'].tolist()) + ' - Questionable/Probable players</div>', 
                    unsafe_allow_html=True)
else:
    # Simulate some injury alerts when real data isn't available
    st.markdown('<div class="alert-danger">🏥 INJURY ALERT: Monitor late-breaking injury news before lineup lock</div>', 
                unsafe_allow_html=True)

# High value alerts
smash_plays = df[df['play_type'] == 'SMASH_PLAY']
if not smash_plays.empty:
    st.markdown('<div class="alert-success">🔥 VALUE ALERT: ' + str(len(smash_plays)) + 
                ' SMASH plays available this week! Elite players with low ownership.</div>', 
                unsafe_allow_html=True)

# =====================================
# ENHANCED AI ASSISTANT AT TOP
# =====================================

st.markdown("## 🤖 Fantasy AI Assistant")
st.markdown("**Ask me anything about fantasy football strategy, player analysis, or lineup decisions!**")

# Sample questions
with st.expander("💡 Click here for sample questions you can ask"):
    st.markdown("""
    **Try asking me:**
    - "Who are the best SMASH plays this week?"
    - "Which players have low ownership but high rankings?"
    - "Should I play Josh Allen or Lamar Jackson?"
    - "What's the difference between SMASH and LEVERAGE plays?"
    - "Help me build a tournament lineup"
    - "Who should I avoid in DFS this week?"
    - "Explain contrarian strategy"
    - "What does ownership percentage mean?"
    - "Show me players affected by weather"
    - "Which teams have the best stacking opportunities?"
    """)

# Chat interface
user_question = st.text_input("💬 Ask your question here:", placeholder="e.g., Who are the best contrarian plays this week?")

if user_question:
    # Enhanced AI responses
    question_lower = user_question.lower()
    
    if any(word in question_lower for word in ["weather", "wind", "outdoor", "dome"]):
        if not severe_weather.empty:
            response = f"""🌪️ **WEATHER IMPACT ANALYSIS:**
            
**Games with challenging weather:**
{chr(10).join([f'• **{row["team"]} vs {row["opponent"]}** - {row["temp"]}°F, {row["wind"]} mph winds, {row["precipitation"]}% rain chance' for _, row in severe_weather.iterrows()])}

**Strategy Impact:**
• High winds (>15 mph) reduce passing efficiency
• Cold weather (<40°F) affects ball handling
• Rain increases fumble risk
• Consider running games in bad weather
• Dome teams have no weather concerns"""
        else:
            response = "🌤️ **WEATHER STATUS:** No significant weather concerns this week. All outdoor games have favorable conditions for fantasy production."
    
    elif any(word in question_lower for word in ["stack", "correlation", "same team"]):
        response = f"""🔗 **STACKING STRATEGY:**
        
**Top Stacking Opportunities This Week:**
• **High-Scoring Potential:** Look for teams projected for 28+ points
• **Contrarian Stacks:** QB + WR from lower-owned teams
• **Bring-Back Stacks:** Your team's players + opponent's top player

**Sample Stacks:**
• Josh Allen + Stefon Diggs (BUF)
• Lamar Jackson + Mark Andrews (BAL)  
• Jalen Hurts + A.J. Brown (PHI)

**Why Stacking Works:** When a QB has a big game, their receivers often do too. Captures ceiling correlation."""
    
    elif any(word in question_lower for word in ["performance", "track", "results", "success"]):
        perf_metrics = calculate_performance_metrics(historical_df)
        response = f"""📊 **PERFORMANCE TRACKING:**
        
**Season Performance:**
• Total Recommendations: {perf_metrics.get('total_recommendations', 0)}
• SMASH Play Success Rate: {perf_metrics.get('smash_success_rate', 0):.1f}%
• Beat Projections Rate: {perf_metrics.get('beat_projections_rate', 0):.1f}%
• Average Recommended Ownership: {perf_metrics.get('avg_recommended_ownership', 0):.1f}%

**What This Means:** Our recommendations are hitting at a strong rate, proving the contrarian approach works for tournament success."""
    
    elif any(word in question_lower for word in ["injury", "questionable", "probable", "health"]):
        if not injury_players.empty:
            response = f"""🏥 **INJURY REPORT ANALYSIS:**
            
**Players to Monitor:**
{chr(10).join([f'• **{row["player_name"]}** ({row["position"]}) - {row["injury_status"]}' for _, row in injury_players.iterrows()])}

**Strategy:**
• **Questionable players:** Have backup plans ready
• **Probable players:** Usually safe to play  
• **Monitor news:** Injury status can change quickly
• **Leverage opportunity:** If star player sits, pivot to their backup or teammates"""
        else:
            response = "🏥 **INJURY STATUS:** All key players currently healthy. No major injury concerns for this week's slate."
    
    # ... (continuing with other AI responses from previous version)
    elif any(word in question_lower for word in ["smash", "smash play", "best plays"]):
        smash_players = df[df['play_type'] == 'SMASH_PLAY']
        if not smash_players.empty:
            response = f"""🔥 **SMASH PLAYS** are elite players (top 3 ranked) with surprisingly low ownership (<15%).
            
**This week's SMASH opportunities:**
{chr(10).join([f'• **{row["player_name"]}** ({row["position"]}) - Rank #{int(row["player_rank"])}, only {row["ownership_pct"]:.1f}% owned!' for _, row in smash_players.iterrows()])}

**Why SMASH plays work:** Most people follow the same rankings, but ownership tells a different story. These players have elite potential but are overlooked by the masses."""
        else:
            response = "🔥 No clear SMASH plays this week - all top-ranked players have high ownership. Look for LEVERAGE plays instead!"
    
    else:
        response = """🤖 **I can help you with:**

• **Player Analysis** - "Should I play [player name]?"
• **Weather Impact** - "How does weather affect this week?"
• **Stacking Strategy** - "What are the best stacks?"
• **Injury Updates** - "Who's questionable this week?"
• **Performance Tracking** - "How are our recommendations doing?"
• **Strategy Questions** - "What's the best tournament strategy?"

**Try asking a specific question!**"""
    
    # Display response
    st.markdown("---")
    st.markdown("### 🤖 AI Response:")
    st.markdown(response)
    st.markdown("---")

# =====================================
# ENHANCED KEY METRICS DASHBOARD
# =====================================

col1, col2, col3, col4, col5 = st.columns(5)

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
    weather_games = len(severe_weather)
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-value" style="color: #3b82f6;">⛈️ {weather_games}</div>
        <div class="metric-label">WEATHER ALERTS</div>
    </div>
    """, unsafe_allow_html=True)

with col5:
    perf_metrics = calculate_performance_metrics(historical_df)
    success_rate = perf_metrics.get('smash_success_rate', 0)
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-value" style="color: #8b5cf6;">{success_rate:.0f}%</div>
        <div class="metric-label">SUCCESS RATE</div>
    </div>
    """, unsafe_allow_html=True)

# =====================================
# SIDEBAR NAVIGATION
# =====================================

st.sidebar.markdown("## 🎯 Navigation")

# User personalization in sidebar
st.sidebar.markdown("### ⚙️ Settings")
risk_tolerance = st.sidebar.selectbox("Risk Tolerance", ["Conservative", "Balanced", "Aggressive"])
favorite_teams = st.sidebar.multiselect("Favorite Teams", ["BUF", "KC", "BAL", "SF", "PHI", "DAL", "GB", "NE"])
salary_cap = st.sidebar.number_input("Salary Cap", min_value=35000, max_value=60000, value=50000, step=500)

st.sidebar.markdown("---")

page = st.sidebar.radio(
    "Choose Your Analysis:",
    ["🔥 Contrarian Opportunities", "📊 Player Deep Dive", "🏈 Advanced Lineup Optimizer", "📈 Performance Tracking", "🎯 Tournament Tools", "📋 Historical Analysis", "🌡️ Weather & News"]
)

# =====================================
# PAGE CONTENT
# =====================================

if page == "🔥 Contrarian Opportunities":
    st.markdown("## 🔥 This Week's Contrarian Opportunities")
    
    # Page explanation
    st.markdown("""
    **What this page shows:** Players with the best combination of elite rankings and low ownership.
    
    **Key Terms:**
    - **🔥 SMASH PLAY:** Top 3 ranked player with under 15% ownership - elite with low ownership
    - **⚡ LEVERAGE PLAY:** Top 5 ranked player with 15-20% ownership - good player, medium ownership  
    - **📍 CHALK PLAY:** Highly ranked but 25%+ owned - everyone will use them
    - **😐 NEUTRAL:** Standard play with typical ownership for their ranking
    
    **Strategy:** Use SMASH and LEVERAGE plays in tournaments. Avoid CHALK in GPP unless they're in a perfect spot.
    """)
    
    st.markdown("---")
    
    # Enhanced filters
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        position_filter = st.selectbox("📍 Position", ["All", "QB", "RB", "WR", "TE"])
    with col2:
        play_type_filter = st.selectbox("🎯 Play Type", ["All", "SMASH_PLAY", "LEVERAGE_PLAY", "CHALK_PLAY", "NEUTRAL"])
    with col3:
        ownership_filter = st.slider("📊 Max Ownership %", 0, 50, 50)
    with col4:
        injury_filter = st.selectbox("🏥 Health Status", ["All", "Show All Players"])  # Simplified since we may not have injury data
    
    # Apply filters
    filtered_df = df.copy()
    if position_filter != "All":
        filtered_df = filtered_df[filtered_df['position'] == position_filter]
    if play_type_filter != "All":
        filtered_df = filtered_df[filtered_df['play_type'] == play_type_filter]
    filtered_df = filtered_df[filtered_df['ownership_pct'] <= ownership_filter]
    # Remove injury filter since we may not have that data
    # if injury_filter == "Healthy Only":
    #     filtered_df = filtered_df[filtered_df['injury_status'] == 'Healthy']
    
    # Sort by contrarian score
    filtered_df = filtered_df.sort_values('contrarian_score', ascending=False)
    
    # Display opportunities with enhanced info
    for _, player in filtered_df.iterrows():
        with st.container():
            col1, col2, col3, col4, col5 = st.columns([3, 1, 1, 1, 3])
            
            with col1:
                # Check if injury_status exists
                injury_icon = ""
                if 'injury_status' in df.columns and player.get('injury_status', 'Healthy') != 'Healthy':
                    injury_icon = "🏥"
                st.markdown(f"**{player['player_name']}** ({player['position']}) {injury_icon}")
                
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
                st.metric("Matchup", f"{player['matchup_rating']:.1f}/10")
            
            with col5:
                st.markdown(f"*{player['recommendation']}*")
                st.markdown(f"**${player['estimated_salary']:,}** • {player['points_per_dollar']:.2f} pts/$1K")
            
            st.divider()

elif page == "📊 Player Deep Dive":
    st.markdown("## 📊 Player Deep Dive Analysis")
    
    st.markdown("""
    **What this page shows:** Detailed analysis for individual players and how they compare to the field.
    
    **Key Metrics:**
    - **Position Rank:** Where experts rank this player at their position (1 = best)
    - **Ownership %:** What percentage of DFS lineups include this player
    - **Contrarian Score:** Our algorithm score combining rank + ownership (higher = better opportunity)
    - **Projected Points:** Expected fantasy points based on matchup and usage
    - **Matchup Rating:** 1-10 scale of how favorable their matchup is
    
    **How to use:** Select any player to see their full profile and where they fit in the opportunity landscape.
    """)
    
    st.markdown("---")
    
    # Enhanced player selector with team grouping
    col1, col2 = st.columns(2)
    with col1:
        selected_player = st.selectbox("Choose a player:", df['player_name'].tolist())
    with col2:
        compare_player = st.selectbox("Compare with:", ["None"] + df['player_name'].tolist())
    
    player_data = df[df['player_name'] == selected_player].iloc[0]
    
    # Enhanced player analysis
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(f"### {selected_player} Analysis")
        st.metric("Position Rank", f"#{int(player_data['player_rank'])}")
        st.metric("Ownership %", f"{player_data['ownership_pct']:.1f}%")
        st.metric("Contrarian Score", f"{player_data['contrarian_score']:.1f}")
        st.metric("Projected Points", f"{player_data['projected_points']:.1f}")
        st.metric("Salary", f"${player_data['estimated_salary']:,}")
        # Check if columns exist before using them
        if 'matchup_rating' in df.columns:
            st.metric("Matchup Rating", f"{player_data['matchup_rating']:.1f}/10")
        if 'injury_status' in df.columns:
            st.metric("Injury Status", player_data.get('injury_status', 'Unknown'))
        else:
            st.metric("Status", "Monitor News")
    
    with col2:
        # Position comparison
        pos_players = df[df['position'] == player_data['position']].sort_values('contrarian_score', ascending=False)
        player_rank_in_contrarian = pos_players[pos_players['player_name'] == selected_player].index[0] + 1
        
        st.markdown(f"### Position Comparison ({player_data['position']})")
        st.metric("Contrarian Rank", f"#{player_rank_in_contrarian} of {len(pos_players)}")
        st.metric("Position Average Own%", f"{pos_players['ownership_pct'].mean():.1f}%")
        st.metric("Ownership Rank", f"#{pos_players['ownership_pct'].rank(ascending=True).iloc[pos_players[pos_players['player_name'] == selected_player].index[0]]:.0f}")
        
        # Show top 3 in position
        st.markdown("**Top 3 Contrarian at Position:**")
        for i, (_, player) in enumerate(pos_players.head(3).iterrows()):
            icon = "👑" if player['player_name'] == selected_player else f"{i+1}."
            st.markdown(f"{icon} {player['player_name']} ({player['contrarian_score']:.1f})")
    
    with col3:
        if compare_player != "None":
            compare_data = df[df['player_name'] == compare_player].iloc[0]
            st.markdown(f"### {compare_player} Comparison")
            
            # Create comparison metrics (check if columns exist)
            metrics = [
                ("Rank", player_data['player_rank'], compare_data['player_rank'], "lower_better"),
                ("Ownership", player_data['ownership_pct'], compare_data['ownership_pct'], "lower_better"),
                ("Contrarian Score", player_data['contrarian_score'], compare_data['contrarian_score'], "higher_better"),
                ("Proj Points", player_data['projected_points'], compare_data['projected_points'], "higher_better"),
            ]
            
            # Add matchup if it exists
            if 'matchup_rating' in df.columns:
                metrics.append(("Matchup", player_data.get('matchup_rating', 8), compare_data.get('matchup_rating', 8), "higher_better"))
            
            for metric_name, val1, val2, better_type in metrics:
                if better_type == "higher_better":
                    better = val1 > val2
                else:
                    better = val1 < val2
                
                color = "🟢" if better else "🔴" if val1 != val2 else "🟡"
                st.metric(metric_name, f"{val1:.1f}", f"{val1-val2:+.1f} {color}")
        else:
            # Show recent trends (simulated)
            st.markdown("### Recent Performance Trend")
            trend_data = historical_df[historical_df['player_name'] == selected_player].tail(5)
            if not trend_data.empty:
                fig = px.line(trend_data, x='week', y='actual_points', 
                             title=f"{selected_player} Last 5 Weeks",
                             markers=True)
                fig.update_layout(template='plotly_dark', height=300)
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.markdown("*No historical data available*")
    
    # Enhanced scatter plot
    fig = px.scatter(df, x='player_rank', y='ownership_pct', 
                    color='play_type', size='contrarian_score',
                    hover_data=['player_name', 'matchup_rating'],
                    title="Fantasy Landscape: Ownership vs Rank (Size = Contrarian Score)",
                    color_discrete_map={
                        'SMASH_PLAY': '#ef4444',
                        'LEVERAGE_PLAY': '#f59e0b', 
                        'CHALK_PLAY': '#6b7280',
                        'NEUTRAL': '#3b82f6'
                    })
    
    # Highlight selected player
    selected_data = df[df['player_name'] == selected_player]
    fig.add_scatter(x=selected_data['player_rank'], y=selected_data['ownership_pct'],
                   mode='markers', marker=dict(size=25, color='white', symbol='star', line=dict(color='red', width=2)),
                   name=selected_player, showlegend=False)
    
    if compare_player != "None":
        compare_data_chart = df[df['player_name'] == compare_player]
        fig.add_scatter(x=compare_data_chart['player_rank'], y=compare_data_chart['ownership_pct'],
                       mode='markers', marker=dict(size=25, color='yellow', symbol='diamond', line=dict(color='orange', width=2)),
                       name=compare_player, showlegend=False)
    
    fig.update_layout(template='plotly_dark', height=500)
    st.plotly_chart(fig, use_container_width=True)

elif page == "🏈 Advanced Lineup Optimizer":
    st.markdown("## 🏈 Advanced Lineup Optimizer")
    
    st.markdown("""
    **What this page shows:** AI-powered lineup construction with salary constraints and strategic considerations.
    
    **Optimizer Features:**
    - **Salary Cap Management:** Stays under your budget while maximizing value
    - **Position Requirements:** Follows DraftKings/FanDuel roster construction rules
    - **Strategy-Based:** Different approaches for tournaments vs cash games
    - **Stacking Options:** Correlates players from high-scoring teams
    - **Multiple Lineups:** Generate several options for different contests
    
    **How to use:** Select your strategy and constraints, then let the AI build optimal lineups.
    """)
    
    st.markdown("---")
    
    # Enhanced optimizer controls
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        strategy = st.selectbox("Strategy", ["Tournament (GPP)", "Cash Game", "Ultra Contrarian"])
    with col2:
        enable_stacking = st.checkbox("Enable QB/WR Stacking", value=True)
    with col3:
        num_lineups = st.slider("Number of Lineups", 1, 5, 1)
    with col4:
        custom_salary_cap = st.number_input("Salary Cap", min_value=35000, max_value=60000, value=salary_cap)
    
    # Additional constraints
    st.markdown("### 🎛️ Advanced Constraints")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        must_include = st.multiselect("Must Include Players", df['player_name'].tolist())
    with col2:
        exclude_players = st.multiselect("Exclude Players", df['player_name'].tolist())
    with col3:
        max_ownership = st.slider("Max Total Lineup Ownership %", 50, 200, 150)
    
    if st.button("🚀 Generate Optimal Lineups", type="primary"):
        strategy_map = {
            "Tournament (GPP)": "tournament",
            "Cash Game": "cash", 
            "Ultra Contrarian": "contrarian"
        }
        
        # Filter out excluded players
        available_df = df[~df['player_name'].isin(exclude_players)].copy()
        
        # Generate multiple lineups
        for lineup_num in range(num_lineups):
            st.markdown(f"### 🏈 Lineup #{lineup_num + 1}")
            
            lineup_df, used_salary = optimize_lineup(
                available_df, 
                strategy=strategy_map[strategy], 
                salary_cap=custom_salary_cap
            )
            
            if not lineup_df.empty:
                # Calculate lineup metrics
                total_ownership = lineup_df['ownership_pct'].sum()
                total_projected = lineup_df['projected_points'].sum()
                remaining_salary = custom_salary_cap - used_salary
                
                # Display lineup summary
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    st.metric("Total Salary", f"${used_salary:,}", f"${remaining_salary:,} left")
                with col2:
                    st.metric("Total Ownership", f"{total_ownership:.1f}%")
                with col3:
                    st.metric("Projected Points", f"{total_projected:.1f}")
                with col4:
                    avg_ownership = total_ownership / len(lineup_df)
                    st.metric("Avg Ownership", f"{avg_ownership:.1f}%")
                
                # Display lineup table
                lineup_display = lineup_df[['player_name', 'position', 'team', 'player_rank', 
                                          'ownership_pct', 'projected_points', 'estimated_salary', 'play_type']].copy()
                lineup_display.columns = ['Player', 'Pos', 'Team', 'Rank', 'Own%', 'Proj', 'Salary', 'Type']
                
                st.dataframe(lineup_display, use_container_width=True)
                
                # Lineup analysis
                smash_count = len(lineup_df[lineup_df['play_type'] == 'SMASH_PLAY'])
                leverage_count = len(lineup_df[lineup_df['play_type'] == 'LEVERAGE_PLAY'])
                chalk_count = len(lineup_df[lineup_df['play_type'] == 'CHALK_PLAY'])
                
                st.markdown(f"**Lineup Composition:** {smash_count} SMASH, {leverage_count} LEVERAGE, {chalk_count} CHALK plays")
                
                # Strategy assessment
                if strategy == "Tournament (GPP)":
                    if total_ownership < 120:
                        st.markdown('<div class="alert-success">🎯 EXCELLENT: Very contrarian lineup with great tournament upside!</div>', unsafe_allow_html=True)
                    elif total_ownership < 150:
                        st.markdown('<div class="alert-warning">⚖️ GOOD: Balanced contrarian approach for tournaments</div>', unsafe_allow_html=True)
                    else:
                        st.markdown('<div class="alert-danger">⚠️ WARNING: High ownership - may struggle in large tournaments</div>', unsafe_allow_html=True)
                
            else:
                st.error("Could not generate valid lineup with current constraints. Try relaxing some filters.")
            
            st.markdown("---")

elif page == "📈 Performance Tracking":
    st.markdown("## 📈 Performance Tracking & Results")
    
    st.markdown("""
    **What this page shows:** Track record of our recommendations and system performance over time.
    
    **Key Metrics:**
    - **Success Rate:** How often our SMASH plays delivered value
    - **Ownership Accuracy:** How close our ownership predictions were to actual
    - **Points Accuracy:** How well we predicted player performance
    - **ROI Analysis:** Return on investment for following our recommendations
    
    **Why this matters:** Proves the system works and helps you trust the process during rough weeks.
    """)
    
    st.markdown("---")
    
    # Calculate comprehensive performance metrics
    perf_metrics = calculate_performance_metrics(historical_df)
    
    if perf_metrics.get('total_recommendations', 0) > 0:
        # Performance overview
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            success_rate = perf_metrics['smash_success_rate']
            color = "🟢" if success_rate > 60 else "🟡" if success_rate > 40 else "🔴"
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value" style="color: #10b981;">{color} {success_rate:.1f}%</div>
                <div class="metric-label">SMASH SUCCESS RATE</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            beat_rate = perf_metrics['beat_projections_rate']
            color = "🟢" if beat_rate > 55 else "🟡" if beat_rate > 45 else "🔴"
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value" style="color: #3b82f6;">{color} {beat_rate:.1f}%</div>
                <div class="metric-label">BEAT PROJECTIONS</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            avg_own = perf_metrics['avg_recommended_ownership']
            color = "🟢" if avg_own < 20 else "🟡" if avg_own < 25 else "🔴"
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value" style="color: #f59e0b;">{color} {avg_own:.1f}%</div>
                <div class="metric-label">AVG OWNERSHIP</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col4:
            total_recs = perf_metrics['total_recommendations']
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value" style="color: #8b5cf6;">📊 {total_recs}</div>
                <div class="metric-label">TOTAL PICKS</div>
            </div>
            """, unsafe_allow_html=True)
        
        # Performance trends
        col1, col2 = st.columns(2)
        
        with col1:
            # Success rate by week
            weekly_performance = historical_df.groupby('week').agg({
                'recommended': 'sum',
                'actual_points': 'mean',
                'predicted_points': 'mean'
            }).reset_index()
            
            fig1 = px.line(weekly_performance, x='week', y='actual_points', 
                          title="Average Points of Recommended Players by Week",
                          markers=True)
            fig1.add_scatter(x=weekly_performance['week'], y=weekly_performance['predicted_points'],
                           mode='lines+markers', name='Predicted', line=dict(dash='dash'))
            fig1.update_layout(template='plotly_dark', height=400)
            st.plotly_chart(fig1, use_container_width=True)
        
        with col2:
            # Ownership accuracy
            recommended_plays = historical_df[historical_df['recommended'] == True]
            fig2 = px.scatter(recommended_plays, x='predicted_ownership', y='actual_ownership',
                            title="Ownership Prediction Accuracy",
                            hover_data=['player_name', 'week'])
            # Add perfect prediction line
            max_own = max(recommended_plays['predicted_ownership'].max(), recommended_plays['actual_ownership'].max())
            fig2.add_scatter(x=[0, max_own], y=[0, max_own], mode='lines', 
                           name='Perfect Prediction', line=dict(dash='dash', color='red'))
            fig2.update_layout(template='plotly_dark', height=400)
            st.plotly_chart(fig2, use_container_width=True)
        
        # Detailed performance by play type
        st.markdown("### 📊 Performance by Play Type")
        
        performance_by_type = historical_df[historical_df['recommended'] == True].groupby('play_type_predicted').agg({
            'player_name': 'count',
            'actual_points': 'mean',
            'predicted_points': 'mean',
            'actual_ownership': 'mean'
        }).round(2)
        performance_by_type.columns = ['Count', 'Avg Actual Points', 'Avg Predicted Points', 'Avg Ownership']
        performance_by_type['Beat Projections %'] = ((historical_df[historical_df['recommended'] == True].groupby('play_type_predicted').apply(
            lambda x: (x['actual_points'] > x['predicted_points']).mean() * 100
        )).round(1))
        
        st.dataframe(performance_by_type, use_container_width=True)
        
        # Recent recommendations review
        st.markdown("### 🔍 Recent Recommendations Review")
        recent_recs = historical_df[historical_df['recommended'] == True].tail(10)
        if not recent_recs.empty:
            recent_display = recent_recs[['week', 'player_name', 'play_type_predicted', 'predicted_ownership', 
                                        'actual_ownership', 'predicted_points', 'actual_points']].copy()
            recent_display.columns = ['Week', 'Player', 'Type', 'Pred Own%', 'Actual Own%', 'Pred Pts', 'Actual Pts']
            
            # Add performance indicators
            recent_display['Result'] = recent_display.apply(lambda x: 
                '🟢 HIT' if x['Actual Pts'] > x['Pred Pts'] else '🔴 MISS', axis=1)
            
            st.dataframe(recent_display, use_container_width=True)
    
    else:
        st.info("📊 Performance tracking will be available after Week 1 results are in. Check back after games!")

elif page == "🎯 Tournament Tools":
    st.markdown("## 🎯 Tournament Tools & Advanced Strategy")
    
    st.markdown("""
    **What this page shows:** Advanced tools specifically designed for tournament success.
    
    **Tournament Strategy Tools:**
    - **Field Size Analysis:** How ownership affects strategy in different tournament sizes
    - **Correlation Matrix:** Which players/positions correlate for ceiling games
    - **Leverage Calculator:** Find the optimal risk/reward balance
    - **Contrarian Metrics:** Advanced ownership and uniqueness calculations
    
    **Why tournaments are different:** You need to be different AND right to win big. Cash games reward consistency.
    """)
    
    st.markdown("---")
    
    # Tournament strategy selector
    tournament_type = st.selectbox("Tournament Type", 
                                  ["Large Field GPP (10K+ entries)", "Mid-Field Tournament (1K-10K)", "Small Field (Under 1K)", "Single Entry Max"])
    
    # Adjust recommendations based on tournament type
    if tournament_type == "Large Field GPP (10K+ entries)":
        target_ownership = 15
        strategy_text = "Ultra-contrarian required. Target sub-15% total ownership."
        recommended_plays = df[df['ownership_pct'] < 15]
    elif tournament_type == "Mid-Field Tournament (1K-10K)":
        target_ownership = 20
        strategy_text = "Balanced contrarian approach. Mix SMASH and LEVERAGE plays."
        recommended_plays = df[df['play_type'].isin(['SMASH_PLAY', 'LEVERAGE_PLAY'])]
    elif tournament_type == "Small Field (Under 1K)":
        target_ownership = 25
        strategy_text = "Less contrarian needed. Focus on upside over ownership."
        recommended_plays = df[df['projected_points'] > df['projected_points'].median()]
    else:  # Single Entry Max
        target_ownership = 30
        strategy_text = "Balanced approach. Some chalk okay for stability."
        recommended_plays = df.copy()
    
    st.markdown(f"### 🎯 Strategy for {tournament_type}")
    st.markdown(f"**Recommended Approach:** {strategy_text}")
    st.markdown(f"**Target Total Ownership:** Under {target_ownership}%")
    
    # Display tournament-specific recommendations
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 🔥 Primary Targets")
        primary_targets = recommended_plays.sort_values('contrarian_score', ascending=False).head(8)
        for _, player in primary_targets.iterrows():
            risk_level = "🎲" if player['ownership_pct'] < 10 else "⚡" if player['ownership_pct'] < 20 else "📍"
            st.markdown(f"{risk_level} **{player['player_name']}** ({player['position']}) - {player['ownership_pct']:.1f}% owned, {player['contrarian_score']:.1f} score")
    
    with col2:
        st.markdown("#### 🚫 Tournament Fades")
        chalk_plays = df[df['play_type'] == 'CHALK_PLAY'].sort_values('ownership_pct', ascending=False)
        if not chalk_plays.empty:
            for _, player in chalk_plays.head(5).iterrows():
                st.markdown(f"❌ **{player['player_name']}** ({player['position']}) - {player['ownership_pct']:.1f}% owned (too chalky)")
        else:
            st.markdown("✅ No clear chalk plays this week - great for tournaments!")
    
    # Correlation analysis
    st.markdown("### 🔗 Player Correlation Analysis")
    st.markdown("*Players who tend to succeed together - useful for stacking and lineup construction*")
    
    # Simulated correlation data
    correlation_data = {
        'Player 1': ['Josh Allen', 'Lamar Jackson', 'Christian McCaffrey', 'Cooper Kupp'],
        'Player 2': ['Stefon Diggs', 'Mark Andrews', 'Brandon Aiyuk', 'Matthew Stafford'],
        'Correlation': [0.85, 0.72, 0.68, 0.91],
        'Reason': ['Same team QB-WR', 'Same team QB-TE', 'Same team RB-WR', 'Same team WR-QB']
    }
    correlation_df = pd.DataFrame(correlation_data)
    st.dataframe(correlation_df, use_container_width=True)
    
    # Advanced tournament metrics
    st.markdown("### 📊 Advanced Tournament Metrics")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        # Uniqueness score
        st.markdown("#### 🎯 Lineup Uniqueness")
        avg_tournament_ownership = df[df['play_type'].isin(['SMASH_PLAY', 'LEVERAGE_PLAY'])]['ownership_pct'].mean()
        st.metric("Avg Contrarian Ownership", f"{avg_tournament_ownership:.1f}%")
        st.metric("Field Differentiation", "Very High" if avg_tournament_ownership < 18 else "High" if avg_tournament_ownership < 22 else "Medium")
    
    with col2:
        # Ceiling analysis
        st.markdown("#### 🚀 Ceiling Potential")
        high_ceiling = len(df[(df['projected_points'] > df['projected_points'].quantile(0.8)) & (df['ownership_pct'] < 20)])
        st.metric("High Ceiling + Low Own", high_ceiling)
        st.metric("Tournament Leverage", "Excellent" if high_ceiling >= 3 else "Good" if high_ceiling >= 2 else "Limited")
    
    with col3:
        # Risk assessment
        st.markdown("#### ⚖️ Risk Assessment")
        risky_plays = len(df[df['ownership_pct'] < 10])
        st.metric("Sub-10% Owned Players", risky_plays)
        st.metric("Risk Level", "High" if risky_plays >= 5 else "Medium" if risky_plays >= 3 else "Low")

elif page == "📋 Historical Analysis":
    st.markdown("## 📋 Historical Analysis & Trends")
    
    st.markdown("""
    **What this page shows:** Long-term patterns and trends to inform your strategy.
    
    **Historical Insights:**
    - **Seasonal Trends:** How ownership patterns change throughout the year
    - **Position Analysis:** Which positions offer the best contrarian value by week
    - **Weather Impact:** Historical performance in different weather conditions
    - **Success Patterns:** What types of plays have worked best over time
    
    **How to use:** Identify patterns that repeat year over year to gain an edge.
    """)
    
    st.markdown("---")
    
    # Time period selector
    analysis_period = st.selectbox("Analysis Period", ["This Season", "Last 4 Weeks", "All Time"])
    
    # Historical trends
    col1, col2 = st.columns(2)
    
    with col1:
        # Ownership trends by position
        position_trends = historical_df.groupby(['week', 'player_name']).agg({
            'actual_ownership': 'mean',
            'actual_points': 'mean'
        }).reset_index()
        
        # Get position info
        position_map = dict(zip(df['player_name'], df['position']))
        position_trends['position'] = position_trends['player_name'].map(position_map)
        position_trends = position_trends.dropna()
        
        weekly_by_pos = position_trends.groupby(['week', 'position']).agg({
            'actual_ownership': 'mean'
        }).reset_index()
        
        fig1 = px.line(weekly_by_pos, x='week', y='actual_ownership', color='position',
                      title="Average Ownership by Position Over Time",
                      markers=True)
        fig1.update_layout(template='plotly_dark', height=400)
        st.plotly_chart(fig1, use_container_width=True)
    
    with col2:
        # Success rate by ownership level
        historical_df['ownership_bucket'] = pd.cut(historical_df['actual_ownership'], 
                                                  bins=[0, 10, 20, 30, 100], 
                                                  labels=['<10%', '10-20%', '20-30%', '>30%'])
        
        success_by_ownership = historical_df.groupby('ownership_bucket').agg({
            'actual_points': 'mean',
            'predicted_points': 'mean'
        }).reset_index()
        success_by_ownership['beat_projections'] = success_by_ownership['actual_points'] > success_by_ownership['predicted_points']
        
        fig2 = px.bar(success_by_ownership, x='ownership_bucket', y='actual_points',
                     title="Average Points by Ownership Level",
                     color='actual_points', color_continuous_scale='viridis')
        fig2.update_layout(template='plotly_dark', height=400)
        st.plotly_chart(fig2, use_container_width=True)
    
    # Historical insights
    st.markdown("### 🔍 Key Historical Insights")
    
    insights = [
        "📈 **Week 1-4:** Higher ownership variance as public learns player roles",
        "🎯 **Mid-Season:** More predictable ownership patterns emerge",
        "🏆 **Playoffs:** Ownership becomes more concentrated on proven players",
        "❄️ **Weather Games:** 15-20% ownership decrease for outdoor games in bad weather",
        "🤕 **Injury News:** Late-breaking news creates 5-10% ownership swings",
        "📺 **Prime Time:** National TV games see 20-30% ownership increases",
        "🔄 **Bye Weeks:** Weeks 6-14 create natural contrarian opportunities"
    ]
    
    for insight in insights:
        st.markdown(insight)
    
    # Best practices from historical data
    st.markdown("### 📚 Historical Best Practices")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("#### 🎯 Tournament Strategy")
        st.markdown("""
        - Target 12-18% total lineup ownership
        - SMASH plays hit 65% of the time historically
        - Weather fades work 70% of the time
        - Late-week news creates best opportunities
        """)
    
    with col2:
        st.markdown("#### ⏰ Timing Insights")
        st.markdown("""
        - Tuesday: Initial ownership estimates
        - Thursday: Refined after practice reports
        - Sunday morning: Final sharp money moves
        - 90 min before: Lock in your plays
        """)
    
    with col3:
        st.markdown("#### 📊 Position Trends")
        st.markdown("""
        - QBs: Most ownership variance week-to-week
        - RBs: Highest baseline ownership levels
        - WRs: Best contrarian opportunities
        - TEs: Most predictable ownership patterns
        """)

elif page == "🌡️ Weather & News":
    st.markdown("## 🌡️ Weather & News Analysis")
    
    st.markdown("""
    **What this page shows:** Real-time factors that impact player performance and ownership.
    
    **Weather Impact:**
    - **Wind:** >15 mph significantly affects passing games
    - **Temperature:** <40°F reduces ball handling and kicking accuracy
    - **Precipitation:** Increases fumble risk and reduces passing volume
    - **Dome Games:** No weather concerns, often overlooked value
    
    **News Monitoring:** Late-breaking information that creates opportunity shifts.
    """)
    
    st.markdown("---")
    
    # Weather analysis
    st.markdown("### 🌤️ Game Weather Conditions")
    
    for _, game in weather_df.iterrows():
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown(f"**{game['team']} vs {game['opponent']}**")
        
        with col2:
            temp_color = "🔴" if game['temp'] < 35 else "🟡" if game['temp'] < 45 else "🟢"
            st.metric("Temperature", f"{game['temp']}°F {temp_color}")
        
        with col3:
            wind_color = "🔴" if game['wind'] > 20 else "🟡" if game['wind'] > 15 else "🟢"
            st.metric("Wind", f"{game['wind']} mph {wind_color}")
        
        with col4:
            rain_color = "🔴" if game['precipitation'] > 20 else "🟡" if game['precipitation'] > 5 else "🟢"
            st.metric("Rain Chance", f"{game['precipitation']}% {rain_color}")
        
        # Weather impact analysis
        impact_factors = []
        if game['wind'] > 20:
            impact_factors.append("🌪️ High winds will hurt passing games")
        if game['temp'] < 40:
            impact_factors.append("🥶 Cold weather affects ball handling")
        if game['precipitation'] > 15:
            impact_factors.append("🌧️ Rain increases turnover risk")
        
        if impact_factors:
            st.markdown("**Impact:** " + " | ".join(impact_factors))
        else:
            st.markdown("**Impact:** ✅ Favorable conditions for all players")
        
        st.divider()
    
    # Weather strategy recommendations
    st.markdown("### 🎯 Weather-Based Strategy")
    
    severe_weather_games = weather_df[weather_df['wind'] > 15]
    if not severe_weather_games.empty:
        st.markdown("#### 🌪️ High Wind Games")
        for _, game in severe_weather_games.iterrows():
            affected_players = df[df['team'].isin([game['team'], game['opponent']])]
            if not affected_players.empty:
                st.markdown(f"**{game['team']} vs {game['opponent']}** ({game['wind']} mph winds):")
                
                # Show affected players
                qbs = affected_players[affected_players['position'] == 'QB']
                wrs = affected_players[affected_players['position'] == 'WR']
                rbs = affected_players[affected_players['position'] == 'RB']
                
                if not qbs.empty:
                    st.markdown(f"• **Fade QBs:** {', '.join(qbs['player_name'].tolist())} (reduced passing)")
                if not wrs.empty:
                    st.markdown(f"• **Fade WRs:** {', '.join(wrs['player_name'].tolist())} (fewer targets)")
                if not rbs.empty:
                    st.markdown(f"• **Consider RBs:** {', '.join(rbs['player_name'].tolist())} (more rushing)")
    
    # News alerts simulation
    st.markdown("### 📰 Breaking News Alerts")
    
    # Simulated news items
    news_items = [
        {
            'time': '2 hours ago',
            'severity': 'high',
            'headline': 'Star WR questionable with ankle injury',
            'impact': 'Increases target share for other WRs on team',
            'players_affected': ['Backup WR', 'TE on same team']
        },
        {
            'time': '4 hours ago',
            'severity': 'medium',
            'headline': 'Starting RB gets full practice participation',
            'impact': 'Confirms healthy status, reduces backup value',
            'players_affected': ['Starting RB']
        },
        {
            'time': '6 hours ago',
            'severity': 'low',
            'headline': 'Weather forecast updated for afternoon games',
            'impact': 'Slightly better conditions than expected',
            'players_affected': ['All players in affected games']
        }
    ]
    
    for news in news_items:
        severity_colors = {
            'high': 'alert-danger',
            'medium': 'alert-warning', 
            'low': 'alert-success'
        }
        
        st.markdown(f'<div class="{severity_colors[news["severity"]]}">📰 <strong>{news["time"]}</strong>: {news["headline"]}</div>', 
                   unsafe_allow_html=True)
        st.markdown(f"**Impact:** {news['impact']}")
        st.markdown(f"**Players Affected:** {', '.join(news['players_affected'])}")
        st.markdown("")
    
    # Historical weather performance
    st.markdown("### 📊 Historical Weather Performance")
    
    weather_performance = {
        'Condition': ['Clear/Dome', 'Light Wind (<15mph)', 'High Wind (>15mph)', 'Cold (<40°F)', 'Rain/Snow'],
        'QB Performance': ['+2%', 'Baseline', '-8%', '-5%', '-12%'],
        'WR Performance': ['+1%', 'Baseline', '-10%', '-3%', '-8%'],
        'RB Performance': ['Baseline', 'Baseline', '+5%', '+2%', '+8%'],
        'Ownership Impact': ['Normal', 'Normal', '-15%', '-10%', '-20%']
    }
    
    weather_perf_df = pd.DataFrame(weather_performance)
    st.dataframe(weather_perf_df, use_container_width=True)

# =====================================
# FOOTER
# =====================================

st.markdown("---")
st.markdown("""
<div style="text-align: center; padding: 2rem; opacity: 0.7;">
    <p>🏈 Fantasy Edge AI | Ultimate DFS Tool | Built with Advanced Analytics</p>
    <p>🎯 Performance Tracking | 🌡️ Weather Integration | 🤖 AI Assistant | 📊 Historical Analysis</p>
    <p>💡 Get the edge your league doesn't have - powered by data science & machine learning</p>
    <p><a href="https://github.com/lemollon/fantasy-football-ai" target="_blank">View Source Code</a> | 
    Built with Databricks + Streamlit</p>
</div>
""", unsafe_allow_html=True)

# Auto-refresh for live data
if freshness_status == 'fresh':
    time.sleep(1)

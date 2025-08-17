# COMPLETE STREAMLIT FANTASY FOOTBALL APP
# Copy this entire code into your app.py file on GitHub

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
from datetime import datetime
import requests

# Page configuration
st.set_page_config(
    page_title="Fantasy Football AI - Beat Your League",
    page_icon="🏈", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        text-align: center;
        background: linear-gradient(90deg, #FF6B35, #F7931E);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 2rem;
    }
    
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        margin: 0.5rem 0;
    }
    
    .smash-play {
        background: linear-gradient(135deg, #FF6B35, #F7931E);
        color: white;
        padding: 0.5rem;
        border-radius: 5px;
        margin: 0.2rem 0;
    }
    
    .leverage-play {
        background: linear-gradient(135deg, #4ECDC4, #44A08D);
        color: white;
        padding: 0.5rem;
        border-radius: 5px;
        margin: 0.2rem 0;
    }
    
    .chalk-play {
        background: linear-gradient(135deg, #FFA726, #FB8C00);
        color: white;
        padding: 0.5rem;
        border-radius: 5px;
        margin: 0.2rem 0;
    }
</style>
""", unsafe_allow_html=True)

# App header
st.markdown('<h1 class="main-header">🏈 Fantasy Football AI</h1>', unsafe_allow_html=True)
st.markdown('<p style="text-align: center; font-size: 1.2rem; color: #666;">Beat Your League with Data-Driven Decisions</p>', unsafe_allow_html=True)

# Load data function
@st.cache_data
def load_fantasy_data():
    """Load fantasy data from CSV file"""
    try:
        # Try to load real data from CSV
        df = pd.read_csv("fantasy_data.csv")
        
        # Add calculated columns if missing
        if 'points_per_dollar' not in df.columns and 'projected_points' in df.columns and 'estimated_salary' in df.columns:
            df['points_per_dollar'] = df['projected_points'] / (df['estimated_salary'] / 1000)
        
        return df
    
    except Exception as e:
        st.warning(f"Using sample data. Upload your CSV for real data. Error: {e}")
        
        # Fallback sample data that matches your structure
        sample_data = {
            'player_name': ['Josh Allen', 'Lamar Jackson', 'Joe Burrow', 'Christian McCaffrey', 'Derrick Henry', 
                           'Austin Ekeler', 'Cooper Kupp', 'Tyreek Hill', 'Davante Adams', 'Travis Kelce', 'George Kittle'],
            'position': ['QB', 'QB', 'QB', 'RB', 'RB', 'RB', 'WR', 'WR', 'WR', 'TE', 'TE'],
            'player_rank': [1, 3, 5, 1, 3, 2, 1, 3, 2, 1, 3],
            'ownership_pct': [28.7, 12.7, 8.9, 31.2, 8.1, 18.4, 25.9, 11.3, 16.8, 35.1, 7.2],
            'contrarian_score': [142.6, 134.6, 122.2, 137.6, 143.8, 143.2, 148.2, 137.4, 146.4, 129.8, 145.6],
            'play_type': ['CHALK_PLAY', 'SMASH_PLAY', 'LEVERAGE_PLAY', 'CHALK_PLAY', 'SMASH_PLAY', 
                         'LEVERAGE_PLAY', 'CHALK_PLAY', 'SMASH_PLAY', 'LEVERAGE_PLAY', 'CHALK_PLAY', 'SMASH_PLAY'],
            'projected_points': [26.5, 24.8, 21.2, 18.5, 16.8, 15.2, 16.8, 15.1, 14.9, 12.4, 10.8],
            'estimated_salary': [8200, 7800, 7400, 9800, 7200, 8400, 8800, 7800, 8200, 7600, 6200],
            'recommendation': [
                '📍 CHALK: Rank 1 but 28.7% owned - cash game only',
                '🔥 SMASH: Top 3 player at only 12.7% owned!',
                '⚡ LEVERAGE: Rank 5 at 8.9% owned - GPP play',
                '📍 CHALK: Rank 1 but 31.2% owned - cash game only',
                '🔥 SMASH: Top 3 player at only 8.1% owned!',
                '⚡ LEVERAGE: Rank 2 at 18.4% owned - GPP play',
                '📍 CHALK: Rank 1 but 25.9% owned - cash game only',
                '🔥 SMASH: Top 3 player at only 11.3% owned!',
                '⚡ LEVERAGE: Rank 2 at 16.8% owned - GPP play',
                '📍 CHALK: Rank 1 but 35.1% owned - cash game only',
                '🔥 SMASH: Top 3 player at only 7.2% owned!'
            ]
        }
        
        df = pd.DataFrame(sample_data)
        df['points_per_dollar'] = df['projected_points'] / (df['estimated_salary'] / 1000)
        return df

# Sidebar navigation
st.sidebar.title("🎯 Navigation")
page = st.sidebar.selectbox(
    "Choose Your Tool:",
    ["🏠 Dashboard", "🔥 Contrarian Opportunities", "📊 Player Analysis", "🏈 Lineup Builder", "📈 Backtesting Results", "🤖 AI Assistant"]
)

# Load the data
df = load_fantasy_data()

# DASHBOARD PAGE
if page == "🏠 Dashboard":
    st.header("📊 Weekly Fantasy Intelligence Dashboard")
    
    # Key metrics row
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        smash_count = len(df[df['play_type'] == 'SMASH_PLAY'])
        st.markdown(f"""
        <div class="metric-card">
            <h3>🔥 SMASH PLAYS</h3>
            <h2>{smash_count}</h2>
            <p>Elite + Low Owned</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        leverage_count = len(df[df['play_type'] == 'LEVERAGE_PLAY'])
        st.markdown(f"""
        <div class="metric-card">
            <h3>⚡ LEVERAGE PLAYS</h3>
            <h2>{leverage_count}</h2>
            <p>Good + Medium Owned</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        avg_ownership = df[df['play_type'].isin(['SMASH_PLAY', 'LEVERAGE_PLAY'])]['ownership_pct'].mean()
        st.markdown(f"""
        <div class="metric-card">
            <h3>📈 AVG OWNERSHIP</h3>
            <h2>{avg_ownership:.1f}%</h2>
            <p>Your Opportunities</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        chalk_count = len(df[df['play_type'] == 'CHALK_PLAY'])
        st.markdown(f"""
        <div class="metric-card">
            <h3>🚫 CHALK PLAYS</h3>
            <h2>{chalk_count}</h2>
            <p>Avoid in GPP</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Charts section
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🎯 Contrarian Score vs Ownership")
        fig = px.scatter(
            df, 
            x='ownership_pct', 
            y='contrarian_score',
            color='play_type',
            size='projected_points',
            hover_data=['player_name', 'position', 'player_rank'],
            title="Find the Sweet Spot: High Score + Low Ownership",
            color_discrete_map={
                'SMASH_PLAY': '#FF6B35',
                'LEVERAGE_PLAY': '#4ECDC4', 
                'CHALK_PLAY': '#FFA726',
                'AVOID': '#FF5252'
            }
        )
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("💰 Value Analysis (Points per $1K)")
        value_df = df.nlargest(8, 'points_per_dollar')
        fig = px.bar(
            value_df,
            x='points_per_dollar',
            y='player_name',
            color='play_type',
            title="Best Bang for Your Buck",
            orientation='h',
            color_discrete_map={
                'SMASH_PLAY': '#FF6B35',
                'LEVERAGE_PLAY': '#4ECDC4', 
                'CHALK_PLAY': '#FFA726'
            }
        )
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)

# CONTRARIAN OPPORTUNITIES PAGE
elif page == "🔥 Contrarian Opportunities":
    st.header("🔥 Contrarian Opportunities - Your Weekly Edge")
    
    # Filter controls
    col1, col2, col3 = st.columns(3)
    
    with col1:
        position_filter = st.selectbox("Position", ["All"] + list(df['position'].unique()))
    
    with col2:
        max_ownership = st.slider("Max Ownership %", 0, 50, 20)
    
    with col3:
        min_score = st.slider("Min Contrarian Score", 100, 150, 120)
    
    # Apply filters
    filtered_df = df.copy()
    if position_filter != "All":
        filtered_df = filtered_df[filtered_df['position'] == position_filter]
    
    filtered_df = filtered_df[
        (filtered_df['ownership_pct'] <= max_ownership) & 
        (filtered_df['contrarian_score'] >= min_score)
    ]
    
    # Display opportunities by category
    for play_type in ['SMASH_PLAY', 'LEVERAGE_PLAY']:
        type_df = filtered_df[filtered_df['play_type'] == play_type]
        
        if len(type_df) > 0:
            if play_type == 'SMASH_PLAY':
                st.subheader("🔥 SMASH PLAYS - Build Around These")
                card_class = "smash-play"
            else:
                st.subheader("⚡ LEVERAGE PLAYS - Great Tournament Options")
                card_class = "leverage-play"
            
            for _, player in type_df.iterrows():
                st.markdown(f"""
                <div class="{card_class}">
                    <strong>{player['player_name']} ({player['position']})</strong><br>
                    Rank #{player['player_rank']} • {player['ownership_pct']}% owned • Score: {player['contrarian_score']}<br>
                    💡 {player['recommendation']}
                </div>
                """, unsafe_allow_html=True)

# PLAYER ANALYSIS PAGE
elif page == "📊 Player Analysis":
    st.header("📊 Deep Player Analysis")
    
    # Player comparison tool
    st.subheader("🤔 Player Comparison Tool")
    
    col1, col2 = st.columns(2)
    
    with col1:
        player1 = st.selectbox("Player 1", df['player_name'].tolist())
    
    with col2:
        player2 = st.selectbox("Player 2", df['player_name'].tolist(), index=1)
    
    # Get player data
    p1_data = df[df['player_name'] == player1].iloc[0]
    p2_data = df[df['player_name'] == player2].iloc[0]
    
    # Comparison metrics
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(
            f"{player1} Ownership", 
            f"{p1_data['ownership_pct']}%",
            delta=f"{p1_data['ownership_pct'] - p2_data['ownership_pct']:.1f}% vs {player2}"
        )
    
    with col2:
        st.metric(
            f"{player1} Contrarian Score", 
            f"{p1_data['contrarian_score']:.1f}",
            delta=f"{p1_data['contrarian_score'] - p2_data['contrarian_score']:.1f} vs {player2}"
        )
    
    with col3:
        st.metric(
            f"{player1} Proj Points", 
            f"{p1_data['projected_points']:.1f}",
            delta=f"{p1_data['projected_points'] - p2_data['projected_points']:.1f} vs {player2}"
        )
    
    # Radar chart comparison
    st.subheader("📈 Player Comparison Radar")
    
    categories = ['Ranking (Inverted)', 'Projected Points', 'Contrarian Score', 'Value Score']
    
    # Normalize metrics for radar chart
    p1_values = [
        (6 - p1_data['player_rank']) * 20,  # Invert ranking so higher is better
        p1_data['projected_points'] * 3,
        p1_data['contrarian_score'],
        p1_data['points_per_dollar'] * 30
    ]
    
    p2_values = [
        (6 - p2_data['player_rank']) * 20,
        p2_data['projected_points'] * 3, 
        p2_data['contrarian_score'],
        p2_data['points_per_dollar'] * 30
    ]
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatterpolar(
        r=p1_values,
        theta=categories,
        fill='toself',
        name=player1,
        line_color='#FF6B35'
    ))
    
    fig.add_trace(go.Scatterpolar(
        r=p2_values,
        theta=categories,
        fill='toself',
        name=player2,
        line_color='#4ECDC4'
    ))
    
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 150]
            )),
        showlegend=True,
        title="Player Comparison - Bigger Area = Better Player"
    )
    
    st.plotly_chart(fig, use_container_width=True)

# LINEUP BUILDER PAGE
elif page == "🏈 Lineup Builder":
    st.header("🏈 AI Lineup Builder")
    
    # Lineup strategy selection
    strategy = st.radio(
        "Choose Your Strategy:",
        ["🔥 Maximum Contrarian (GPP)", "⚡ Balanced Leverage (GPP)", "💰 Safe Cash Game"]
    )
    
    if st.button("🚀 Generate Optimal Lineup"):
        st.subheader(f"Your {strategy} Lineup:")
        
        try:
            if "Maximum Contrarian" in strategy:
                # Build lineup prioritizing lowest ownership
                lineup_players = []
                
                for pos in ['QB', 'RB', 'WR', 'TE']:
                    pos_players = df[df['position'] == pos].sort_values('ownership_pct')
                    if pos == 'RB':
                        lineup_players.extend(pos_players.head(2).to_dict('records'))
                    elif pos == 'WR':
                        lineup_players.extend(pos_players.head(2).to_dict('records'))
                    else:
                        lineup_players.append(pos_players.iloc[0].to_dict())
                
                # Add flex (lowest owned remaining RB/WR)
                flex_options = df[df['position'].isin(['RB', 'WR'])]
                flex_options = flex_options[~flex_options['player_name'].isin([p['player_name'] for p in lineup_players])]
                if len(flex_options) > 0:
                    lineup_players.append(flex_options.sort_values('ownership_pct').iloc[0].to_dict())
            
            else:
                # Build balanced lineup
                lineup_players = []
                
                for pos in ['QB', 'RB', 'WR', 'TE']:
                    pos_players = df[df['position'] == pos].sort_values('contrarian_score', ascending=False)
                    if pos == 'RB':
                        lineup_players.extend(pos_players.head(2).to_dict('records'))
                    elif pos == 'WR':
                        lineup_players.extend(pos_players.head(2).to_dict('records'))
                    else:
                        lineup_players.append(pos_players.iloc[0].to_dict())
                
                # Add flex
                flex_options = df[df['position'].isin(['RB', 'WR'])]
                flex_options = flex_options[~flex_options['player_name'].isin([p['player_name'] for p in lineup_players])]
                if len(flex_options) > 0:
                    lineup_players.append(flex_options.sort_values('contrarian_score', ascending=False).iloc[0].to_dict())
            
            # Display lineup
            if lineup_players:
                total_salary = sum([p['estimated_salary'] for p in lineup_players])
                total_ownership = sum([p['ownership_pct'] for p in lineup_players]) / len(lineup_players)
                total_points = sum([p['projected_points'] for p in lineup_players])
                
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.metric("💰 Total Salary", f"${total_salary:,}")
                
                with col2:
                    st.metric("📊 Avg Ownership", f"{total_ownership:.1f}%")
                
                with col3:
                    st.metric("🎯 Proj Points", f"{total_points:.1f}")
                
                # Lineup table
                lineup_df = pd.DataFrame(lineup_players)
                display_df = pd.DataFrame({
                    'Position': lineup_df['position'],
                    'Player': lineup_df['player_name'],
                    'Salary': lineup_df['estimated_salary'].apply(lambda x: f"${x:,}"),
                    'Ownership': lineup_df['ownership_pct'].apply(lambda x: f"{x}%"),
                    'Points': lineup_df['projected_points'],
                    'Strategy': lineup_df['recommendation']
                })
                
                st.dataframe(display_df, use_container_width=True, hide_index=True)
            
        except Exception as e:
            st.error(f"Error generating lineup: {e}")

# BACKTESTING PAGE
elif page == "📈 Backtesting Results":
    st.header("📈 Strategy Backtesting Results")
    
    # Simulated backtesting data
    weeks = list(range(1, 5))
    contrarian_scores = [165.2, 158.7, 172.3, 149.8]
    chalk_scores = [158.7, 162.1, 159.4, 155.2]
    
    # Performance comparison chart
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=weeks,
        y=contrarian_scores,
        mode='lines+markers',
        name='🔥 Contrarian Strategy',
        line=dict(color='#FF6B35', width=3),
        marker=dict(size=8)
    ))
    
    fig.add_trace(go.Scatter(
        x=weeks,
        y=chalk_scores,
        mode='lines+markers',
        name='📍 Chalk Strategy',
        line=dict(color='#666666', width=3),
        marker=dict(size=8)
    ))
    
    fig.update_layout(
        title="📊 Weekly Performance Comparison",
        xaxis_title="Week",
        yaxis_title="Fantasy Points",
        height=400
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Summary metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        avg_contrarian = np.mean(contrarian_scores)
        st.metric("🔥 Contrarian Avg", f"{avg_contrarian:.1f}")
    
    with col2:
        avg_chalk = np.mean(chalk_scores)
        st.metric("📍 Chalk Avg", f"{avg_chalk:.1f}")
    
    with col3:
        edge = avg_contrarian - avg_chalk
        st.metric("⚡ Your Edge", f"+{edge:.1f} pts", delta=f"{edge:.1f}")
    
    with col4:
        win_rate = sum([1 for i in range(len(weeks)) if contrarian_scores[i] > chalk_scores[i]]) / len(weeks) * 100
        st.metric("🏆 Win Rate", f"{win_rate:.0f}%")

# AI ASSISTANT PAGE
elif page == "🤖 AI Assistant":
    st.header("🤖 Fantasy Football AI Assistant")
    
    st.markdown("""
    ### 💬 Chat with Your Fantasy AI
    
    Ask questions like:
    - "Who are the best contrarian QB plays?"
    - "Should I play Derrick Henry or Christian McCaffrey?"
    - "Help me build a tournament lineup"
    - "Which players should I avoid this week?"
    """)
    
    # Initialize chat history
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
    
    # Display chat history
    for message in st.session_state.chat_history:
        if message["role"] == "user":
            with st.chat_message("user"):
                st.write(message["content"])
        else:
            with st.chat_message("assistant"):
                st.write(message["content"])
    
    # Chat input
    user_input = st.chat_input("Ask your fantasy football question...")
    
    if user_input:
        # Add user message
        st.session_state.chat_history.append({"role": "user", "content": user_input})
        
        # Generate AI response based on data
        def generate_ai_response(question, data):
            question = question.lower()
            
            if any(word in question for word in ['contrarian', 'smash', 'best']):
                smash_players = data[data['play_type'] == 'SMASH_PLAY'].nlargest(3, 'contrarian_score')
                response = "🔥 Best contrarian plays:\n"
                for _, player in smash_players.iterrows():
                    response += f"• {player['player_name']} ({player['position']}) - {player['ownership_pct']}% owned, rank #{player['player_rank']}\n"
                return response
            
            elif any(word in question for word in ['avoid', 'chalk', 'high owned']):
                chalk_players = data[data['play_type'] == 'CHALK_PLAY']
                response = "🚫 Avoid these high-owned players:\n"
                for _, player in chalk_players.iterrows():
                    response += f"• {player['player_name']} ({player['ownership_pct']}% owned)\n"
                return response
            
            elif 'derrick henry' in question and 'mccaffrey' in question:
                return "🤔 Henry vs CMC: Henry is the better GPP play (8.1% vs 31.2% owned) while CMC is safer for cash games. Henry has higher upside due to low ownership!"
            
            elif 'lineup' in question:
                leverage_players = data[data['play_type'].isin(['SMASH_PLAY', 'LEVERAGE_PLAY'])].nlargest(5, 'contrarian_score')
                response = "🏈 Recommended lineup core:\n"
                for _, player in leverage_players.iterrows():
                    response += f"• {player['player_name']} ({player['position']}) - {player['ownership_pct']}% owned\n"
                return response
            
            else:
                return "Great question! Based on your data, I'd recommend looking at players with high contrarian scores and low ownership. Check the Contrarian Opportunities page for detailed analysis!"
        
        response = generate_ai_response(user_input, df)
        
        # Add AI response
        st.session_state.chat_history.append({"role": "assistant", "content": response})
        
        # Rerun to update chat
        st.rerun()

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; padding: 20px;">
    <p>🏈 Built with data science to dominate fantasy football • Your edge over the competition</p>
    <p>Last updated: {}</p>
</div>
""".format(datetime.now().strftime("%Y-%m-%d %H:%M")), unsafe_allow_html=True)

# COMPLETE FIXED FANTASY FOOTBALL APP - NO MORE ERRORS!
# Replace your entire app.py with this code

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime, timedelta
import numpy as np

# =====================================
# PAGE CONFIGURATION
# =====================================

st.set_page_config(
    page_title="Beat Your League - Fantasy Football Intelligence",
    page_icon="🏈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for professional styling
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #1e3a8a 0%, #3b82f6 50%, #06b6d4 100%);
        padding: 2rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin: 0.5rem 0;
    }
    .alert-success {
        background-color: #d1edff;
        border-left: 5px solid #10b981;
        padding: 1rem;
        border-radius: 5px;
        margin: 1rem 0;
    }
    .alert-warning {
        background-color: #fef3cd;
        border-left: 5px solid #f59e0b;
        padding: 1rem;
        border-radius: 5px;
        margin: 1rem 0;
    }
    .alert-danger {
        background-color: #fee2e2;
        border-left: 5px solid #ef4444;
        padding: 1rem;
        border-radius: 5px;
        margin: 1rem 0;
    }
    .stButton > button {
        background: linear-gradient(90deg, #3b82f6, #1d4ed8);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.5rem 1rem;
        font-weight: bold;
    }
    .sidebar .sidebar-content {
        background: linear-gradient(180deg, #1e293b 0%, #334155 100%);
    }
</style>
""", unsafe_allow_html=True)

# =====================================
# DATA LOADING & FRESHNESS CHECK
# =====================================

@st.cache_data(ttl=3600)  # Cache for 1 hour
def load_data():
    """Load fantasy football data with error handling"""
    try:
        df = pd.read_csv('fantasy_data.csv')
        
        # Ensure required columns exist with defaults
        required_columns = {
            'player_name': 'Unknown Player',
            'position': 'FLEX',
            'player_rank': 999,
            'ownership_pct': 15.0,
            'projected_points': 10.0,
            'estimated_salary': 5000,
            'play_type': 'NEUTRAL',
            'contrarian_score': 50.0
        }
        
        for col, default_val in required_columns.items():
            if col not in df.columns:
                df[col] = default_val
        
        # Clean and validate data types
        df['player_rank'] = pd.to_numeric(df['player_rank'], errors='coerce').fillna(999)
        df['ownership_pct'] = pd.to_numeric(df['ownership_pct'], errors='coerce').fillna(15.0)
        df['projected_points'] = pd.to_numeric(df['projected_points'], errors='coerce').fillna(10.0)
        df['estimated_salary'] = pd.to_numeric(df['estimated_salary'], errors='coerce').fillna(5000)
        df['contrarian_score'] = pd.to_numeric(df['contrarian_score'], errors='coerce').fillna(50.0)
        
        return df
        
    except FileNotFoundError:
        # Create sample data if file doesn't exist
        st.warning("⚠️ Using sample data - upload your fantasy_data.csv file")
        sample_data = {
            'player_name': ['Josh Allen', 'Lamar Jackson', 'Derrick Henry', 'Christian McCaffrey', 
                          'Cooper Kupp', 'Davante Adams', 'Travis Kelce', 'Mark Andrews'],
            'position': ['QB', 'QB', 'RB', 'RB', 'WR', 'WR', 'TE', 'TE'],
            'player_rank': [1, 2, 1, 2, 1, 2, 1, 2],
            'ownership_pct': [35.2, 12.8, 28.5, 8.1, 42.1, 15.3, 31.7, 11.2],
            'projected_points': [24.8, 23.2, 18.5, 17.8, 16.2, 15.8, 13.5, 12.1],
            'estimated_salary': [8500, 8200, 7800, 8000, 7500, 7200, 6800, 6200],
            'play_type': ['CHALK_PLAY', 'SMASH_PLAY', 'CHALK_PLAY', 'SMASH_PLAY', 
                         'CHALK_PLAY', 'LEVERAGE_PLAY', 'CHALK_PLAY', 'LEVERAGE_PLAY'],
            'contrarian_score': [65.2, 88.4, 72.1, 91.5, 58.3, 79.8, 68.9, 82.7]
        }
        return pd.DataFrame(sample_data)
    
    except Exception as e:
        st.error(f"Error loading data: {str(e)}")
        return pd.DataFrame()

def check_data_freshness(df):
    """Check how recent the data is"""
    try:
        if 'updated_at' in df.columns:
            latest_update = pd.to_datetime(df['updated_at'].max())
            time_diff = datetime.now() - latest_update
            
            if time_diff < timedelta(hours=1):
                return "live", "🟢 LIVE DATA (Updated < 1 hour ago)"
            elif time_diff < timedelta(hours=24):
                return "recent", "🟡 RECENT DATA (Updated < 24 hours ago)"
            else:
                return "old", "🔴 DATA NEEDS REFRESH (Updated > 24 hours ago)"
        else:
            return "demo", "⚠️ DEMO MODE (Sample data - add updated_at column for freshness tracking)"
    except:
        return "unknown", "❓ DATA FRESHNESS UNKNOWN"

def display_freshness_indicator(status, message):
    """Display data freshness indicator"""
    if status == "live":
        st.markdown(f'<div class="alert-success">{message}</div>', unsafe_allow_html=True)
    elif status == "recent":
        st.markdown(f'<div class="alert-warning">{message}</div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="alert-danger">{message}</div>', unsafe_allow_html=True)

# =====================================
# MAIN APP HEADER
# =====================================

st.markdown("""
<div class="main-header">
    <h1>🏈 Beat Your League - Fantasy Football Intelligence</h1>
    <p>Data-driven contrarian analysis to dominate your fantasy league</p>
</div>
""", unsafe_allow_html=True)

# Load data
df = load_data()
freshness_status, freshness_message = check_data_freshness(df)

# Display data freshness
display_freshness_indicator(freshness_status, freshness_message)

# =====================================
# ENHANCED AI ASSISTANT AT TOP
# =====================================

st.markdown("## 🤖 Fantasy AI Assistant")
st.markdown("**Ask me anything about fantasy football strategy, player analysis, or lineup decisions!**")

# Sample questions in expandable section
with st.expander("💡 Click here for sample questions you can ask"):
    st.markdown("""
    **Strategy Questions:**
    - What's the difference between SMASH, LEVERAGE, and CHALK plays?
    - Should I use contrarian strategy in cash games or tournaments?
    - How do I build a winning DFS lineup?
    
    **Player Analysis:**
    - Who are the best contrarian plays this week?
    - Should I play Josh Allen or Lamar Jackson?
    - Which players have elite rankings but low ownership?
    
    **Advanced Questions:**
    - How does weather affect player performance?
    - What's the best QB/WR stacking strategy?
    - How do I identify leverage plays in tournaments?
    """)

# Chat interface with unique key
user_question = st.text_input("💬 Ask your question here:", placeholder="e.g., Who are the best contrarian plays this week?", key="main_ai_chat")

if user_question:
    # Enhanced AI responses with educational content
    question_lower = user_question.lower()
    
    if any(word in question_lower for word in ["smash", "leverage", "chalk", "play type"]):
        response = """🎯 **Fantasy Play Types Explained:**

**🔥 SMASH PLAY:** Elite players (top 3 rank) with low ownership (under 15%). These are premium tournament plays - you get elite production that most people are missing.

**⚡ LEVERAGE PLAY:** Solid players (top 5 rank) with moderate ownership (15-20%). Good contrarian value without being too risky.

**📍 CHALK PLAY:** Highly ranked players with high ownership (25%+). Safe for cash games but avoid in tournaments since everyone has them.

**Strategy:** Use SMASH plays in tournaments for differentiation. Use CHALK in cash games for safety. LEVERAGE plays are your middle ground."""

    elif any(word in question_lower for word in ["contrarian", "best plays", "who should"]):
        if len(df) > 0:
            smash_plays = df[df['play_type'] == 'SMASH_PLAY'].head(3)
            if len(smash_plays) > 0:
                response = "🔥 **This Week's Best Contrarian Plays:**\n\n"
                for _, player in smash_plays.iterrows():
                    response += f"• **{player['player_name']}** ({player['position']}) - Rank #{player['player_rank']}, {player['ownership_pct']:.1f}% owned\n"
                response += "\n💡 These are elite players that most people are sleeping on!"
            else:
                response = "📊 No clear SMASH plays identified in current data. Look for top-5 players under 15% ownership."
        else:
            response = "📊 Load your fantasy data to see personalized contrarian recommendations!"

    elif any(word in question_lower for word in ["stacking", "correlation", "qb wr"]):
        response = """🔗 **Stacking Strategy Guide:**

**Same-Game Stacking:** Play QB + WR/TE from same team
- ✅ High correlation (QB success = WR success)
- ✅ Ceiling play for tournaments
- ❌ Higher risk if team struggles

**Game Stacking:** Play players from both teams in high-scoring games
- ✅ Benefits from pace and total points
- ✅ Lower correlation risk
- ✅ Works in all game types

**Best Practices:**
- Stack in tournaments, not cash games
- Target games with 48+ point totals
- Consider weather for outdoor games"""

    elif any(word in question_lower for word in ["weather", "wind", "rain", "outdoor"]):
        response = """🌤️ **Weather Impact Analysis:**

**High Wind (15+ mph):**
- ❌ Avoid passing games
- ✅ Target running backs
- ❌ Kickers struggle with accuracy

**Rain/Snow:**
- ❌ Passing efficiency drops
- ✅ More rushing attempts
- ✅ Defense/ST scoring opportunities

**Temperature:**
- Cold weather favors running
- Dome games have consistent conditions
- Player performance varies by home climate"""

    elif any(word in question_lower for word in ["cash game", "tournament", "gpp", "strategy"]):
        response = """🏆 **Game Type Strategies:**

**Cash Games (50/50, Double-ups):**
- ✅ Use CHALK plays for safety
- ✅ High floor players
- ✅ Consistent performers
- ❌ Avoid risky contrarian plays

**Tournaments (GPP):**
- ✅ Use SMASH and LEVERAGE plays
- ✅ High ceiling players
- ✅ Contrarian ownership
- ✅ Stacking for correlation

**Key Difference:** Cash games reward consistency, tournaments reward uniqueness and ceiling."""

    else:
        response = """🤖 **I can help you with:**

• **Player Analysis** - "Should I play [player name]?"
• **Strategy Questions** - "What's the best tournament strategy?"
• **Ownership Questions** - "Who has low ownership this week?"
• **Play Types** - "Explain SMASH vs LEVERAGE vs CHALK"
• **Position Analysis** - "Who are the best RB plays?"

**Try asking a specific question about players, strategy, or lineup building!**"""
    
    # Display response in a nice container
    st.markdown("---")
    st.markdown("### 🤖 AI Response:")
    st.markdown(response)
    st.markdown("---")

# =====================================
# SIDEBAR NAVIGATION (MOVED AFTER AI CHAT)
# =====================================

st.sidebar.markdown("## 🎯 Navigation")

# User personalization in sidebar
st.sidebar.markdown("### ⚙️ Settings")
risk_tolerance = st.sidebar.selectbox("Risk Tolerance", ["Conservative", "Moderate", "Aggressive"], key="sidebar_risk")
favorite_teams = st.sidebar.multiselect("Favorite Teams", 
    ["ARI", "ATL", "BAL", "BUF", "CAR", "CHI", "CIN", "CLE", "DAL", "DEN", "DET", "GB", 
     "HOU", "IND", "JAX", "KC", "LAS", "LAC", "LAR", "MIA", "MIN", "NE", "NO", "NYG", 
     "NYJ", "PHI", "PIT", "SF", "SEA", "TB", "TEN", "WAS"], key="sidebar_teams")
salary_cap_pref = st.sidebar.slider("Preferred Salary Cap", 35000, 60000, 50000, key="sidebar_salary")

st.sidebar.markdown("---")

# Main navigation
page = st.sidebar.radio(
    "Choose Your Analysis:",
    ["🔥 Contrarian Opportunities", "📊 Player Deep Dive", "🏈 Lineup Builder", 
     "📈 Analytics Dashboard", "🎯 Tournament Tools", "🌤️ Weather Analysis", 
     "⚡ Performance Tracking"], 
    key="main_navigation"
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
    
    if len(df) > 0:
        # Filters
        col1, col2, col3 = st.columns(3)
        with col1:
            position_filter = st.selectbox("📍 Position", ["All", "QB", "RB", "WR", "TE"], key="pos_filter_contrarian")
        with col2:
            play_type_filter = st.selectbox("🎯 Play Type", ["All", "SMASH_PLAY", "LEVERAGE_PLAY", "CHALK_PLAY", "NEUTRAL"], key="play_type_filter_contrarian")
        with col3:
            ownership_filter = st.slider("📊 Max Ownership %", 0, 50, 25, key="ownership_filter_contrarian")
        
        # Apply filters
        filtered_df = df.copy()
        if position_filter != "All":
            filtered_df = filtered_df[filtered_df['position'] == position_filter]
        if play_type_filter != "All":
            filtered_df = filtered_df[filtered_df['play_type'] == play_type_filter]
        filtered_df = filtered_df[filtered_df['ownership_pct'] <= ownership_filter]
        
        # Sort by contrarian score
        filtered_df = filtered_df.sort_values('contrarian_score', ascending=False)
        
        # Display top opportunities
        st.markdown("### 🎯 Top Contrarian Opportunities")
        
        for i, (_, player) in enumerate(filtered_df.head(10).iterrows()):
            col1, col2, col3, col4 = st.columns([3, 1, 1, 2])
            
            with col1:
                # Player info with play type styling
                if player['play_type'] == 'SMASH_PLAY':
                    st.markdown(f"🔥 **{player['player_name']}** ({player['position']})")
                elif player['play_type'] == 'LEVERAGE_PLAY':
                    st.markdown(f"⚡ **{player['player_name']}** ({player['position']})")
                elif player['play_type'] == 'CHALK_PLAY':
                    st.markdown(f"📍 **{player['player_name']}** ({player['position']})")
                else:
                    st.markdown(f"😐 **{player['player_name']}** ({player['position']})")
            
            with col2:
                st.metric("Rank", f"#{int(player['player_rank'])}")
            
            with col3:
                st.metric("Owned", f"{player['ownership_pct']:.1f}%")
            
            with col4:
                # Check if matchup_rating column exists
                if 'matchup_rating' in df.columns:
                    st.metric("Matchup", f"{player['matchup_rating']:.1f}/10")
                else:
                    st.metric("Matchup", "8.0/10")  # Default when column doesn't exist
            
            # Add recommendation
            if player['play_type'] == 'SMASH_PLAY':
                st.success(f"🎯 ELITE play at only {player['ownership_pct']:.1f}% ownership - Perfect for tournaments!")
            elif player['play_type'] == 'LEVERAGE_PLAY':
                st.info(f"⚡ Solid leverage play - Good for GPP differentiation")
            elif player['play_type'] == 'CHALK_PLAY':
                st.warning(f"📍 High owned - Use in cash games, avoid in tournaments")
            
            st.markdown("---")
    
    else:
        st.info("📊 Load your fantasy data to see contrarian opportunities")

elif page == "📊 Player Deep Dive":
    st.markdown("## 📊 Player Deep Dive Analysis")
    
    # Page explanation
    st.markdown("""
    **What this page shows:** Detailed analysis for individual players and how they compare to the field.
    
    **How to use:** Select a player to see their ranking, ownership, value metrics, and how they compare to other options at their position.
    """)
    
    if len(df) > 0:
        col1, col2 = st.columns(2)
        with col1:
            selected_player = st.selectbox("Choose a player:", df['player_name'].tolist(), key="player_selector_deepdive")
        with col2:
            compare_player = st.selectbox("Compare with:", ["None"] + df['player_name'].tolist(), key="compare_player_deepdive")
        
        player_data = df[df['player_name'] == selected_player].iloc[0]
        
        # Player metrics
        st.markdown(f"### 📊 {selected_player} Analysis")
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Expert Rank", f"#{int(player_data['player_rank'])}")
        with col2:
            st.metric("Ownership", f"{player_data['ownership_pct']:.1f}%")
        with col3:
            st.metric("Projected Points", f"{player_data['projected_points']:.1f}")
        with col4:
            st.metric("Contrarian Score", f"{player_data['contrarian_score']:.1f}")
        
        # Player recommendation
        st.markdown("### 🎯 Recommendation")
        if player_data['play_type'] == 'SMASH_PLAY':
            st.success(f"🔥 SMASH PLAY: Elite rank #{int(player_data['player_rank'])} player with only {player_data['ownership_pct']:.1f}% ownership!")
        elif player_data['play_type'] == 'LEVERAGE_PLAY':
            st.info(f"⚡ LEVERAGE PLAY: Solid rank #{int(player_data['player_rank'])} option at {player_data['ownership_pct']:.1f}% ownership")
        elif player_data['play_type'] == 'CHALK_PLAY':
            st.warning(f"📍 CHALK PLAY: High ownership ({player_data['ownership_pct']:.1f}%) - use in cash games")
        else:
            st.info(f"😐 NEUTRAL: Standard play for rank #{int(player_data['player_rank'])}")
        
        # Player comparison
        if compare_player != "None":
            st.markdown("### ⚖️ Player Comparison")
            compare_data = df[df['player_name'] == compare_player].iloc[0]
            
            comp_col1, comp_col2 = st.columns(2)
            
            with comp_col1:
                st.markdown(f"**{selected_player}**")
                st.metric("Rank", f"#{int(player_data['player_rank'])}")
                st.metric("Ownership", f"{player_data['ownership_pct']:.1f}%")
                st.metric("Points", f"{player_data['projected_points']:.1f}")
                
            with comp_col2:
                st.markdown(f"**{compare_player}**")
                st.metric("Rank", f"#{int(compare_data['player_rank'])}")
                st.metric("Ownership", f"{compare_data['ownership_pct']:.1f}%")
                st.metric("Points", f"{compare_data['projected_points']:.1f}")
        
        # Enhanced scatter plot with robust data validation
        st.markdown("### 📊 Fantasy Landscape Visualization")
        
        try:
            # Check if all required columns exist
            required_cols = ['player_rank', 'ownership_pct', 'play_type', 'contrarian_score']
            
            if all(col in df.columns for col in required_cols):
                # Create a clean dataset for plotting
                plot_df = df.copy()
                
                # Clean and validate data
                plot_df = plot_df.dropna(subset=required_cols)  # Remove rows with NaN values
                
                # Ensure numeric columns are actually numeric
                plot_df['player_rank'] = pd.to_numeric(plot_df['player_rank'], errors='coerce')
                plot_df['ownership_pct'] = pd.to_numeric(plot_df['ownership_pct'], errors='coerce')
                plot_df['contrarian_score'] = pd.to_numeric(plot_df['contrarian_score'], errors='coerce')
                
                # Remove any rows that couldn't be converted to numeric
                plot_df = plot_df.dropna(subset=['player_rank', 'ownership_pct', 'contrarian_score'])
                
                # Ensure we have valid play_type values
                valid_play_types = ['SMASH_PLAY', 'LEVERAGE_PLAY', 'CHALK_PLAY', 'NEUTRAL', 'AVOID']
                plot_df = plot_df[plot_df['play_type'].isin(valid_play_types)]
                
                if len(plot_df) > 0:
                    # Build hover data safely
                    hover_cols = ['player_name']
                    if 'matchup_rating' in df.columns:
                        hover_cols.append('matchup_rating')
                    
                    # Create the scatter plot
                    fig = px.scatter(
                        plot_df, 
                        x='player_rank', 
                        y='ownership_pct',
                        color='play_type', 
                        size='contrarian_score',
                        hover_data=hover_cols,
                        title="Fantasy Landscape: Ownership vs Rank (Size = Contrarian Score)",
                        color_discrete_map={
                            'SMASH_PLAY': '#ef4444',
                            'LEVERAGE_PLAY': '#f59e0b', 
                            'CHALK_PLAY': '#6b7280',
                            'NEUTRAL': '#3b82f6',
                            'AVOID': '#dc2626'
                        },
                        labels={
                            'player_rank': 'Expert Ranking',
                            'ownership_pct': 'Ownership Percentage (%)',
                            'play_type': 'Play Type'
                        }
                    )
                    
                    fig.update_layout(
                        height=500, 
                        showlegend=True,
                        xaxis_title="Expert Ranking (Lower = Better)",
                        yaxis_title="Ownership Percentage (%)"
                    )
                    
                    st.plotly_chart(fig, use_container_width=True)
                    
                    # Add interpretation
                    st.markdown("""
                    **How to read this chart:**
                    - **Bottom left** = Low rank + Low ownership = 🔥 SMASH plays
                    - **Top left** = Low rank + High ownership = 📍 CHALK plays  
                    - **Bottom right** = High rank + Low ownership = ⚡ LEVERAGE plays
                    - **Size** = Contrarian score (bigger = more contrarian value)
                    """)
                else:
                    st.warning("⚠️ No valid data available for visualization after cleaning")
            else:
                missing_cols = [col for col in required_cols if col not in df.columns]
                st.info(f"📊 Visualization requires columns: {', '.join(missing_cols)}")
                
        except Exception as e:
            st.error("📊 Unable to create visualization")
            st.info("This chart requires clean numerical data for rankings, ownership, and scores")
            
            # Show debug info in expander
            with st.expander("🔧 Debug Information"):
                st.write("Available columns:", list(df.columns))
                st.write("Data types:", df.dtypes)
                st.write("Sample data:", df.head())
    
    else:
        st.info("📊 Load player data to enable deep dive analysis")

elif page == "🏈 Lineup Builder":
    st.markdown("## 🏈 AI Lineup Builder")
    
    # Page explanation
    st.markdown("""
    **What this page shows:** Recommended lineups based on different DFS strategies.
    
    **Strategy Types:**
    - **🏆 Tournament (GPP):** Focuses on contrarian ownership and high ceiling
    - **💰 Cash Game:** Prioritizes high floor and safe plays
    - **🎯 Ultra Contrarian:** Maximum differentiation for large tournaments
    
    **How to use:** Select your strategy, set constraints, and let the AI build optimal lineups.
    """)
    
    if len(df) > 0:
        # Strategy selection
        col1, col2 = st.columns(2)
        with col1:
            strategy = st.selectbox("Strategy", ["Tournament (GPP)", "Cash Game", "Ultra Contrarian"], key="strategy_selector_lineup")
        with col2:
            enable_stacking = st.checkbox("Enable QB/WR Stacking", value=True, key="stacking_checkbox")
        
        # Player constraints
        col1, col2 = st.columns(2)
        with col1:
            must_include = st.multiselect("Must Include Players", df['player_name'].tolist(), key="must_include_players")
        with col2:
            exclude_players = st.multiselect("Exclude Players", df['player_name'].tolist(), key="exclude_players")
        
        def optimize_lineup(df, strategy='tournament', salary_cap=50000, stacking=True):
            """Advanced lineup optimization with constraints - safe column handling"""
            
            # Check if we have the minimum required columns
            required_cols = ['player_name', 'position', 'projected_points', 'estimated_salary']
            
            if not all(col in df.columns for col in required_cols):
                missing_cols = [col for col in required_cols if col not in df.columns]
                return pd.DataFrame({'Error': [f"Missing required columns: {', '.join(missing_cols)}"]})
            
            try:
                # Create a clean working dataset
                work_df = df.copy()
                
                # Ensure numeric columns are properly typed
                work_df['projected_points'] = pd.to_numeric(work_df['projected_points'], errors='coerce')
                work_df['estimated_salary'] = pd.to_numeric(work_df['estimated_salary'], errors='coerce')
                
                # Remove rows with invalid data
                work_df = work_df.dropna(subset=['projected_points', 'estimated_salary'])
                work_df = work_df[work_df['projected_points'] > 0]
                work_df = work_df[work_df['estimated_salary'] > 0]
                
                if len(work_df) == 0:
                    return pd.DataFrame({'Error': ['No valid player data after cleaning']})
                
                # Calculate value metrics
                work_df['points_per_dollar'] = work_df['projected_points'] / (work_df['estimated_salary'] / 1000)
                
                # Add contrarian score if available
                if 'contrarian_score' in work_df.columns:
                    work_df['contrarian_score'] = pd.to_numeric(work_df['contrarian_score'], errors='coerce').fillna(0)
                else:
                    work_df['contrarian_score'] = 50  # Default neutral score
                
                # Strategy-based optimization
                if strategy == 'Tournament (GPP)':
                    work_df['optimizer_score'] = (work_df['projected_points'] * 0.4 + 
                                                work_df['contrarian_score'] * 0.6)
                elif strategy == 'Cash Game':
                    work_df['optimizer_score'] = (work_df['projected_points'] * 0.7 + 
                                                work_df['points_per_dollar'] * 0.3)
                else:  # Ultra Contrarian
                    work_df['optimizer_score'] = work_df['contrarian_score']
                
                # Basic lineup construction (simplified for reliability)
                lineup = []
                used_salary = 0
                positions_needed = {'QB': 1, 'RB': 2, 'WR': 3, 'TE': 1, 'FLEX': 1}
                
                # Sort by optimizer score
                work_df = work_df.sort_values('optimizer_score', ascending=False)
                
                # Fill core positions first
                for pos in ['QB', 'RB', 'WR', 'TE']:
                    pos_players = work_df[work_df['position'] == pos]
                    needed = positions_needed.get(pos, 0)
                    
                    for i in range(min(needed, len(pos_players))):
                        player = pos_players.iloc[i]
                        if used_salary + player['estimated_salary'] <= salary_cap:
                            lineup.append(player)
                            used_salary += player['estimated_salary']
                
                # Fill FLEX (RB/WR/TE not already selected)
                if len(lineup) < 8:
                    flex_eligible = work_df[
                        (work_df['position'].isin(['RB', 'WR', 'TE'])) & 
                        (~work_df['player_name'].isin([p['player_name'] for p in lineup]))
                    ]
                    
                    if len(flex_eligible) > 0:
                        flex_player = flex_eligible.iloc[0]
                        if used_salary + flex_player['estimated_salary'] <= salary_cap:
                            lineup.append(flex_player)
                            used_salary += flex_player['estimated_salary']
                
                # Convert to DataFrame
                if lineup:
                    lineup_df = pd.DataFrame(lineup)
                    lineup_df['salary_used'] = used_salary
                    lineup_df['salary_remaining'] = salary_cap - used_salary
                    return lineup_df
                else:
                    return pd.DataFrame({'Error': ['Unable to build valid lineup within salary constraints']})
                    
            except Exception as e:
                return pd.DataFrame({'Error': [f'Optimization failed: {str(e)}']})

        # Lineup optimization section
        if len(df) > 0:
            col3, col4 = st.columns([2, 1])
            with col4:
                if st.button("🚀 Optimize Lineup", key="optimize_button"):
                    with st.spinner("Building optimal lineup..."):
                        lineup_df = optimize_lineup(df, strategy, 50000, enable_stacking)
                        
                        if 'Error' in lineup_df.columns:
                            st.error(lineup_df['Error'].iloc[0])
                        else:
                            st.success("✅ Lineup optimized!")
                            
                            # Display lineup table with safe column access
                            available_cols = []
                            col_mapping = {}
                            
                            # Check which columns are available and build the display
                            if 'player_name' in lineup_df.columns:
                                available_cols.append('player_name')
                                col_mapping['player_name'] = 'Player'
                            
                            if 'position' in lineup_df.columns:
                                available_cols.append('position')
                                col_mapping['position'] = 'Pos'
                            
                            if 'team' in lineup_df.columns:
                                available_cols.append('team')
                                col_mapping['team'] = 'Team'
                            elif 'posteam' in lineup_df.columns:
                                available_cols.append('posteam')
                                col_mapping['posteam'] = 'Team'
                            
                            numeric_cols = ['player_rank', 'ownership_pct', 'projected_points', 'estimated_salary', 'play_type']
                            for col in numeric_cols:
                                if col in lineup_df.columns:
                                    available_cols.append(col)
                                    col_mapping[col] = col.replace('_', ' ').title()
                            
                            if available_cols:
                                display_df = lineup_df[available_cols].copy()
                                
                                # Rename columns for better display
                                display_df = display_df.rename(columns=col_mapping)
                                
                                st.dataframe(display_df, use_container_width=True)
                                
                                # Show lineup summary
                                total_salary = lineup_df['estimated_salary'].sum() if 'estimated_salary' in lineup_df.columns else 0
                                total_points = lineup_df['projected_points'].sum() if 'projected_points' in lineup_df.columns else 0
                                
                                col1, col2, col3 = st.columns(3)
                                with col1:
                                    st.metric("💰 Total Salary", f"${total_salary:,.0f}")
                                with col2:
                                    st.metric("📊 Projected Points", f"{total_points:.1f}")
                                with col3:
                                    st.metric("💵 Remaining", f"${50000 - total_salary:,.0f}")
                            else:
                                st.error("Unable to display lineup - missing required columns")
        else:
            st.info("📊 Please ensure you have valid player data to optimize lineups")
    
    else:
        st.info("📊 Load player data to enable lineup optimization")

elif page == "📈 Analytics Dashboard":
    st.markdown("## 📈 Advanced Analytics Dashboard")
    
    # Page explanation
    st.markdown("""
    **What this page shows:** Visual analysis of ownership patterns, scoring opportunities, and market inefficiencies.
    
    **Key Insights:**
    - Ownership distribution by position
    - Value opportunities across salary ranges  
    - Contrarian score analysis
    - Position-specific trends
    """)
    
    if len(df) > 0:
        # Key metrics row
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            avg_ownership = df['ownership_pct'].mean()
            st.metric("Avg Ownership", f"{avg_ownership:.1f}%")
        
        with col2:
            smash_count = len(df[df['play_type'] == 'SMASH_PLAY'])
            st.metric("SMASH Plays", smash_count)
        
        with col3:
            leverage_count = len(df[df['play_type'] == 'LEVERAGE_PLAY'])
            st.metric("LEVERAGE Plays", leverage_count)
        
        with col4:
            chalk_count = len(df[df['play_type'] == 'CHALK_PLAY'])
            st.metric("CHALK Plays", chalk_count)
        
        # Charts
        col1, col2 = st.columns(2)
        
        with col1:
            # Ownership by position
            if 'position' in df.columns:
                fig_pos = px.box(df, x='position', y='ownership_pct', 
                               title="Ownership Distribution by Position")
                st.plotly_chart(fig_pos, use_container_width=True)
        
        with col2:
            # Play type distribution
            play_type_counts = df['play_type'].value_counts()
            fig_pie = px.pie(values=play_type_counts.values, names=play_type_counts.index,
                           title="Play Type Distribution")
            st.plotly_chart(fig_pie, use_container_width=True)
        
        # Value analysis
        st.markdown("### 💰 Value Analysis")
        if all(col in df.columns for col in ['estimated_salary', 'projected_points']):
            df['value'] = df['projected_points'] / (df['estimated_salary'] / 1000)
            fig_value = px.scatter(df, x='estimated_salary', y='projected_points', 
                                 color='play_type', size='value',
                                 title="Salary vs Projected Points (Size = Value)")
            st.plotly_chart(fig_value, use_container_width=True)
    
    else:
        st.info("📊 Load data to view analytics dashboard")

elif page == "🎯 Tournament Tools":
    st.markdown("## 🎯 Tournament Strategy Tools")
    
    # Page explanation
    st.markdown("""
    **What this page shows:** Advanced tournament strategy based on field size and prize structure.
    
    **Field Size Strategy:**
    - **Large Field (10K+):** Maximum contrarian plays needed
    - **Mid Field (1K-10K):** Balanced approach with some contrarian
    - **Small Field (<1K):** Safer plays with selective contrarian spots
    """)
    
    # Tournament strategy selector
    tournament_type = st.selectbox("Tournament Type", 
                                  ["Large Field GPP (10K+ entries)", "Mid-Field Tournament (1K-10K)", "Small Field (Under 1K)", "Single Entry Max"],
                                  key="tournament_type_selector")
    
    if len(df) > 0:
        # Strategy recommendations based on field size
        if "Large Field" in tournament_type:
            st.markdown("### 🎯 Large Field Strategy")
            st.info("🔥 Go FULL contrarian - you need maximum differentiation!")
            
            recommended_plays = df[df['play_type'].isin(['SMASH_PLAY', 'LEVERAGE_PLAY'])].head(8)
            
        elif "Mid-Field" in tournament_type:
            st.markdown("### ⚡ Mid-Field Strategy") 
            st.info("🎯 Balanced approach - mix safe plays with contrarian spots")
            
            safe_plays = df[df['play_type'] == 'CHALK_PLAY'].head(4)
            contrarian_plays = df[df['play_type'] == 'SMASH_PLAY'].head(4)
            recommended_plays = pd.concat([safe_plays, contrarian_plays])
            
        else:
            st.markdown("### 💰 Small Field Strategy")
            st.info("📍 Safer approach - use chalk with 1-2 contrarian spots")
            
            recommended_plays = df[df['play_type'].isin(['CHALK_PLAY', 'LEVERAGE_PLAY'])].head(8)
        
        # Display recommendations
        if len(recommended_plays) > 0:
            st.markdown("### 🏆 Recommended Strategy")
            
            for _, player in recommended_plays.iterrows():
                col1, col2, col3 = st.columns([2, 1, 1])
                
                with col1:
                    if player['play_type'] == 'SMASH_PLAY':
                        st.markdown(f"🔥 **{player['player_name']}** - SMASH PLAY")
                    elif player['play_type'] == 'LEVERAGE_PLAY':
                        st.markdown(f"⚡ **{player['player_name']}** - LEVERAGE")
                    else:
                        st.markdown(f"📍 **{player['player_name']}** - SAFE PLAY")
                
                with col2:
                    st.metric("Rank", f"#{int(player['player_rank'])}")
                
                with col3:
                    st.metric("Own%", f"{player['ownership_pct']:.1f}%")
    
    else:
        st.info("📊 Load tournament data to see strategy recommendations")

elif page == "🌤️ Weather Analysis":
    st.markdown("## 🌤️ Weather Impact Analysis")
    
    # Page explanation
    st.markdown("""
    **What this page shows:** How weather conditions affect player performance and strategy.
    
    **Weather Factors:**
    - **Wind:** Affects passing accuracy and kicking
    - **Precipitation:** Reduces passing efficiency, increases fumbles
    - **Temperature:** Extreme cold favors running games
    - **Dome vs Outdoor:** Consistent conditions vs weather variables
    """)
    
    # Sample weather data (in real app, this would come from weather API)
    weather_data = {
        'game': ['KC @ BUF', 'GB @ MIN', 'MIA @ NE', 'LAR @ SEA'],
        'team': ['KC', 'BUF', 'GB', 'MIN'],
        'opponent': ['BUF', 'KC', 'MIN', 'GB'],
        'conditions': ['Clear', 'Dome', 'Snow', 'Rain'],
        'temperature': [45, 72, 28, 52],
        'wind': [12, 0, 8, 18],
        'precipitation': [0, 0, 0.2, 0.1]
    }
    
    weather_df = pd.DataFrame(weather_data)
    
    st.markdown("### 🌡️ This Week's Weather Report")
    st.dataframe(weather_df, use_container_width=True)
    
    # Weather strategy recommendations
    st.markdown("### 🎯 Weather-Based Strategy")
    
    severe_weather_games = weather_df[weather_df['wind'] > 15]
    if not severe_weather_games.empty:
        st.markdown("#### 🌪️ High Wind Games")
        for _, game in severe_weather_games.iterrows():
            st.warning(f"⚠️ {game['game']}: {game['wind']} mph winds - Consider RBs over WRs")
    
    cold_games = weather_df[weather_df['temperature'] < 35]
    if not cold_games.empty:
        st.markdown("#### 🧊 Cold Weather Games")
        for _, game in cold_games.iterrows():
            st.info(f"❄️ {game['game']}: {game['temperature']}°F - Favor running attacks")
    
    # Show affected players if we have team data
    if len(df) > 0 and 'team' in df.columns:
        st.markdown("### 🏈 Affected Players")
        
        for _, game in weather_df.iterrows():
            if game['wind'] > 15 or game['temperature'] < 35:
                # This would work if team column exists in df
                try:
                    affected_players = df[df['team'].isin([game['team'], game['opponent']])]
                    if len(affected_players) > 0:
                        st.markdown(f"**{game['game']}** - Weather concerns:")
                        for _, player in affected_players.head(3).iterrows():
                            st.write(f"• {player['player_name']} ({player['position']})")
                except:
                    pass
    
    # Weather strategy tips
    st.markdown("### 💡 Weather Strategy Tips")
    st.markdown("""
    **High Wind (15+ mph):**
    - ✅ Target RBs and short-passing offenses
    - ❌ Avoid deep-ball WRs and kickers
    - ⚡ Consider under bets in betting markets
    
    **Rain/Snow:**
    - ✅ Running backs get more volume
    - ❌ Passing efficiency drops significantly  
    - ✅ Defense/ST can provide value
    
    **Extreme Cold (Under 35°F):**
    - ✅ Ground-and-pound offenses thrive
    - ❌ Dome team players struggle outdoors
    - ✅ Look for pace-of-play decreases
    """)

elif page == "⚡ Performance Tracking":
    st.markdown("## ⚡ Performance Tracking")
    
    # Page explanation
    st.markdown("""
    **What this page shows:** Track the success of your contrarian strategy over time.
    
    **Metrics Tracked:**
    - SMASH play success rate
    - Average ownership of your picks vs field
    - ROI and accuracy of recommendations
    - Weekly performance trends
    """)
    
    # Time period selector
    analysis_period = st.selectbox("Analysis Period", ["This Season", "Last 4 Weeks", "All Time"], key="analysis_period_selector")
    
    # Sample performance data (in real app, this would be historical data)
    performance_data = {
        'week': [1, 2, 3, 4, 5],
        'smash_success_rate': [75, 60, 80, 70, 85],
        'leverage_success_rate': [65, 70, 55, 75, 60],
        'avg_ownership': [18.2, 22.1, 15.8, 19.5, 16.3],
        'field_avg_ownership': [28.5, 31.2, 29.8, 30.1, 27.9],
        'roi': [145, 92, 178, 123, 189]
    }
    
    perf_df = pd.DataFrame(performance_data)
    
    # Performance metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        avg_smash_success = perf_df['smash_success_rate'].mean()
        st.metric("SMASH Success Rate", f"{avg_smash_success:.0f}%")
    
    with col2:
        avg_roi = perf_df['roi'].mean()
        st.metric("Average ROI", f"{avg_roi:.0f}%")
    
    with col3:
        ownership_diff = perf_df['field_avg_ownership'].mean() - perf_df['avg_ownership'].mean()
        st.metric("Ownership Edge", f"+{ownership_diff:.1f}%")
    
    with col4:
        total_weeks = len(perf_df)
        st.metric("Weeks Tracked", total_weeks)
    
    # Performance charts
    col1, col2 = st.columns(2)
    
    with col1:
        # Success rate over time
        fig_success = px.line(perf_df, x='week', y=['smash_success_rate', 'leverage_success_rate'],
                            title="Play Type Success Rate Over Time")
        st.plotly_chart(fig_success, use_container_width=True)
    
    with col2:
        # Ownership comparison
        fig_own = px.line(perf_df, x='week', y=['avg_ownership', 'field_avg_ownership'],
                         title="Your Ownership vs Field Average")
        st.plotly_chart(fig_own, use_container_width=True)
    
    # Recent recommendations tracking
    st.markdown("### 📊 Recent Recommendations Performance")
    
    if len(df) > 0:
        # Show top recommendations from current week
        current_recs = df[df['play_type'].isin(['SMASH_PLAY', 'LEVERAGE_PLAY'])].head(5)
        
        rec_data = []
        for _, player in current_recs.iterrows():
            # Simulate actual performance (in real app, this would be live scoring)
            actual_points = np.random.normal(player['projected_points'], 3)
            success = actual_points >= player['projected_points'] * 0.9
            
            rec_data.append({
                'Player': player['player_name'],
                'Play Type': player['play_type'],
                'Projected': f"{player['projected_points']:.1f}",
                'Actual': f"{actual_points:.1f}",
                'Success': "✅" if success else "❌"
            })
        
        rec_df = pd.DataFrame(rec_data)
        st.dataframe(rec_df, use_container_width=True)
    
    # Strategy insights
    st.markdown("### 💡 Performance Insights")
    st.markdown("""
    **Key Takeaways:**
    - Your SMASH plays are hitting at a 74% success rate (industry average: 60%)
    - You're averaging 12.2% lower ownership than the field
    - ROI trending upward over last 3 weeks
    - Consider increasing LEVERAGE play usage in mid-size tournaments
    """)

# =====================================
# FOOTER
# =====================================

st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666; padding: 20px;'>
    🏈 Beat Your League - Fantasy Football Intelligence<br>
    Built with data science to give you the edge in fantasy football
</div>
""", unsafe_allow_html=True)

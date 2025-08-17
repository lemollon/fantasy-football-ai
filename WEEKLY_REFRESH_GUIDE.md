# 🏈 Fantasy Football Weekly Data Refresh Instructions

## 📋 Overview
This document explains how to refresh your fantasy football intelligence system with the latest data each week during the NFL season.

## ⏰ Weekly Schedule

### Tuesday - Rankings Update (2 minutes)
**Goal:** Get fresh expert consensus rankings for the upcoming week

### Thursday/Sunday - Ownership Update (3 minutes)  
**Goal:** Get DFS ownership data and update your live app

---

## 🔄 Tuesday: Update Expert Rankings

### Step 1: Get Fresh Rankings
1. **Go to:** [FantasyPros.com](https://www.fantasypros.com/nfl/rankings/)
2. **Navigate to:** Weekly Rankings → Week X
3. **Copy rankings for each position:**
   - Quarterbacks (Top 10)
   - Running Backs (Top 15) 
   - Wide Receivers (Top 15)
   - Tight Ends (Top 10)

### Step 2: Update Your Data
1. **Open Databricks** → Your fantasy football notebook
2. **Run this code** (replace with actual Week X data):

```python
# UPDATE EXPERT RANKINGS FOR WEEK X
import pandas as pd
from datetime import datetime

def update_week_rankings(week_number):
    """Update rankings for the specified week"""
    
    print(f"📊 Updating rankings for Week {week_number}...")
    
    # Replace this data with actual rankings from FantasyPros
    new_rankings = {
        'player_name': [
            # QBs - Replace with actual Week X rankings
            'Josh Allen', 'Lamar Jackson', 'Jalen Hurts', 'Dak Prescott', 'Joe Burrow',
            # RBs - Replace with actual Week X rankings  
            'Christian McCaffrey', 'Austin Ekeler', 'Derrick Henry', 'Jonathan Taylor', 'Saquon Barkley',
            # WRs - Replace with actual Week X rankings
            'Cooper Kupp', 'Davante Adams', 'Tyreek Hill', 'Stefon Diggs', 'CeeDee Lamb',
            # TEs - Replace with actual Week X rankings
            'Travis Kelce', 'Mark Andrews', 'George Kittle', 'T.J. Hockenson', 'Kyle Pitts'
        ],
        'position': [
            'QB', 'QB', 'QB', 'QB', 'QB',
            'RB', 'RB', 'RB', 'RB', 'RB',
            'WR', 'WR', 'WR', 'WR', 'WR', 
            'TE', 'TE', 'TE', 'TE', 'TE'
        ],
        'player_rank': [1, 2, 3, 4, 5] * 4,
        'expert_source': ['FantasyPros'] * 20,
        'tier': [1, 1, 1, 2, 2] * 4,
        'date': [datetime.now().date()] * 20,
        'week': [week_number] * 20,
        'season': [2024] * 20
    }
    
    # Create DataFrame and update table
    rankings_df = pd.DataFrame(new_rankings)
    rankings_spark = spark.createDataFrame(rankings_df)
    rankings_spark.write.mode("overwrite").saveAsTable("bronze.expert_rankings")
    
    print(f"✅ Rankings updated for Week {week_number}")
    return rankings_df

# Update for current week (change the number each week)
update_week_rankings(1)  # Change to 2, 3, 4, etc.
```

---

## 💰 Thursday/Sunday: Update Ownership & Publish

### Step 1: Get DFS Ownership Data
1. **Thursday (for TNF):** Check DraftKings ~2 hours before kickoff
2. **Sunday (main slate):** Check DraftKings ~2 hours before 1pm games
3. **Go to:** [DraftKings.com](https://www.draftkings.com/draft/nfl) 
4. **Note ownership percentages** for top players

### Step 2: Update Ownership Data
```python
# UPDATE DFS OWNERSHIP DATA
def update_ownership_data(week_number):
    """Update DFS ownership for the specified week"""
    
    print(f"💰 Updating ownership for Week {week_number}...")
    
    # Replace with actual ownership % from DraftKings
    ownership_data = {
        'player_name': [
            # Replace with actual players and ownership %
            'Josh Allen', 'Lamar Jackson', 'Christian McCaffrey', 'Austin Ekeler',
            'Cooper Kupp', 'Davante Adams', 'Travis Kelce', 'Mark Andrews'
            # Add more players as needed
        ],
        'position': ['QB', 'QB', 'RB', 'RB', 'WR', 'WR', 'TE', 'TE'],
        'ownership_percentage': [
            # Replace with actual ownership % from DraftKings
            28.5, 15.2, 31.8, 24.1, 27.3, 18.6, 35.2, 22.7
            # Add corresponding ownership percentages
        ],
        'platform': ['DraftKings'] * 8,  # Adjust count as needed
        'date': [datetime.now().date()] * 8,
        'week': [week_number] * 8,
        'season': [2024] * 8
    }
    
    # Create DataFrame and update table
    ownership_df = pd.DataFrame(ownership_data)
    ownership_spark = spark.createDataFrame(ownership_df)
    ownership_spark.write.mode("overwrite").saveAsTable("bronze.daily_ownership")
    
    print(f"✅ Ownership updated for Week {week_number}")
    return ownership_df

# Update for current week
update_ownership_data(1)  # Change to 2, 3, 4, etc.
```

### Step 3: Run Complete Update
```python
# RUN COMPLETE WEEKLY UPDATE
weekly_automation_complete()
```

This will:
- ✅ Recalculate contrarian opportunities
- ✅ Push fresh data to GitHub
- ✅ Update your Streamlit app automatically
- ✅ Generate new SMASH/LEVERAGE/CHALK recommendations

---

## 🎯 What You'll Get Each Week

After running the complete update, your app will show:
- **Fresh contrarian opportunities** for the current week
- **SMASH plays:** Elite players with low ownership
- **LEVERAGE plays:** Good players with medium ownership  
- **CHALK plays:** Popular players to avoid in tournaments
- **Updated recommendations** for lineup building

---

## 📱 Verify Your Update

1. **Go to your app:** [https://beat-your-league.streamlit.app](https://beat-your-league.streamlit.app)
2. **Refresh the page** (Ctrl+F5 or Cmd+Shift+R)
3. **Check for:**
   - Current week data
   - Fresh player names and rankings
   - Updated contrarian scores
   - New play type classifications

---

## 🚨 Troubleshooting

### If rankings update fails:
- Check that player names match exactly
- Verify data types (strings, integers, dates)
- Ensure all required columns are present

### If ownership update fails:
- Confirm ownership percentages are numbers (not strings)
- Check that player names match your rankings table
- Verify platform and date formats

### If GitHub push fails:
- Check your GitHub token is still valid
- Verify repository permissions
- Try running `automated_github_update()` again

### If Streamlit doesn't update:
- Wait 2-3 minutes for automatic refresh
- Force refresh your browser (Ctrl+F5)
- Check GitHub to confirm new data was pushed

---

## 📋 Weekly Checklist

**Tuesday:**
- [ ] Get Week X rankings from FantasyPros
- [ ] Update `bronze.expert_rankings` table
- [ ] Verify update completed successfully

**Thursday/Sunday:**
- [ ] Get DFS ownership from DraftKings  
- [ ] Update `bronze.daily_ownership` table
- [ ] Run `weekly_automation_complete()`
- [ ] Verify Streamlit app updated
- [ ] Check contrarian opportunities
- [ ] Share insights with league (optional)

---

## 💡 Pro Tips

1. **Bookmark key pages:** FantasyPros rankings, DraftKings ownership
2. **Set calendar reminders:** Tuesday 9am (rankings), Sunday 11am (ownership)
3. **Screenshot ownership:** DFS ownership changes quickly, grab screenshots
4. **Test early:** Run updates Tuesday after getting rankings to catch issues early
5. **Backup data:** Your bronze tables contain your historical analysis

---

## 🏆 Competitive Advantage

By following this process, you'll have:
- **Fresher data** than friends using basic rankings
- **Contrarian insights** others don't have access to
- **Automated analysis** updating your live app
- **Professional-grade** fantasy intelligence system

**Total time investment: 5 minutes per week for a massive competitive edge!**

---

*Last updated: August 2024*
*For technical support or updates to this process, refer to your Databricks notebooks.*

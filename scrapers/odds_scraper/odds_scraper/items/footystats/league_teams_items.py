from scrapy import Item, Field
from scrapy.loader import ItemLoader
from itemloaders.processors import MapCompose, TakeFirst, Identity
from datetime import datetime

def clean_string(value):
    """Clean and strip string values"""
    if isinstance(value, str):
        return value.strip()
    return value

def safe_int(value):
    """Safely convert to integer"""
    try:
        return int(value) if value is not None else None
    except (ValueError, TypeError):
        return None

def safe_float(value):
    """Safely convert to float"""
    try:
        return float(value) if value is not None else None
    except (ValueError, TypeError):
        return None

class LeagueTeamItem(Item):
    """
    Comprehensive item for FootyStats /league-teams endpoint
    
    Based on actual JSON structure with exact field names matching the API response.
    Captures 700+ statistical fields when include=stats parameter is used.
    """
    
    # ===== BASIC TEAM INFORMATION =====
    id = Field()                                    # Team ID
    name = Field()                                  # Full team name
    cleanName = Field()                             # Clean team name for matching
    shortName = Field()                             # Short team name (if available)
    image = Field()                                 # Team logo URL
    flag_element = Field()                          # Flag element
    season = Field()                                # Season string (e.g., "2019/2020")
    seasonClean = Field()                           # Clean season
    url = Field()                                   # FootyStats team URL
    table_position = Field()                        # League table position
    performance_rank = Field()                      # Performance ranking
    risk = Field()                                  # Risk rating
    season_format = Field()                         # Season format (e.g., "Domestic League")
    competition_id = Field()                        # Competition ID
    full_name = Field()                             # Full official team name
    alt_names = Field()                             # Alternative names (array)
    official_sites = Field()                        # Official websites (array)
    
    # ===== CORE SEASON STATISTICS (from stats object) =====
    # Previous seasons data
    previous_seasons = Field()                      # Previous seasons array
    suspended_matches = Field()                     # Suspended matches count
    
    # Home advantage statistics
    homeAttackAdvantage = Field()                   # Home attack advantage
    homeDefenceAdvantage = Field()                  # Home defence advantage  
    homeOverallAdvantage = Field()                  # Overall home advantage
    
    # ===== GOAL STATISTICS =====
    # Season goal totals
    seasonGoals_overall = Field()                   # Total goals scored this season
    seasonGoals_home = Field()                      # Goals scored at home (array of minute strings)
    seasonGoals_away = Field()                      # Goals scored away (array of minute strings)
    seasonConceded_overall = Field()                # Total goals conceded this season
    seasonConceded_home = Field()                   # Goals conceded at home (array of minute strings)
    seasonConceded_away = Field()                   # Goals conceded away (array of minute strings)
    
    # Season goal totals by venue
    seasonGoalsTotal_overall = Field()              # Total goals in all matches
    seasonGoalsTotal_home = Field()                 # Total goals in home matches
    seasonGoalsTotal_away = Field()                 # Total goals in away matches
    
    # Goal counts by type
    seasonScoredNum_overall = Field()               # Number of goals scored overall
    seasonScoredNum_home = Field()                  # Number of goals scored at home
    seasonScoredNum_away = Field()                  # Number of goals scored away
    seasonConcededNum_overall = Field()             # Number of goals conceded overall
    seasonConcededNum_home = Field()                # Number of goals conceded at home
    seasonConcededNum_away = Field()                # Number of goals conceded away
    
    # Goal timing statistics
    seasonGoalsMin_overall = Field()                # Average minute of goals scored overall
    seasonGoalsMin_home = Field()                   # Average minute of goals scored at home
    seasonGoalsMin_away = Field()                   # Average minute of goals scored away
    seasonScoredMin_overall = Field()               # Average minute when team scores overall
    seasonScoredMin_home = Field()                  # Average minute when team scores at home
    seasonScoredMin_away = Field()                  # Average minute when team scores away
    seasonConcededMin_overall = Field()             # Average minute when team concedes overall
    seasonConcededMin_home = Field()                # Average minute when team concedes at home
    seasonConcededMin_away = Field()                # Average minute when team concedes away
    
    # Goal differences
    seasonGoalDifference_overall = Field()          # Goal difference overall
    seasonGoalDifference_home = Field()             # Goal difference at home
    seasonGoalDifference_away = Field()             # Goal difference away
    
    # Highest scoring statistics
    seasonHighestScored_home = Field()              # Highest goals scored in home match
    seasonHighestConceded_home = Field()            # Most goals conceded in home match
    seasonHighestScored_away = Field()              # Highest goals scored in away match
    seasonHighestConceded_away = Field()            # Most goals conceded in away match
    
    # ===== WIN/DRAW/LOSS STATISTICS =====
    seasonWinsNum_overall = Field()                 # Total wins
    seasonWinsNum_home = Field()                    # Wins at home
    seasonWinsNum_away = Field()                    # Wins away
    seasonDrawsNum_overall = Field()                # Total draws
    seasonDrawsNum_home = Field()                   # Draws at home
    seasonDrawsNum_away = Field()                   # Draws away
    seasonLossesNum_overall = Field()               # Total losses
    seasonLossesNum_home = Field()                  # Losses at home
    seasonLossesNum_away = Field()                  # Losses away
    
    # Matches played
    seasonMatchesPlayed_overall = Field()           # Total matches played
    seasonMatchesPlayed_home = Field()              # Matches played at home
    seasonMatchesPlayed_away = Field()              # Matches played away
    
    # ===== CLEAN SHEET STATISTICS =====
    seasonCS_overall = Field()                      # Clean sheets overall
    seasonCS_home = Field()                         # Clean sheets at home
    seasonCS_away = Field()                         # Clean sheets away
    seasonCSPercentage_overall = Field()            # Clean sheet percentage overall
    seasonCSPercentage_home = Field()               # Clean sheet percentage at home
    seasonCSPercentage_away = Field()               # Clean sheet percentage away
    
    # Halftime clean sheets
    seasonCSHT_overall = Field()                    # Halftime clean sheets overall
    seasonCSHT_home = Field()                       # Halftime clean sheets at home
    seasonCSHT_away = Field()                       # Halftime clean sheets away
    seasonCSPercentageHT_overall = Field()          # Halftime clean sheet percentage overall
    seasonCSPercentageHT_home = Field()             # Halftime clean sheet percentage at home
    seasonCSPercentageHT_away = Field()             # Halftime clean sheet percentage away
    
    # ===== FAILED TO SCORE STATISTICS =====
    seasonFTS_overall = Field()                     # Failed to score matches overall
    seasonFTS_home = Field()                        # Failed to score matches at home
    seasonFTS_away = Field()                        # Failed to score matches away
    seasonFTSPercentage_overall = Field()           # Failed to score percentage overall
    seasonFTSPercentage_home = Field()              # Failed to score percentage at home
    seasonFTSPercentage_away = Field()              # Failed to score percentage away
    
    # Halftime failed to score
    seasonFTSHT_overall = Field()                   # Halftime failed to score overall
    seasonFTSHT_home = Field()                      # Halftime failed to score at home
    seasonFTSHT_away = Field()                      # Halftime failed to score away
    seasonFTSPercentageHT_overall = Field()         # Halftime FTS percentage overall
    seasonFTSPercentageHT_home = Field()            # Halftime FTS percentage at home
    seasonFTSPercentageHT_away = Field()            # Halftime FTS percentage away
    
    # ===== BOTH TEAMS TO SCORE (BTTS) STATISTICS =====
    seasonBTTS_overall = Field()                    # BTTS matches overall
    seasonBTTS_home = Field()                       # BTTS matches at home
    seasonBTTS_away = Field()                       # BTTS matches away
    seasonBTTSPercentage_overall = Field()          # BTTS percentage overall
    seasonBTTSPercentage_home = Field()             # BTTS percentage at home
    seasonBTTSPercentage_away = Field()             # BTTS percentage away
    
    # Halftime BTTS
    seasonBTTSHT_overall = Field()                  # Halftime BTTS overall
    seasonBTTSHT_home = Field()                     # Halftime BTTS at home
    seasonBTTSHT_away = Field()                     # Halftime BTTS away
    seasonBTTSPercentageHT_overall = Field()        # Halftime BTTS percentage overall
    seasonBTTSPercentageHT_home = Field()           # Halftime BTTS percentage at home
    seasonBTTSPercentageHT_away = Field()           # Halftime BTTS percentage away
    
    # ===== POINTS PER GAME STATISTICS =====
    seasonPPG_overall = Field()                     # Points per game overall
    seasonPPG_home = Field()                        # Points per game at home
    seasonPPG_away = Field()                        # Points per game away
    seasonRecentPPG = Field()                       # Recent points per game
    
    # Current form
    currentFormHome = Field()                       # Current home form
    currentFormAway = Field()                       # Current away form
    
    # ===== GOAL AVERAGES =====
    seasonAVG_overall = Field()                     # Average total goals per match overall
    seasonAVG_home = Field()                        # Average total goals per match at home
    seasonAVG_away = Field()                        # Average total goals per match away
    seasonScoredAVG_overall = Field()               # Average goals scored per match overall
    seasonScoredAVG_home = Field()                  # Average goals scored per match at home
    seasonScoredAVG_away = Field()                  # Average goals scored per match away
    seasonConcededAVG_overall = Field()             # Average goals conceded per match overall
    seasonConcededAVG_home = Field()                # Average goals conceded per match at home
    seasonConcededAVG_away = Field()                # Average goals conceded per match away
    
    # ===== WIN/DRAW/LOSS PERCENTAGES =====
    winPercentage_overall = Field()                 # Win percentage overall
    winPercentage_home = Field()                    # Win percentage at home
    winPercentage_away = Field()                    # Win percentage away
    drawPercentage_overall = Field()                # Draw percentage overall
    drawPercentage_home = Field()                   # Draw percentage at home
    drawPercentage_away = Field()                   # Draw percentage away
    losePercentage_overall = Field()                # Loss percentage overall
    losePercentage_home = Field()                   # Loss percentage at home
    losePercentage_away = Field()                   # Loss percentage away

    # ===== HALFTIME POSITION STATISTICS =====
    leadingAtHT_overall = Field()                   # Leading at halftime overall
    leadingAtHT_home = Field()                      # Leading at halftime at home
    leadingAtHT_away = Field()                      # Leading at halftime away
    leadingAtHTPercentage_overall = Field()         # Leading at halftime percentage overall
    leadingAtHTPercentage_home = Field()            # Leading at halftime percentage at home
    leadingAtHTPercentage_away = Field()            # Leading at halftime percentage away
    
    drawingAtHT_overall = Field()                   # Drawing at halftime overall
    drawingAtHT_home = Field()                      # Drawing at halftime at home
    drawingAtHT_away = Field()                      # Drawing at halftime away
    drawingAtHTPercentage_overall = Field()         # Drawing at halftime percentage overall
    drawingAtHTPercentage_home = Field()            # Drawing at halftime percentage at home
    drawingAtHTPercentage_away = Field()            # Drawing at halftime percentage away
    
    trailingAtHT_overall = Field()                  # Trailing at halftime overall
    trailingAtHT_home = Field()                     # Trailing at halftime at home
    trailingAtHT_away = Field()                     # Trailing at halftime away
    trailingAtHTPercentage_overall = Field()        # Trailing at halftime percentage overall
    trailingAtHTPercentage_home = Field()           # Trailing at halftime percentage at home
    trailingAtHTPercentage_away = Field()           # Trailing at halftime percentage away
    
    # ===== HALFTIME POINTS AND AVERAGES =====
    HTPoints_overall = Field()                      # Halftime points overall
    HTPoints_home = Field()                         # Halftime points at home
    HTPoints_away = Field()                         # Halftime points away
    HTPPG_overall = Field()                         # Halftime points per game overall
    HTPPG_home = Field()                            # Halftime points per game at home
    HTPPG_away = Field()                            # Halftime points per game away
    
    # Halftime goal averages
    scoredAVGHT_overall = Field()                   # Average goals scored at halftime overall
    scoredAVGHT_home = Field()                      # Average goals scored at halftime at home
    scoredAVGHT_away = Field()                      # Average goals scored at halftime away
    concededAVGHT_overall = Field()                 # Average goals conceded at halftime overall
    concededAVGHT_home = Field()                    # Average goals conceded at halftime at home
    concededAVGHT_away = Field()                    # Average goals conceded at halftime away
    AVGHT_overall = Field()                         # Average total goals at halftime overall
    AVGHT_home = Field()                            # Average total goals at halftime at home
    AVGHT_away = Field()                            # Average total goals at halftime away
    
    # ===== HALFTIME GOAL COUNTS =====
    scoredGoalsHT_overall = Field()                 # Goals scored at halftime overall
    scoredGoalsHT_home = Field()                    # Goals scored at halftime at home
    scoredGoalsHT_away = Field()                    # Goals scored at halftime away
    concededGoalsHT_overall = Field()               # Goals conceded at halftime overall
    concededGoalsHT_home = Field()                  # Goals conceded at halftime at home
    concededGoalsHT_away = Field()                  # Goals conceded at halftime away
    GoalsHT_overall = Field()                       # Total goals at halftime overall
    GoalsHT_home = Field()                          # Total goals at halftime at home
    GoalsHT_away = Field()                          # Total goals at halftime away
    GoalDifferenceHT_overall = Field()              # Goal difference at halftime overall
    GoalDifferenceHT_home = Field()                 # Goal difference at halftime at home
    GoalDifferenceHT_away = Field()                 # Goal difference at halftime away
    
    # ===== OVER/UNDER GOAL STATISTICS - COUNTS =====
    # Over 0.5 goals
    seasonOver05Num_overall = Field()               # Over 0.5 goals matches overall
    seasonOver05Num_home = Field()                  # Over 0.5 goals matches at home
    seasonOver05Num_away = Field()                  # Over 0.5 goals matches away
    seasonOver05Percentage_overall = Field()        # Over 0.5 goals percentage overall
    seasonOver05Percentage_home = Field()           # Over 0.5 goals percentage at home
    seasonOver05Percentage_away = Field()           # Over 0.5 goals percentage away
    
    # Over 1.5 goals
    seasonOver15Num_overall = Field()               # Over 1.5 goals matches overall
    seasonOver15Num_home = Field()                  # Over 1.5 goals matches at home
    seasonOver15Num_away = Field()                  # Over 1.5 goals matches away
    seasonOver15Percentage_overall = Field()        # Over 1.5 goals percentage overall
    seasonOver15Percentage_home = Field()           # Over 1.5 goals percentage at home
    seasonOver15Percentage_away = Field()           # Over 1.5 goals percentage away
    
    # Over 2.5 goals
    seasonOver25Num_overall = Field()               # Over 2.5 goals matches overall
    seasonOver25Num_home = Field()                  # Over 2.5 goals matches at home
    seasonOver25Num_away = Field()                  # Over 2.5 goals matches away
    seasonOver25Percentage_overall = Field()        # Over 2.5 goals percentage overall
    seasonOver25Percentage_home = Field()           # Over 2.5 goals percentage at home
    seasonOver25Percentage_away = Field()           # Over 2.5 goals percentage away
    
    # Over 3.5 goals
    seasonOver35Num_overall = Field()               # Over 3.5 goals matches overall
    seasonOver35Num_home = Field()                  # Over 3.5 goals matches at home
    seasonOver35Num_away = Field()                  # Over 3.5 goals matches away
    seasonOver35Percentage_overall = Field()        # Over 3.5 goals percentage overall
    seasonOver35Percentage_home = Field()           # Over 3.5 goals percentage at home
    seasonOver35Percentage_away = Field()           # Over 3.5 goals percentage away
    
    # Over 4.5 goals
    seasonOver45Num_overall = Field()               # Over 4.5 goals matches overall
    seasonOver45Num_home = Field()                  # Over 4.5 goals matches at home
    seasonOver45Num_away = Field()                  # Over 4.5 goals matches away
    seasonOver45Percentage_overall = Field()        # Over 4.5 goals percentage overall
    seasonOver45Percentage_home = Field()           # Over 4.5 goals percentage at home
    seasonOver45Percentage_away = Field()           # Over 4.5 goals percentage away
    
    # Over 5.5 goals
    seasonOver55Num_overall = Field()               # Over 5.5 goals matches overall
    seasonOver55Num_home = Field()                  # Over 5.5 goals matches at home
    seasonOver55Num_away = Field()                  # Over 5.5 goals matches away
    seasonOver55Percentage_overall = Field()        # Over 5.5 goals percentage overall
    seasonOver55Percentage_home = Field()           # Over 5.5 goals percentage at home
    seasonOver55Percentage_away = Field()           # Over 5.5 goals percentage away
    
    # ===== UNDER GOAL STATISTICS - COUNTS =====
    # Under 0.5 goals
    seasonUnder05Num_overall = Field()              # Under 0.5 goals matches overall
    seasonUnder05Num_home = Field()                 # Under 0.5 goals matches at home
    seasonUnder05Num_away = Field()                 # Under 0.5 goals matches away
    seasonUnder05Percentage_overall = Field()       # Under 0.5 goals percentage overall
    seasonUnder05Percentage_home = Field()          # Under 0.5 goals percentage at home
    seasonUnder05Percentage_away = Field()          # Under 0.5 goals percentage away
    
    # Under 1.5 goals
    seasonUnder15Num_overall = Field()              # Under 1.5 goals matches overall
    seasonUnder15Num_home = Field()                 # Under 1.5 goals matches at home
    seasonUnder15Num_away = Field()                 # Under 1.5 goals matches away
    seasonUnder15Percentage_overall = Field()       # Under 1.5 goals percentage overall
    seasonUnder15Percentage_home = Field()          # Under 1.5 goals percentage at home
    seasonUnder15Percentage_away = Field()          # Under 1.5 goals percentage away
    
    # Under 2.5 goals
    seasonUnder25Num_overall = Field()              # Under 2.5 goals matches overall
    seasonUnder25Num_home = Field()                 # Under 2.5 goals matches at home
    seasonUnder25Num_away = Field()                 # Under 2.5 goals matches away
    seasonUnder25Percentage_overall = Field()       # Under 2.5 goals percentage overall
    seasonUnder25Percentage_home = Field()          # Under 2.5 goals percentage at home
    seasonUnder25Percentage_away = Field()          # Under 2.5 goals percentage away
    
    # Under 3.5 goals
    seasonUnder35Num_overall = Field()              # Under 3.5 goals matches overall
    seasonUnder35Num_home = Field()                 # Under 3.5 goals matches at home
    seasonUnder35Num_away = Field()                 # Under 3.5 goals matches away
    seasonUnder35Percentage_overall = Field()       # Under 3.5 goals percentage overall
    seasonUnder35Percentage_home = Field()          # Under 3.5 goals percentage at home
    seasonUnder35Percentage_away = Field()          # Under 3.5 goals percentage away
    
    # Under 4.5 goals
    seasonUnder45Num_overall = Field()              # Under 4.5 goals matches overall
    seasonUnder45Num_home = Field()                 # Under 4.5 goals matches at home
    seasonUnder45Num_away = Field()                 # Under 4.5 goals matches away
    seasonUnder45Percentage_overall = Field()       # Under 4.5 goals percentage overall
    seasonUnder45Percentage_home = Field()          # Under 4.5 goals percentage at home
    seasonUnder45Percentage_away = Field()          # Under 4.5 goals percentage away
    
    # Under 5.5 goals
    seasonUnder55Num_overall = Field()              # Under 5.5 goals matches overall
    seasonUnder55Num_home = Field()                 # Under 5.5 goals matches at home
    seasonUnder55Num_away = Field()                 # Under 5.5 goals matches away
    seasonUnder55Percentage_overall = Field()       # Under 5.5 goals percentage overall
    seasonUnder55Percentage_home = Field()          # Under 5.5 goals percentage at home
    seasonUnder55Percentage_away = Field()          # Under 5.5 goals percentage away

    # ===== HALFTIME OVER/UNDER GOAL STATISTICS =====
    # Over 0.5 goals at halftime
    seasonOver05NumHT_overall = Field()             # Over 0.5 goals at halftime overall
    seasonOver05NumHT_home = Field()                # Over 0.5 goals at halftime at home
    seasonOver05NumHT_away = Field()                # Over 0.5 goals at halftime away
    seasonOver05PercentageHT_overall = Field()      # Over 0.5 goals at halftime percentage overall
    seasonOver05PercentageHT_home = Field()         # Over 0.5 goals at halftime percentage at home
    seasonOver05PercentageHT_away = Field()         # Over 0.5 goals at halftime percentage away
    
    # Over 1.5 goals at halftime
    seasonOver15NumHT_overall = Field()             # Over 1.5 goals at halftime overall
    seasonOver15NumHT_home = Field()                # Over 1.5 goals at halftime at home
    seasonOver15NumHT_away = Field()                # Over 1.5 goals at halftime away
    seasonOver15PercentageHT_overall = Field()      # Over 1.5 goals at halftime percentage overall
    seasonOver15PercentageHT_home = Field()         # Over 1.5 goals at halftime percentage at home
    seasonOver15PercentageHT_away = Field()         # Over 1.5 goals at halftime percentage away
    
    # Over 2.5 goals at halftime
    seasonOver25NumHT_overall = Field()             # Over 2.5 goals at halftime overall
    seasonOver25NumHT_home = Field()                # Over 2.5 goals at halftime at home
    seasonOver25NumHT_away = Field()                # Over 2.5 goals at halftime away
    seasonOver25PercentageHT_overall = Field()      # Over 2.5 goals at halftime percentage overall
    seasonOver25PercentageHT_home = Field()         # Over 2.5 goals at halftime percentage at home
    seasonOver25PercentageHT_away = Field()         # Over 2.5 goals at halftime percentage away
    
    # ===== CORNER STATISTICS =====
    cornersRecorded_matches_overall = Field()       # Matches with corner data overall
    cornersRecorded_matches_home = Field()          # Matches with corner data at home
    cornersRecorded_matches_away = Field()          # Matches with corner data away
    cornersAVG_overall = Field()                    # Average corners per match overall
    cornersAVG_home = Field()                       # Average corners per match at home
    cornersAVG_away = Field()                       # Average corners per match away
    cornersTotal_overall = Field()                  # Total corners overall
    cornersTotal_home = Field()                     # Total corners at home
    cornersTotal_away = Field()                     # Total corners away
    
    # Corner over statistics
    over65Corners_overall = Field()                 # Over 6.5 corners overall
    over65Corners_home = Field()                    # Over 6.5 corners at home
    over65Corners_away = Field()                    # Over 6.5 corners away
    over65CornersPercentage_overall = Field()       # Over 6.5 corners percentage overall
    over65CornersPercentage_home = Field()          # Over 6.5 corners percentage at home
    over65CornersPercentage_away = Field()          # Over 6.5 corners percentage away
    
    over75Corners_overall = Field()                 # Over 7.5 corners overall
    over75Corners_home = Field()                    # Over 7.5 corners at home
    over75Corners_away = Field()                    # Over 7.5 corners away
    over75CornersPercentage_overall = Field()       # Over 7.5 corners percentage overall
    over75CornersPercentage_home = Field()          # Over 7.5 corners percentage at home
    over75CornersPercentage_away = Field()          # Over 7.5 corners percentage away
    
    over85Corners_overall = Field()                 # Over 8.5 corners overall
    over85Corners_home = Field()                    # Over 8.5 corners at home
    over85Corners_away = Field()                    # Over 8.5 corners away
    over85CornersPercentage_overall = Field()       # Over 8.5 corners percentage overall
    over85CornersPercentage_home = Field()          # Over 8.5 corners percentage at home
    over85CornersPercentage_away = Field()          # Over 8.5 corners percentage away
    
    over95Corners_overall = Field()                 # Over 9.5 corners overall
    over95Corners_home = Field()                    # Over 9.5 corners at home
    over95Corners_away = Field()                    # Over 9.5 corners away
    over95CornersPercentage_overall = Field()       # Over 9.5 corners percentage overall
    over95CornersPercentage_home = Field()          # Over 9.5 corners percentage at home
    over95CornersPercentage_away = Field()          # Over 9.5 corners percentage away
    
    over105Corners_overall = Field()                # Over 10.5 corners overall
    over105Corners_home = Field()                   # Over 10.5 corners at home
    over105Corners_away = Field()                   # Over 10.5 corners away
    over105CornersPercentage_overall = Field()      # Over 10.5 corners percentage overall
    over105CornersPercentage_home = Field()         # Over 10.5 corners percentage at home
    over105CornersPercentage_away = Field()         # Over 10.5 corners percentage away
    
    over115Corners_overall = Field()                # Over 11.5 corners overall
    over115Corners_home = Field()                   # Over 11.5 corners at home
    over115Corners_away = Field()                   # Over 11.5 corners away
    over115CornersPercentage_overall = Field()      # Over 11.5 corners percentage overall
    over115CornersPercentage_home = Field()         # Over 11.5 corners percentage at home
    over115CornersPercentage_away = Field()         # Over 11.5 corners percentage away
    
    over125Corners_overall = Field()                # Over 12.5 corners overall
    over125Corners_home = Field()                   # Over 12.5 corners at home
    over125Corners_away = Field()                   # Over 12.5 corners away
    over125CornersPercentage_overall = Field()      # Over 12.5 corners percentage overall
    over125CornersPercentage_home = Field()         # Over 12.5 corners percentage at home
    over125CornersPercentage_away = Field()         # Over 12.5 corners percentage away
    
    over135Corners_overall = Field()                # Over 13.5 corners overall
    over135Corners_home = Field()                   # Over 13.5 corners at home
    over135Corners_away = Field()                   # Over 13.5 corners away
    over135CornersPercentage_overall = Field()      # Over 13.5 corners percentage overall
    over135CornersPercentage_home = Field()         # Over 13.5 corners percentage at home
    over135CornersPercentage_away = Field()         # Over 13.5 corners percentage away
    
    over145Corners_overall = Field()                # Over 14.5 corners overall
    over145Corners_home = Field()                   # Over 14.5 corners at home
    over145Corners_away = Field()                   # Over 14.5 corners away
    over145CornersPercentage_overall = Field()      # Over 14.5 corners percentage overall
    over145CornersPercentage_home = Field()         # Over 14.5 corners percentage at home
    over145CornersPercentage_away = Field()         # Over 14.5 corners percentage away
    
    # Corner under statistics
    under65Corners_overall = Field()                # Under 6.5 corners overall
    under65Corners_home = Field()                   # Under 6.5 corners at home
    under65Corners_away = Field()                   # Under 6.5 corners away
    under65CornersPercentage_overall = Field()      # Under 6.5 corners percentage overall
    under65CornersPercentage_home = Field()         # Under 6.5 corners percentage at home
    under65CornersPercentage_away = Field()         # Under 6.5 corners percentage away
    
    under75Corners_overall = Field()                # Under 7.5 corners overall
    under75Corners_home = Field()                   # Under 7.5 corners at home
    under75Corners_away = Field()                   # Under 7.5 corners away
    under75CornersPercentage_overall = Field()      # Under 7.5 corners percentage overall
    under75CornersPercentage_home = Field()         # Under 7.5 corners percentage at home
    under75CornersPercentage_away = Field()         # Under 7.5 corners percentage away
    
    under85Corners_overall = Field()                # Under 8.5 corners overall
    under85Corners_home = Field()                   # Under 8.5 corners at home
    under85Corners_away = Field()                   # Under 8.5 corners away
    under85CornersPercentage_overall = Field()      # Under 8.5 corners percentage overall
    under85CornersPercentage_home = Field()         # Under 8.5 corners percentage at home
    under85CornersPercentage_away = Field()         # Under 8.5 corners percentage away
    
    under95Corners_overall = Field()                # Under 9.5 corners overall
    under95Corners_home = Field()                   # Under 9.5 corners at home
    under95Corners_away = Field()                   # Under 9.5 corners away
    under95CornersPercentage_overall = Field()      # Under 9.5 corners percentage overall
    under95CornersPercentage_home = Field()         # Under 9.5 corners percentage at home
    under95CornersPercentage_away = Field()         # Under 9.5 corners percentage away
    
    under105Corners_overall = Field()               # Under 10.5 corners overall
    under105Corners_home = Field()                  # Under 10.5 corners at home
    under105Corners_away = Field()                  # Under 10.5 corners away
    under105CornersPercentage_overall = Field()     # Under 10.5 corners percentage overall
    under105CornersPercentage_home = Field()        # Under 10.5 corners percentage at home
    under105CornersPercentage_away = Field()        # Under 10.5 corners percentage away
    
    under115Corners_overall = Field()               # Under 11.5 corners overall
    under115Corners_home = Field()                  # Under 11.5 corners at home
    under115Corners_away = Field()                  # Under 11.5 corners away
    under115CornersPercentage_overall = Field()     # Under 11.5 corners percentage overall
    under115CornersPercentage_home = Field()        # Under 11.5 corners percentage at home
    under115CornersPercentage_away = Field()        # Under 11.5 corners percentage away
    
    under125Corners_overall = Field()               # Under 12.5 corners overall
    under125Corners_home = Field()                  # Under 12.5 corners at home
    under125Corners_away = Field()                  # Under 12.5 corners away
    under125CornersPercentage_overall = Field()     # Under 12.5 corners percentage overall
    under125CornersPercentage_home = Field()        # Under 12.5 corners percentage at home
    under125CornersPercentage_away = Field()        # Under 12.5 corners percentage away
    
    under135Corners_overall = Field()               # Under 13.5 corners overall
    under135Corners_home = Field()                  # Under 13.5 corners at home
    under135Corners_away = Field()                  # Under 13.5 corners away
    under135CornersPercentage_overall = Field()     # Under 13.5 corners percentage overall
    under135CornersPercentage_home = Field()        # Under 13.5 corners percentage at home
    under135CornersPercentage_away = Field()        # Under 13.5 corners percentage away
    
    under145Corners_overall = Field()               # Under 14.5 corners overall
    under145Corners_home = Field()                  # Under 14.5 corners at home
    under145Corners_away = Field()                  # Under 14.5 corners away
    under145CornersPercentage_overall = Field()     # Under 14.5 corners percentage overall
    under145CornersPercentage_home = Field()        # Under 14.5 corners percentage at home
    under145CornersPercentage_away = Field()        # Under 14.5 corners percentage away
    
    # ===== CORNER FIRST TEAM STATISTICS =====
    cornerFirstTeam_overall = Field()               # First corner for team overall
    cornerFirstTeam_home = Field()                  # First corner for team at home
    cornerFirstTeam_away = Field()                  # First corner for team away
    cornerFirstTeamPercentage_overall = Field()     # First corner for team percentage overall
    cornerFirstTeamPercentage_home = Field()        # First corner for team percentage at home
    cornerFirstTeamPercentage_away = Field()        # First corner for team percentage away
    
    cornerFirstOpp_overall = Field()                # First corner for opponent overall
    cornerFirstOpp_home = Field()                   # First corner for opponent at home
    cornerFirstOpp_away = Field()                   # First corner for opponent away
    cornerFirstOppPercentage_overall = Field()      # First corner for opponent percentage overall
    cornerFirstOppPercentage_home = Field()         # First corner for opponent percentage at home
    cornerFirstOppPercentage_away = Field()         # First corner for opponent percentage away

    # ===== CARD STATISTICS =====
    cardsRecorded_matches_overall = Field()         # Matches with card data overall
    cardsRecorded_matches_home = Field()            # Matches with card data at home
    cardsRecorded_matches_away = Field()            # Matches with card data away
    cardsAVG_overall = Field()                      # Average cards per match overall
    cardsAVG_home = Field()                         # Average cards per match at home
    cardsAVG_away = Field()                         # Average cards per match away
    cardsTotal_overall = Field()                    # Total cards overall
    cardsTotal_home = Field()                       # Total cards at home
    cardsTotal_away = Field()                       # Total cards away
    
    # Card over statistics
    over15Cards_overall = Field()                   # Over 1.5 cards overall
    over15Cards_home = Field()                      # Over 1.5 cards at home
    over15Cards_away = Field()                      # Over 1.5 cards away
    over15CardsPercentage_overall = Field()         # Over 1.5 cards percentage overall
    over15CardsPercentage_home = Field()            # Over 1.5 cards percentage at home
    over15CardsPercentage_away = Field()            # Over 1.5 cards percentage away
    
    over25Cards_overall = Field()                   # Over 2.5 cards overall
    over25Cards_home = Field()                      # Over 2.5 cards at home
    over25Cards_away = Field()                      # Over 2.5 cards away
    over25CardsPercentage_overall = Field()         # Over 2.5 cards percentage overall
    over25CardsPercentage_home = Field()            # Over 2.5 cards percentage at home
    over25CardsPercentage_away = Field()            # Over 2.5 cards percentage away
    
    over35Cards_overall = Field()                   # Over 3.5 cards overall
    over35Cards_home = Field()                      # Over 3.5 cards at home
    over35Cards_away = Field()                      # Over 3.5 cards away
    over35CardsPercentage_overall = Field()         # Over 3.5 cards percentage overall
    over35CardsPercentage_home = Field()            # Over 3.5 cards percentage at home
    over35CardsPercentage_away = Field()            # Over 3.5 cards percentage away
    
    over45Cards_overall = Field()                   # Over 4.5 cards overall
    over45Cards_home = Field()                      # Over 4.5 cards at home
    over45Cards_away = Field()                      # Over 4.5 cards away
    over45CardsPercentage_overall = Field()         # Over 4.5 cards percentage overall
    over45CardsPercentage_home = Field()            # Over 4.5 cards percentage at home
    over45CardsPercentage_away = Field()            # Over 4.5 cards percentage away
    
    over55Cards_overall = Field()                   # Over 5.5 cards overall
    over55Cards_home = Field()                      # Over 5.5 cards at home
    over55Cards_away = Field()                      # Over 5.5 cards away
    over55CardsPercentage_overall = Field()         # Over 5.5 cards percentage overall
    over55CardsPercentage_home = Field()            # Over 5.5 cards percentage at home
    over55CardsPercentage_away = Field()            # Over 5.5 cards percentage away
    
    # Card under statistics
    under15Cards_overall = Field()                  # Under 1.5 cards overall
    under15Cards_home = Field()                     # Under 1.5 cards at home
    under15Cards_away = Field()                     # Under 1.5 cards away
    under15CardsPercentage_overall = Field()        # Under 1.5 cards percentage overall
    under15CardsPercentage_home = Field()           # Under 1.5 cards percentage at home
    under15CardsPercentage_away = Field()           # Under 1.5 cards percentage away
    
    under25Cards_overall = Field()                  # Under 2.5 cards overall
    under25Cards_home = Field()                     # Under 2.5 cards at home
    under25Cards_away = Field()                     # Under 2.5 cards away
    under25CardsPercentage_overall = Field()        # Under 2.5 cards percentage overall
    under25CardsPercentage_home = Field()           # Under 2.5 cards percentage at home
    under25CardsPercentage_away = Field()           # Under 2.5 cards percentage away
    
    under35Cards_overall = Field()                  # Under 3.5 cards overall
    under35Cards_home = Field()                     # Under 3.5 cards at home
    under35Cards_away = Field()                     # Under 3.5 cards away
    under35CardsPercentage_overall = Field()        # Under 3.5 cards percentage overall
    under35CardsPercentage_home = Field()           # Under 3.5 cards percentage at home
    under35CardsPercentage_away = Field()           # Under 3.5 cards percentage away
    
    under45Cards_overall = Field()                  # Under 4.5 cards overall
    under45Cards_home = Field()                     # Under 4.5 cards at home
    under45Cards_away = Field()                     # Under 4.5 cards away
    under45CardsPercentage_overall = Field()        # Under 4.5 cards percentage overall
    under45CardsPercentage_home = Field()           # Under 4.5 cards percentage at home
    under45CardsPercentage_away = Field()           # Under 4.5 cards percentage away
    
    under55Cards_overall = Field()                  # Under 5.5 cards overall
    under55Cards_home = Field()                     # Under 5.5 cards at home
    under55Cards_away = Field()                     # Under 5.5 cards away
    under55CardsPercentage_overall = Field()        # Under 5.5 cards percentage overall
    under55CardsPercentage_home = Field()           # Under 5.5 cards percentage at home
    under55CardsPercentage_away = Field()           # Under 5.5 cards percentage away
    
    # ===== GOAL TIMING STATISTICS BY MINUTE INTERVALS =====
    # Goals scored by time intervals (0-10, 11-20, 21-30, 31-40, 41-50, 51-60, 61-70, 71-80, 81-90)
    goals_0_10_num_overall = Field()                # Goals scored 0-10 minutes overall
    goals_0_10_num_home = Field()                   # Goals scored 0-10 minutes at home
    goals_0_10_num_away = Field()                   # Goals scored 0-10 minutes away
    goals_0_10_percentage_overall = Field()         # Goals scored 0-10 minutes percentage overall
    goals_0_10_percentage_home = Field()            # Goals scored 0-10 minutes percentage at home
    goals_0_10_percentage_away = Field()            # Goals scored 0-10 minutes percentage away
    
    goals_11_20_num_overall = Field()               # Goals scored 11-20 minutes overall
    goals_11_20_num_home = Field()                  # Goals scored 11-20 minutes at home
    goals_11_20_num_away = Field()                  # Goals scored 11-20 minutes away
    goals_11_20_percentage_overall = Field()        # Goals scored 11-20 minutes percentage overall
    goals_11_20_percentage_home = Field()           # Goals scored 11-20 minutes percentage at home
    goals_11_20_percentage_away = Field()           # Goals scored 11-20 minutes percentage away
    
    goals_21_30_num_overall = Field()               # Goals scored 21-30 minutes overall
    goals_21_30_num_home = Field()                  # Goals scored 21-30 minutes at home
    goals_21_30_num_away = Field()                  # Goals scored 21-30 minutes away
    goals_21_30_percentage_overall = Field()        # Goals scored 21-30 minutes percentage overall
    goals_21_30_percentage_home = Field()           # Goals scored 21-30 minutes percentage at home
    goals_21_30_percentage_away = Field()           # Goals scored 21-30 minutes percentage away
    
    goals_31_40_num_overall = Field()               # Goals scored 31-40 minutes overall
    goals_31_40_num_home = Field()                  # Goals scored 31-40 minutes at home
    goals_31_40_num_away = Field()                  # Goals scored 31-40 minutes away
    goals_31_40_percentage_overall = Field()        # Goals scored 31-40 minutes percentage overall
    goals_31_40_percentage_home = Field()           # Goals scored 31-40 minutes percentage at home
    goals_31_40_percentage_away = Field()           # Goals scored 31-40 minutes percentage away
    
    goals_41_50_num_overall = Field()               # Goals scored 41-50 minutes overall
    goals_41_50_num_home = Field()                  # Goals scored 41-50 minutes at home
    goals_41_50_num_away = Field()                  # Goals scored 41-50 minutes away
    goals_41_50_percentage_overall = Field()        # Goals scored 41-50 minutes percentage overall
    goals_41_50_percentage_home = Field()           # Goals scored 41-50 minutes percentage at home
    goals_41_50_percentage_away = Field()           # Goals scored 41-50 minutes percentage away
    
    goals_51_60_num_overall = Field()               # Goals scored 51-60 minutes overall
    goals_51_60_num_home = Field()                  # Goals scored 51-60 minutes at home
    goals_51_60_num_away = Field()                  # Goals scored 51-60 minutes away
    goals_51_60_percentage_overall = Field()        # Goals scored 51-60 minutes percentage overall
    goals_51_60_percentage_home = Field()           # Goals scored 51-60 minutes percentage at home
    goals_51_60_percentage_away = Field()           # Goals scored 51-60 minutes percentage away
    
    goals_61_70_num_overall = Field()               # Goals scored 61-70 minutes overall
    goals_61_70_num_home = Field()                  # Goals scored 61-70 minutes at home
    goals_61_70_num_away = Field()                  # Goals scored 61-70 minutes away
    goals_61_70_percentage_overall = Field()        # Goals scored 61-70 minutes percentage overall
    goals_61_70_percentage_home = Field()           # Goals scored 61-70 minutes percentage at home
    goals_61_70_percentage_away = Field()           # Goals scored 61-70 minutes percentage away
    
    goals_71_80_num_overall = Field()               # Goals scored 71-80 minutes overall
    goals_71_80_num_home = Field()                  # Goals scored 71-80 minutes at home
    goals_71_80_num_away = Field()                  # Goals scored 71-80 minutes away
    goals_71_80_percentage_overall = Field()        # Goals scored 71-80 minutes percentage overall
    goals_71_80_percentage_home = Field()           # Goals scored 71-80 minutes percentage at home
    goals_71_80_percentage_away = Field()           # Goals scored 71-80 minutes percentage away
    
    goals_81_90_num_overall = Field()               # Goals scored 81-90+ minutes overall
    goals_81_90_num_home = Field()                  # Goals scored 81-90+ minutes at home
    goals_81_90_num_away = Field()                  # Goals scored 81-90+ minutes away
    goals_81_90_percentage_overall = Field()        # Goals scored 81-90+ minutes percentage overall
    goals_81_90_percentage_home = Field()           # Goals scored 81-90+ minutes percentage at home
    goals_81_90_percentage_away = Field()           # Goals scored 81-90+ minutes percentage away
    
    # Goals conceded by time intervals
    conceded_0_10_num_overall = Field()             # Goals conceded 0-10 minutes overall
    conceded_0_10_num_home = Field()                # Goals conceded 0-10 minutes at home
    conceded_0_10_num_away = Field()                # Goals conceded 0-10 minutes away
    conceded_0_10_percentage_overall = Field()      # Goals conceded 0-10 minutes percentage overall
    conceded_0_10_percentage_home = Field()         # Goals conceded 0-10 minutes percentage at home
    conceded_0_10_percentage_away = Field()         # Goals conceded 0-10 minutes percentage away
    
    conceded_11_20_num_overall = Field()            # Goals conceded 11-20 minutes overall
    conceded_11_20_num_home = Field()               # Goals conceded 11-20 minutes at home
    conceded_11_20_num_away = Field()               # Goals conceded 11-20 minutes away
    conceded_11_20_percentage_overall = Field()     # Goals conceded 11-20 minutes percentage overall
    conceded_11_20_percentage_home = Field()        # Goals conceded 11-20 minutes percentage at home
    conceded_11_20_percentage_away = Field()        # Goals conceded 11-20 minutes percentage away
    
    conceded_21_30_num_overall = Field()            # Goals conceded 21-30 minutes overall
    conceded_21_30_num_home = Field()               # Goals conceded 21-30 minutes at home
    conceded_21_30_num_away = Field()               # Goals conceded 21-30 minutes away
    conceded_21_30_percentage_overall = Field()     # Goals conceded 21-30 minutes percentage overall
    conceded_21_30_percentage_home = Field()        # Goals conceded 21-30 minutes percentage at home
    conceded_21_30_percentage_away = Field()        # Goals conceded 21-30 minutes percentage away
    
    conceded_31_40_num_overall = Field()            # Goals conceded 31-40 minutes overall
    conceded_31_40_num_home = Field()               # Goals conceded 31-40 minutes at home
    conceded_31_40_num_away = Field()               # Goals conceded 31-40 minutes away
    conceded_31_40_percentage_overall = Field()     # Goals conceded 31-40 minutes percentage overall
    conceded_31_40_percentage_home = Field()        # Goals conceded 31-40 minutes percentage at home
    conceded_31_40_percentage_away = Field()        # Goals conceded 31-40 minutes percentage away
    
    conceded_41_50_num_overall = Field()            # Goals conceded 41-50 minutes overall
    conceded_41_50_num_home = Field()               # Goals conceded 41-50 minutes at home
    conceded_41_50_num_away = Field()               # Goals conceded 41-50 minutes away
    conceded_41_50_percentage_overall = Field()     # Goals conceded 41-50 minutes percentage overall
    conceded_41_50_percentage_home = Field()        # Goals conceded 41-50 minutes percentage at home
    conceded_41_50_percentage_away = Field()        # Goals conceded 41-50 minutes percentage away
    
    conceded_51_60_num_overall = Field()            # Goals conceded 51-60 minutes overall
    conceded_51_60_num_home = Field()               # Goals conceded 51-60 minutes at home
    conceded_51_60_num_away = Field()               # Goals conceded 51-60 minutes away
    conceded_51_60_percentage_overall = Field()     # Goals conceded 51-60 minutes percentage overall
    conceded_51_60_percentage_home = Field()        # Goals conceded 51-60 minutes percentage at home
    conceded_51_60_percentage_away = Field()        # Goals conceded 51-60 minutes percentage away
    
    conceded_61_70_num_overall = Field()            # Goals conceded 61-70 minutes overall
    conceded_61_70_num_home = Field()               # Goals conceded 61-70 minutes at home
    conceded_61_70_num_away = Field()               # Goals conceded 61-70 minutes away
    conceded_61_70_percentage_overall = Field()     # Goals conceded 61-70 minutes percentage overall
    conceded_61_70_percentage_home = Field()        # Goals conceded 61-70 minutes percentage at home
    conceded_61_70_percentage_away = Field()        # Goals conceded 61-70 minutes percentage away
    
    conceded_71_80_num_overall = Field()            # Goals conceded 71-80 minutes overall
    conceded_71_80_num_home = Field()               # Goals conceded 71-80 minutes at home
    conceded_71_80_num_away = Field()               # Goals conceded 71-80 minutes away
    conceded_71_80_percentage_overall = Field()     # Goals conceded 71-80 minutes percentage overall
    conceded_71_80_percentage_home = Field()        # Goals conceded 71-80 minutes percentage at home
    conceded_71_80_percentage_away = Field()        # Goals conceded 71-80 minutes percentage away
    
    conceded_81_90_num_overall = Field()            # Goals conceded 81-90+ minutes overall
    conceded_81_90_num_home = Field()               # Goals conceded 81-90+ minutes at home
    conceded_81_90_num_away = Field()               # Goals conceded 81-90+ minutes away
    conceded_81_90_percentage_overall = Field()     # Goals conceded 81-90+ minutes percentage overall
    conceded_81_90_percentage_home = Field()        # Goals conceded 81-90+ minutes percentage at home
    conceded_81_90_percentage_away = Field()        # Goals conceded 81-90+ minutes percentage away

    # ===== METADATA =====
    extracted_at = Field()                          # Timestamp when data was extracted
    season_id = Field()                             # Season ID for reference


class LeagueTeamLoader(ItemLoader):
    """Item loader for league team data with proper field processing"""
    default_item_class = LeagueTeamItem
    default_output_processor = TakeFirst()
    
    # String fields
    name_in = MapCompose(clean_string)
    cleanName_in = MapCompose(clean_string)
    shortName_in = MapCompose(clean_string)
    image_in = MapCompose(clean_string)
    season_in = MapCompose(clean_string)
    seasonClean_in = MapCompose(clean_string)
    url_in = MapCompose(clean_string)
    season_format_in = MapCompose(clean_string)
    full_name_in = MapCompose(clean_string)
    currentFormHome_in = MapCompose(clean_string)
    currentFormAway_in = MapCompose(clean_string)
    
    # Integer fields
    id_in = MapCompose(safe_int)
    table_position_in = MapCompose(safe_int)
    performance_rank_in = MapCompose(safe_int)
    risk_in = MapCompose(safe_int)
    competition_id_in = MapCompose(safe_int)
    suspended_matches_in = MapCompose(safe_int)
    homeAttackAdvantage_in = MapCompose(safe_int)
    homeDefenceAdvantage_in = MapCompose(safe_int)
    homeOverallAdvantage_in = MapCompose(safe_int)
    
    # Goal count fields (integers)
    seasonGoals_overall_in = MapCompose(safe_int)
    seasonConceded_overall_in = MapCompose(safe_int)
    seasonGoalsTotal_overall_in = MapCompose(safe_int)
    seasonGoalsTotal_home_in = MapCompose(safe_int)
    seasonGoalsTotal_away_in = MapCompose(safe_int)
    seasonScoredNum_overall_in = MapCompose(safe_int)
    seasonScoredNum_home_in = MapCompose(safe_int)
    seasonScoredNum_away_in = MapCompose(safe_int)
    seasonConcededNum_overall_in = MapCompose(safe_int)
    seasonConcededNum_home_in = MapCompose(safe_int)
    seasonConcededNum_away_in = MapCompose(safe_int)
    
    # Goal timing fields (integers)
    seasonGoalsMin_overall_in = MapCompose(safe_int)
    seasonGoalsMin_home_in = MapCompose(safe_int)
    seasonGoalsMin_away_in = MapCompose(safe_int)
    seasonScoredMin_overall_in = MapCompose(safe_int)
    seasonScoredMin_home_in = MapCompose(safe_int)
    seasonScoredMin_away_in = MapCompose(safe_int)
    seasonConcededMin_overall_in = MapCompose(safe_int)
    seasonConcededMin_home_in = MapCompose(safe_int)
    seasonConcededMin_away_in = MapCompose(safe_int)
    
    # Goal difference fields (integers)
    seasonGoalDifference_overall_in = MapCompose(safe_int)
    seasonGoalDifference_home_in = MapCompose(safe_int)
    seasonGoalDifference_away_in = MapCompose(safe_int)
    
    # Match results (integers)
    seasonWinsNum_overall_in = MapCompose(safe_int)
    seasonWinsNum_home_in = MapCompose(safe_int)
    seasonWinsNum_away_in = MapCompose(safe_int)
    seasonDrawsNum_overall_in = MapCompose(safe_int)
    seasonDrawsNum_home_in = MapCompose(safe_int)
    seasonDrawsNum_away_in = MapCompose(safe_int)
    seasonLossesNum_overall_in = MapCompose(safe_int)
    seasonLossesNum_home_in = MapCompose(safe_int)
    seasonLossesNum_away_in = MapCompose(safe_int)
    
    # Timestamp field
    extracted_at_in = MapCompose(lambda x: datetime.now())


def validate_league_team_item(item_data: dict) -> bool:
    """
    Validate league team data structure
    
    Args:
        item_data: Raw data from API response
        
    Returns:
        bool: True if data structure is valid
    """
    if not isinstance(item_data, dict):
        return False
    
    # Check for required fields
    required_fields = ['id', 'name']
    for field in required_fields:
        if field not in item_data or item_data[field] is None:
            return False
    
    # Validate data types for critical fields
    try:
        # ID should be convertible to int
        int(item_data['id'])
        
        # Name should be a string
        if not isinstance(item_data['name'], str):
            return False
            
    except (ValueError, TypeError):
        return False
    
    return True


def create_league_team_item(item_data: dict) -> LeagueTeamItem:
    """
    Create league team item from API data
    
    Args:
        item_data: Raw data from API response
        
    Returns:
        LeagueTeamItem: Processed item
    """
    loader = LeagueTeamLoader()
    
    # Basic team information
    loader.add_value('id', item_data.get('id'))
    loader.add_value('name', item_data.get('name'))
    loader.add_value('cleanName', item_data.get('cleanName'))
    loader.add_value('shortName', item_data.get('shortName'))
    loader.add_value('image', item_data.get('image'))
    loader.add_value('season', item_data.get('season'))
    loader.add_value('seasonClean', item_data.get('seasonClean'))
    loader.add_value('url', item_data.get('url'))
    loader.add_value('table_position', item_data.get('table_position'))
    loader.add_value('performance_rank', item_data.get('performance_rank'))
    loader.add_value('risk', item_data.get('risk'))
    loader.add_value('season_format', item_data.get('season_format'))
    loader.add_value('competition_id', item_data.get('competition_id'))
    loader.add_value('full_name', item_data.get('full_name'))
    
    # Goal statistics
    loader.add_value('seasonGoals_overall', item_data.get('seasonGoals_overall'))
    loader.add_value('seasonConceded_overall', item_data.get('seasonConceded_overall'))
    loader.add_value('seasonGoalDifference_overall', item_data.get('seasonGoalDifference_overall'))
    
    # Match results
    loader.add_value('seasonWinsNum_overall', item_data.get('seasonWinsNum_overall'))
    loader.add_value('seasonDrawsNum_overall', item_data.get('seasonDrawsNum_overall'))
    loader.add_value('seasonLossesNum_overall', item_data.get('seasonLossesNum_overall'))
    
    # Home/away stats
    loader.add_value('seasonGoals_home', item_data.get('seasonGoals_home'))
    loader.add_value('seasonGoals_away', item_data.get('seasonGoals_away'))
    loader.add_value('seasonConceded_home', item_data.get('seasonConceded_home'))
    loader.add_value('seasonConceded_away', item_data.get('seasonConceded_away'))
    
    # Add all other fields dynamically (skip already processed ones)
    processed_fields = {
        'id', 'name', 'cleanName', 'shortName', 'image', 'season', 
        'seasonClean', 'url', 'table_position', 'performance_rank', 
        'risk', 'season_format', 'competition_id', 'full_name',
        'seasonGoals_overall', 'seasonConceded_overall', 'seasonGoalDifference_overall',
        'seasonWinsNum_overall', 'seasonDrawsNum_overall', 'seasonLossesNum_overall',
        'seasonGoals_home', 'seasonGoals_away', 'seasonConceded_home', 'seasonConceded_away'
    }
    
    for key, value in item_data.items():
        if key not in processed_fields:
            # Check if the field exists in the item definition before adding
            try:
                loader.add_value(key, value)
            except KeyError:
                # Field doesn't exist in item definition, skip it
                continue
    
    # Add metadata
    loader.add_value('extracted_at', datetime.now())
    
    return loader.load_item()
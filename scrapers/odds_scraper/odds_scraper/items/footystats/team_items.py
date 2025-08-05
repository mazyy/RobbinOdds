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

class TeamItem(Item):
    """
    Comprehensive item for FootyStats /team endpoint
    
    Captures 1000+ statistical fields including:
    - Basic team information and metadata
    - Season statistics and league position
    - Goal statistics (overall, home, away, halftime)
    - Over/Under goal statistics
    - Corner statistics and betting markets
    - Card statistics 
    - Shot and possession statistics
    - BTTS and clean sheet analysis
    - Goal timing analysis by minute intervals
    - Multilingual team name translations
    - Advanced metrics (xG, attacks, etc.)
    """
    
    # ===== BASIC TEAM INFORMATION =====
    id = Field()
    name = Field()
    full_name = Field()
    english_name = Field()
    alt_names = Field() 
    continent = Field()
    country = Field()
    founded = Field()
    image = Field()
    url = Field()
    official_sites = Field()
    
    # ===== SEASON AND COMPETITION =====
    season = Field()
    season_format = Field()
    competition_id = Field()
    table_position = Field()
    performance_rank = Field()
    risk = Field()
    prediction_risk = Field()
    
    # ===== STADIUM =====
    stadium_name = Field()
    stadium_address = Field()
    
    # ===== MATCH STATISTICS =====
    suspended_matches = Field()
    
    # ===== HOME ADVANTAGES =====
    homeAttackAdvantage = Field()
    homeDefenceAdvantage = Field()
    homeOverallAdvantage = Field()
    
    # ===== SEASON GOALS BASIC =====
    seasonGoals_overall = Field()
    seasonConceded_overall = Field()
    seasonGoalsTotal_overall = Field()
    seasonGoalsTotal_home = Field()
    seasonGoalsTotal_away = Field()
    
    # ===== GOALS SCORED/CONCEDED =====
    seasonScoredNum_overall = Field()
    seasonScoredNum_home = Field()
    seasonScoredNum_away = Field()
    seasonConcededNum_overall = Field()
    seasonConcededNum_home = Field()
    seasonConcededNum_away = Field()
    
    # ===== GOAL MINIMUMS =====
    seasonGoalsMin_overall = Field()
    seasonGoalsMin_home = Field()
    seasonGoalsMin_away = Field()
    seasonScoredMin_overall = Field()
    seasonScoredMin_home = Field()
    seasonScoredMin_away = Field()
    seasonConcededMin_overall = Field()
    seasonConcededMin_home = Field()
    seasonConcededMin_away = Field()
    
    # ===== GOAL DIFFERENCE =====
    seasonGoalDifference_overall = Field()
    seasonGoalDifference_home = Field()
    seasonGoalDifference_away = Field()
    
    # ===== WIN/DRAW/LOSS =====
    seasonWinsNum_overall = Field()
    seasonWinsNum_home = Field()
    seasonWinsNum_away = Field()
    seasonDrawsNum_overall = Field()
    seasonDrawsNum_home = Field()
    seasonDrawsNum_away = Field()
    seasonLossesNum_overall = Field()
    seasonLossesNum_home = Field()
    seasonLossesNum_away = Field()
    
    # ===== MATCHES PLAYED =====
    seasonMatchesPlayed_overall = Field()
    seasonMatchesPlayed_home = Field()
    seasonMatchesPlayed_away = Field()
    
    # ===== HIGHEST SCORES =====
    seasonHighestScored_home = Field()
    seasonHighestConceded_home = Field()
    seasonHighestScored_away = Field()
    seasonHighestConceded_away = Field()
    
    # ===== CLEAN SHEETS =====
    seasonCS_overall = Field()
    seasonCS_home = Field()
    seasonCS_away = Field()
    seasonCSPercentage_overall = Field()
    seasonCSPercentage_home = Field()
    seasonCSPercentage_away = Field()
    
    # ===== CLEAN SHEETS HALFTIME =====
    seasonCSHT_overall = Field()
    seasonCSHT_home = Field()
    seasonCSHT_away = Field()
    seasonCSPercentageHT_overall = Field()
    seasonCSPercentageHT_home = Field()
    seasonCSPercentageHT_away = Field()
    
    # ===== FAILED TO SCORE =====
    seasonFTS_overall = Field()
    seasonFTSPercentage_overall = Field()
    seasonFTSPercentage_home = Field()
    seasonFTSPercentage_away = Field()
    seasonFTS_home = Field()
    seasonFTS_away = Field()
    
    # ===== FAILED TO SCORE HALFTIME =====
    seasonFTSHT_overall = Field()
    seasonFTSPercentageHT_overall = Field()
    seasonFTSPercentageHT_home = Field()
    seasonFTSPercentageHT_away = Field()
    seasonFTSHT_home = Field()
    seasonFTSHT_away = Field()
    
    # ===== BOTH TEAMS TO SCORE (BTTS) =====
    seasonBTTS_overall = Field()
    seasonBTTS_home = Field()
    seasonBTTS_away = Field()
    seasonBTTSPercentage_overall = Field()
    seasonBTTSPercentage_home = Field()
    seasonBTTSPercentage_away = Field()
    
    # ===== BTTS HALFTIME =====
    seasonBTTSHT_overall = Field()
    seasonBTTSHT_home = Field()
    seasonBTTSHT_away = Field()
    seasonBTTSPercentageHT_overall = Field()
    seasonBTTSPercentageHT_home = Field()
    seasonBTTSPercentageHT_away = Field()
    
    # ===== POINTS PER GAME =====
    seasonPPG_overall = Field()
    seasonPPG_home = Field()
    seasonPPG_away = Field()
    
    # ===== AVERAGE GOALS =====
    seasonAVG_overall = Field()
    seasonAVG_home = Field()
    seasonAVG_away = Field()
    seasonScoredAVG_overall = Field()
    seasonScoredAVG_home = Field()
    seasonScoredAVG_away = Field()
    seasonConcededAVG_overall = Field()
    seasonConcededAVG_home = Field()
    seasonConcededAVG_away = Field()
    
    # ===== WIN/DRAW/LOSS PERCENTAGES =====
    winPercentage_overall = Field()
    winPercentage_home = Field()
    winPercentage_away = Field()
    drawPercentage_overall = Field()
    drawPercentage_home = Field()
    drawPercentage_away = Field()
    losePercentage_overall = Field()
    losePercentage_home = Field()
    losePercentage_away = Field()
    
    # ===== HALFTIME POSITION =====
    leadingAtHT_overall = Field()
    leadingAtHT_home = Field()
    leadingAtHT_away = Field()
    leadingAtHTPercentage_overall = Field()
    leadingAtHTPercentage_home = Field()
    leadingAtHTPercentage_away = Field()
    
    drawingAtHT_home = Field()
    drawingAtHT_away = Field()
    drawingAtHT_overall = Field()
    drawingAtHTPercentage_home = Field()
    drawingAtHTPercentage_away = Field()
    drawingAtHTPercentage_overall = Field()
    
    trailingAtHT_home = Field()
    trailingAtHT_away = Field()
    trailingAtHT_overall = Field()
    trailingAtHTPercentage_home = Field()
    trailingAtHTPercentage_away = Field()
    trailingAtHTPercentage_overall = Field()
    
    # ===== HALFTIME POINTS =====
    HTPoints_overall = Field()
    HTPoints_home = Field()
    HTPoints_away = Field()
    HTPPG_overall = Field()
    HTPPG_home = Field()
    HTPPG_away = Field()
    
    # ===== HALFTIME GOALS =====
    scoredAVGHT_overall = Field()
    scoredAVGHT_home = Field()
    scoredAVGHT_away = Field()
    concededAVGHT_overall = Field()
    concededAVGHT_home = Field()
    concededAVGHT_away = Field()
    AVGHT_overall = Field()
    AVGHT_home = Field()
    AVGHT_away = Field()
    
    scoredGoalsHT_overall = Field()
    scoredGoalsHT_home = Field()
    scoredGoalsHT_away = Field()
    concededGoalsHT_overall = Field()
    concededGoalsHT_home = Field()
    concededGoalsHT_away = Field()
    GoalsHT_overall = Field()
    GoalsHT_home = Field()
    GoalsHT_away = Field()
    GoalDifferenceHT_overall = Field()
    GoalDifferenceHT_home = Field()
    GoalDifferenceHT_away = Field()
    
    # ===== OVER/UNDER GOALS - OVERALL =====
    seasonOver55Num_overall = Field()
    seasonOver45Num_overall = Field()
    seasonOver35Num_overall = Field()
    seasonOver25Num_overall = Field()
    seasonOver15Num_overall = Field()
    seasonOver05Num_overall = Field()
    
    seasonOver55Percentage_overall = Field()
    seasonOver45Percentage_overall = Field()
    seasonOver35Percentage_overall = Field()
    seasonOver25Percentage_overall = Field()
    seasonOver15Percentage_overall = Field()
    seasonOver05Percentage_overall = Field()
    
    seasonUnder55Percentage_overall = Field()
    seasonUnder45Percentage_overall = Field()
    seasonUnder35Percentage_overall = Field()
    seasonUnder25Percentage_overall = Field()
    seasonUnder15Percentage_overall = Field()
    seasonUnder05Percentage_overall = Field()
    
    seasonUnder55Num_overall = Field()
    seasonUnder45Num_overall = Field()
    seasonUnder35Num_overall = Field()
    seasonUnder25Num_overall = Field()
    seasonUnder15Num_overall = Field()
    seasonUnder05Num_overall = Field()
    
    # ===== OVER/UNDER GOALS - HOME =====
    seasonOver55Percentage_home = Field()
    seasonOver45Percentage_home = Field()
    seasonOver35Percentage_home = Field()
    seasonOver25Percentage_home = Field()
    seasonOver15Percentage_home = Field()
    seasonOver05Percentage_home = Field()
    seasonOver55Num_home = Field()
    seasonOver45Num_home = Field()
    seasonOver35Num_home = Field()
    seasonOver25Num_home = Field()
    seasonOver15Num_home = Field()
    seasonOver05Num_home = Field()
    
    seasonUnder55Percentage_home = Field()
    seasonUnder45Percentage_home = Field()
    seasonUnder35Percentage_home = Field()
    seasonUnder25Percentage_home = Field()
    seasonUnder15Percentage_home = Field()
    seasonUnder05Percentage_home = Field()
    seasonUnder55Num_home = Field()
    seasonUnder45Num_home = Field()
    seasonUnder35Num_home = Field()
    seasonUnder25Num_home = Field()
    seasonUnder15Num_home = Field()
    seasonUnder05Num_home = Field()
    
    # ===== OVER/UNDER GOALS - AWAY =====
    seasonOver55Percentage_away = Field()
    seasonOver45Percentage_away = Field()
    seasonOver35Percentage_away = Field()
    seasonOver25Percentage_away = Field()
    seasonOver15Percentage_away = Field()
    seasonOver05Percentage_away = Field()
    seasonOver55Num_away = Field()
    seasonOver45Num_away = Field()
    seasonOver35Num_away = Field()
    seasonOver25Num_away = Field()
    seasonOver15Num_away = Field()
    seasonOver05Num_away = Field()
    
    seasonUnder55Percentage_away = Field()
    seasonUnder45Percentage_away = Field()
    seasonUnder35Percentage_away = Field()
    seasonUnder25Percentage_away = Field()
    seasonUnder15Percentage_away = Field()
    seasonUnder05Percentage_away = Field()
    seasonUnder55Num_away = Field()
    seasonUnder45Num_away = Field()
    seasonUnder35Num_away = Field()
    seasonUnder25Num_away = Field()
    seasonUnder15Num_away = Field()
    seasonUnder05Num_away = Field()
    
    # ===== HALFTIME OVER/UNDER GOALS =====
    seasonOver25NumHT_overall = Field()
    seasonOver15NumHT_overall = Field()
    seasonOver05NumHT_overall = Field()
    seasonOver25PercentageHT_overall = Field()
    seasonOver15PercentageHT_overall = Field()
    seasonOver05PercentageHT_overall = Field()
    
    seasonOver25PercentageHT_home = Field()
    seasonOver15PercentageHT_home = Field()
    seasonOver05PercentageHT_home = Field()
    seasonOver25NumHT_home = Field()
    seasonOver15NumHT_home = Field()
    seasonOver05NumHT_home = Field()
    
    seasonOver25PercentageHT_away = Field()
    seasonOver15PercentageHT_away = Field()
    seasonOver05PercentageHT_away = Field()
    seasonOver25NumHT_away = Field()
    seasonOver15NumHT_away = Field()
    seasonOver05NumHT_away = Field()
    
    # ===== CORNER STATISTICS =====
    cornersRecorded_matches_overall = Field()
    cornersRecorded_matches_home = Field()
    cornersRecorded_matches_away = Field()
    
    # Over corners - Overall
    over65Corners_overall = Field()
    over75Corners_overall = Field()
    over85Corners_overall = Field()
    over95Corners_overall = Field()
    over105Corners_overall = Field()
    over115Corners_overall = Field()
    over125Corners_overall = Field()
    over135Corners_overall = Field()
    over145Corners_overall = Field()
    
    over65CornersPercentage_overall = Field()
    over75CornersPercentage_overall = Field()
    over85CornersPercentage_overall = Field()
    over95CornersPercentage_overall = Field()
    over105CornersPercentage_overall = Field()
    over115CornersPercentage_overall = Field()
    over125CornersPercentage_overall = Field()
    over135CornersPercentage_overall = Field()
    over145CornersPercentage_overall = Field()
    
    # Over corners - Home
    over65Corners_home = Field()
    over75Corners_home = Field()
    over85Corners_home = Field()
    over95Corners_home = Field()
    over105Corners_home = Field()
    over115Corners_home = Field()
    over125Corners_home = Field()
    over135Corners_home = Field()
    over145Corners_home = Field()
    
    over65CornersPercentage_home = Field()
    over75CornersPercentage_home = Field()
    over85CornersPercentage_home = Field()
    over95CornersPercentage_home = Field()
    over105CornersPercentage_home = Field()
    over115CornersPercentage_home = Field()
    over125CornersPercentage_home = Field()
    over135CornersPercentage_home = Field()
    over145CornersPercentage_home = Field()
    
    # Over corners - Away
    over65Corners_away = Field()
    over75Corners_away = Field()
    over85Corners_away = Field()
    over95Corners_away = Field()
    over105Corners_away = Field()
    over115Corners_away = Field()
    over125Corners_away = Field()
    over135Corners_away = Field()
    over145Corners_away = Field()
    
    over65CornersPercentage_away = Field()
    over75CornersPercentage_away = Field()
    over85CornersPercentage_away = Field()
    over95CornersPercentage_away = Field()
    over105CornersPercentage_away = Field()
    over115CornersPercentage_away = Field()
    over125CornersPercentage_away = Field()
    over135CornersPercentage_away = Field()
    over145CornersPercentage_away = Field()
    
    # ===== CORNERS FOR TEAM =====
    over25CornersFor_overall = Field()
    over35CornersFor_overall = Field()
    over45CornersFor_overall = Field()
    over55CornersFor_overall = Field()
    over65CornersFor_overall = Field()
    over75CornersFor_overall = Field()
    over85CornersFor_overall = Field()
    
    over25CornersForPercentage_overall = Field()
    over35CornersForPercentage_overall = Field()
    over45CornersForPercentage_overall = Field()
    over55CornersForPercentage_overall = Field()
    over65CornersForPercentage_overall = Field()
    over75CornersForPercentage_overall = Field()
    over85CornersForPercentage_overall = Field()
    
    # Corners for - Home/Away (abbreviated for space)
    over25CornersFor_home = Field()
    over35CornersFor_home = Field()
    over45CornersFor_home = Field()
    over55CornersFor_home = Field()
    over65CornersFor_home = Field()
    over75CornersFor_home = Field()
    over85CornersFor_home = Field()
    
    over25CornersFor_away = Field()
    over35CornersFor_away = Field()
    over45CornersFor_away = Field()
    over55CornersFor_away = Field()
    over65CornersFor_away = Field()
    over75CornersFor_away = Field()
    over85CornersFor_away = Field()
    
    # ===== CORNERS AGAINST TEAM =====
    over25CornersAgainst_overall = Field()
    over35CornersAgainst_overall = Field()
    over45CornersAgainst_overall = Field()
    over55CornersAgainst_overall = Field()
    over65CornersAgainst_overall = Field()
    over75CornersAgainst_overall = Field()
    over85CornersAgainst_overall = Field()
    
    # ===== CARD STATISTICS =====
    over05Cards_overall = Field()
    over15Cards_overall = Field()
    over25Cards_overall = Field()
    over35Cards_overall = Field()
    over45Cards_overall = Field()
    over55Cards_overall = Field()
    over65Cards_overall = Field()
    over75Cards_overall = Field()
    over85Cards_overall = Field()
    
    over05CardsPercentage_overall = Field()
    over15CardsPercentage_overall = Field()
    over25CardsPercentage_overall = Field()
    over35CardsPercentage_overall = Field()
    over45CardsPercentage_overall = Field()
    over55CardsPercentage_overall = Field()
    over65CardsPercentage_overall = Field()
    over75CardsPercentage_overall = Field()
    over85CardsPercentage_overall = Field()
    
    # Cards Home/Away (abbreviated)
    over05Cards_home = Field()
    over15Cards_home = Field()
    over25Cards_home = Field()
    over35Cards_home = Field()
    over45Cards_home = Field()
    
    over05Cards_away = Field()
    over15Cards_away = Field()
    over25Cards_away = Field()
    over35Cards_away = Field()
    over45Cards_away = Field()

    # ===== LEAGUE POSITION =====
    leaguePosition_overall = Field()
    leaguePosition_home = Field()
    leaguePosition_away = Field()
    
    # ===== FIRST GOAL =====
    firstGoalScored_home = Field()
    firstGoalScored_away = Field()
    firstGoalScored_overall = Field()
    firstGoalScoredPercentage_home = Field()
    firstGoalScoredPercentage_away = Field()
    firstGoalScoredPercentage_overall = Field()
    
    # ===== TOTALS =====
    cornersTotal_overall = Field()
    cornersTotal_home = Field()
    cornersTotal_away = Field()
    cardsTotal_overall = Field()
    cardsTotal_home = Field()
    cardsTotal_away = Field()
    
    # ===== AVERAGES =====
    cornersTotalAVG_overall = Field()
    cornersTotalAVG_home = Field()
    cornersTotalAVG_away = Field()
    cornersAVG_overall = Field()
    cornersAVG_home = Field()
    cornersAVG_away = Field()
    cornersAgainst_overall = Field()
    cornersAgainst_home = Field()
    cornersAgainst_away = Field()
    cornersAgainstAVG_overall = Field()
    cornersAgainstAVG_home = Field()
    cornersAgainstAVG_away = Field()
    
    cornersHighest_overall = Field()
    cornersLowest_overall = Field()
    cardsHighest_overall = Field()
    cardsLowest_overall = Field()
    cardsAVG_overall = Field()
    cardsAVG_home = Field()
    cardsAVG_away = Field()
    
    # ===== SHOT STATISTICS =====
    shotsTotal_overall = Field()
    shotsTotal_home = Field()
    shotsTotal_away = Field()
    shotsAVG_overall = Field()
    shotsAVG_home = Field()
    shotsAVG_away = Field()
    
    shotsOnTargetTotal_overall = Field()
    shotsOnTargetTotal_home = Field()
    shotsOnTargetTotal_away = Field()
    shotsOffTargetTotal_overall = Field()
    shotsOffTargetTotal_home = Field()
    shotsOffTargetTotal_away = Field()
    
    shotsOnTargetAVG_overall = Field()
    shotsOnTargetAVG_home = Field()
    shotsOnTargetAVG_away = Field()
    shotsOffTargetAVG_overall = Field()
    shotsOffTargetAVG_home = Field()
    shotsOffTargetAVG_away = Field()
    
    # ===== POSSESSION =====
    possessionAVG_overall = Field()
    possessionAVG_home = Field()
    possessionAVG_away = Field()
    
    # ===== FOULS =====
    foulsAVG_overall = Field()
    foulsAVG_home = Field()
    foulsAVG_away = Field()
    foulsTotal_overall = Field()
    foulsTotal_home = Field()
    foulsTotal_away = Field()
    
    # ===== OFFSIDES =====
    offsidesTotal_overall = Field()
    offsidesTotal_home = Field()
    offsidesTotal_away = Field()
    offsidesTeamTotal_overall = Field()
    offsidesTeamTotal_home = Field()
    offsidesTeamTotal_away = Field()
    
    offsidesRecorded_matches_overall = Field()
    offsidesRecorded_matches_home = Field()
    offsidesRecorded_matches_away = Field()
    
    offsidesAVG_overall = Field()
    offsidesAVG_home = Field()
    offsidesAVG_away = Field()
    offsidesTeamAVG_overall = Field()
    offsidesTeamAVG_home = Field()
    offsidesTeamAVG_away = Field()
    
    # ===== SCORING PATTERNS =====
    scoredBothHalves_overall = Field()
    scoredBothHalves_home = Field()
    scoredBothHalves_away = Field()
    scoredBothHalvesPercentage_overall = Field()
    scoredBothHalvesPercentage_home = Field()
    scoredBothHalvesPercentage_away = Field()
    
    # ===== BTTS COMBINATIONS =====
    BTTS_and_win_overall = Field()
    BTTS_and_win_home = Field()
    BTTS_and_win_away = Field()
    BTTS_and_win_percentage_overall = Field()
    BTTS_and_win_percentage_home = Field()
    BTTS_and_win_percentage_away = Field()
    
    BTTS_and_draw_overall = Field()
    BTTS_and_draw_home = Field()
    BTTS_and_draw_away = Field()
    BTTS_and_draw_percentage_overall = Field()
    BTTS_and_draw_percentage_home = Field()
    BTTS_and_draw_percentage_away = Field()
    
    BTTS_and_lose_overall = Field()
    BTTS_and_lose_home = Field()
    BTTS_and_lose_away = Field()
    BTTS_and_lose_percentage_overall = Field()
    BTTS_and_lose_percentage_home = Field()
    BTTS_and_lose_percentage_away = Field()
    
    # ===== SECOND HALF STATISTICS =====
    AVG_2hg_overall = Field()
    AVG_2hg_home = Field()
    AVG_2hg_away = Field()
    scored_2hg_avg_overall = Field()
    scored_2hg_avg_home = Field()
    scored_2hg_avg_away = Field()
    conceded_2hg_avg_overall = Field()
    conceded_2hg_avg_home = Field()
    conceded_2hg_avg_away = Field()
    
    total_2hg_overall = Field()
    total_2hg_home = Field()
    total_2hg_away = Field()
    conceded_2hg_overall = Field()
    conceded_2hg_home = Field()
    conceded_2hg_away = Field()
    scored_2hg_overall = Field()
    scored_2hg_home = Field()
    scored_2hg_away = Field()
    
    # ===== ATTENDANCE =====
    average_attendance_overall = Field()
    average_attendance_home = Field()
    average_attendance_away = Field()
    
    # ===== ATTACK STATISTICS =====
    attack_num_recoded_matches_overall = Field()
    dangerous_attacks_num_overall = Field()
    attacks_num_overall = Field()
    dangerous_attacks_avg_overall = Field()
    dangerous_attacks_avg_home = Field()
    dangerous_attacks_avg_away = Field()
    attacks_avg_overall = Field()
    attacks_avg_home = Field()
    attacks_avg_away = Field()
    
    # ===== EXPECTED GOALS (xG) =====
    xg_for_avg_overall = Field()
    xg_for_avg_home = Field()
    xg_for_avg_away = Field()
    xg_against_avg_overall = Field()
    xg_against_avg_home = Field()
    xg_against_avg_away = Field()
    
    # ===== GOAL TIMING ANALYSIS =====
    # 10-minute intervals
    goals_scored_min_0_to_10 = Field()
    goals_conceded_min_0_to_10 = Field()
    goals_scored_min_11_to_20 = Field()
    goals_conceded_min_11_to_20 = Field()
    goals_scored_min_21_to_30 = Field()
    goals_conceded_min_21_to_30 = Field()
    goals_scored_min_31_to_40 = Field()
    goals_conceded_min_31_to_40 = Field()
    goals_scored_min_41_to_50 = Field()
    goals_conceded_min_41_to_50 = Field()
    goals_scored_min_51_to_60 = Field()
    goals_conceded_min_51_to_60 = Field()
    goals_scored_min_61_to_70 = Field()
    goals_conceded_min_61_to_70 = Field()
    goals_scored_min_71_to_80 = Field()
    goals_conceded_min_71_to_80 = Field()
    goals_scored_min_81_to_90 = Field()
    goals_conceded_min_81_to_90 = Field()
    
    # 15-minute intervals
    goals_scored_min_0_to_15 = Field()
    goals_scored_min_16_to_30 = Field()
    goals_scored_min_31_to_45 = Field()
    goals_scored_min_46_to_60 = Field()
    goals_scored_min_61_to_75 = Field()
    goals_scored_min_76_to_90 = Field()
    
    goals_conceded_min_0_to_15 = Field()
    goals_conceded_min_16_to_30 = Field()
    goals_conceded_min_31_to_45 = Field()
    goals_conceded_min_46_to_60 = Field()
    goals_conceded_min_61_to_75 = Field()
    goals_conceded_min_76_to_90 = Field()
    
    # Total goals by intervals
    goals_all_min_0_to_10 = Field()
    goals_all_min_11_to_20 = Field()
    goals_all_min_21_to_30 = Field()
    goals_all_min_31_to_40 = Field()
    goals_all_min_41_to_50 = Field()
    goals_all_min_51_to_60 = Field()
    goals_all_min_61_to_70 = Field()
    goals_all_min_71_to_80 = Field()
    goals_all_min_81_to_90 = Field()
    
    goals_all_min_0_to_15 = Field()
    goals_all_min_16_to_30 = Field()
    goals_all_min_31_to_45 = Field()
    goals_all_min_46_to_60 = Field()
    goals_all_min_61_to_75 = Field()
    goals_all_min_76_to_90 = Field()
    
    # ===== HOME GOAL TIMING =====
    goals_scored_min_0_to_10_home = Field()
    goals_scored_min_11_to_20_home = Field()
    goals_scored_min_21_to_30_home = Field()
    goals_scored_min_31_to_40_home = Field()
    goals_scored_min_41_to_50_home = Field()
    goals_scored_min_51_to_60_home = Field()
    goals_scored_min_61_to_70_home = Field()
    goals_scored_min_71_to_80_home = Field()
    goals_scored_min_81_to_90_home = Field()
    
    goals_conceded_min_0_to_10_home = Field()
    goals_conceded_min_11_to_20_home = Field()
    goals_conceded_min_21_to_30_home = Field()
    goals_conceded_min_31_to_40_home = Field()
    goals_conceded_min_41_to_50_home = Field()
    goals_conceded_min_51_to_60_home = Field()
    goals_conceded_min_61_to_70_home = Field()
    goals_conceded_min_71_to_80_home = Field()
    goals_conceded_min_81_to_90_home = Field()
    
    # ===== AWAY GOAL TIMING =====
    goals_scored_min_0_to_10_away = Field()
    goals_scored_min_11_to_20_away = Field()
    goals_scored_min_21_to_30_away = Field()
    goals_scored_min_31_to_40_away = Field()
    goals_scored_min_41_to_50_away = Field()
    goals_scored_min_51_to_60_away = Field()
    goals_scored_min_61_to_70_away = Field()
    goals_scored_min_71_to_80_away = Field()
    goals_scored_min_81_to_90_away = Field()
    
    goals_conceded_min_0_to_10_away = Field()
    goals_conceded_min_11_to_20_away = Field()
    goals_conceded_min_21_to_30_away = Field()
    goals_conceded_min_31_to_40_away = Field()
    goals_conceded_min_41_to_50_away = Field()
    goals_conceded_min_51_to_60_away = Field()
    goals_conceded_min_61_to_70_away = Field()
    goals_conceded_min_71_to_80_away = Field()
    goals_conceded_min_81_to_90_away = Field()
    
    # ===== MULTILINGUAL NAMES =====
    name_jp = Field()           # Japanese
    name_tr = Field()           # Turkish
    name_kr = Field()           # Korean
    name_pt = Field()           # Portuguese
    name_ru = Field()           # Russian
    name_es = Field()           # Spanish
    name_se = Field()           # Swedish
    name_de = Field()           # German
    name_zht = Field()          # Traditional Chinese
    name_nl = Field()           # Dutch
    name_it = Field()           # Italian
    name_fr = Field()           # French
    name_id = Field()           # Indonesian
    name_pl = Field()           # Polish
    name_gr = Field()           # Greek
    name_dk = Field()           # Danish
    name_th = Field()           # Thai
    name_hr = Field()           # Croatian
    name_ro = Field()           # Romanian
    name_in = Field()           # Hindi
    name_no = Field()           # Norwegian
    name_hu = Field()           # Hungarian
    name_cz = Field()           # Czech
    name_cn = Field()           # Simplified Chinese
    name_ara = Field()          # Arabic
    name_si = Field()           # Slovenian
    name_vn = Field()           # Vietnamese
    name_my = Field()           # Malay
    name_sk = Field()           # Slovak
    name_rs = Field()           # Serbian
    name_ua = Field()           # Ukrainian
    name_bg = Field()           # Bulgarian
    name_lv = Field()           # Latvian
    name_ge = Field()           # Georgian
    name_swa = Field()          # Swahili
    name_kur = Field()          # Kurdish
    name_ee = Field()           # Estonian
    name_lt = Field()           # Lithuanian
    name_ba = Field()           # Bosnian
    name_by = Field()           # Belarusian
    name_fi = Field()           # Finnish
    
    # ===== ADDITIONAL METADATA =====
    additional_info = Field()   # Additional information object
    women = Field()             # Women's team indicator
    parent_url = Field()        # Parent URL
    extracted_at = Field()      # Extraction timestamp


class TeamLoader(ItemLoader):
    """
    Item loader for comprehensive team data
    Handles data type conversion for 1000+ statistical fields
    """
    
    default_item_class = TeamItem
    default_input_processor = MapCompose(clean_string)
    default_output_processor = TakeFirst()
    
    # ===== INTEGER CONVERSIONS =====
    id_in = MapCompose(safe_int)
    founded_in = MapCompose(safe_int)
    competition_id_in = MapCompose(safe_int)
    table_position_in = MapCompose(safe_int)
    performance_rank_in = MapCompose(safe_int)
    suspended_matches_in = MapCompose(safe_int)
    
    # Season stats
    seasonGoals_overall_in = MapCompose(safe_int)
    seasonConceded_overall_in = MapCompose(safe_int)
    seasonGoalsTotal_overall_in = MapCompose(safe_int)
    seasonGoalsTotal_home_in = MapCompose(safe_int)
    seasonGoalsTotal_away_in = MapCompose(safe_int)
    
    # Win/Loss stats
    seasonWinsNum_overall_in = MapCompose(safe_int)
    seasonWinsNum_home_in = MapCompose(safe_int)
    seasonWinsNum_away_in = MapCompose(safe_int)
    seasonDrawsNum_overall_in = MapCompose(safe_int)
    seasonDrawsNum_home_in = MapCompose(safe_int)
    seasonDrawsNum_away_in = MapCompose(safe_int)
    seasonLossesNum_overall_in = MapCompose(safe_int)
    seasonLossesNum_home_in = MapCompose(safe_int)
    seasonLossesNum_away_in = MapCompose(safe_int)
    
    # Matches played
    seasonMatchesPlayed_overall_in = MapCompose(safe_int)
    seasonMatchesPlayed_home_in = MapCompose(safe_int)
    seasonMatchesPlayed_away_in = MapCompose(safe_int)
    
    # ===== FLOAT CONVERSIONS =====
    homeAttackAdvantage_in = MapCompose(safe_float)
    homeDefenceAdvantage_in = MapCompose(safe_float)
    homeOverallAdvantage_in = MapCompose(safe_float)
    
    # Points per game
    seasonPPG_overall_in = MapCompose(safe_float)
    seasonPPG_home_in = MapCompose(safe_float)
    seasonPPG_away_in = MapCompose(safe_float)
    
    # Average goals
    seasonAVG_overall_in = MapCompose(safe_float)
    seasonAVG_home_in = MapCompose(safe_float)
    seasonAVG_away_in = MapCompose(safe_float)
    seasonScoredAVG_overall_in = MapCompose(safe_float)
    seasonScoredAVG_home_in = MapCompose(safe_float)
    seasonScoredAVG_away_in = MapCompose(safe_float)
    seasonConcededAVG_overall_in = MapCompose(safe_float)
    seasonConcededAVG_home_in = MapCompose(safe_float)
    seasonConcededAVG_away_in = MapCompose(safe_float)
    
    # Percentages
    seasonCSPercentage_overall_in = MapCompose(safe_float)
    seasonCSPercentage_home_in = MapCompose(safe_float)
    seasonCSPercentage_away_in = MapCompose(safe_float)
    seasonBTTSPercentage_overall_in = MapCompose(safe_float)
    seasonBTTSPercentage_home_in = MapCompose(safe_float)
    seasonBTTSPercentage_away_in = MapCompose(safe_float)
    winPercentage_overall_in = MapCompose(safe_float)
    winPercentage_home_in = MapCompose(safe_float)
    winPercentage_away_in = MapCompose(safe_float)
    drawPercentage_overall_in = MapCompose(safe_float)
    drawPercentage_home_in = MapCompose(safe_float)
    drawPercentage_away_in = MapCompose(safe_float)
    losePercentage_overall_in = MapCompose(safe_float)
    losePercentage_home_in = MapCompose(safe_float)
    losePercentage_away_in = MapCompose(safe_float)
    
    # Over/Under percentages (sample)
    seasonOver55Percentage_overall_in = MapCompose(safe_float)
    seasonOver45Percentage_overall_in = MapCompose(safe_float)
    seasonOver35Percentage_overall_in = MapCompose(safe_float)
    seasonOver25Percentage_overall_in = MapCompose(safe_float)
    seasonOver15Percentage_overall_in = MapCompose(safe_float)
    seasonOver05Percentage_overall_in = MapCompose(safe_float)
    
    # Corner percentages (sample)
    over65CornersPercentage_overall_in = MapCompose(safe_float)
    over75CornersPercentage_overall_in = MapCompose(safe_float)
    over85CornersPercentage_overall_in = MapCompose(safe_float)
    
    # Card percentages (sample)
    over05CardsPercentage_overall_in = MapCompose(safe_float)
    over15CardsPercentage_overall_in = MapCompose(safe_float)
    over25CardsPercentage_overall_in = MapCompose(safe_float)
    
    # Shot averages
    shotsAVG_overall_in = MapCompose(safe_float)
    shotsAVG_home_in = MapCompose(safe_float)
    shotsAVG_away_in = MapCompose(safe_float)
    shotsOnTargetAVG_overall_in = MapCompose(safe_float)
    shotsOnTargetAVG_home_in = MapCompose(safe_float)
    shotsOnTargetAVG_away_in = MapCompose(safe_float)
    
    # Possession
    possessionAVG_overall_in = MapCompose(safe_float)
    possessionAVG_home_in = MapCompose(safe_float)
    possessionAVG_away_in = MapCompose(safe_float)
    
    # Expected goals
    xg_for_avg_overall_in = MapCompose(safe_float)
    xg_for_avg_home_in = MapCompose(safe_float)
    xg_for_avg_away_in = MapCompose(safe_float)
    xg_against_avg_overall_in = MapCompose(safe_float)
    xg_against_avg_home_in = MapCompose(safe_float)
    xg_against_avg_away_in = MapCompose(safe_float)
    
    # ===== SPECIAL FIELDS =====
    alt_names_out = Identity()          # Keep as list
    official_sites_out = Identity()     # Keep as list
    additional_info_out = Identity()    # Keep as object
    
    # Timestamp
    extracted_at_in = MapCompose(lambda x: datetime.now())


def validate_team_item(item_data: dict) -> bool:
    """
    Validate team data structure before processing
    
    Args:
        item_data: Team data from API response
        
    Returns:
        bool: True if valid, False otherwise
    """
    required_fields = ['id', 'name']
    
    if not isinstance(item_data, dict):
        return False
    
    for field in required_fields:
        if field not in item_data or not item_data[field]:
            return False
    
    return True

def create_team_item(item_data: dict) -> TeamItem:
    """
    Create comprehensive team item from FootyStats API data
    
    The FootyStats team endpoint returns:
    {
        "id": 59,
        "name": "Arsenal",
        "season": "2025/2026", 
        "stats": {
            // 1000+ statistical fields
        }
    }
    
    Args:
        item_data: Single team object from API response
        
    Returns:
        TeamItem: Processed team item with all statistics
    """
    loader = TeamLoader()
    
    # ===== BASIC TEAM INFORMATION =====
    loader.add_value('id', item_data.get('id'))
    loader.add_value('name', item_data.get('name'))
    loader.add_value('full_name', item_data.get('full_name'))
    loader.add_value('english_name', item_data.get('english_name'))
    loader.add_value('alt_names', item_data.get('alt_names', []))
    loader.add_value('continent', item_data.get('continent'))
    loader.add_value('country', item_data.get('country'))
    loader.add_value('founded', item_data.get('founded'))
    loader.add_value('image', item_data.get('image'))
    loader.add_value('url', item_data.get('url'))
    loader.add_value('official_sites', item_data.get('official_sites', []))
    
    # ===== SEASON AND COMPETITION =====
    loader.add_value('season', item_data.get('season'))
    loader.add_value('season_format', item_data.get('season_format'))
    loader.add_value('competition_id', item_data.get('competition_id'))
    loader.add_value('table_position', item_data.get('table_position'))
    loader.add_value('performance_rank', item_data.get('performance_rank'))
    loader.add_value('risk', item_data.get('risk'))
    loader.add_value('prediction_risk', item_data.get('prediction_risk'))
    
    # ===== STADIUM =====
    loader.add_value('stadium_name', item_data.get('stadium_name'))
    loader.add_value('stadium_address', item_data.get('stadium_address'))
    
    # ===== ADDITIONAL METADATA =====
    loader.add_value('women', item_data.get('women'))
    loader.add_value('parent_url', item_data.get('parent_url'))
    
    # ===== STATISTICAL DATA FROM STATS OBJECT =====
    stats = item_data.get('stats', {})
    if stats:
        # Map ALL statistical fields from the stats object
        # This uses dynamic mapping to capture all 1000+ fields
        
        # Key statistical fields (explicit mapping for important ones)
        loader.add_value('suspended_matches', stats.get('suspended_matches'))
        loader.add_value('homeAttackAdvantage', stats.get('homeAttackAdvantage'))
        loader.add_value('homeDefenceAdvantage', stats.get('homeDefenceAdvantage'))
        loader.add_value('homeOverallAdvantage', stats.get('homeOverallAdvantage'))
        
        # Season goals
        loader.add_value('seasonGoals_overall', stats.get('seasonGoals_overall'))
        loader.add_value('seasonConceded_overall', stats.get('seasonConceded_overall'))
        loader.add_value('seasonGoalsTotal_overall', stats.get('seasonGoalsTotal_overall'))
        loader.add_value('seasonGoalsTotal_home', stats.get('seasonGoalsTotal_home'))
        loader.add_value('seasonGoalsTotal_away', stats.get('seasonGoalsTotal_away'))
        
        # Win/Draw/Loss
        loader.add_value('seasonWinsNum_overall', stats.get('seasonWinsNum_overall'))
        loader.add_value('seasonWinsNum_home', stats.get('seasonWinsNum_home'))
        loader.add_value('seasonWinsNum_away', stats.get('seasonWinsNum_away'))
        loader.add_value('seasonDrawsNum_overall', stats.get('seasonDrawsNum_overall'))
        loader.add_value('seasonDrawsNum_home', stats.get('seasonDrawsNum_home'))
        loader.add_value('seasonDrawsNum_away', stats.get('seasonDrawsNum_away'))
        loader.add_value('seasonLossesNum_overall', stats.get('seasonLossesNum_overall'))
        loader.add_value('seasonLossesNum_home', stats.get('seasonLossesNum_home'))
        loader.add_value('seasonLossesNum_away', stats.get('seasonLossesNum_away'))
        
        # Matches played
        loader.add_value('seasonMatchesPlayed_overall', stats.get('seasonMatchesPlayed_overall'))
        loader.add_value('seasonMatchesPlayed_home', stats.get('seasonMatchesPlayed_home'))
        loader.add_value('seasonMatchesPlayed_away', stats.get('seasonMatchesPlayed_away'))
        
        # Points and averages
        loader.add_value('seasonPPG_overall', stats.get('seasonPPG_overall'))
        loader.add_value('seasonPPG_home', stats.get('seasonPPG_home'))
        loader.add_value('seasonPPG_away', stats.get('seasonPPG_away'))
        loader.add_value('seasonAVG_overall', stats.get('seasonAVG_overall'))
        loader.add_value('seasonAVG_home', stats.get('seasonAVG_home'))
        loader.add_value('seasonAVG_away', stats.get('seasonAVG_away'))
        loader.add_value('seasonScoredAVG_overall', stats.get('seasonScoredAVG_overall'))
        loader.add_value('seasonScoredAVG_home', stats.get('seasonScoredAVG_home'))
        loader.add_value('seasonScoredAVG_away', stats.get('seasonScoredAVG_away'))
        loader.add_value('seasonConcededAVG_overall', stats.get('seasonConcededAVG_overall'))
        loader.add_value('seasonConcededAVG_home', stats.get('seasonConcededAVG_home'))
        loader.add_value('seasonConcededAVG_away', stats.get('seasonConcededAVG_away'))
        
        # BTTS and Clean Sheets
        loader.add_value('seasonBTTS_overall', stats.get('seasonBTTS_overall'))
        loader.add_value('seasonBTTS_home', stats.get('seasonBTTS_home'))
        loader.add_value('seasonBTTS_away', stats.get('seasonBTTS_away'))
        loader.add_value('seasonBTTSPercentage_overall', stats.get('seasonBTTSPercentage_overall'))
        loader.add_value('seasonBTTSPercentage_home', stats.get('seasonBTTSPercentage_home'))
        loader.add_value('seasonBTTSPercentage_away', stats.get('seasonBTTSPercentage_away'))
        
        loader.add_value('seasonCS_overall', stats.get('seasonCS_overall'))
        loader.add_value('seasonCS_home', stats.get('seasonCS_home'))
        loader.add_value('seasonCS_away', stats.get('seasonCS_away'))
        loader.add_value('seasonCSPercentage_overall', stats.get('seasonCSPercentage_overall'))
        loader.add_value('seasonCSPercentage_home', stats.get('seasonCSPercentage_home'))
        loader.add_value('seasonCSPercentage_away', stats.get('seasonCSPercentage_away'))
        
        # Win/Draw/Loss percentages
        loader.add_value('winPercentage_overall', stats.get('winPercentage_overall'))
        loader.add_value('winPercentage_home', stats.get('winPercentage_home'))
        loader.add_value('winPercentage_away', stats.get('winPercentage_away'))
        loader.add_value('drawPercentage_overall', stats.get('drawPercentage_overall'))
        loader.add_value('drawPercentage_home', stats.get('drawPercentage_home'))
        loader.add_value('drawPercentage_away', stats.get('drawPercentage_away'))
        loader.add_value('losePercentage_overall', stats.get('losePercentage_overall'))
        loader.add_value('losePercentage_home', stats.get('losePercentage_home'))
        loader.add_value('losePercentage_away', stats.get('losePercentage_away'))
        
        # Over/Under goals (key thresholds)
        loader.add_value('seasonOver25Num_overall', stats.get('seasonOver25Num_overall'))
        loader.add_value('seasonOver25Percentage_overall', stats.get('seasonOver25Percentage_overall'))
        loader.add_value('seasonOver15Num_overall', stats.get('seasonOver15Num_overall'))
        loader.add_value('seasonOver15Percentage_overall', stats.get('seasonOver15Percentage_overall'))
        
        # Corner statistics
        loader.add_value('cornersRecorded_matches_overall', stats.get('cornersRecorded_matches_overall'))
        loader.add_value('cornersTotal_overall', stats.get('cornersTotal_overall'))
        loader.add_value('cornersAVG_overall', stats.get('cornersAVG_overall'))
        
        # Card statistics
        loader.add_value('cardsTotal_overall', stats.get('cardsTotal_overall'))
        loader.add_value('cardsAVG_overall', stats.get('cardsAVG_overall'))
        
        # Shot statistics
        loader.add_value('shotsTotal_overall', stats.get('shotsTotal_overall'))
        loader.add_value('shotsAVG_overall', stats.get('shotsAVG_overall'))
        loader.add_value('shotsOnTargetTotal_overall', stats.get('shotsOnTargetTotal_overall'))
        loader.add_value('shotsOnTargetAVG_overall', stats.get('shotsOnTargetAVG_overall'))
        
        # Possession and fouls
        loader.add_value('possessionAVG_overall', stats.get('possessionAVG_overall'))
        loader.add_value('foulsTotal_overall', stats.get('foulsTotal_overall'))
        loader.add_value('foulsAVG_overall', stats.get('foulsAVG_overall'))
        
        # Expected goals
        loader.add_value('xg_for_avg_overall', stats.get('xg_for_avg_overall'))
        loader.add_value('xg_for_avg_home', stats.get('xg_for_avg_home'))
        loader.add_value('xg_for_avg_away', stats.get('xg_for_avg_away'))
        loader.add_value('xg_against_avg_overall', stats.get('xg_against_avg_overall'))
        loader.add_value('xg_against_avg_home', stats.get('xg_against_avg_home'))
        loader.add_value('xg_against_avg_away', stats.get('xg_against_avg_away'))
        
        # Goal timing (sample)
        loader.add_value('goals_scored_min_0_to_10', stats.get('goals_scored_min_0_to_10'))
        loader.add_value('goals_scored_min_11_to_20', stats.get('goals_scored_min_11_to_20'))
        loader.add_value('goals_conceded_min_0_to_10', stats.get('goals_conceded_min_0_to_10'))
        
        # Multilingual names
        loader.add_value('name_jp', stats.get('name_jp'))
        loader.add_value('name_tr', stats.get('name_tr'))
        loader.add_value('name_kr', stats.get('name_kr'))
        loader.add_value('name_pt', stats.get('name_pt'))
        loader.add_value('name_ru', stats.get('name_ru'))
        loader.add_value('name_es', stats.get('name_es'))
        loader.add_value('name_de', stats.get('name_de'))
        loader.add_value('name_fr', stats.get('name_fr'))
        loader.add_value('name_it', stats.get('name_it'))
        loader.add_value('name_nl', stats.get('name_nl'))
        
        # Additional info
        loader.add_value('additional_info', stats.get('additional_info'))
        
        # ===== DYNAMIC FIELD MAPPING =====
        # This ensures we capture ALL statistical fields, not just the explicit ones above
        for field_name, field_value in stats.items():
            # Only add if the field exists in our TeamItem and hasn't been set yet
            if hasattr(TeamItem, field_name):
                try:
                    current_value = loader.get_output_value(field_name)
                    if current_value is None:
                        loader.add_value(field_name, field_value)
                except:
                    # If field doesn't exist in loader output yet, add it
                    loader.add_value(field_name, field_value)
    
    # ===== METADATA =====
    loader.add_value('extracted_at', None)  # Will be set to current datetime
    
    return loader.load_item()


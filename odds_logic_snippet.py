
def find_dynamic_odds(bets, home_goals, away_goals):
    total_goals = home_goals + away_goals
    over_key = f"Over {total_goals + 0.5}"
    under_key = f"Under {total_goals + 2.5}"
    
    over_odds = None
    under_odds = None

    for bet in bets:
        if "Over/Under" in bet["name"]:
            for value in bet["values"]:
                if value["value"] == over_key:
                    over_odds = value["odd"]
                elif value["value"] == under_key:
                    under_odds = value["odd"]
    
    return over_odds, under_odds

import requests
from django.shortcuts import render

def fetch_espn_data(sport_code):
    """
    Fetches 100% FREE live data from ESPN's public hidden API.
    No API keys required.
    """
    endpoints = {
        'nfl': 'football/nfl',
        'nba': 'basketball/nba',
        'mlb': 'baseball/mlb',
        'nhl': 'hockey/nhl',
        'soccer': 'soccer/eng.1' # English Premier League
    }
    
    path = endpoints.get(sport_code, 'football/nfl')
    api_url = f'https://site.api.espn.com/apis/site/v2/sports/{path}/scoreboard'
    
    try:
        response = requests.get(api_url, timeout=5)
        data = response.json()
        events = data.get('events', [])
        
        games = []
        for event in events:
            comp = event['competitions'][0]
            status_desc = event['status']['type']['description'] # e.g. "Final", "Scheduled"
            
            team1 = comp['competitors'][0]
            team2 = comp['competitors'][1]
            
            home_team = team1 if team1['homeAway'] == 'home' else team2
            away_team = team1 if team1['homeAway'] == 'away' else team2
            
            home_team_info = home_team['team']
            away_team_info = away_team['team']
            
            games.append({
                'home_team': home_team_info.get('displayName', 'Unknown'),
                'home_abbr': home_team_info.get('abbreviation', 'TBD'),
                'home_logo': home_team_info.get('logo', ''),
                'home_score': home_team.get('score', '-'),
                'away_team': away_team_info.get('displayName', 'Unknown'),
                'away_abbr': away_team_info.get('abbreviation', 'TBD'),
                'away_logo': away_team_info.get('logo', ''),
                'away_score': away_team.get('score', '-'),
                'status': 'Final' if 'Final' in status_desc else ('Upcoming' if 'Scheduled' in status_desc else 'Live'),
                'week': event.get('shortName', 'Game')
            })
        return games
    except Exception as e:
        print(f"ESPN API Error: {e}")
        return []

def home(request):
    # Make the website completely dynamic! Read the sport from the URL (e.g., ?sport=nba)
    # Defaults to 'nfl' if nothing is selected.
    selected_sport = request.GET.get('sport', 'nfl')
    
    # Fetch data dynamically using the free ESPN API
    games = fetch_espn_data(selected_sport)

    # Dictionary to set titles properly in the HTML
    titles = {
        'nfl': '🏈 NFL Football',
        'nba': '🏀 NBA Basketball',
        'soccer': '⚽ Premier League Soccer',
        'mlb': '⚾ MLB Baseball',
        'nhl': '🏒 NHL Hockey'
    }

    context = {
        'games': games,
        'current_sport': selected_sport,
        'season': titles.get(selected_sport, 'Live Sports')
    }
    return render(request, 'sportsbook/home.html', context)

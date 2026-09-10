import requests
from django.shortcuts import render

def home(request):
    """
    Fetches the real NFL live data from the BetBuilder API
    and displays it exactly like the gambling.com/betbuilderai/nfl interface.
    """
    api_url = 'https://www.gambling.com/betbuilderai/api/nfl/games?recent=12&type=all'
    headers = {'User-Agent': 'Mozilla/5.0'}
    
    try:
        response = requests.get(api_url, headers=headers, timeout=5)
        data = response.json()
        raw_games = data.get('games', [])
        
        games = []
        for g in raw_games:
            games.append({
                'home_team': g.get('home_team'),
                'home_abbr': g.get('home_abbr'),
                'away_team': g.get('away_team'),
                'away_abbr': g.get('away_abbr'),
                'home_score': g.get('home_score', '-'),
                'away_score': g.get('away_score', '-'),
                'status': 'Final' if g.get('status') == 'completed' else 'Upcoming',
                'week': f"Week {g.get('week')}" if g.get('week') else g.get('season_type')
            })
    except Exception as e:
        games = []

    context = {
        'games': games,
        'season': '2026 NFL Season'
    }
    return render(request, 'sportsbook/home.html', context)

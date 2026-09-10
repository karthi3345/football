import requests
from django.shortcuts import render

def fetch_nfl_games():
    """
    Fetches the actual NFL game data directly from the gambling.com BetBuilder API.
    Since they use a JSON API to load their games, we don't even need BeautifulSoup!
    We can get the raw data instantly.
    """
    target_api_url = 'https://www.gambling.com/betbuilderai/api/nfl/games?recent=12&type=all'
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Accept': 'application/json'
    }
    
    try:
        response = requests.get(target_api_url, headers=headers, timeout=10)
        
        # Parse the JSON response
        data = response.json()
        
        # The API returns a dictionary with a "games" list
        games_list = data.get('games', [])
        
        # Format the data cleanly for our Django template
        formatted_games = []
        for game in games_list:
            
            # Determine if it's finished or upcoming based on status
            is_completed = game.get('status') == 'completed'
            
            formatted_games.append({
                'home_team': game.get('home_team'),
                'home_abbr': game.get('home_abbr'),
                'away_team': game.get('away_team'),
                'away_abbr': game.get('away_abbr'),
                'home_score': game.get('home_score', '-'),
                'away_score': game.get('away_score', '-'),
                'status': 'Final' if is_completed else 'Upcoming',
                'week': f"Week {game.get('week')}" if game.get('week') else game.get('season_type')
            })
            
        return formatted_games

    except Exception as e:
        print(f"Error fetching API data: {e}")
        return []

def nfl_games_view(request):
    """
    Your Django view that passes the NFL games to your HTML template.
    """
    nfl_games = fetch_nfl_games()
    
    # Pass it to the HTML template
    context = {
        'nfl_games': nfl_games
    }
    
    return render(request, 'myvepower/nfl_games.html', context)

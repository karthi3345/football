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
        'soccer': 'soccer/eng.1', # English Premier League
        'mls': 'soccer/usa.1'     # Major League Soccer
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
            status_desc = event['status']['type']['description']
            
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

def get_player_props(sport):
    players = {
        'nfl': [
            {'name': 'Patrick Mahomes', 'team': 'KC', 'prop': 'Passing Yards', 'line': 'O/U 285.5', 'img': 'https://a.espncdn.com/i/headshots/nfl/players/full/3139477.png'},
            {'name': 'C. McCaffrey', 'team': 'SF', 'prop': 'Rushing Yards', 'line': 'O/U 85.5', 'img': 'https://a.espncdn.com/i/headshots/nfl/players/full/3117251.png'},
            {'name': 'Justin Jefferson', 'team': 'MIN', 'prop': 'Receiving Yds', 'line': 'O/U 92.5', 'img': 'https://a.espncdn.com/i/headshots/nfl/players/full/4262921.png'}
        ],
        'mls': [
            {'name': 'Lionel Messi', 'team': 'MIA', 'prop': 'Anytime Goal', 'line': '+110', 'img': 'https://a.espncdn.com/i/headshots/soccer/players/full/45843.png'},
            {'name': 'Denis Bouanga', 'team': 'LAFC', 'prop': 'Total Shots', 'line': 'O/U 3.5', 'img': 'https://a.espncdn.com/i/headshots/soccer/players/full/409224.png'},
            {'name': 'Luciano Acosta', 'team': 'CIN', 'prop': 'Assists', 'line': 'O/U 0.5', 'img': 'https://a.espncdn.com/i/headshots/soccer/players/full/226197.png'}
        ],
        'soccer': [
            {'name': 'Erling Haaland', 'team': 'MCI', 'prop': 'Anytime Goal', 'line': '-150', 'img': 'https://a.espncdn.com/i/headshots/soccer/players/full/260021.png'},
            {'name': 'Mohamed Salah', 'team': 'LIV', 'prop': 'Total Shots', 'line': 'O/U 2.5', 'img': 'https://a.espncdn.com/i/headshots/soccer/players/full/173896.png'},
            {'name': 'Bukayo Saka', 'team': 'ARS', 'prop': 'Assists', 'line': 'O/U 0.5', 'img': 'https://a.espncdn.com/i/headshots/soccer/players/full/285078.png'}
        ],
        'nba': [
            {'name': 'LeBron James', 'team': 'LAL', 'prop': 'Total Points', 'line': 'O/U 25.5', 'img': 'https://a.espncdn.com/i/headshots/nba/players/full/1966.png'},
            {'name': 'Stephen Curry', 'team': 'GSW', 'prop': '3-Pointers', 'line': 'O/U 4.5', 'img': 'https://a.espncdn.com/i/headshots/nba/players/full/3975.png'},
            {'name': 'Nikola Jokic', 'team': 'DEN', 'prop': 'Triple Double', 'line': 'Yes +150', 'img': 'https://a.espncdn.com/i/headshots/nba/players/full/3112335.png'}
        ],
        'mlb': [
            {'name': 'Shohei Ohtani', 'team': 'LAD', 'prop': 'Home Runs', 'line': 'O/U 0.5', 'img': 'https://a.espncdn.com/i/headshots/mlb/players/full/39832.png'},
            {'name': 'Aaron Judge', 'team': 'NYY', 'prop': 'Total Bases', 'line': 'O/U 1.5', 'img': 'https://a.espncdn.com/i/headshots/mlb/players/full/33192.png'},
            {'name': 'Mookie Betts', 'team': 'LAD', 'prop': 'Hits', 'line': 'O/U 1.5', 'img': 'https://a.espncdn.com/i/headshots/mlb/players/full/33039.png'}
        ],
        'nhl': [
            {'name': 'Connor McDavid', 'team': 'EDM', 'prop': 'Total Points', 'line': 'O/U 1.5', 'img': 'https://a.espncdn.com/i/headshots/nhl/players/full/3899664.png'},
            {'name': 'Auston Matthews', 'team': 'TOR', 'prop': 'Anytime Goal', 'line': '-120', 'img': 'https://a.espncdn.com/i/headshots/nhl/players/full/4001150.png'},
            {'name': 'N. MacKinnon', 'team': 'COL', 'prop': 'Total Shots', 'line': 'O/U 4.5', 'img': 'https://a.espncdn.com/i/headshots/nhl/players/full/3041969.png'}
        ]
    }
    return players.get(sport, players['nfl'])

def home(request):
    selected_sport = request.GET.get('sport', 'nfl')
    games = fetch_espn_data(selected_sport)
    players = get_player_props(selected_sport)

    titles = {
        'nfl': '🏈 NFL Football',
        'nba': '🏀 NBA Basketball',
        'soccer': '⚽ Premier League',
        'mls': '⚽ MLS Soccer',
        'mlb': '⚾ MLB Baseball',
        'nhl': '🏒 NHL Hockey'
    }

    context = {
        'games': games,
        'players': players,
        'current_sport': selected_sport,
        'season': titles.get(selected_sport, 'Live Sports')
    }
    return render(request, 'sportsbook/home.html', context)

def squads(request):
    leagues = [
        {'name': 'ALL', 'count': 150, 'active': False},
        {'name': 'MLS', 'count': 30, 'active': True},
        {'name': 'PREMIER LEAGUE', 'count': 20, 'active': False},
        {'name': 'LA LIGA', 'count': 20, 'active': False},
        {'name': 'SERIE A', 'count': 20, 'active': False},
        {'name': 'BUNDESLIGA', 'count': 18, 'active': False},
        {'name': 'LIGUE 1', 'count': 18, 'active': False},
        {'name': 'CHAMPIONSHIP', 'count': 24, 'active': False},
    ]

    fixtures = [
        {
            'league': 'MLS',
            'time': '05:00 GMT+5:30',
            'home_team': 'Orlando City SC',
            'home_logo': 'https://a.espncdn.com/i/teamlogos/soccer/500/10450.png',
            'away_team': 'Toronto FC',
            'away_logo': 'https://a.espncdn.com/i/teamlogos/soccer/500/7318.png',
        },
        {
            'league': 'MLS',
            'time': '05:00 GMT+5:30',
            'home_team': 'Columbus Crew',
            'home_logo': 'https://a.espncdn.com/i/teamlogos/soccer/500/182.png',
            'away_team': 'New York Red Bulls',
            'away_logo': 'https://a.espncdn.com/i/teamlogos/soccer/500/190.png',
        },
        {
            'league': 'MLS',
            'time': '05:00 GMT+5:30',
            'home_team': 'DC United',
            'home_logo': 'https://a.espncdn.com/i/teamlogos/soccer/500/183.png',
            'away_team': 'Atlanta United FC',
            'away_logo': 'https://a.espncdn.com/i/teamlogos/soccer/500/18230.png',
        },
        {
            'league': 'MLS',
            'time': '05:00 GMT+5:30',
            'home_team': 'FC Cincinnati',
            'home_logo': 'https://a.espncdn.com/i/teamlogos/soccer/500/18204.png',
            'away_team': 'Charlotte FC',
            'away_logo': 'https://a.espncdn.com/i/teamlogos/soccer/500/21577.png',
        }
    ]

    context = {
        'leagues': leagues,
        'fixtures': fixtures,
        'filters': ['ALL', 'MLS', 'EPL', 'LALIGA', 'SERIE A', 'BUNDES', 'LIGUE 1', 'CHAMP', 'UCL', 'UEL']
    }
    return render(request, 'sportsbook/squads.html', context)

def ai_analysis(request):
    query = request.GET.get('q', '')
    show_result = bool(query)
    
    context = {
        'query': query,
        'show_result': show_result
    }
    return render(request, 'sportsbook/ai_analysis.html', context)

def match_centre(request):
    # Mock data for Arsenal vs Liverpool Match Centre
    context = {}
    return render(request, 'sportsbook/match_centre.html', context)

def live_dashboard(request):
    return render(request, 'sportsbook/live.html', {})

def team_page(request):
    return render(request, 'sportsbook/team.html', {})

def player_page(request):
    return render(request, 'sportsbook/player.html', {})

def my_picks(request):
    return render(request, 'sportsbook/picks.html', {})

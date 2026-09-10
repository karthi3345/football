from django.shortcuts import render

def home(request):
    # This represents the affiliate data you would normally pull from a database.
    # We are structuring it like Gambling.com's top lists, but strictly for Sweepstakes Betting.
    sweepstakes_sportsbooks = [
        {
            'rank': 1,
            'name': 'Fliff Social Sportsbook',
            'logo': 'Fliff',
            'rating': 9.8,
            'bonus_gc': '600,000 Fliff Coins',
            'bonus_sc': '$100 Fliff Cash Match',
            'features': ['Best odds in the sweeps market', 'Daily free coins', 'Live in-play betting'],
            'color': '#111827'
        },
        {
            'rank': 2,
            'name': 'Sportzino',
            'logo': 'Sportzino',
            'rating': 9.5,
            'bonus_gc': '1,500,000 GC',
            'bonus_sc': '40 FREE Sweeps Coins',
            'features': ['Massive esports coverage', 'Frequent daily login bonuses', 'Fast redemptions'],
            'color': '#ff4500'
        },
        {
            'rank': 3,
            'name': 'Rebet',
            'logo': 'Rebet',
            'rating': 9.3,
            'bonus_gc': '100,000 Rebet Coins',
            'bonus_sc': '100 Rebet Cash',
            'features': ['Peer-to-peer social betting', 'Clean mobile app', 'Follow friends'],
            'color': '#3b82f6'
        },
        {
            'rank': 4,
            'name': 'Thrillzz',
            'logo': 'Thrillzz',
            'rating': 9.1,
            'bonus_gc': '3,000 Thrillzz Coins',
            'bonus_sc': '3 Sweeps Tickets',
            'features': ['Unique ticketing system', 'Great community features', 'No purchase necessary'],
            'color': '#8b5cf6'
        }
    ]

    context = {
        'top_sites': sweepstakes_sportsbooks
    }
    return render(request, 'sportsbook/home.html', context)

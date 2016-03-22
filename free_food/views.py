from django.shortcuts import render
from facepy import GraphAPI

def parse_event(event):
    if 'free food' in event['description'] or 'free food' in event['name']:
        return True
    else:
        return False

def index(request):
    if request.user:
        social = request.user.social_auth.get(provider='facebook')
        access_token = social.extra_data['access_token']
        graph = GraphAPI(access_token)

        filtered = []
        events = graph.search('free food', 'event', page=False, retry=3, center={'longitude': 40.4842, 'latitude': 88.9936}, distance=1000)
        for event in events['data']:
            if parse_event(event):
                filtered.append(event)

        return render(request, 'index.html', {'user': request.user, 'events': filtered})

    else:
        return render(request, 'index.html', {'user': request.user})

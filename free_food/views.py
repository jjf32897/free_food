import requests, json
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

        location = graph.get('me?fields=location')['location']['name']
        events = graph.search(location, 'event', page=False, retry=3, center={'longitude': 40.4842, 'latitude': 88.9936}, distance=1000)

        # query = 'Bloomington, IL'
        # url = 'https://graph.facebook.com/search?q=%s&type=event' % query
        # parameters = {'access_token': access_token}
        # r = requests.get(url, params = parameters)
        # events = json.loads(r.text)

        for event in events['data']:
            # if parse_event(event):
            filtered.append(event)

        return render(request, 'index.html', {'user': request.user, 'events': filtered})

    else:
        return render(request, 'index.html', {'user': request.user})

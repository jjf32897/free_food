import requests, json
from django.shortcuts import render
from facepy import GraphAPI
from geopy.geocoders import Nominatim

def parse_event(event):
    if 'description' in event:
        if 'free food' in event['description'].lower() or 'free' in event['name'].lower():
            return True

    return False


def index(request):
    if request.user:
        social = request.user.social_auth.get(provider='facebook')
        access_token = social.extra_data['access_token']
        graph = GraphAPI(access_token)

        ids = []
        events = []
        filtered = []
        check = []

        city = graph.get('me?fields=location')['location']['name']
        geolocator = Nominatim()
        location = geolocator.geocode(city)
        coordinates = '%f,%f' % (location.latitude, location.longitude)

        # queries for places
        places = graph.search('*', 'place', page=False, retry=3, center=coordinates, distance=10000, limit=1000, fields='name')

        # query = '*'
        # url = 'https://graph.facebook.com/search?q=%s&type=place&center=40.110539,-88.228411&distance=5000&limit=1000&fields=name' % query
        # parameters = {'access_token': access_token}
        # r = requests.get(url, params = parameters)
        # places = json.loads(r.text)

        for place in places['data']:
            ids.append(place['id'])

        startIndex = 0
        id_list = []

        for a in range(len(ids) / 50):
            for b in range(50):
                id_list.append(ids[startIndex + b])
            url = 'https://graph.facebook.com/v2.5/?ids=%s&fields=id,name,cover.fields(id,source),picture.type(large),location,events.fields(id,name,cover.fields(id,source),picture.type(large),description,start_time,attending_count,declined_count,maybe_count,noreply_count)' % ','.join(id_list)
            parameters = {'access_token': access_token}
            r = requests.get(url, params = parameters)
            data = json.loads(r.text)

            for place_id in data:
                if 'events' in data[place_id]:
                    for c in range(len(data[place_id]['events']['data'])):
                        events.append(data[place_id]['events']['data'][c])

            startIndex += 50
            id_list = []

        for i in range(len(ids) % 50):
            id_list.append(ids[startIndex + i])
        check.append(','.join(id_list))
        url = 'https://graph.facebook.com/v2.5/?ids=%s&fields=id,name,cover.fields(id,source),picture.type(large),location,events.fields(id,name,cover.fields(id,source),picture.type(large),description,start_time,attending_count,declined_count,maybe_count,noreply_count)' % ','.join(id_list)
        parameters = {'access_token': access_token}
        r = requests.get(url, params = parameters)
        data = json.loads(r.text)

        for place_id in data:
            if 'events' in data[place_id]:
                for d in range(len(data[place_id]['events']['data'])):
                    events.append(data[place_id]['events']['data'][d])

        count = 0

        for event in events:
            if parse_event(event):
                count += 1
                filtered.append(event)

        return render(request, 'index.html', {'user': request.user, 'events': filtered})

    else:
        return render(request, 'index.html', {'user': request.user})

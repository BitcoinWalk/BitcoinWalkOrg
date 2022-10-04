from urllib import request
import json
from datetime import datetime
from collections import defaultdict

json_url = "https://drive.google.com/uc?id=1QMzXSJYtEA3tF_kqaoyxNdTKEs3OZDXm"
output_json_path = "static/plots/proof-of-walk.json"

color_map = {
    'Edinburgh': "#f7931a",
    'Other': "#808080"
}

with request.urlopen(json_url) as response:
    data = json.load(response)

# Dictionary indexed by location name, containing walk data
walks = defaultdict(lambda: {'time': [], 'attendance': [], 'tweetLink': []})

for timestamp, entry in data['Sheet1'].items():
    date = datetime.strptime(timestamp.split('-')[0], "%a %b %d %Y %X %Z")
    tweet_link = entry.pop('Tweet link', None)
    for location, value in entry.items():
        attendance = int(value) if value is not None else 0
        if attendance > 0:
            walks[location]['time'].append(date.strftime("%Y-%m-%d"))
            walks[location]['attendance'].append(attendance)
            walks[location]['tweetLink'].append(tweet_link)

output = {
    'layout': {
        'title': "#ProofOfWalk",
        'yaxis': {
            'title': "Number of People",
            'showgrid': False,
            'zeroline': False
        },
        'xaxis': {'title': "Time"},
        'barmode': "stack",
        'paper_bgcolor': "transparent",
        'plot_bgcolor': "transparent",
        'font': {
            'color': "black"
        }
    },
    'data': [
        {
            'name': location,
            'marker': {
                'color': color_map[location]
            },
            'type': "bar",
            'x': points['time'],
            'y': points['attendance'],
            'customdata': points['tweetLink']
        }
        for location, points in walks.items()
    ]
}

with open(output_json_path, 'w') as f:
    f.write(json.dumps(output))

print("Done")

import requests

url = 'https://swishanalytics.com/injury/ajax/ajax-status-pie-chart.php'

url = 'https://swishanalytics.com/injury/ajax/all-sports-ajax.php'
player_id = 756880
data = {'sport': 'nba', 'player_id': player_id}
res=requests.post(url, data=data)

print(res.text)

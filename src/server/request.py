import requests

url = 'http://127.0.0.1:5000/api/fill_mask'

x = requests.post(url, json={
    'x': 'New study links disturbed [MASK] metabolism in depressed '
         'individuals to disruption of the gut microbiome.'
})

print(x.text)

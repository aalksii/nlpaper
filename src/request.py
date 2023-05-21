import requests

from configs.server_config import rest_api_port

x = requests.post(f'http://127.0.0.1:{rest_api_port}/api/fill_mask', json={
    'x': 'New study links disturbed [MASK] metabolism in depressed '
         'individuals to disruption of the gut microbiome.'
})
print('fill mask:', x.text)

x = requests.post(f'http://127.0.0.1:{rest_api_port}/api/summarize', json={
    'x': 'Depression is a widespread mental health condition '
         'that significantly affects population health. Major '
         'depression is known to cause a range of debilitating '
         'symptoms beyond emotional distress, including cognitive '
         'impairments, motor function problems, inflammation, '
         'disturbances in the immune system, and increased risk '
         'of cardiometabolic disorders and mortality.'
})
print('summarize:', x.text)

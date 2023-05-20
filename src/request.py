import requests

x = requests.post('http://127.0.0.1:5000/api/fill_mask', json={
    'x': 'New study links disturbed [MASK] metabolism in depressed '
         'individuals to disruption of the gut microbiome.'
})
print('fill mask:', x.text)

x = requests.post('http://127.0.0.1:5000/api/summarize', json={
    'x': 'Depression is a widespread mental health condition '
         'that significantly affects population health. Major '
         'depression is known to cause a range of debilitating '
         'symptoms beyond emotional distress, including cognitive '
         'impairments, motor function problems, inflammation, '
         'disturbances in the immune system, and increased risk '
         'of cardiometabolic disorders and mortality.'
})
print('summarize:', x.text)


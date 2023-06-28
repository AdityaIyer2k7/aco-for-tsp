import json
import sys

filename = sys.argv[-1]

with open(filename) as fl: data = fl.read()

data = data.replace('(', '')
data = data.replace(')', '')
data = data.strip(',')

if not (data.startswith('[[') or data.startswith('[\n  [')):
    data = f"[{data}]"

data = json.loads(data)
data.sort()

with open(filename, mode='w') as fl: json.dump(data, fl, indent='  ')

import json

def parse_parameters(row):
    try:
        parameters = json.loads(row.get('参数json', '{}'))
    except Exception:
        parameters = {}
    return parameters

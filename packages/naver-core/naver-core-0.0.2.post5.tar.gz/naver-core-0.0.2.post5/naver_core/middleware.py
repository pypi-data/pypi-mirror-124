import json


def ErrorResponse(e):
    if isinstance(e, dict):
        return e
    error = eval(str(e))
    data = {'data': None, 'state': False,
            'code': error[0], 'message': error[1]}
    res = json.loads(json.dumps(data, indent=4, sort_keys=True, default=str))
    return res


def Ok(e):
    if isinstance(e, dict):
        return e
    data = eval(str(e))
    data = {'data': data, 'state': True, 'code': None, 'message': None}
    res = json.loads(json.dumps(data, indent=4, sort_keys=True, default=str))
    return res

def getValue(input, key):
    data = input.get('data')
    if isinstance(data, dict):
        if key in data:
            return data[key]
        else:
            return None
    else:
        return None

if __name__ == '__main__':
    pass

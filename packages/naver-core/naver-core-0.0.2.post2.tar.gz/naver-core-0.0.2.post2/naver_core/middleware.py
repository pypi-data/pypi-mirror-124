    
import json


 

def ErrorResponse(e):
    print(type(e))
    if isinstance(e, dict):
        return e     
    error = eval(str(e))


    data = {'data':None,'state':False,'code': error[0], 'message': error[1]}
    res = json.loads(json.dumps(data, indent=4, sort_keys=True, default=str))
    return res

def Ok(e): 
    print(type(e))
    if isinstance(e, dict):
        return e  
    data = eval(str(e))
    data = {'data':data,'state':True,'code': None, 'message': None}
    res = json.loads(json.dumps(data, indent=4, sort_keys=True, default=str))
    return res


if __name__ == '__main__':
   pass
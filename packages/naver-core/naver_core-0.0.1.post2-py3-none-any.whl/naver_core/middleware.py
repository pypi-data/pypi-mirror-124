try:
    __import__('pkg_resources').declare_namespace(__name__)
except ImportError:
    __path__ = __import__('pkgutil').extend_path(__path__, __name__)
    
import json



def Ok(e): 
    data = eval(str(e))
    data = {'data':data,'state':True,'code': None, 'message': None}
    res = json.loads(json.dumps(data, indent=4, sort_keys=True, default=str))
    return res
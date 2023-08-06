vars = dict()

def add_var(key, value):
    vars[key] = value
    
def get(key, default):
    return vars.get(key, default)


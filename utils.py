import hashlib;
# hashlib.sha256('bitcoin'.encode()).hexdigest();
def sort_by_key(target:dict):
    sorted_dict = {}
    for key in sorted(target.keys()):
        sorted_dict[key] = target[key]
    return sorted_dict


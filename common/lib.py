def list_to_dict(lst):
    it = iter(lst)
    res_dct = dict(zip(it, it))
    return res_dct


def list_whitespace_remove(lst):
    lst = list(map(lambda x: x.strip(), lst))
    lst = list(filter(lambda x: x != '', lst))
    return lst
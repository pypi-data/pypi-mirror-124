def have_key(response,key, global_search=None):

    if response.get(key):  # 找到了key就直接返回
        return True
    elif global_search:  # 看是否全局
        return _have_key(response, key)
    else:
        return False

def is_equal(response, expect_dict):
    return response == expect_dict

def is_value(response, value, global_search=None):
    response_items = list(response.items())
    if isinstance(value, dict):
        if len(value) == 1:
            value_items = list(value.items())[0]
            if value_items in response_items:
                return True
            elif global_search:
                return _have_value(response_items, value_items)
            else:
                return False


def _have_key(response, key):
    for value in response.values():
        if isinstance(value, dict):
            if value.get(key):
                return True
            else:
                return _have_key(value, key)
        else:
            return False


def _have_value(response_items, value_items):
    for item in response_items:
        if isinstance(item[1], dict):
            _items = list(item[1].items())
            if value_items in _items:
                return True
            else:
                return _have_value(_items, value_items)
        else:
            return False

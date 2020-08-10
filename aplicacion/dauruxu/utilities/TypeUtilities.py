def get_tuple_from_enum(enumeration):
    enum_list = []
    for item in enumeration:
        enum_list.append((item.name, item.name))
    return tuple(enum_list)


def get_tuple_from_dict_key(dict_keys):
    keys_list = []
    for item in dict_keys:
        keys_list.append((item, item))
    return tuple(keys_list)


def tuple_from_list_and_remove_item(list, item_index_to_remove):
    field_names = []
    for items in list:
        field_names.append((str(items.name), str(items.name)))
    field_names.pop(item_index_to_remove)
    return tuple(field_names)


def get_correct_instance_from_object_as_string(object_as_string):
    try:
        corrected = eval(object_as_string)
    except ValueError:
        corrected = object_as_string
    return corrected

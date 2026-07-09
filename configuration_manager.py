test_settings = {
    'Theme':   'dark',
    'Volume':   'high',
    'Notifications':   'enabled'
}
def add_setting(dict_setting, tuple_pair):
    key = tuple_pair[0].lower()
    value = tuple_pair[1].lower()
    if key in dict_setting:
        return f"Setting '{key}' already exists! Cannot adda a new setting with this name."
    else:
        dict_setting[key] = value
        return f"Setting '{key}' added with value '{value}' successfully!"
def update_setting(dict_setting, tuple_pair):
    key = tuple_pair[0].lower()
    value = tuple_pair[1].lower()
    if key in dict_setting:
        dict_setting[key] = value
        return f"Setting {key} updated to {value} successfully!"
    else:
        return f"Setting {key} does not exist! Cannot update a non-existing setting."
def delete_setting(dict_setting, key):
    key = key.lower()
    if key in dict_setting:
        del dict_setting[key]
        return f"Setting {key} deleted successfully!"
    else:
        "Setting not found!"
def view_settings(dict_setting):
    if dict_setting == {}:
        return "No settings available."
    else:
        output_text = 'Current User Settings:\n'
        for key, value in dict_setting.items():
            capital_key = key.capitalize()
            output_text += f"{capital_key}: {value}\n"

ALL_ELEMENTS = -2


def get(url):
    return lambda chrome: chrome.get(url)


def xpath(xpath, index=0):
    if index != ALL_ELEMENTS:
        return lambda chrome: chrome.xpath(xpath)[index]
    else:
        return lambda chrome: chrome.xpath(xpath)


def click():
    def _click(element):
        element.click()
        return element
    return _click


def send_keys(string):
    def _send_keys(element):
        element.send_keys(string)
        return element
    return _send_keys


def return_text():
    def _return_text(element):
        print(element.text)
        return element.text
    return _return_text


RETERN_TEXT = return_text


def do_actions(chrome, action_rows):
    returns = []
    for raw_action in action_rows:
        action_func = parse_action(raw_action)
        returns.append(action_func(chrome))
    return returns


def parse_action(raw_action):
    tupled_action = (raw_action,) if type(raw_action) is str else raw_action
    first_string = tupled_action[0]
    print(first_string)
    if first_string.startswith("http"):
        return get(first_string)

    if len(tupled_action) > 1 and type(tupled_action[1]) is int:
        xpath_index = tupled_action[1]
        rest_action = tupled_action[2:]
    else:
        xpath_index = 0
        rest_action = tupled_action[1:]

    element_find_func = xpath(first_string, index=xpath_index)
    if len(rest_action) == 0:
        action_func = click()
    else:
        if rest_action[0] is RETERN_TEXT:
            action_func = return_text()
        else:
            action_func = send_keys(rest_action[0])
    if xpath_index != ALL_ELEMENTS:
        return lambda chrome: action_func(element_find_func(chrome))
    else:
        return lambda chrome: [action_func(element)
                               for element in element_find_func(chrome)]

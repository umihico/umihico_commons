import codecs


def get_local_html(path):
    with codecs.open(path, 'r', 'utf-8') as f:
        src = f.readlines()
        src = '\n'.join(src)
        return src


def lxmls_to_onetext(lxml_element_list):
    string = ''.join([x.text_content() for x in lxml_element_list])
    return string


def strip_string(string, deletings=(':', ' ', "　", "\n", "\t", "\xa0")):
    if len(string) == 0:
        return string
    for deleting in deletings:
        if string[0] == deleting:
            string = string[1:]
        if string[-1] == deleting:
            string = string[:len(string) - 1]
    string = string.strip()
    return string

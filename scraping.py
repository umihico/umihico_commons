try:
    from lxml_commons import url_to_lxml
    from chrome_wrapper import Chrome
    from proxy import ProxyRequests
    from requests_wrapper import get, get_with_proxy
except (Exception, ) as e:
    from .lxml_commons import url_to_lxml
    from .chrome_wrapper import Chrome
    from .proxy import ProxyRequests
    from .requests_wrapper import get, get_with_proxy

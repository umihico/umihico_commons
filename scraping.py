try:
    from lxml_commons import url_to_lxml
    from chrome_wrapper import Chrome, Keys
    from proxy import ProxyRequests
    from requests_wrapper import get, get_with_proxy
    from tor import get as tor_get
except (Exception, ) as e:
    from .lxml_commons import url_to_lxml
    from .chrome_wrapper import Chrome, Keys
    from .proxy import ProxyRequests
    from .requests_wrapper import get, get_with_proxy, save_img, save_img_response_test_func
    from .tor import get as tor_get

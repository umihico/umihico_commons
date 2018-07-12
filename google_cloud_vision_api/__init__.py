try:
    from request import get_text_dict
except (Exception, ) as e:
    from .request import get_text_dict

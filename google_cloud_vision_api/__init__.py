try:
    from recognize_captcha import recognize_captcha, gen_ocr_pair_on_new_xlsx
except (Exception, ) as e:
    from .recognize_captcha import recognize_captcha, gen_ocr_pair_on_new_xlsx

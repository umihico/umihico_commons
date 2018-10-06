try:
    from requests_wrapper import get
except (Exception, ) as e:
    from .requests_wrapper import get
from collections import OrderedDict
from lxml import html


def get_hint(lxml_element):
    current_element = lxml_element
    hint_string = ''
    while True:
        attributes = ' '.join(
            [k + '=' + v for k, v in current_element.items()])
        hint_string = f"<{current_element.tag} {attributes}>/" + \
            hint_string
        if current_element.tag == 'html':
            break
        current_element = current_element.getparent()
    return hint_string


def url_to_lxml(url, get_func=get):
    lxml_ = html.fromstring(get_func(url).text)
    return lxml_


def add_ths(lxml_table_element):
    trs = lxml_table_element.xpath("//tr")
    row_length = len(trs)
    col_length = max([len(tr.xpath("./*")) for tr in trs])
    if col_length >= 3:
        for element in trs[0].xpath("./*"):
            element.tag = "th"
    if row_length >= 3:
        for element in [tr.xpath("./*")[0] for tr in trs]:
            element.tag = "th"


def table_to_dict(lxml_table_element):
    trs = lxml_table_element.xpath("//tr")
    th_pos_dict = OrderedDict()
    td_pos_dict = OrderedDict()
    for rowint, tr in enumerate(trs):
        th_td = [t for t in tr.xpath(
            "./*") if t.tag == 'td' or t.tag == "th"]
        colint = 0
        for t in th_td:
            current_pos = (rowint, colint)
            if t.tag == "th":
                th_pos_dict[current_pos] = t
            else:
                td_pos_dict[current_pos] = t
            colint += int(t.attrib.get("colspan", 1))
    result = OrderedDict()
    for pos, td in td_pos_dict.items():
        td_row, td_col = pos
        try:
            same_col_th = [(th_row, th) for (th_row, th_col), th in th_pos_dict.items(
            ) if th_col == td_col and th_row < td_row]
            most_close_same_col_th = sorted(
                same_col_th, key=lambda x: x[0], reverse=True)[0][1]
            col_key = most_close_same_col_th.text_content()
        except (Exception, ) as e:
            col_key = ""
        try:
            same_row_th = [(th_col, th) for (th_row, th_col), th in th_pos_dict.items(
            ) if th_col < td_col and th_row == td_row]
            most_close_same_row_th = sorted(
                same_row_th, key=lambda x: x[0], reverse=True)[0][1]
            row_key = most_close_same_row_th.text_content()
        except (Exception, ) as e:
            row_key = ""
        if col_key and row_key:
            key = col_key + ':' + row_key
        else:
            key = col_key or row_key
        result[key] = td.text_content()
    return result


def _test_table_to_dict():
    page_source = """<table class="qik-responsive-06 qik-table qik-table-transform qik-grid-24">
			<thead>
				<tr class="">
					<th class="qik-valign-m qik-align-c qik-align-sd-l qik-ttl-row qik-ttl-row-pt2 qik-grid-3">【業績】</th>
					<th class="qik-valign-m qik-align-c qik-align-sd-l qik-ttl-row qik-ttl-row-pt2 qik-grid-3">売上高</th>
					<th class="qik-valign-m qik-align-c qik-align-sd-l qik-ttl-row qik-ttl-row-pt2 qik-grid-3">営業利益</th>
					<th class="qik-valign-m qik-align-c qik-align-sd-l qik-ttl-row qik-ttl-row-pt2 qik-grid-3">経常利益</th>
					<th class="qik-valign-m qik-align-c qik-align-sd-l qik-ttl-row qik-ttl-row-pt2 qik-grid-3">純利益</th>
					<th class="qik-valign-m qik-align-c qik-align-sd-l qik-ttl-row qik-ttl-row-pt2 qik-grid-3">1株益(円)</th>
					<th class="qik-valign-m qik-align-c qik-align-sd-l qik-ttl-row qik-ttl-row-pt2 qik-grid-3">1株配(円)</th>
				</tr>
			</thead>
			<tbody>

				<tr class="">
					<th class="qik-valign-m qik-align-l qik-align-sd-l qik-ttl-row qik-ttl-row-pt2">連14. 3*</th>
					<td data-title="売上高" class="qik-valign-m qik-align-r qik-align-sd-r">202,387</td>
					<td data-title="営業利益" class="qik-valign-m qik-align-r qik-align-sd-r">2,915</td>
					<td data-title="経常利益" class="qik-valign-m qik-align-r qik-align-sd-r">2,985</td>
					<td data-title="純利益" class="qik-valign-m qik-align-r qik-align-sd-r">2,968</td>
					<td data-title="1株益(円)" class="qik-valign-m qik-align-r qik-align-sd-r">282.6</td>
					<td data-title="1株配(円)" class="qik-valign-m qik-align-r qik-align-sd-r">50</td>
				</tr>


				<tr class="">
					<th class="qik-valign-m qik-align-l qik-align-sd-l qik-ttl-row qik-ttl-row-pt2 xh-highlight">連15. 3*</th>
					<td data-title="売上高" class="qik-valign-m qik-align-r qik-align-sd-r">218,350</td>
					<td data-title="営業利益" class="qik-valign-m qik-align-r qik-align-sd-r">2,460</td>
					<td data-title="経常利益" class="qik-valign-m qik-align-r qik-align-sd-r">2,107</td>
					<td data-title="純利益" class="qik-valign-m qik-align-r qik-align-sd-r">2,433</td>
					<td data-title="1株益(円)" class="qik-valign-m qik-align-r qik-align-sd-r">231.7</td>
					<td data-title="1株配(円)" class="qik-valign-m qik-align-r qik-align-sd-r">50</td>
				</tr>


				<tr class="">
					<th class="qik-valign-m qik-align-l qik-align-sd-l qik-ttl-row qik-ttl-row-pt2">連16. 3*</th>
					<td data-title="売上高" class="qik-valign-m qik-align-r qik-align-sd-r">226,626</td>
					<td data-title="営業利益" class="qik-valign-m qik-align-r qik-align-sd-r">2,433</td>
					<td data-title="経常利益" class="qik-valign-m qik-align-r qik-align-sd-r">2,814</td>
					<td data-title="純利益" class="qik-valign-m qik-align-r qik-align-sd-r">1,799</td>
					<td data-title="1株益(円)" class="qik-valign-m qik-align-r qik-align-sd-r">171.3</td>
					<td data-title="1株配(円)" class="qik-valign-m qik-align-r qik-align-sd-r">50</td>
				</tr>


				<tr class="">
					<th class="qik-valign-m qik-align-l qik-align-sd-l qik-ttl-row qik-ttl-row-pt2">連17. 3</th>
					<td data-title="売上高" class="qik-valign-m qik-align-r qik-align-sd-r">236,561</td>
					<td data-title="営業利益" class="qik-valign-m qik-align-r qik-align-sd-r">3,723</td>
					<td data-title="経常利益" class="qik-valign-m qik-align-r qik-align-sd-r">3,709</td>
					<td data-title="純利益" class="qik-valign-m qik-align-r qik-align-sd-r">2,422</td>
					<td data-title="1株益(円)" class="qik-valign-m qik-align-r qik-align-sd-r">230.7</td>
					<td data-title="1株配(円)" class="qik-valign-m qik-align-r qik-align-sd-r">60記</td>
				</tr>


				<tr class="">
					<th class="qik-valign-m qik-align-l qik-align-sd-l qik-ttl-row qik-ttl-row-pt2">連18. 3</th>
					<td data-title="売上高" class="qik-valign-m qik-align-r qik-align-sd-r">254,783</td>
					<td data-title="営業利益" class="qik-valign-m qik-align-r qik-align-sd-r">4,066</td>
					<td data-title="経常利益" class="qik-valign-m qik-align-r qik-align-sd-r">4,437</td>
					<td data-title="純利益" class="qik-valign-m qik-align-r qik-align-sd-r">3,211</td>
					<td data-title="1株益(円)" class="qik-valign-m qik-align-r qik-align-sd-r">304.3</td>
					<td data-title="1株配(円)" class="qik-valign-m qik-align-r qik-align-sd-r">60</td>
				</tr>


				<tr class="">
					<th class="qik-valign-m qik-align-l qik-align-sd-l qik-ttl-row qik-ttl-row-pt2">連19. 3予</th>
					<td data-title="売上高" class="qik-valign-m qik-align-r qik-align-sd-r">267,000</td>
					<td data-title="営業利益" class="qik-valign-m qik-align-r qik-align-sd-r">4,800</td>
					<td data-title="経常利益" class="qik-valign-m qik-align-r qik-align-sd-r">4,600</td>
					<td data-title="純利益" class="qik-valign-m qik-align-r qik-align-sd-r">3,200</td>
					<td data-title="1株益(円)" class="qik-valign-m qik-align-r qik-align-sd-r">296.7</td>
					<td data-title="1株配(円)" class="qik-valign-m qik-align-r qik-align-sd-r">60</td>
				</tr>


				<tr class="">
					<th class="qik-valign-m qik-align-l qik-align-sd-l qik-ttl-row qik-ttl-row-pt2">連20. 3予</th>
					<td data-title="売上高" class="qik-valign-m qik-align-r qik-align-sd-r">270,000</td>
					<td data-title="営業利益" class="qik-valign-m qik-align-r qik-align-sd-r">5,000</td>
					<td data-title="経常利益" class="qik-valign-m qik-align-r qik-align-sd-r">4,800</td>
					<td data-title="純利益" class="qik-valign-m qik-align-r qik-align-sd-r">3,300</td>
					<td data-title="1株益(円)" class="qik-valign-m qik-align-r qik-align-sd-r">306.0</td>
					<td data-title="1株配(円)" class="qik-valign-m qik-align-r qik-align-sd-r">60</td>
				</tr>


				<tr class="">
					<th class="qik-valign-m qik-align-l qik-align-sd-l qik-ttl-row qik-ttl-row-pt2">中17. 9</th>
					<td data-title="売上高" class="qik-valign-m qik-align-r qik-align-sd-r">120,458</td>
					<td data-title="営業利益" class="qik-valign-m qik-align-r qik-align-sd-r">2,246</td>
					<td data-title="経常利益" class="qik-valign-m qik-align-r qik-align-sd-r">2,396</td>
					<td data-title="純利益" class="qik-valign-m qik-align-r qik-align-sd-r">1,633</td>
					<td data-title="1株益(円)" class="qik-valign-m qik-align-r qik-align-sd-r">155.5</td>
					<td data-title="1株配(円)" class="qik-valign-m qik-align-r qik-align-sd-r">0</td>
				</tr>


				<tr class="">
					<th class="qik-valign-m qik-align-l qik-align-sd-l qik-ttl-row qik-ttl-row-pt2">中18. 9予</th>
					<td data-title="売上高" class="qik-valign-m qik-align-r qik-align-sd-r">122,000</td>
					<td data-title="営業利益" class="qik-valign-m qik-align-r qik-align-sd-r">2,200</td>
					<td data-title="経常利益" class="qik-valign-m qik-align-r qik-align-sd-r">2,100</td>
					<td data-title="純利益" class="qik-valign-m qik-align-r qik-align-sd-r">1,600</td>
					<td data-title="1株益(円)" class="qik-valign-m qik-align-r qik-align-sd-r">148.4</td>
					<td data-title="1株配(円)" class="qik-valign-m qik-align-r qik-align-sd-r">0</td>
				</tr>


				<tr class="">
					<th class="qik-valign-m qik-align-l qik-align-sd-l qik-ttl-row qik-ttl-row-pt2">会19. 3予</th>
					<td data-title="売上高" class="qik-valign-m qik-align-r qik-align-sd-r">267,000</td>
					<td data-title="営業利益" class="qik-valign-m qik-align-r qik-align-sd-r">4,800</td>
					<td data-title="経常利益" class="qik-valign-m qik-align-r qik-align-sd-r">4,600</td>
					<td data-title="純利益" class="qik-valign-m qik-align-r qik-align-sd-r">3,200</td>
					<td data-title="1株益(円)" class="qik-valign-m qik-align-r qik-align-sd-r">-</td>
					<td data-title="1株配(円)" class="qik-valign-m qik-align-r qik-align-sd-r">(18.5.10)</td>
				</tr>

				<tr>
					<th class="qik-valign-m qik-align-l qik-align-sd-l qik-ttl-row qik-ttl-row-pt2">&nbsp;</th>
					<td data-title="売上高" class="qik-valign-m qik-align-r qik-align-sd-r">&nbsp;</td>
					<td data-title="営業利益" class="qik-valign-m qik-align-r qik-align-sd-r">&nbsp;</td>
					<td data-title="経常利益" class="qik-valign-m qik-align-r qik-align-sd-r">&nbsp;</td>
					<td data-title="純利益" class="qik-valign-m qik-align-r qik-align-sd-r">&nbsp;</td>
					<td data-title="1株益(円)" class="qik-valign-m qik-align-r qik-align-sd-r">&nbsp;</td>
					<td data-title="1株配(円)" class="qik-valign-m qik-align-r qik-align-sd-r">&nbsp;</td>
				</tr>
				<tr>
					<th class="qik-valign-m qik-align-l qik-align-sd-l qik-ttl-row qik-ttl-row-pt2">&nbsp;</th>
					<td data-title="売上高" class="qik-valign-m qik-align-r qik-align-sd-r">&nbsp;</td>
					<td data-title="営業利益" class="qik-valign-m qik-align-r qik-align-sd-r">&nbsp;</td>
					<td data-title="経常利益" class="qik-valign-m qik-align-r qik-align-sd-r">&nbsp;</td>
					<td data-title="純利益" class="qik-valign-m qik-align-r qik-align-sd-r">&nbsp;</td>
					<td data-title="1株益(円)" class="qik-valign-m qik-align-r qik-align-sd-r">&nbsp;</td>
					<td data-title="1株配(円)" class="qik-valign-m qik-align-r qik-align-sd-r">&nbsp;</td>
				</tr>
				<tr>
					<th class="qik-valign-m qik-align-l qik-align-sd-l qik-ttl-row qik-ttl-row-pt2">&nbsp;</th>
					<td data-title="売上高" class="qik-valign-m qik-align-r qik-align-sd-r">&nbsp;</td>
					<td data-title="営業利益" class="qik-valign-m qik-align-r qik-align-sd-r">&nbsp;</td>
					<td data-title="経常利益" class="qik-valign-m qik-align-r qik-align-sd-r">&nbsp;</td>
					<td data-title="純利益" class="qik-valign-m qik-align-r qik-align-sd-r">&nbsp;</td>
					<td data-title="1株益(円)" class="qik-valign-m qik-align-r qik-align-sd-r">&nbsp;</td>
					<td data-title="1株配(円)" class="qik-valign-m qik-align-r qik-align-sd-r">&nbsp;</td>
				</tr>
				<tr>
					<th class="qik-valign-m qik-align-l qik-align-sd-l qik-ttl-row qik-ttl-row-pt2">&nbsp;</th>
					<td data-title="売上高" class="qik-valign-m qik-align-r qik-align-sd-r">&nbsp;</td>
					<td data-title="営業利益" class="qik-valign-m qik-align-r qik-align-sd-r">&nbsp;</td>
					<td data-title="経常利益" class="qik-valign-m qik-align-r qik-align-sd-r">&nbsp;</td>
					<td data-title="純利益" class="qik-valign-m qik-align-r qik-align-sd-r">&nbsp;</td>
					<td data-title="1株益(円)" class="qik-valign-m qik-align-r qik-align-sd-r">&nbsp;</td>
					<td data-title="1株配(円)" class="qik-valign-m qik-align-r qik-align-sd-r">&nbsp;</td>
				</tr>
				<tr>
					<th class="qik-valign-m qik-align-l qik-align-sd-l qik-ttl-row qik-ttl-row-pt2">&nbsp;</th>
					<td data-title="売上高" class="qik-valign-m qik-align-r qik-align-sd-r">&nbsp;</td>
					<td data-title="営業利益" class="qik-valign-m qik-align-r qik-align-sd-r">&nbsp;</td>
					<td data-title="経常利益" class="qik-valign-m qik-align-r qik-align-sd-r">&nbsp;</td>
					<td data-title="純利益" class="qik-valign-m qik-align-r qik-align-sd-r">&nbsp;</td>
					<td data-title="1株益(円)" class="qik-valign-m qik-align-r qik-align-sd-r">&nbsp;</td>
					<td data-title="1株配(円)" class="qik-valign-m qik-align-r qik-align-sd-r">&nbsp;</td>
				</tr>
				<tr>
					<th class="qik-valign-m qik-align-l qik-align-sd-l qik-ttl-row qik-ttl-row-pt2">&nbsp;</th>
					<td data-title="売上高" class="qik-valign-m qik-align-r qik-align-sd-r">&nbsp;</td>
					<td data-title="営業利益" class="qik-valign-m qik-align-r qik-align-sd-r">&nbsp;</td>
					<td data-title="経常利益" class="qik-valign-m qik-align-r qik-align-sd-r">&nbsp;</td>
					<td data-title="純利益" class="qik-valign-m qik-align-r qik-align-sd-r">&nbsp;</td>
					<td data-title="1株益(円)" class="qik-valign-m qik-align-r qik-align-sd-r">&nbsp;</td>
					<td data-title="1株配(円)" class="qik-valign-m qik-align-r qik-align-sd-r">&nbsp;</td>
				</tr>
				<tr>
					<th class="qik-valign-m qik-align-l qik-align-sd-l qik-ttl-row qik-ttl-row-pt2">&nbsp;</th>
					<td data-title="売上高" class="qik-valign-m qik-align-r qik-align-sd-r">&nbsp;</td>
					<td data-title="営業利益" class="qik-valign-m qik-align-r qik-align-sd-r">&nbsp;</td>
					<td data-title="経常利益" class="qik-valign-m qik-align-r qik-align-sd-r">&nbsp;</td>
					<td data-title="純利益" class="qik-valign-m qik-align-r qik-align-sd-r">&nbsp;</td>
					<td data-title="1株益(円)" class="qik-valign-m qik-align-r qik-align-sd-r">&nbsp;</td>
					<td data-title="1株配(円)" class="qik-valign-m qik-align-r qik-align-sd-r">&nbsp;</td>
				</tr>
				<tr>
					<th class="qik-valign-m qik-align-l qik-align-sd-l qik-ttl-row qik-ttl-row-pt2">&nbsp;</th>
					<td data-title="売上高" class="qik-valign-m qik-align-r qik-align-sd-r">&nbsp;</td>
					<td data-title="営業利益" class="qik-valign-m qik-align-r qik-align-sd-r">&nbsp;</td>
					<td data-title="経常利益" class="qik-valign-m qik-align-r qik-align-sd-r">&nbsp;</td>
					<td data-title="純利益" class="qik-valign-m qik-align-r qik-align-sd-r">&nbsp;</td>
					<td data-title="1株益(円)" class="qik-valign-m qik-align-r qik-align-sd-r">&nbsp;</td>
					<td data-title="1株配(円)" class="qik-valign-m qik-align-r qik-align-sd-r">&nbsp;</td>
				</tr>
				<tr>
					<th class="qik-valign-m qik-align-l qik-align-sd-l qik-ttl-row qik-ttl-row-pt2">&nbsp;</th>
					<td data-title="売上高" class="qik-valign-m qik-align-r qik-align-sd-r">&nbsp;</td>
					<td data-title="営業利益" class="qik-valign-m qik-align-r qik-align-sd-r">&nbsp;</td>
					<td data-title="経常利益" class="qik-valign-m qik-align-r qik-align-sd-r">&nbsp;</td>
					<td data-title="純利益" class="qik-valign-m qik-align-r qik-align-sd-r">&nbsp;</td>
					<td data-title="1株益(円)" class="qik-valign-m qik-align-r qik-align-sd-r">&nbsp;</td>
					<td data-title="1株配(円)" class="qik-valign-m qik-align-r qik-align-sd-r">&nbsp;</td>
				</tr>
				<tr>
					<th class="qik-valign-m qik-align-l qik-align-sd-l qik-ttl-row qik-ttl-row-pt2">&nbsp;</th>
					<td data-title="売上高" class="qik-valign-m qik-align-r qik-align-sd-r">&nbsp;</td>
					<td data-title="営業利益" class="qik-valign-m qik-align-r qik-align-sd-r">&nbsp;</td>
					<td data-title="経常利益" class="qik-valign-m qik-align-r qik-align-sd-r">&nbsp;</td>
					<td data-title="純利益" class="qik-valign-m qik-align-r qik-align-sd-r">&nbsp;</td>
					<td data-title="1株益(円)" class="qik-valign-m qik-align-r qik-align-sd-r">&nbsp;</td>
					<td data-title="1株配(円)" class="qik-valign-m qik-align-r qik-align-sd-r">&nbsp;</td>
				</tr>
			</tbody>
	</table>"""
    from lxml import html
    lxml = html.fromstring(page_source)
    pprint(table_to_dict(lxml.xpath("//table")[0]))


def _test_add_ths():
    page_source = """<table class="qik-table qik-grid-15 qik-grid-sd-24 xh-highlight">
	<tbody><tr>
		<th class="qik-valign-m qik-align-c qik-align-sd-c qik-ttl-row qik-ttl-row-pt2 qik-grid-3">ＪＱ(Ｓ)</th>
		<th class="qik-valign-m qik-align-c qik-align-sd-c qik-ttl-row qik-ttl-row-pt2 qik-grid-3">高値</th>
		<th class="qik-valign-m qik-align-c qik-align-sd-c qik-ttl-row qik-ttl-row-pt2 qik-grid-3">安値</th>
	</tr>
	<tr>
		<td class="left qik-valign-m qik-align-l">05-16</td>
		<td class="qik-valign-m qik-align-r">1239(06)</td>
		<td class="qik-valign-m qik-align-r">84(12)</td>
	</tr>
	<tr>
		<td class="left qik-valign-m qik-align-l">17</td>
		<td class="qik-valign-m qik-align-r">215(7)</td>
		<td class="qik-valign-m qik-align-r">138(5)</td>
	</tr>


	<tr>
		<td class="left qik-valign-m qik-align-l">18.1-5</td>
		<td class="qik-valign-m qik-align-r">288(5)</td>
		<td class="qik-valign-m qik-align-r">160(1)</td>
	</tr>

    </tbody></table>"""
    from lxml import html
    lxml = html.fromstring(page_source)
    table = lxml.xpath("//table")[0]
    add_ths(table)
    pprint(table_to_dict(table))


if __name__ == '__main__':
    from pprint import pprint
    _test_add_ths()
    _test_table_to_dict()

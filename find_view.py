from lxml import etree

def convert_to_int(text):
    num = text.split(' ')[0]
    if(num[-1] == 'K'):
        return int(float(num[:-1]) * 1000)
    elif(num[-1] == 'M'):
        return int(float(num[:-1]) * 1000000)
    else: 
        return int(num)

def get_text_from_span_containing(html_content, search_text = 'views'):

    # Parse HTML content
    tree = etree.HTML(html_content)

    # Tìm span chứa text cụ thể
    xpath = f"//span[contains(text(), '{search_text}')]"
    elements = tree.xpath(xpath)

    # Kiểm tra nếu có element được tìm thấy
    if elements:
        # Lấy text đầy đủ từ span đầu tiên (nếu có nhiều)
        return convert_to_int(elements[0].text.strip())
    else:
        return f"Không tìm thấy span nào chứa '{search_text}'"


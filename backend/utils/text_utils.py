"""
文本处理工具函数（从原 zjyc_api.py 抽取）
"""
import re


def camel_case(s: str) -> str:
    """下划线命名转驼峰命名（首字母小写）"""
    parts = s.split('_')
    if len(parts) <= 1:
        return s
    return parts[0] + ''.join(part.capitalize() for part in parts[1:])


def full_to_half_width(text):
    """全角字符转半角字符"""
    result = []
    for char in text:
        code = ord(char)
        if code == 0x3000:
            result.append(' ')
        elif 0xFF01 <= code <= 0xFF5E:
            result.append(chr(code - 0xFEE0))
        else:
            result.append(char)
    return ''.join(result)


def preprocess_chinese_text(text):
    """预处理中文字符：处理全角半角、大小写、特殊字符"""
    if not text:
        return ""
    text = full_to_half_width(text)
    text = text.strip()
    text = text.upper()
    pattern = re.compile(r'[^\u4e00-\u9fa5a-zA-Z0-9;:\(\)，,.\-+ ]')
    text = pattern.sub('', text)
    text = re.sub(r'\s+', ' ', text)
    return text


def parse_event_field(field_value, field_type):
    """解析事件字段，提取日期和事件描述"""
    events = []
    if not field_value:
        return events
    processed_value = preprocess_chinese_text(field_value)
    if not processed_value:
        return events
    event_items = [item.strip() for item in re.split(r'[;；]', processed_value) if item.strip()]
    for item in event_items:
        year_match = re.search(r'\((\d{4})年\)', item)
        if not year_match:
            continue
        year = year_match.group(1)
        event_desc = re.sub(r'^[\u4e00-\u9fa5]+：?', '', item)
        event_desc = re.sub(r'\(\d{4}年\)：?', '', event_desc)
        event_desc = event_desc.strip()
        level = "市级" if "市级" in item else "省级及以上"
        events.append({
            "date": f"{year}-01",
            "event": f"{level}：{event_desc}",
            "type": field_type
        })
    return events

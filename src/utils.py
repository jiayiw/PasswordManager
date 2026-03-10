def fullwidth_to_halfwidth(text: str) -> str:
    """将全角字符转换为半角字符"""
    result = []
    for char in text:
        code = ord(char)
        if code == 0x3000:
            result.append(" ")
        elif 0xFF01 <= code <= 0xFF5E:
            result.append(chr(code - 0xFEE0))
        else:
            result.append(char)
    return "".join(result)

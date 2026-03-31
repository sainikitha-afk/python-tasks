import re

TOKENS = [
    ("FN", r"fn"),
    ("LET", r"let"),
    ("RETURN", r"return"),
    ("IF", r"if"),
    ("PRINT", r"print"),
    ("INT", r"\d+"),
    ("IDENT", r"[a-zA-Z_]\w*"),
    ("PLUS", r"\+"),
    ("MINUS", r"-"),
    ("LPAREN", r"\("),
    ("RPAREN", r"\)"),
    ("LBRACE", r"\{"),
    ("RBRACE", r"\}"),
    ("ASSIGN", r"="),
    ("LTE", r"<="),
    ("STRING", r'"[^"]*"'),
    ("SKIP", r"[ \t\n]+"),
]

def tokenize(code):
    tokens = []
    while code:
        for name, pattern in TOKENS:
            match = re.match(pattern, code)
            if match:
                value = match.group(0)
                if name != "SKIP":
                    tokens.append((name, value))
                code = code[len(value):]
                break
        else:
            raise SyntaxError(f"Unknown token: {code[0]}")
    tokens.append(("EOF", None))
    return tokens
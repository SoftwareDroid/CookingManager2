#https://stackoverflow.com/questions/1976007/what-characters-are-forbidden-in-windows-and-linux-directory-names
_forbidden_chars = ["/","\\","<",">",'"',"'","|","?","*",":"," ","." ]
_replace_char = ""

def is_fillname_ok(name: str) -> bool:
    for c in _forbidden_chars:
        if c in name:
            return False
    return True

def create_ok_filename(name: str) -> str:
    for c in _forbidden_chars:
        name = name.replace(c,_replace_char)
    return name

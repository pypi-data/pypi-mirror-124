import namu

def run():
    """나무 인프리터를 실행합니다."""
    while True:
        text = input('나무 > ')
        if text.strip() == '': continue
        result, error = namu.run('<입력>', text)
        
        if error: print(error.as_string())
        elif result:
            if hasattr(result, 'elements') and len(result.elements) == 1:
                print(repr(result.elements[0]))
            else:
                print(repr(result))
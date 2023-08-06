def symbols_in(text, symbol, i=0):
    length:int = len(text)
    letter = ''
    while i < length:
        letter += symbol+text[i]+symbol
        i+=1
    return letter

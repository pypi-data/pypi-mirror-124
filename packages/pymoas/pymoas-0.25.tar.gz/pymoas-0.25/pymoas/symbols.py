engl = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L',
        'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
rus = ["а", "б", "в", "г", "д", "е", "ё", "ж", "з", "и", "й", "к", "л", "м", "н", "о",
       "п", "р", "с", "т", "у", "ф", "х", "ц", "ч", "ш", "щ", "ъ", "ы", "ь", "э", "ю", "я"]


def symbols_in(text, symbol):
    i = 0
    letter = ''
    length: int = len(text)
    while i < length:
        letter += symbol+text[i]+symbol
        i += 1
    return letter


def words_plus_list(words, arg, string=False, cow=False):
    i = 0
    if string == False:
        letter = []
    elif string == True:
        letter = ''
    while i < len(arg):
        if string == True:
            if cow == False:
                letter += words + ' ' + arg[i]+'\n'
            elif cow == True:
                letter += '"'+words + ' ' + arg[i]+'"'+'\n'

        else:
            letter.append(words + ' ' + arg[i])
        i += 1

    return letter


def restr(arg, arr=False, split=True):
    i = 0
    if arr == True:
        letter = []
        while i < len(arg):
            if split == False:
                letter.append(str(arg[i]))
            elif split == True:
                letter += str(arg[i])
            i += 1
    elif arr == False:
        letter = ""
        while i < len(arg):
            if split == False:
                letter += str(arg[i])
            elif split == True:
                letter += str(arg[i]) + '\n'
            i += 1
    return letter


def numut(arg):
    letter = []
    i = 1
    while i <= arg:
        letter.append(i)
        i += 1
    return letter


def strmath_minus(arg1, arg2):
    letter = ''
    i = 0
    result = arg1
    while i > 0:
        result = result - arg2
        letter += str(result) + ' - '+str(arg2) + '\n'
        i += 1
    return letter



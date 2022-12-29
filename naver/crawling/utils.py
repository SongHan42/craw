   
def array_to_string(array):
    s = ""
    for arg in array:
        s += arg + ","
    s = s[:-1]
    return (s)

def only_num_price(s):
    arr = s.split(" ")

    if arr[-1] == "(품절)":
        if arr[-2].find("원)") != -1:
            return arr[-2].replace("원)", "").replace(",", "").replace("(", "").replace("+", "")
    elif arr[-1].find("원)") != -1:
        return arr[-1].replace("원)", "").replace(",", "").replace("(", "").replace("+", "")
    return "0"

def remove_price_single(text):
    t = text.split(' ')
    if t[-1] == "(품절)":
        if t[-2].find("원)") != -1:
            option_str  = ""
            for str in t[:-2]:
                option_str += str + " "
            return option_str[:-1]
        else:
            return text[:text.rfind(" (")]
    elif t[-1].find("원)") != -1:
        return text[:text.rfind(" (")]
    else:
        return text

def remove_price(array) :
    ret = []

    for arr in array:
        t = arr.split(' ')
        if t[-1] == "(품절)":
            if t[-2].find("원)") != -1:
                option_str  = ""
                for str in t[:-2]:
                    option_str += str + " "
                ret+= [option_str[:-1]]
            else:
                ret += [arr[:arr.rfind("(")]]
        elif t[-1].find("원)") != -1:
            ret += [arr[:arr.rfind("(")]]
        else:
            ret += [arr]
    return (ret)
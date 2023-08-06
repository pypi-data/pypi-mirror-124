Keys = ["a", "z", "e", "r", "t", "y", "u", "i", "o", "p", "q", "s", "²",  "d", "f", "g", "h", "j", "k", "l", "m", "w", "x", "c", "v", "b", "n", "1", "2", "3", "4", "5", "6", "7", "8", "9", "0", "é", "à", "è", " ", "A", "Z", "E", "R", "T", "Y", "U", "I", "O", "P", "Q", "S", "D", "F", "G", "H", "J", "K", "L", "M", "W", "X", "C", "V", "B", "N", "?", ",", ";", ".", ":", "/", "!", ")", "(", "^", "'", "+", "-", "=", "[", "]", "{", "}", "ê", "¨", "@", "-", ",", "/", "'", "<", ">", "_", "-", "~", "#", "|", "ç", "*", "&", "°"]

def chiffrerII(msg):
    return msg

def chiffrerI(msg):

    return msg

def dechiffrer(msg):
    New_Message = ","

    m = msg.split(".")
    for Number in m:
        try:
            index = Keys[int(Number)]
            New_Message = str(New_Message) + str(index)
        except:
            pass
    New_Message = New_Message.replace(",", "")
    return New_Message

def chiffrer(msg):
    New_Message = ","
    for Letter in msg:
        if Letter in Keys:
            index = Keys.index(Letter)
            New_Message = str(New_Message) + "." + str(index)
    New_Message = New_Message.replace(",", "")
    return New_Message
rulelanguages = ["english","spanish"]
def get_rules():
    f = open("rules", "r")
    f1 = f.readlines()
    rulemessages = {}
    key = ""
    message = ""
    for i in f1:
        i=i.rstrip()
        if i in rulelanguages:
            key = i
        elif i:
            message = message+i+"\n"
        else:
            rulemessages[key] = message
            message = ""
            key = ""
    return rulemessages

def ruleprint(language = "english"):
    message = ""
    if language not in rulelanguages:
        message = "Sorry, this language does not have the translation yet. Here are the English ones: \n"
        language = "english"
    resp = get_rules()
    message = message+resp[language]
    return message



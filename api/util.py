from firebase import firebase
import re


firebase = firebase.FirebaseApplication("https://berlinabot.firebaseio.com", None)

def get_data(url):
    result = firebase.get(url, None)
    if result:
        return result
    else:
        return None

def remove_html(text, nl=True):
    if text:
        if nl == True:
            return re.sub('<[^<]+?>', '\n', text)
        else:
            return re.sub('<[^<]+?>', '', text)
    else:
        return text

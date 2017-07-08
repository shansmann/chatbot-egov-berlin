from firebase import firebase
firebase = firebase.FirebaseApplication("https://berlinabot.firebaseio.com", None)

def get_data(url):
    result = firebase.get(url, None)
    if result:
        return result
    else:
        return None

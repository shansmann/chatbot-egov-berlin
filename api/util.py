"""
util script
"""

from firebase import firebase
import re


firebase = firebase.FirebaseApplication("https://berlinabot.firebaseio.com", None)

def get_data(url):
    """
    get data from firebase
    """
    result = firebase.get(url, None)
    if result:
        return result
    else:
        return None

def remove_html(text, nl=True):
    """
    remove html elements
    """
    if text:
        if nl == True:
            return re.sub('<[^<]+?>', '\n', text)
        else:
            return re.sub('<[^<]+?>', '', text)
    else:
        return text

def split_by_spaces(sentence, max_length):
    """
    Splits sentence into chunks, preferably by spaces.
    """
    start = 0
    sentence_length = len(sentence)
    while sentence_length - start > max_length:
        space_index = sentence.rfind(' ', start, start + max_length)
        if space_index == -1:
            yield sentence[start:start + max_length]
            start = start + max_length
        else:
            yield sentence[start:space_index]
            start = space_index + 1

    if start < sentence_length:
        yield sentence[start:]


def split_into_sentences(text):
    """
    Split into sentences by punctuation. Return only non-empty trimmed ones
    """
    sentences = re.findall('([^\?\.\!]*[\?\.\!]*)', text)
    trimmed_sentences = [x.strip() for x in sentences]
    return [x for x in trimmed_sentences if x]


def split_message(text, max_length=640):
    """
    Splits message into paragraphs. In edge cases paragraphs split will be in the middle of the sentence.
    """
    res = []
    sub_message = ''
    sentences = split_into_sentences(text)
    for sentence in sentences:
        new_sub_message = sub_message + ' ' + sentence if sub_message else sentence
        if len(sentence) > max_length:
            res.extend(split_by_spaces(sentence, max_length))
        elif len(new_sub_message) > max_length:
            if len(sub_message) > 0:
                res.append(sub_message)
            sub_message = sentence
        else:
            sub_message = new_sub_message
    if len(sub_message) > 0:
        res.append(sub_message)
    return res

import json


f = open('wikiferheng.json', 'r', encoding='utf-8')
data = json.load(f)
all_words = data['all_words']


def get_all_words():
    return all_words


def find(word):
    word = word.strip()
    return [word_item for word_item in all_words if word_item['word'] == word]


def find_one(word):
    word = word.strip()
    return find(word)[0]


def get_synonyms(word):
    word = word.strip()
    try:
        synonyms = find_one(word)['senses'][0]['synonyms']
        if synonyms is not None:
            return {'synonyms': synonyms}
        else:
            return {'error': word + ' has no synonyms'}
    except KeyError as ex:
        return {'error': word + ' has no synonyms'}


def get_glosses(word):
    word = word.strip()
    try:
        glosses = find_one(word)['senses'][0]['glosses']
        if glosses is not None:
            return {'glosses': glosses}
        else:
            return {'error': word + ' has no glosses'}
    except KeyError as ex:
        return {'error': word + ' has no glosses'}


def get_tags(word):
    word = word.strip()
    try:
        tags = find_one(word)['senses'][0]['tags']
        if tags is not None:
            return {'tags': tags}
        else:
            return {'tags': word + ' has no tags'}
    except KeyError as ex:
        return {'error': word + ' has no tags'}


def get_form_of(word):
    word = word.strip()
    try:
        form_of = find_one(word)['senses'][0]['form_of']
        if form_of is not None:
            return {'form_of': form_of}
        else:
            return {'form_of': word + ' has no form of'}
    except KeyError as ex:
        return {'error': word + ' has no form of'}


def get_pos(word):
    word = word.strip()
    try:
        pos = find_one(word)['pos']
        if pos is not None:
            return {'pos': pos}
        else:
            return {'pos': word + ' position is not available'}
    except KeyError as ex:
        return {'error': word + ' position is not available'}


def get_sounds(word):
    word = word.strip()
    try:
        sounds = find_one(word)['sounds']
        if sounds is not None:
            return {'sounds': sounds}
        else:
            return {'sounds': word + ' sounds is not available'}
    except KeyError as ex:
        return {'error': word + ' sounds is not available'}


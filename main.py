import string
import pymorphy2

morph = pymorphy2.MorphAnalyzer()

def lemmatize_word(word):
    parsed = morph.parse(word)[0]
    return parsed.normal_form

def lemmatize_text(text):
    words = text.split()
    lemmatized_words = [lemmatize_word(word) for word in words]
    return ' '.join(lemmatized_words)

def remove_punctuation(text):
    translator = str.maketrans('', '', string.punctuation + '––')
    return text.translate(translator)

def make_pairs(ind_words, n=1):
    for i in range(len(ind_words) - n):
        yield tuple(ind_words[i:i + n]), ind_words[i + n]

def make_dict(text, n):
    words = text.split()
    pair = make_pairs(words, n)

    word_dict = {}
    for word_tuple, next_word in pair:
        if word_tuple in word_dict:
            if next_word in word_dict[word_tuple]:
                word_dict[word_tuple][next_word] += 1
            else:
                word_dict[word_tuple][next_word] = 1
        else:
            word_dict[word_tuple] = {next_word: 1}
    return word_dict

def get_most_frequent_next_word(word_dict, word_tuple):
    if word_tuple in word_dict:
        next_words = word_dict[word_tuple]
        most_frequent_next_word = max(next_words, key=next_words.get)
        return most_frequent_next_word
    else:
        return None

data = open('lider.txt', encoding='utf8').read()
copy = remove_punctuation(data)
text = lemmatize_text(remove_punctuation(data))

initial_words = input(f"Введите слова для поиска: ").lower()
n=len(initial_words.split())
if n==' ':
    print('Вы ничего не ввели')


word_dict = make_dict(text, n)
lemmatized_input = ' '.join([lemmatize_word(word) for word in initial_words.split()])
word_tuple = tuple(lemmatized_input.split())

while n != 0:
    next_word = get_most_frequent_next_word(word_dict, word_tuple)
    if next_word:
        next_word_index = text.split().index(next_word)
        print('Подсказка следующего слова:', copy.split()[next_word_index])
        break
    else:
        n -= 1
        word_dict = make_dict(text, n)
        lemmatized_input = ' '.join([lemmatize_word(word) for word in initial_words.split()[:n]])
        word_tuple = tuple(lemmatized_input.split())
else:
    print('Ничего не найдено')

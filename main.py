import re
import nltk


def handle_text(text):
    text = text.lower()
    text = re.sub(r"[\s\n]+", ' ', text)
    text = re.sub(r"[,+!?.;:…()—«»“”-]+", '', text)
    return text


authors = ["Pushkin.txt", "Gogol.txt"]

profiles = {}

n = 4

alpha = 5

# Сформируем профили авторов
for author in authors:
    # Считывание тренировочного текста
    with open("trainingData/" + author, encoding='utf-8') as f:
        s = f.read()
    # Предварительная обработка текста
    s = handle_text(s)
    s = list(s)  # Разбиваем весь текст по сивмолам
    tetragram_list = list(nltk.ngrams(s, n))  # Получаем тетраграммы из исходного текста
    frequency = nltk.FreqDist(tetragram_list)  # Подсчёт частоты появления всех тетраграмм
    # Формируем профиль автора
    authorProfile = {}
    for item in sorted(frequency, key=frequency.get, reverse=True)[:alpha]:
        authorProfile[item] = frequency[item] / (len(s) / n)
    # Добавляем профиль автора в список
    profiles[author] = authorProfile

testTextProfile = {}

# Теперь считаем исследуемый текст и сравним его профиль с профилем каждого из авторов
with open("testData/test.txt", encoding='utf-8') as f:
    test = f.read()
    test = handle_text(test)
    test = list(test)
    # Составим профиль текста с помощью тетраграмм
    testProfile = nltk.ngrams(test, n)
    testProfile = nltk.FreqDist(testProfile)
    # Выберем 5 наиболее часто встречающихся тетраграмм
    for item in sorted(testProfile, key=testProfile.get, reverse=True)[:alpha]:
        testTextProfile[item] = testProfile[item] / (len(test) / n)

# Пройдёмся по каждому из авторов и вычислим "расстояние" между профилем автора и профилем текста
distances = {}
for author in authors:
    actual_distance = 0
    #print("AUTHOR:", author)
    for k in profiles[author].keys():
        #print("DEBUG: k =", k, "profiles[author][k] =", profiles[author][k])
        if k in testTextProfile:
            #print(1)
            actual_distance += abs(profiles[author][k] - testTextProfile[k])
        else:
            #print(2)
            actual_distance += profiles[author][k]
    #print("DEBUG: distance for", author, "is", actual_distance)
    distances[author] = actual_distance

print("Results\n")
for author in authors:
    print(author, '->', distances[author])
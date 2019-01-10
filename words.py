import flask
import random
import urllib
from bs4 import BeautifulSoup

app = flask.Flask(__name__)
words = None


def read_word_count():
    with open("./files/words.txt", "r+", encoding="utf8")as f:
        return len(f.readlines())


def read_words():
    with open("./files/words.txt", "r+", encoding="utf8")as f:
        words = [i.replace("\n", "") for i in f.readlines()
                 if i and i != "" and i != "\n"]
        return words


def read_random_word():
    global words
    if not words:
        words = read_words()
    random.shuffle(words)
    return words[0]


@app.route('/')
def home():
    return flask.render_template('index.html')


@app.route("/word", methods=["GET"])
def get_word():
    return flask.jsonify({
        "word": read_random_word(),
        "index": get_index()
    })


@app.route("/finish", methods=["GET"])
def finish_process():
    index = get_index()
    words_length = read_word_count()
    rate = int(round(((index + 1) * 100) / words_length))
    result = {
        "rate": rate,
        "result": "You have completed {}% of test!".format(rate),
        "index": index
    }
    return flask.jsonify(result)


def get_index():
    index = flask.request.args.get("index")
    if not index:
        index = 0
    else:
        index = int(index)

    return index


@app.route("/learn", methods=["GET"])
def learn():
    word = flask.request.args.get("word")
    url = "http://tureng.com/en/turkish-english/"+urllib.parse.quote_plus(word)
    page = urllib.request.urlopen(url)
    soup = BeautifulSoup(page, "html.parser")
    table = soup.find('table', attrs={'id': 'englishResultsTable'})
    rows = table.find_all('tr')
    data = []
    for row in rows:
        cols = row.find_all('td')
        cols = [ele.text.strip() for ele in cols]
        if cols and len(cols) > 3:
            data.append(cols[3])

    return flask.jsonify(data)


if __name__ == '__main__':
    # learn("book")
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.run(host='0.0.0.0', port=2442)

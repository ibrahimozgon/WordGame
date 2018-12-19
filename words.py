import flask
import random

app = flask.Flask(__name__)
words = []


def read_words():
    global words
    with open("./files/words.txt", "r+")as f:
        words = [i.replace("\n", "") for i in f.readlines() if i and i != "" and i != "\n"]
        random.shuffle(words)


@app.route('/')
def home():
    return flask.render_template('index.html')


@app.route("/word", methods=["GET"])
def get_word():
    index = get_index()
    return flask.jsonify({
        "word": words[index],
        "index": index
    })


@app.route("/finish", methods=["GET"])
def finish_process():
    index = get_index()
    rate = int(round(((index + 1) * 100) / len(words)))
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
    elif int(index) >= len(words):
        index = 0
        random.shuffle(words)
    else:
        index = int(index)

    return index


if __name__ == '__main__':
    read_words()
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.run(host='0.0.0.0', port=2442)

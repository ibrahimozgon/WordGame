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
    index = flask.request.args.get("index")
    if not index:
        index = 0
    else:
        index = int(index)

    return flask.jsonify({
        "word": words[index],
        "index": index
    })


@app.route("/finish", methods=["GET"])
def finish_process():
    index = flask.request.args.get("index")
    if not index:
        index = 0
    else:
        index = int(index)
    count = len(words) < (index + 1) and len(words) or (index + 1)
    rate = int(round(((index + 1) * 100) / count))
    result = {
        "rate": rate,
        "result": "You have completed {}% of test!".format(rate)
    }
    return flask.jsonify(result)


if __name__ == '__main__':
    read_words()
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.run(host='0.0.0.0', port=2442)

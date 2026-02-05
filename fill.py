from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/stats/day/<date>', methods=['GET'])
def daily_stats(date):
    with open("./raw-data/" + date + ".txt", "r", encoding="utf-8") as file:
        first_line = file.readline().strip()
    return jsonify(first_line)

app.run(debug=True)


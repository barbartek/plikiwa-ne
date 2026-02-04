from flask import Flask, request, jsonify

app = Flask(__name__)
@app.route('/stats/day/<date>', methods=['GET'])
def daily_stats(date):
 with open("20250101.txt", "r") as file:
        first_line = file.readline().strip()
    return jsonify(first_line)
 



app.run(debug=True)
from flask import Flask, jsonify
import json

app = Flask(__name__)

@app.route('/stats/day/<date>', methods=['GET'])
def daily_stats(date):
    with open("./raw-data/" + date + ".txt", "r", encoding="utf-8") as file:
        text = file.read() 
        lines = text.split("\n")
       # print(file)
        readings = []
        for line in lines:
            clean_line = line.rstrip(",").replace("'",'"')
            readings.append(json.loads(clean_line))
        # print (lines[11])
        temperatury = []
        for reading in readings:
           # print(reading['temp'])
            temperatury.append(reading['temp'])

        temp_min = min(temperatury)
        temp_max = max(temperatury)
        print(f"Temperatura minimalna: {temp_min:.2f}°C")
        print(f"Temperatura maksymalna: {temp_max:.2f}°C")
      # print(values)
     #   max_val = max(values)
        # return jsonify({
                
        # })
    return "dsdsdds"
app.run(debug=True)
from flask import Flask, request, jsonify

app = Flask(__name__)
@app.route('/stats/day/<date>', methods=['GET'])
def daily_stats(date):
    #otworzyć plik - jeden który bkolwiek nie korzystać z parametrówn dawanych do przyeglądarki
    #zwrócuić zawartość pliku -tylko pierwsza linia 
    return date


 



app.run(debug=True)
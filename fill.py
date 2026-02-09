from flask import Flask, jsonify, render_template#Flask to silnik tej apliacji bez niego serwer sie nie uruchomi, jsonify zmiania dane pythona na poprawan odpowiedz http i dba o proceskodowania render_template szuka pliku HTML w katalogu templates/ wstawia do niego zmienne (np. liczby, tekst, listy)  generuje gotową stronę HTML zwraca ją jako odpowiedź HTTP
from datetime import datetime, timedelta
import json# linia ładuje wbudowany moduł Pythona json, który służy do: wczytywania danych JSON z tekstu (json.loads) zapisywania danych do JSON (json.dumps) czytania JSON z pliku (json.load) zapisywania JSON do pliku (json.dump)
import os # sprawdzać, czy plik istnieje, tworzyć katalogi,usuwać pliki,pobierać listę plików w folderze,łączyć ścieżki w sposób niezależny od systemu,pobierać zmienne środowiskowe.
import my
import cleaner

app = Flask(__name__)#Tworzy główny obiekt aplikacji Flask To jest „serce” Twojego serwera. Wszystkie trasy (@app.route(...)), konfiguracje i uruchamianie serwera opierają się właśnie na tym obiekcie. Możesz myśleć o tym tak:

@app.route("/") 
def home(): 
    return render_template("index.html")

@app.route("/cleaning")
def cleaning():
    data_exists = os.path.exists("data")
    return render_template("cleaning.html",  data_exists=data_exists)

@app.route("/cleaning/delete", methods=["POST"])
def cleaning_delete():
    if os.path.exists("data"):
        for root, dirs, files in os.walk("data", topdown=False):
            for f in files:
                os.remove(os.path.join(root, f))

            for d in dirs:
                os.rmdir(os.path.join(root, d))

        os.rmdir("data")

    return render_template(
        "cleaning.html",
        data_exists=False,
        message="Folder data został usunięty."
    )

@app.route("/cleaning/generate", methods=["POST"])
def cleaning_generate():
    for file in os.listdir("raw-data"):
        cleaner.clean_data(os.path.join("raw-data", file))

    return render_template("cleaning.html", data_exists=True, message="Czyste dane wygenerowane")

@app.route("/days")
def days_browser():
    days_stats = []  # tu będziemy trzymać statystyki każdego dnia

    if os.path.exists("data"):
        for f in os.listdir("data"):
            if f.endswith(".txt"):
                file_date = f.replace(".txt", "")
                path = os.path.join("data", f)
                readings = my.read_readings_from_filepath(path)
                temperatury = [r['temp'] for r in readings]
                if temperatury:  # jeśli są odczyty
                    days_stats.append({
                        "date": file_date,
                        "temp_min": min(temperatury),
                        "temp_max": max(temperatury)
                    })
    days_stats.sort(key=lambda x: x["date"])  # sortowanie po dacie

    return render_template("days.html", days_stats=days_stats)
@app.route("/stats/recent")
def recent_stats():
    if not os.path.exists("data"):
        return render_template("statystyki.html", stats=None, message="brak flodera")
    
    files = [f for f in os.listdir("data") if f.endswith(".txt")]
    all_readings = []
    for f in files:
        file_date_str = f.replace(".txt", "")
        file_date = datetime.strptime(file_date_str, "%Y%m%d")
        path = os.path.join("data", f)
        readings = my.read_readings_from_filepath(path)
        temps = [r['temp']for r in readings]
        for t in temps :
            all_readings.append((file_date,t))

    if not all_readings:
        return render_template("")



@app.route('/stats/day/<date>', methods=['GET'])#endpoint do wyświetlania statystyk danego dnia
def daily_stats(date):
    file_date = date.replace("-", "") 
    path = os.path.join("data", file_date + ".txt")
    if not os.path.exists(path):
        return f" Plik nie istnieje: {os.path.abspath(path)}"

    readings = my.read_readings_from_filepath(path)
    temperatury = [r['temp'] for r in readings]

    temp_min = min(temperatury)
    temp_max = max(temperatury)

    return render_template(
        "stats.html",
        date=date,
        temp_min=temp_min,
        temp_max=temp_max,
    )

app.run(debug=True)#app.run(debug=True) to ostatni element Twojej a plikacji Flask — właśnie ta linia uruchamia serwer i po zwala Ci wejść na stronę w przeglądarce.

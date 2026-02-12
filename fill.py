from flask import Flask, jsonify, render_template, request, url_for  # dodany url_for do linków
from datetime import datetime, timedelta
import os # sprawdzać, czy plik istnieje, tworzyć katalogi,usuwać pliki,pobierać listę plików w folderze,łączyć ścieżki w sposób niezależny od systemu,pobierać zmienne środowiskowe.
import my
import cleaner
import shutil
from data_service import reading_data

class Statistic:
    temp = None
    date = None

app = Flask(__name__) #Tworzy główny obiekt aplikacji Flask To jest „serce” Twojego serwera. Wszystkie trasy (@app.route(...)), konfiguracje i uruchamianie serwera opierają się właśnie na tym obiekcie. Możesz myśleć o tym tak:

@app.route("/") 
def home(): 
    return render_template("index.html")

@app.route("/cleaning")
def cleaning():
    data_exists = os.path.exists("data")
    return render_template("cleaning.html",  data_exists=data_exists)

@app.route("/stats/recent/chartjs")
def recent_chartjs():
    start_date_str = request.args.get("start")
    mode = request.args.get("mode", "start")  # start / end

    if not start_date_str:
        return render_template("chartjs.html", chart_data={})

    try:
        start_date = datetime.strptime(start_date_str, "%Y-%m-%d")
    except:
        return "Zły format daty. Użyj YYYY-MM-DD"

    if not os.path.exists("data"):
        return "Brak folderu data"

    files = sorted([plik for plik in os.listdir("data") if plik.endswith(".txt")])
    all_readings = []

    # Wczytywanie
    for plik_name in files:
        file_date = datetime.strptime(plik_name.replace(".txt", ""), "%Y%m%d")
        readings = my.read_readings_from_filepath(os.path.join("data", plik_name))

        for reading in readings:

            # --- poprawne parsowanie czasu ---
            if "time" in reading:
                raw_time = reading["time"].strip()

                parsed_time = None
                for fmt in ("%H:%M", "%H:%M:%S", "%H:%M:%S.%f"):
                    try:
                        parsed_time = datetime.strptime(raw_time, fmt).time()
                        break
                    except ValueError:
                        pass

                if parsed_time is None:
                    raise ValueError(f"Nieznany format czasu: {raw_time}")

                dt = datetime.combine(file_date.date(), parsed_time)

            else:
                dt = file_date

            all_readings.append((dt, reading["temp"]))

    if not all_readings:
        return "Brak odczytów"

    chart_data = {}
    zakresy = [1, 3, 7]

    
    for days in zakresy:

        if mode == "start":
            left = start_date
           
        else:
            left = start_date - timedelta(days=days)

        right = left + timedelta(days=days)
    

     
        selected = [
            (dt, temp)
            for dt, temp in all_readings
            if left <= dt <= right
        ]

        dates = [dt.strftime("%Y-%m-%d %H:%M") for dt, temp in selected]
        temps = [temp for dt, temp in selected]

        chart_data[days] = {
            "dates": dates,
            "temps": temps
        }

    return render_template(
    "chartjs.html",
    chart_data=chart_data,
    start=start_date_str,
    mode=mode
)




        



@app.route("/days")
def days_browser():
    days_stats = reading_data("data")  
    return render_template("days.html", days_stats=days_stats)

@app.route("/stats/recent/form")
def recent_stats_form():
    
    start_date_str = request.args.get("start") 
    if not start_date_str:
        return render_template("recent.html")  


    try:
        start_date = datetime.strptime(start_date_str, "%Y-%m-%d")
    except:
        return "Niepoprawny format daty. Użyj YYYY-MM-DD"

    
    if not os.path.exists("data"):
        return "Brak folderu data"

    files = [f for f in os.listdir("data") if f.endswith(".txt")]
    all_readings = []

    for f in files:
        file_date = datetime.strptime(f.replace(".txt", ""), "%Y%m%d")
        readings = my.read_readings_from_filepath(os.path.join("data", f))
        temps = [r['temp'] for r in readings]
        for t in temps:
            all_readings.append((file_date, t))

    if not all_readings:
        return "Brak odczytów"

    all_readings.sort(key=lambda x: x[0], reverse=True)
    first_file_date = min(d for d, t in all_readings)

    statystki = [1, 3, 7, 14, 30]
    staty = {}

    for days in statystki:
        cutoff = start_date - timedelta(days=days-1)
        if cutoff < first_file_date:
            cutoff = first_file_date
        temps_in_statystki = [
            (reading_date, temperature)
            for reading_date, temperature in all_readings
            if cutoff <= reading_date <= start_date
        ]
        if temps_in_statystki:
            min_date, min_temp = min(temps_in_statystki, key=lambda x: x[1])
            min_stat = Statistic()
            min_stat.temp = round(min_temp, 1)
            min_stat.date = min_date.strftime("%Y%m%d")
            
            max_date, max_temp = max(temps_in_statystki, key=lambda x: x[1])
            max_stat = Statistic()
            max_stat.temp = round(max_temp, 1)     
            max_stat.date = max_date.strftime("%Y%m%d")
    
            staty[days] = {"min": min_stat, "max": max_stat}

        else:
            staty[days] = {"min": None, "max": None}


    return render_template("recent.html", staty=staty)

@app.route('/stats/day/<date>', methods=['GET']) 
def daily_stats(date):
    file_date = date.replace("-", "") 
    path = os.path.join("data", file_date + ".txt")
    if not os.path.exists(path):
        return f" Plik nie istnieje: {os.path.abspath(path)}"

    readings = my.read_readings_from_filepath(path)
    temperatury = [r['temp'] for r in readings]

    temp_min = round(min(temperatury), 1)
    temp_max = round(max(temperatury), 1)


    back_url = url_for('recent_stats_form')  

    return render_template(
        "stats.html",
        date=date,
        temp_min=temp_min,
        temp_max=temp_max,
        back_url=back_url,  
        staty={}
    )

app.run(debug=True) #app.run(debug=True) to ostatni element Twojej aplikacji Flask — właśnie ta linia uruchamia serwer i pozwala Ci wejść na stronę w przeglądarce.

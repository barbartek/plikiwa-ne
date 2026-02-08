from flask import Flask, jsonify,render_template#Flask to silnik tej apliacji bez niego serwer sie nie uruchomi, jsonify zmiania dane pythona na poprawan odpowiedz http i dba o proceskodowania render_template szuka pliku HTML w katalogu templates/ wstawia do niego zmienne (np. liczby, tekst, listy)  generuje gotową stronę HTML zwraca ją jako odpowiedź HTTP
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



@app.route('/stats/day/<date>', methods=['GET'])#jest sposobem, w jaki Flask rejestruje endpoint w Twojej aplikacji. To jedna z kluczowych rzeczy, które sprawiają, że Flask działa jak serwer webowy. Rozbijmy to na części, żeby było absolutnie jasne.
def daily_stats(date):#To jest funkcja obsługująca żądanie HTTP. Flask wywoła ją automatycznie, gdy użytkownik odwiedzi adres:
    path = "./raw-data/" + date + ".txt"#tworzy ścieżkę do pliku na podstawie wartości date, którą dostałeś z URL‑a. Rozbijmy to na czynniki, żeby było absolutnie jasne.
    if not os.path.exists(path):#to bardzo typowy sposób w Pythonie na sprawdzenie, czy plik lub folder istnieje.W Twoim przypadku chodzi o to, żeby upewnić się, że plik z danym dniem (2024-12-31.txt) naprawdę jest w katalogu raw-data/, zanim spróbujesz go otworzyć.
        return render_template("error.html", message="Plik nie istnieje"), 404 # 1. render_template("error.html", message="Plik nie istnieje") To polecenie:ładuje plik error.html z folderu templates/przekazuje do niego zmienną message o wartości "Plik nie istnieje"generuje gotowy HTML, który zobaczy użytkownikW szablonie możesz użyć tej zmiennej:2. Zwracanie HTML jako odpowiedź render_template(...) zwraca pełną stronę HTML, więc użytkownik dostaje normalną stronę błędu zamiast surowego JSON‑a czy tekstu. To jest eleganckie rozwiązanie, jeśli Twoje API ma też frontend. 3. , 404 — ustawienie kodu HTTp To ustawia kod odpowiedzi HTTP na 404 Not Found. Czyli: przeglądarka wie, że zasób nie istnieje narzędzia typu Postman też to rozpoznają wyszukiwarki nie indeksują błędnych stron Bez tego linia zwróciłaby kod 200 OK, co byłoby mylące.
   
    
    readings = my.read_readings_from_filepath(path)
    temperatury = []#to po prostu inicjalizacja pustej listy, ale w Twoim kodzie pełni bardzo konkretną rolę — przygotowuje miejsce na same wartości temperatur, wyciągnięte z każdego odczytu.
    for reading in readings:#to klasyczna pętla for w Pythonie, ale w Twoim kodzie pełni bardzo konkretną rolę — przechodzisz po każdym odczycie z pliku, który wcześniej zamieniłeś na słownik (dict).Rozbijmy to na części, żeby było naprawdę klarowne.

        temperatury.append(reading['temp'])#temperatury.append(reading['temp'])to bardzo prosty, ale kluczowy krok w Twoim przetwarzaniu danych. Właśnie tutaj wyciągasz samą wartość temperatury z każdego odczytu i dodajesz ją do listy temperatury.Rozbijmy to na części, żeby było absolutnie jasne.

    temp_min = min(temperatury)#to najprostszy i najbardziej naturalny sposób na wyciągnięcie minimalnej i maksymalnej temperatury z listy wartości.Rozbijmy to na krótkie, konkretne punkty.
    temp_max = max(temperatury)#to najprostszy i najbardziej naturalny sposób na wyciągnięcie minimalnej i maksymalnej temperatury z listy wartości.Rozbijmy to na krótkie, konkretne punkty.
    print(f"Temperatura minimalna: {temp_min:.2f}°C")#to elegancki sposób na formatowanie liczb i wyświetlanie ich w czytelnej formie. W Twoim kodzie pełnią rolę szybkiej kontroli — pozwalają zobaczyć, czy statystyki liczą się poprawnie, zanim zwrócisz je w API.
    print(f"Temperatura maksymalna: {temp_max:.2f}°C")#to elegancki sposób na formatowanie liczb i wyświetlanie ich w czytelnej formie. W Twoim kodzie pełnią rolę szybkiej kontroli — pozwalają zobaczyć, czy statystyki liczą się poprawnie, zanim zwrócisz je w API.

    return  render_template(
        "./stats.html",
        date = date,
        temp_min = temp_min,
        temp_max =  temp_max,
        
       )#to klasyczny sposób przekazania danych z backendu Flask do szablonu HTML. W Twojej aplikacji to właśnie tutaj kończy się logika obliczeń, a zaczyna prezentacja wyników. Rozbijmy to na części, żebyś miał pełny obraz tego, co się dzieje.


@app.route("/cleaning/generate", methods=["POST"])
def cleaning_generate():
    for file in os.listdir("raw-data"):
        cleaner.clean_data(os.path.join("raw-data", file))

    return render_template("cleaning.html", data_exists=True, message="Czyste dane wygenerowane")


app.run(debug=True)#app.run(debug=True) to ostatni element Twojej aplikacji Flask — właśnie ta linia uruchamia serwer i pozwala Ci wejść na stronę w przeglądarce.
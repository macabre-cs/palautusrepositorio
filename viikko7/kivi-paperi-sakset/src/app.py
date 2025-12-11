from flask import Flask, render_template, request, session, redirect, url_for
from tuomari import Tuomari
from kps_tehdas import luo_peli
from tekoaly import Tekoaly
from tekoaly_parannettu import TekoalyParannettu
import secrets

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)


@app.route("/")
def index():
    """Aloitussivu, jossa valitaan pelitila"""
    session.clear()
    return render_template("index.html")


@app.route("/start", methods=["POST"])
def start_game():
    """Aloittaa pelin valitulla pelitilalla"""
    game_mode = request.form.get("game_mode")
    session["game_mode"] = game_mode
    session["tuomari"] = {"ekan_pisteet": 0, "tokan_pisteet": 0, "tasapelit": 0}
    session["siirrot"] = []

    # Alustetaan tekoäly tarvittaessa
    if game_mode == "b":
        session["tekoaly_muisti"] = []
    elif game_mode == "c":
        session["tekoaly_muisti"] = []

    return redirect(url_for("play"))


@app.route("/play", methods=["GET", "POST"])
def play():
    """Pelinäkymä"""
    if "game_mode" not in session:
        return redirect(url_for("index"))

    game_mode = session["game_mode"]
    tuomari_data = session["tuomari"]

    if request.method == "POST":
        player_move = request.form.get("move")

        if player_move not in ["k", "p", "s"]:
            # Virheellinen siirto, peli päättyy
            return redirect(url_for("results"))

        # Määritä vastustajan siirto
        if game_mode == "a":
            # Pelaaja vs pelaaja
            opponent_move = request.form.get("opponent_move")
            if opponent_move not in ["k", "p", "s"]:
                return redirect(url_for("results"))
        elif game_mode == "b":
            # Tekoäly (yksinkertainen)
            tekoaly = Tekoaly()
            opponent_move = tekoaly.anna_siirto()
        else:  # game_mode == 'c'
            # Parannettu tekoäly
            muisti = session.get("tekoaly_muisti", [])
            tekoaly = TekoalyParannettu(10)
            for siirto in muisti:
                tekoaly.aseta_siirto(siirto)
            opponent_move = tekoaly.anna_siirto()

        # Päivitä tuomarin tiedot
        tuomari = Tuomari()
        tuomari.ekan_pisteet = tuomari_data["ekan_pisteet"]
        tuomari.tokan_pisteet = tuomari_data["tokan_pisteet"]
        tuomari.tasapelit = tuomari_data["tasapelit"]

        tuomari.kirjaa_siirto(player_move, opponent_move)

        session["tuomari"] = {
            "ekan_pisteet": tuomari.ekan_pisteet,
            "tokan_pisteet": tuomari.tokan_pisteet,
            "tasapelit": tuomari.tasapelit,
        }

        # Tallenna siirto historiaan
        siirrot = session.get("siirrot", [])
        siirrot.append({"player": player_move, "opponent": opponent_move})
        session["siirrot"] = siirrot

        # Päivitä tekoälyn muisti tarvittaessa
        if game_mode == "c":
            muisti = session.get("tekoaly_muisti", [])
            muisti.append(player_move)
            session["tekoaly_muisti"] = muisti

        session.modified = True

    game_titles = {
        "a": "Pelaaja vs Pelaaja",
        "b": "Pelaaja vs Tekoäly",
        "c": "Pelaaja vs Parannettu Tekoäly",
    }

    # Always get the current scores from session (which are updated after POST)
    current_scores = session.get("tuomari", tuomari_data)

    return render_template(
        "play.html",
        game_mode=game_mode,
        game_title=game_titles.get(game_mode),
        tuomari=current_scores,
        siirrot=session.get("siirrot", []),
        game_won=(
            current_scores.get("ekan_pisteet", 0) >= 3
            or current_scores.get("tokan_pisteet", 0) >= 3
        ),
    )


@app.route("/results")
def results():
    """Lopputulokset"""
    if "tuomari" not in session:
        return redirect(url_for("index"))

    tuomari_data = session["tuomari"]
    siirrot = session.get("siirrot", [])

    game_titles = {
        "a": "Pelaaja vs Pelaaja",
        "b": "Pelaaja vs Tekoäly",
        "c": "Pelaaja vs Parannettu Tekoäly",
    }

    return render_template(
        "results.html",
        game_title=game_titles.get(session.get("game_mode")),
        tuomari=tuomari_data,
        siirrot=siirrot,
    )


if __name__ == "__main__":
    app.run(debug=True)

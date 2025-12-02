class Summa:
    def __init__(self, sovelluslogiikka, lue_syote):
        self._sovelluslogiikka = sovelluslogiikka
        self._lue_syote = lue_syote
        self._edellinen_arvo = None

    def suorita(self):
        try:
            arvo = int(self._lue_syote())
        except:
            arvo = 0

        self._edellinen_arvo = self._sovelluslogiikka.arvo()
        self._sovelluslogiikka.plus(arvo)

    def kumoa(self):
        if self._edellinen_arvo is not None:
            self._sovelluslogiikka.aseta_arvo(self._edellinen_arvo)


class Erotus:
    def __init__(self, sovelluslogiikka, lue_syote):
        self._sovelluslogiikka = sovelluslogiikka
        self._lue_syote = lue_syote
        self._edellinen_arvo = None

    def suorita(self):
        try:
            arvo = int(self._lue_syote())
        except:
            arvo = 0

        self._edellinen_arvo = self._sovelluslogiikka.arvo()
        self._sovelluslogiikka.miinus(arvo)

    def kumoa(self):
        if self._edellinen_arvo is not None:
            self._sovelluslogiikka.aseta_arvo(self._edellinen_arvo)


class Nollaus:
    def __init__(self, sovelluslogiikka, lue_syote):
        self._sovelluslogiikka = sovelluslogiikka
        self._lue_syote = lue_syote
        self._edellinen_arvo = None

    def suorita(self):
        self._edellinen_arvo = self._sovelluslogiikka.arvo()
        self._sovelluslogiikka.nollaa()

    def kumoa(self):
        if self._edellinen_arvo is not None:
            self._sovelluslogiikka.aseta_arvo(self._edellinen_arvo)


class Kumoa:
    def __init__(self, sovelluslogiikka, lue_syote, viimeisin_komento):
        self._sovelluslogiikka = sovelluslogiikka
        self._lue_syote = lue_syote
        self._viimeisin_komento = viimeisin_komento

    def suorita(self):
        if self._viimeisin_komento():
            self._viimeisin_komento().kumoa()

    def kumoa(self):
        pass

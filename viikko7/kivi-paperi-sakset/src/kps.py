from tuomari import Tuomari


class KPS:
    def pelaa(self):
        tuomari = Tuomari()

        ekan_siirto = self._ekan_siirto()
        tokan_siirto = self._tokan_siirto()

        while self._onko_ok_siirto(ekan_siirto) and self._onko_ok_siirto(tokan_siirto):
            tuomari.kirjaa_siirto(ekan_siirto, tokan_siirto)
            print(tuomari)

            self._jalkikasiittely(ekan_siirto, tokan_siirto)

            ekan_siirto = self._ekan_siirto()
            tokan_siirto = self._tokan_siirto()

        print("Kiitos!")
        print(tuomari)

    def _ekan_siirto(self):
        raise NotImplementedError()

    def _tokan_siirto(self):
        raise NotImplementedError()

    def _jalkikasiittely(self, ekan, tokan):
        pass

    def _onko_ok_siirto(self, siirto):
        return siirto in ["k", "p", "s"]

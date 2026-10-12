import csv
from operator import attrgetter



class Strumento:

    def __init__(self, id_s, tipo, marca, anno, val):
        self.id_s = id_s
        self.tipo = tipo
        self.marca = marca
        self.anno = int(anno)
        self.valore = float(val)
        self.prestato = False

    def __str__(self):
        st = "In prestito" if self.prestato else "Disponibile"
        return f"[{self.id_s}] {self.tipo} {self.marca} ({self.anno}) - €{self.valore} - {st}"


class Prestito:

    def __init__(self, id_p, data, strum, allievo):
        self.id_p = id_p
        self.data = data
        self.strum = strum
        self.allievo = allievo



    def __str__(self):
        return f"Prestito {self.id_p}: {self.strum.tipo} a {self.allievo} ({self.data})"





class DepositoStrumenti:

    def __init__(self, nome, responsabile):
        self.nome = nome
        self.responsabile = responsabile
        self.strumenti = []
        self.prestiti = []



    def carica_file_strumenti(self, file_path):
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                lettore = csv.reader(f)
                for r in lettore:
                    if len(r) == 5:
                        s = Strumento(r[0], r[1], r[2], r[3], r[4])
                        self.strumenti.append(s)

        except FileNotFoundError:
            raise FileNotFoundError("file non trovato.")



    def aggiungi_strumento(self, tipo, marca, anno_acquisto, valore):

        max_id = 0
        for s in self.strumenti:
            num = int(s.id_s[1:])
            if num > max_id:
                max_id = num

        nuovo_id = f"S{max_id + 1}"

        nuovo_s = Strumento(nuovo_id, tipo, marca, anno_acquisto, valore)

        self.strumenti.append(nuovo_s)

        return nuovo_s



    def strumenti_ordinati_per_marca(self):
        return sorted(self.strumenti, key=attrgetter('marca'))



    def nuovo_prestito(self, data, id_strumento, cognome_allievo):

        strum_cercato = None

        for s in self.strumenti:
            if s.id_s == id_strumento:
                strum_cercato = s
                break

        if not strum_cercato:
            raise Exception("Strumento inesistente.")


        if strum_cercato.prestato:
            raise Exception("Strumento già in prestito.")



        id_p = f"P{len(self.prestiti) + 1}"

        p = Prestito(id_p, data, strum_cercato, cognome_allievo)

        strum_cercato.prestato = True
        self.prestiti.append(p)

        return p



    def termina_prestito(self, id_prestito):

        p_da_chiudere = None

        for p in self.prestiti:
            if p.id_p == id_prestito:
                p_da_chiudere = p
                break

        if not p_da_chiudere:

            raise Exception("Prestito non trovato.")

        p_da_chiudere.strum.prestato = False

        self.prestiti.remove(p_da_chiudere)


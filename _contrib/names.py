"""Using the CSV generated by Apoia.se, creates the HTML code to be inserted in
the about.html (#supporters). The file is expected to be called `data.csv` and
is expected to have the following headers in order:
  * Apoiador
  * Email
  * Valor
  * Recompensa
  * Apoios Efetuados
  * Total Apoiado
  * Tipo
  * Status da Promessa
  * Visibilidade
  * Data da Última Mudança no Status da Promessa
  * CEP
  * Rua
  * Número
  * Complementos
  * Bairro
  * Cidade
  * UF
  * País
  * Endereço Completo
"""
from csv import DictReader
from pathlib import Path
from re import search
from unicodedata import category, normalize


INDENT = 10 * " "
FILENAME = "data.csv"


def normalized(name):
    return "".join(
        char for char in normalize("NFD", name.lower()) if category(char) != "Mn"
    )


def current_names():
    pattern = r"<p>(?P<name>.+)</p>"
    with open(Path("..") / "about.html") as fobj:
        names_section = False
        for line in fobj.readlines():
            if names_section and "</div>" in line:
                break

            if names_section:
                match = search(pattern, line)
                yield match.group("name")

            if 'id="supporters"' in line:
                names_section = True


def names():
    with open(FILENAME) as fobj:
        names = list(
            line["Apoiador"]
            for line in DictReader(fobj)
            if line["Visibilidade"] == "Público"
        )
        names.extend(current_names())
        names = {normalized(name): name for name in names}
        return sorted(names.values(), key=lambda name: normalized(name))


def html(names):
    for name in names:
        print(f"{INDENT}<p>{name}</p>")


if __name__ == "__main__":
    html(names())

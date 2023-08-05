# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['webuntis_cli']

package_data = \
{'': ['*']}

install_requires = \
['webuntis>=0.1.11,<0.2.0']

entry_points = \
{'console_scripts': ['webuntis-cli = webuntis_cli.run:main']}

setup_kwargs = {
    'name': 'webuntis-cli',
    'version': '0.6.5',
    'description': 'WebUntis CLI',
    'long_description': 'Das Projekt `webuntis-cli` stellt eine Kommandozeile\nfür [WebUntis](https://www.untis.at) zur Verfügung. Bei Webuntis\nhandelt es sich um eine Software zum Erstellen und Verwalten von\nStundenplänen in Schulen.\n\n\nInstallation/Upgrade\n====================\n\nBenutze `pip` (oder `pip3`) für eine einfache Installation. Hierfür muss \n[python](https://www.python.org) installiert sein. \n\n    $ pip install --upgrade webuntis-cli\n\nMit der Option `--upgrade` wird immer die jeweils aktuelle Version installiert. \n\n\nBenutzung\n=========\n\nNach der Installation steht der Befehl `webuntis-cli` zur Verfügung. Dieser \nverfügt über eine Hilfefunktion.\n\n    $ webuntis-cli --help\n\nNach dem ersten Aufruf wird die Konfigurationsdatei  `.webuntis-cli.ini` im \nHome-Verzeichnis des Nutzers angelegt. Diese muss bearbeitet und mit den \nkorrekten Nutzerdaten wie Schulname, Server, Benutzername und Passwort befüllt \nwerden. \n\nWenn das Speichern von Passwörtern in einer Datei unerwünscht ist, kann\nder Eintrag für das Passwort aus der Konfigurationsdatei entfernt werden. In \ndiesem Falle muss es bei jeder Ausführung eingegen werden.\n\nBeispiele\n---------\n\nEin Aufruf für den aktuellen Stundenplan von Herr Mustermann würde wie folgt\naussehen:\n\n    $ webuntis-cli --lehrer Mustermann    \n\nEs können auch mehrere Personen angegeben werden:\n\n    $ webuntis-cli --lehrer Mustermann Musterfrau\n    \nEbeso können die Pläne für verschiedene Räume oder Klassen angezeigt werden.\n\n    $ webuntis-cli --raum 12 13 14\n    $ webuntis-cli --klasse 10a 10b 10c\n\nDer anzuzeigende Zeitraum kann über die folgenden Optionen festgelegt werden:\n\n- `--start` der erste Termin\n- `--tage` die Anzahl der angezeigten Tage\n\n\n    $ webuntis-cli --lehrer Mustermann --start 1.1. --tage 3\n\n\nProbleme, Fehler oder Verbesserungsvorschläge\n=============================================\n\nFehler, Probleme oder Vorschläge für Verbesserungen kannst du über den [Bugtracker bei\ngithub](https://github.com/tbs1-bo/webuntis_cli/issues/new) melden. Hierfür \nbenötigst du einen einen Account bei github.\n\nEntwicklerdokumentation\n=======================\n\nEs können Debugausgaben aktiviert werden, indem die Umgebungsvariable \n`WEBUNTIS_CLI_DEBUG` mit einem belibiegen Wert initialisiert wird.\n\n    $ WEBUNTIS_CLI_DEBUG=1 webuntis-cli --help\n    \n',
    'author': 'Marco Bakera',
    'author_email': 'marco@bakera.de',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://tbs1-bo.github.io/webuntis_cli/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)

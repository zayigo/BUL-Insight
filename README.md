<div align="center">
  <img src="https://i.imgur.com/2IhIywQ.png" width="150" />
  <h1>BUL Insight</h1>
  <em>Elaborazione e archiviazione dei dati di avanzamento del <a href="https://fibra.click/piano-bul/">piano nazionale italiano per la Banda Ultralarga (piano BUL)</a> nelle <a href="https://fibra.click/piano-aree-bianche/">aree bianche</a></em>
  <br>
  <br>
  <img src="https://img.shields.io/badge/Python-3776AB.svg?style=flat&logo=Python&logoColor=white" alt="Python">
</div>

---

## Requisiti

Assicurati di avere le seguenti dipendenze installate sul tuo sistema:

- **Python**: `versione >= 3`
- **Installazione delle dipendenze**:
  - Senza Pipenv: Esegui `pip install -r requirements.txt` per installare le dipendenze elencate nel file `requirements.txt`.
  - Con Pipenv: Assicurati di avere [Pipenv](https://pipenv.pypa.io/en/latest/) installato ed esegui `pipenv install` per creare un ambiente virtuale e installare le dipendenze dal `Pipfile`.

## Utilizzo

### Creare e inizializzare il database:

```
python3 -m database
```

### Eaborare un singolo file:

```
python3 main.py --file archive/2023_11.pdf
```

### Elaborare tutti i file in una cartella:

```
python3 main.py --folder archive
```

### Esportare i dati elaborati:

```
python3 main.py --export --export-dir export
```

## Come funziona

1. **Estrazione del testo con PyMuPDF**: Utilizziamo [PyMuPDF](https://pymupdf.readthedocs.io/en/latest/) per cercare all'interno del documento i titoli delle sezioni di nostro interesse. Una volta identificate, estraiamo il range di pagine corrispondente a ciascuna sezione. Questo ci permette di lavorare solo con le parti del documento che ci interessano e facilita l'estrazione dei dati.

2. **Estrazione delle tabelle con Camelot**: Le pagine estratte nella fase precedente vengono poi analizzate con [Camelot](https://camelot-py.readthedocs.io/en/master/), una libreria specializzata nell'estrazione di tabelle da documenti PDF. Camelot trasforma le tabelle in [DataFrame di pandas](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.html), rendendo i dati facilmente manipolabili con strumenti di analisi dati in Python.

3. **Elaborazione dei dati**: Una volta estratti, i dati vengono elaborati in base alla sezione di provenienza ed inseriti all'interno di un database.

## Archiviazione e Accesso ai Dati

I PDF originali sono archiviati in questa repository nella cartella `archive/`, dove è presente anche il file `index.csv` che contiene i link esterni ai documenti.

Nella cartella `export/` sono invece disponibili i file CSV, divisi per regione e aggiornati al **31/12/2022**.

> [!WARNING]
> La correttezza dei dati non è garantita.

### Fonte dei dati

- [Notizie Banda Ultralarga](https://bandaultralarga.italia.it/category/notizie/)
- [Archivio News Infratel Italia](https://www.infratelitalia.it/archivio-news)

## License

This project is licensed under the GNU General Public License v3.0. For more details, see the [LICENSE](https://github.com/zayigo/postfix-to-cloudflare/blob/main/LICENSE) file.

SCHEMA = {
    'PROGETTAZIONE DEFINITIVA': {
        "Progettazione definitiva FTTH": [
            "Progetti previsti",
            "Comuni previsti",
            "Progetti consegnati",
            "Comuni con progetti consegnati",
            "Progetti approvati",
            "Comuni con progetti approvati"
        ],
        "Progettazione definitiva FWA": [
            "Progetti previsti",
            "Comuni previsti",
            "Progetti consegnati",
            "Comuni con progetti consegnati",
            "Progetti approvati",
            "Comuni con progetti approvati"
        ],
    },
    'PROGETTAZIONE ESECUTIVA': {
        "Progettazione esecutiva FTTH": [
            "Progetti previsti",
            "Comuni previsti",
            "Progetti consegnati",
            "Comuni con progetti consegnati",
            "Progetti approvati",
            "Comuni con progetti approvati"
        ],
        "Progettazione esecutiva FWA": [
            "Progetti previsti",  #
            "Comuni previsti",
            "Progetti approvati"
        ],
    },
    'ESECUZIONE DEI CANTIERI': {
        "Esecuzione dei cantieri FTTH": [
            "Ordini emessi",
            "Comuni con ordine",
            "Cantieri aperti",
            "Comuni avviati",
            "Cantieri con CUIR",
            "Comuni completati"
        ],
        "Esecuzione dei cantieri FWA": [
            "Ordini emessi",
            "Cantieri aperti",
            "Cantieri con CUIR",
        ],
        "Esecuzione dei cantieri rendicontazione": [
            "Valore cantieri avviati",  #
            "Avanzamento lavori",
            "Lavori Contabilizzati da DL"
        ],
    },  # old layout 05/2020
    'AVVIO DEI CANTIERI': {
        "Esecuzione dei cantieri FTTH": [
            "Ordini emessi",
            "Comuni con ordine",
            "Cantieri aperti",
            "Comuni avviati",
            "Cantieri con CUIR",
            "Comuni completati"
        ],
        "Esecuzione dei cantieri FWA": [
            "Ordini emessi",
            "Cantieri aperti",
            "Cantieri con CUIR",
        ],
        "Esecuzione dei cantieri rendicontazione": [
            "Valore cantieri avviati",  #
            "Avanzamento lavori",
            "Lavori Contabilizzati da DL"
        ],
    },
    'COLLAUDO': {
        "Collaudo FTTH": [
            "Impianti collaudabili",  #
            "Impianti complessivamente collaudati in campo",
            "Collaudi positivi"
        ],
        "Collaudo FWA": [
            "Impianti collaudabili",  #
            "Impianti complessivamente collaudati in campo",
            "Siti collaudati positivamente"
        ],
    },
    'UNITA’ IMMOBILIARI': {
        "Unita immobiliari": [
            "Pianificate", "Progettazione esecutiva", "In lavorazione", "In collaudo", "Collaudate", "Totale"
        ],
    },
    'AVVIO DEI SERVIZI': {
        "Avvio dei servizi": [
            "Quantita OLO Presenti",  #
            "Ordini complessivi",
            "Ordini in lavorazione",
            "Ordini KO",
            "Ordini OK"
        ]
    },
    'COMMERCIALIZZAZIONE DEI SERVIZI': {}
}

SCHEMA_EXCEPTIONS = {
    'UNITA’ IMMOBILIARI': {
        "Unita immobiliari": ["Pianificate", "Progettazione esecutiva", "In lavorazione", "Collaudate", "Totale"],
    },
}

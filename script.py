from faker import Faker
import pandas as pd
import sqlite3

# Inizializza Faker
fake = Faker()

def genera_dati(n=10):
    """Genera un dataset di utenti senza ID."""
    return [{
        "Nome": fake.first_name(),
        "Cognome": fake.last_name(),
        "Email": fake.email(),
        "Telefono": fake.phone_number()[:15]
    } for _ in range(n)]

def salva_excel(df, filename="utenti_compatti.xlsx"):
    """Salva i dati in un file Excel."""
    df.to_excel(filename, index=False)
    print(f"File Excel '{filename}' generato con successo!")

def carica_excel(filename="utenti_compatti.xlsx"):
    """Carica i dati da un file Excel."""
    return pd.read_excel(filename)

def crea_tabella_sqlite(conn):
    """Crea la tabella utenti nel database SQLite senza ID."""
    conn.execute("""
        CREATE TABLE IF NOT EXISTS utenti (
            Nome TEXT,
            Cognome TEXT,
            Email TEXT,
            Telefono TEXT
        )
    """)
    conn.commit()

def inserisci_dati_sqlite(conn, df):
    """Inserisce i dati nella tabella SQLite."""
    df.to_sql("utenti", conn, if_exists="replace", index=False)
    print("Dati inseriti nel database SQLite.")

def verifica_sqlite(conn):
    """Recupera i dati dalla tabella SQLite e li stampa."""
    df = pd.read_sql_query("SELECT * FROM utenti", conn)
    print("\nContenuto della tabella SQLite:")
    print(df)

def main():
    # Genera e salva i dati in Excel
    df = pd.DataFrame(genera_dati(10))
    salva_excel(df)

    # Legge i dati da Excel
    df_excel = carica_excel()

    # Connessione a SQLite e operazioni sul database
    with sqlite3.connect("utenti_colab.db") as conn:
        crea_tabella_sqlite(conn)
        inserisci_dati_sqlite(conn, df_excel)
        verifica_sqlite(conn)

if __name__ == "__main__":
    main()

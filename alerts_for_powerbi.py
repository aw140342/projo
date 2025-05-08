
import csv
import json

ALERT_THRESHOLD = 500  # mm
OUTPUT_CSV = "alerty.csv"

# Przykład funkcji generującej alerty (np. z danych z IMGW)
def get_alerts_from_data(data):
    alerts = []
    for record in data:
        try:
            level = float(record.get("stan_wody") or 0)
            if level > ALERT_THRESHOLD:
                alerts.append({
                    "station_id": record.get("id_stacji"),
                    "station_name": record.get("stacja"),
                    "river": record.get("rzeka"),
                    "level": level,
                    "date": record.get("data_pomiaru"),
                    "wojewodztwo": record.get("wojewodztwo", "nieznane"),
                    "latitude": float(record.get("szerokosc_geograficzna") or 0),
                    "longitude": float(record.get("dlugosc_geograficzna") or 0)
                })
        except Exception as e:
            print(f"⚠️ Błąd rekordu: {e}")
    return alerts

# Eksport alertów do CSV do Power BI
def export_alerts_to_csv(alerts, output_file=OUTPUT_CSV):
    if not alerts:
        print("Brak alertów do eksportu.")
        return

    keys = [
        "station_id", "station_name", "river", "level",
        "date", "wojewodztwo", "latitude", "longitude"
    ]

    with open(output_file, "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=keys)
        writer.writeheader()
        for alert in alerts:
            writer.writerow(alert)

    print(f"💾 Zapisano {len(alerts)} alertów do pliku CSV: {output_file}")
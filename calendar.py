import argparse
import json
from pathlib import Path
from datetime import datetime, timezone, timedelta

from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

  # --------------------------------------------------------------
  # 1️⃣Configuration
SCOPES = [
      "https://www.googleapis.com/auth/calendar",               # lecture + écriture
      # Si tu ne veux jamais créer/modifier, remplace par:
      # "https://www.googleapis.com/auth/calendar.readonly"
  ]

CREDENTIALS_FILE = Path("client_secret.json")   # <‑‑ à créer à l’étape 1️⃣
TOKEN_FILE       = Path("token.json")          # créé après le 1ᵉ login

  # --------------------------------------------------------------
  # 2️⃣Gestion du token OAuth
def get_credentials():
      if TOKEN_FILE.is_file():
          # Token existant → on le charge
          from google.oauth2.credentials import Credentials
          creds = Credentials.from_authorized_user_file(str(TOKEN_FILE), SCOPES)
      else:
          # Première utilisation → ouverture du navigateur
          flow = InstalledAppFlow.from_client_secrets_file(str(CREDENTIALS_FILE), SCOPES)
          creds = flow.run_local_server(port=0)
          # Sauvegarde du jeton (réutilisable à chaque exécution)
          with TOKEN_FILE.open("w") as f:
              f.write(creds.to_json())
      return creds
service = build("calendar", "v3", credentials=get_credentials())

  # --------------------------------------------------------------
  # 3️⃣Fonctions utilitaires
def list_events(max_results: int = 10):
      """Affiche les prochains événements du calendrier principal."""
      events = (
          service.events()
          .list(
              calendarId="primary",
              maxResults=max_results,
              singleEvents=True,
              orderBy="startTime",
          )
          .execute()
      )
      items = events.get("items", [])
      if not items:
          print("✅ Aucun événement trouvé.")
      else:
          print(f"✅ Prochains {len(items)} événements :")
          for ev in items:
              start = ev["start"].get("dateTime", ev["start"].get("date"))
              print(f"- {start} | {ev.get('summary', '(sans titre)')} (id={ev.get('id')})")

def add_event(summary: str, start_iso: str, end_iso: str):
      """Crée un événement simple."""
      event_body = {
          "summary": summary,
          "start": {"dateTime": start_iso, "timeZone": "Europe/Paris"},
          "end":   {"dateTime": end_iso,   "timeZone": "Europe/Paris"},
      }
      created = service.events().insert(calendarId="primary", body=event_body).execute()
      print("✅ Événement créé :")
      print(f"   → {created.get('htmlLink')}")
      print(f"   → id = {created.get('id')}")

def delete_event(event_id: str):
      """Supprime un événement donné."""
      service.events().delete(calendarId="primary", eventId=event_id).execute()
      print(f"✅ Événement {event_id} supprimé.")

  # --------------------------------------------------------------
  # 4️⃣Interface en ligne de commande
def main():
      parser = argparse.ArgumentParser(
          description="Interface minimaliste pour Google Calendar (lecture/écriture)."
      )
      sub = parser.add_subparsers(dest="cmd", required=True)

      # list
      p_list = sub.add_parser("list", help="Lister les prochains événements")
      p_list.add_argument("-n", "--number", type=int, default=10,
                          help="Nombre d’événements à récupérer (défaut : 10)")

      # add
      p_add = sub.add_parser("add", help="Créer un nouvel événement")
      p_add.add_argument("summary", help="Titre de l’événement")
      p_add.add_argument("start", help="Heure de début ISO‑8601 (ex. 2026-06-05T14:00:00+02:00)")
      p_add.add_argument("end",   help="Heure de fin   ISO‑8601 (ex. 2026-06-05T15:00:00+02:00)")

      # delete
      p_del = sub.add_parser("delete", help="Supprimer un événement")
      p_del.add_argument("id", help="Identifiant de l’événement (obtenu avec `list`)")

      args = parser.parse_args()

      if args.cmd == "list":
          list_events(max_results=args.number)
      elif args.cmd == "add":
          add_event(args.summary, args.start, args.end)
      elif args.cmd == "delete":
          delete_event(args.id)

if __name__ == "__main__":
        main()
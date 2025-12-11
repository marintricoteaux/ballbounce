"""
Script qui consiste à l'aide d'une librairie titkok-uploader,
en mode headless sur un serveur à part (viel ordi ou hostinger).
PS : Modifié par GPT5
"""

import os
import random
import subprocess
import shutil
import json
from datetime import datetime
from tiktok_uploader.upload import upload_video

from rich.console import Console


console = Console()


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
VIDEOS_DIR = os.path.join(BASE_DIR, "videos")
SETTINGS_PATH = os.path.join(BASE_DIR, "config/settings.json")
COOKIES_PATH = os.path.join(BASE_DIR, "config/cookies.json")


def load_settings():
    with open(SETTINGS_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def generate_video():
    console.print("[bold cyan]🎬 Génération de la vidéo...[/]")

    result = subprocess.run(
        ["python", "main.py"],
        capture_output=True,
        text=True
    )

    if result.returncode != 0:
        console.print(f"[red]Erreur génération vidéo :[/] {result.stderr}")
        return None

    # Cherche la dernière vidéo dans /videos
    files = sorted(
        [f for f in os.listdir(VIDEOS_DIR) if f.endswith(".mp4")],
        key=lambda x: os.path.getmtime(os.path.join(VIDEOS_DIR, x)),
        reverse=True
    )

    if not files:
        console.print("[red]Aucune vidéo trouvée dans videos/ready ![/]")
        return None

    latest = os.path.join(VIDEOS_DIR, files[0])
    console.print(f"[green]Vidéo générée :[/] {latest}")
    return latest


def generate_description(settings):
    hashtags = settings["hashtags"]
    base_lines = settings["description_lines"]

    line = random.choice(base_lines)
    tag_str = " ".join(hashtags)

    return f"{line}\n\n{tag_str}"


def upload(video_path, description):
    console.print("[bold cyan]📤 Upload en cours...[/]")

    import json

    # Charger la liste de cookies que tu as exportés (utilise le chemin absolu)
    try:
        with open(COOKIES_PATH, "r", encoding="utf-8") as f:
            cookies_list = json.load(f)
    except FileNotFoundError:
        console.print(f"[red]Fichier de cookies introuvable : {COOKIES_PATH}[/]")
        return False

    # Le backend n'a besoin au minimum que du cookie `sessionid`.
    if isinstance(cookies_list, dict):
        # Certains exports donnent un objet — normaliser en liste
        cookies_list = [cookies_list]

    session_present = any(c.get("name") == "sessionid" for c in cookies_list)
    if not session_present:
        console.print("[red]Erreur: le cookie 'sessionid' est introuvable dans config/cookies.json[/]")
        return False

    # Supprime les caractères hors BMP (Chromedriver n'accepte pas certains emojis)
    def _to_bmp(s: str) -> str:
        return "".join(ch for ch in s if ord(ch) <= 0xFFFF)

    description_sanitized = _to_bmp(description) if description else description

    try:
        result = upload_video(
            video_path,
            description=description_sanitized,
            cookies_list=cookies_list,
        )

        # `upload_video` retourne une liste des vidéos ayant échoué.
        if isinstance(result, list):
            if len(result) == 0:
                console.print("[green]✔ Upload réussi ![/]")
                return True
            else:
                console.print(f"[red]Échec pour {len(result)} vidéo(x)[/]")
                return False
        else:
            console.print("[green]✔ Upload terminé[/]")
            return True
    except Exception as e:
        console.print(f"[red]Erreur upload : {e}[/]")
        return False


def supp_video(video_path):
    name = os.path.basename(video_path)
    #Video à supprimer


def main():
    settings = load_settings()
    
    """
    # Génération vidéo
    video = generate_video()
    if not video:
        return
    """
    video = "/Users/marin/Documents/ballbounce/videos/video_2025-12-11_19-48-52.mp4"

    # Description
    description = generate_description(settings)
    console.print(f"[bold yellow]📝 Description générée :[/]\n{description}")

    # Upload
    success = upload(video, description)

    # Cleanup + logs
    if success:
        supp_video(video)


if __name__ == "__main__":
    main()
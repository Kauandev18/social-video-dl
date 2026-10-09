import os
import re
import sys
from pathlib import Path

from dotenv import load_dotenv
import yt_dlp

VALID_DOMAINS = (
    "tiktok.com",
    "vm.tiktok.com",
    "vt.tiktok.com",
    "instagram.com",
)


def is_valid_url(url: str) -> bool:
    return any(domain in url for domain in VALID_DOMAINS)


def is_story_url(url: str) -> bool:
    return "instagram.com/stories" in url


def build_ydl_opts(output_dir: Path, cookies_file: str, cookies_browser: str) -> dict:
    opts = {
        "outtmpl": str(output_dir / "%(extractor)s" / "%(uploader)s_%(id)s.%(ext)s"),
        "format": "bv*+ba/b",
        "merge_output_format": "mp4",
        "noplaylist": True,
        "restrictfilenames": True,
        "retries": 3,
    }

    if cookies_file:
        opts["cookiefile"] = cookies_file
    elif cookies_browser:
        opts["cookiesfrombrowser"] = (cookies_browser,)

    return opts


def main() -> int:
    load_dotenv()

    raw_urls = os.getenv("VIDEO_URLS", "")
    urls = [u for u in re.split(r"[,\s]+", raw_urls) if u]

    if not urls:
        print("Erro: VIDEO_URLS está vazio ou não definido no .env")
        return 1

    valid_urls = []
    for url in urls:
        if is_valid_url(url):
            valid_urls.append(url)
        else:
            print(f"Aviso: link ignorado (domínio não suportado): {url}")

    if not valid_urls:
        print("Erro: nenhum link válido encontrado.")
        return 1

    output_dir_raw = os.getenv("OUTPUT_DIR", "./downloads")
    output_dir = Path(output_dir_raw).expanduser().resolve()
    output_dir.mkdir(parents=True, exist_ok=True)

    cookies_file = os.getenv("COOKIES_FILE", "")
    cookies_browser = os.getenv("COOKIES_BROWSER", "")

    ydl_opts = build_ydl_opts(output_dir, cookies_file, cookies_browser)

    success = 0
    total = len(valid_urls)

    for url in valid_urls:
        print(f"\nBaixando: {url}")
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
            success += 1
        except yt_dlp.utils.DownloadError as e:
            error_msg = str(e)
            print(f"Erro ao baixar {url}: {error_msg}")

            if is_story_url(url) or "login" in error_msg.lower():
                print(
                    "Dica: este conteúdo requer autenticação. "
                    "Configure COOKIES_FILE ou COOKIES_BROWSER no .env"
                )

    print(f"\nConcluído: {success}/{total} com sucesso")
    return 0 if success == total else 1


if __name__ == "__main__":
    sys.exit(main())

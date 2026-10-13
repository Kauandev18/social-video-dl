import os
import re
import sys
from pathlib import Path

from dotenv import load_dotenv
import yt_dlp

# Largura da barra de progresso
BAR_WIDTH = 30

# Lista de domínios aceitos (insta e tiktok)
VALID_DOMAINS = (
    "tiktok.com",
    "vm.tiktok.com",   
    "vt.tiktok.com", 
    "instagram.com",
)



def _fmt_bytes(n: float) -> str:
    for unit in ("B", "KB", "MB", "GB"):
        if n < 1024:
            return f"{n:.1f} {unit}"
        n /= 1024
    return f"{n:.1f} TB"

#Barra de progresso 
# com o estado atual do download. É aqui que toda a exibição visual acontece.
def progress_hook(d: dict) -> None:
    if d["status"] == "downloading":
        downloaded = d.get("downloaded_bytes", 0)
        total = d.get("total_bytes") or d.get("total_bytes_estimate")
        speed = d.get("speed") or 0
        eta = d.get("eta")

        if total:
            pct = downloaded / total
            filled = int(BAR_WIDTH * pct)
            bar = "█" * filled + "░" * (BAR_WIDTH - filled)
            size_info = f"{_fmt_bytes(downloaded)} / {_fmt_bytes(total)}"
        else:
            bar = "?" * BAR_WIDTH
            pct = 0.0
            size_info = _fmt_bytes(downloaded)

        speed_info = f"{_fmt_bytes(speed)}/s" if speed else "? B/s"
        eta_info = f"ETA: {eta}s" if eta is not None else "ETA: ?"

        sys.stdout.write(
            f"\r  [{bar}] {pct:5.1%} | {size_info} | {speed_info} | {eta_info}   "
        )
        sys.stdout.flush()

    elif d["status"] == "finished": 

      #pulamos a linha para o próximo print não
        # sobrescrever a barra do vídeo anterior.
        sys.stdout.write(f"\r  [{'█' * BAR_WIDTH}] 100.0% | concluído{' ' * 30}\n")
        sys.stdout.flush()


# --- Validação de URL ---
def is_valid_url(url: str) -> bool:
    return any(domain in url for domain in VALID_DOMAINS)


def is_story_url(url: str) -> bool:
    return "instagram.com/stories" in url



def build_ydl_opts(output_dir: Path, cookies_file: str, cookies_browser: str) -> dict:
    opts = {
       
        "outtmpl": str(output_dir / "%(extractor)s" / "%(uploader)s_%(id)s.%(ext)s"),

      
        "format": "b[ext=mp4]/b[ext=webm]/b",

        "noplaylist": True,      
        "restrictfilenames": True, 
        "retries": 3,              

        
        "progress_hooks": [progress_hook],
        "quiet": True,
        "no_warnings": True,
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
            # Avisa mas não para — um link ruim não deve cancelar os outros.
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
    # Exit code 1 sinaliza falha parcial ou total para quem chamar o script.
    return 0 if success == total else 1


if __name__ == "__main__":
    sys.exit(main())

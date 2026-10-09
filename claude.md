# TAREFA: Criar script Python para baixar vídeos do TikTok e Instagram

## Objetivo
Construir um projeto Python de linha de comando que baixa vídeos do TikTok
(vídeos) e do Instagram (reels, posts de feed e stories). Os links e o destino
dos arquivos são configurados em um arquivo `.env`. Ao rodar `python downloader.py`,
tudo é baixado para a pasta indicada.

## Stack (usar exatamente isto)
- Python 3.10+
- `yt-dlp`: usar como BIBLIOTECA (`import yt_dlp`), não via subprocess.
  Ele já suporta TikTok e Instagram (reels, posts, stories).
- `python-dotenv`: ler o `.env`
- Bibliotecas da stdlib: `os`, `re`, `sys`, `pathlib`
- NÃO usar scraping manual, Selenium nem APIs não oficiais. O yt-dlp resolve.

## Estrutura de arquivos
```
projeto/
├── downloader.py
├── requirements.txt     # yt-dlp, python-dotenv
├── .env.example         # modelo, versionado
├── .env                 # real, NUNCA versionado
└── .gitignore           # deve conter: .env, cookies.txt, downloads/, venv/, __pycache__/
```

## Configuração via `.env`
| Variável          | Obrigatória | Descrição |
|-------------------|-------------|-----------|
| `VIDEO_URLS`      | sim | Um ou vários links, separados por vírgula, espaço ou quebra de linha |
| `OUTPUT_DIR`      | não (padrão `./downloads`) | Pasta de destino, absoluta ou relativa; criar se não existir |
| `COOKIES_FILE`    | não | Caminho de um `cookies.txt` (formato Netscape), para stories/conteúdo com login |
| `COOKIES_BROWSER` | não | Navegador de onde o yt-dlp lê a sessão (firefox, chrome, edge, brave). Usado só se `COOKIES_FILE` estiver vazio |

## Comportamento esperado do `downloader.py`
1. Carregar o `.env` com `load_dotenv()`.
2. Ler `VIDEO_URLS`, separar com `re.split(r"[,\s]+", ...)`, remover vazios.
3. Validar cada link. Aceitar só domínios `tiktok.com`, `vm.tiktok.com`,
   `vt.tiktok.com` e `instagram.com`. Links inválidos são ignorados com aviso, sem derrubar o script.
4. Resolver `OUTPUT_DIR` com `Path(...).expanduser().resolve()` e criar com `mkdir(parents=True, exist_ok=True)`.
5. Montar as opções do yt-dlp:
   - `outtmpl`: `OUTPUT_DIR/%(extractor)s/%(uploader)s_%(id)s.%(ext)s`
   - `format`: `"bv*+ba/b"` (melhor vídeo + áudio, com fallback)
   - `merge_output_format`: `"mp4"`
   - `noplaylist`: True
   - `restrictfilenames`: True
   - `retries`: 3
   - Se `COOKIES_FILE` existir, usar `cookiefile`; senão, se `COOKIES_BROWSER`
     existir, usar `cookiesfrombrowser = (navegador,)`.
6. Baixar cada link dentro de try/except `yt_dlp.utils.DownloadError`.
   Um erro em um link NÃO pode interromper os outros.
7. Se o link for de story (`instagram.com/stories`) ou o erro mencionar "login",
   imprimir a dica: configurar `COOKIES_FILE` ou `COOKIES_BROWSER`.
8. No final, imprimir "Concluído: X/Y com sucesso" e retornar exit code 1 se
   houve alguma falha, 0 caso contrário.
9. Se não houver nenhum link válido, avisar e sair com código 1.
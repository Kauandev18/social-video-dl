# TikTok & Instagram Video Downloader

Script de linha de comando em Python para baixar vídeos do TikTok e Instagram (reels, posts e stories).

---

## Requisitos

- Python 3.10+
- Dependências listadas em `requirements.txt`

## Instalação

```bash
python -m venv venv
source venv/bin/activate        # Linux/macOS
venv\Scripts\activate           # Windows

pip install -r requirements.txt
```

Copie o arquivo de exemplo e configure suas variáveis:

```bash
cp .env.example .env
```

---

## Configuração — `.env`

| Variável          | Obrigatória | Descrição |
|-------------------|:-----------:|-----------|
| `VIDEO_URLS`      | sim | Um ou vários links separados por vírgula, espaço ou quebra de linha |
| `OUTPUT_DIR`      | não | Pasta de destino (padrão: `./downloads`) |
| `COOKIES_FILE`    | não | Caminho de um `cookies.txt` (formato Netscape) para conteúdo com login |
| `COOKIES_BROWSER` | não | Navegador de onde o yt-dlp lê a sessão: `firefox`, `chrome`, `edge`, `brave` |

Exemplo de `.env`:

```dotenv
VIDEO_URLS=https://www.tiktok.com/@user/video/123, https://www.instagram.com/reel/abc/
OUTPUT_DIR=./downloads
# COOKIES_FILE=cookies.txt
# COOKIES_BROWSER=chrome
```

---

## Uso

```bash
python downloader.py
```

O script vai:

1. Ler os links de `VIDEO_URLS`.
2. Validar domínios — aceita apenas `tiktok.com`, `vm.tiktok.com`, `vt.tiktok.com` e `instagram.com`.
3. Criar `OUTPUT_DIR` caso não exista.
4. Baixar cada vídeo em formato MP4, organizando por extractor e uploader, exibindo uma barra de progresso em tempo real.
5. Imprimir o resumo final e sair com código `0` (tudo ok) ou `1` (alguma falha).

### Saída de exemplo

```
Baixando: https://www.tiktok.com/@user/video/123
  [████████████████████░░░░░░░░░░] 66.7% | 20.1 MB / 30.2 MB | 3.4 MB/s | ETA: 3s
  [██████████████████████████████] 100.0% | concluído

Baixando: https://www.instagram.com/reel/abc/
  [██████████████████████████████] 100.0% | concluído

Concluído: 2/2 com sucesso
```

---

## Estrutura dos arquivos baixados

```
downloads/
├── tiktok/
│   └── username_videoid.mp4
└── instagram/
    └── username_postid.mp4
```

---

## Stories e conteúdo com login

Stories do Instagram e conteúdo privado exigem autenticação. Configure uma das opções abaixo no `.env`:

- **`COOKIES_FILE`** — exporte os cookies do browser como `cookies.txt` (extensão [Get cookies.txt LOCALLY](https://chrome.google.com/webstore/detail/get-cookiestxt-locally)).
- **`COOKIES_BROWSER`** — deixe o yt-dlp ler a sessão diretamente do navegador instalado (`chrome`, `firefox`, `edge`, `brave`).

---

## Plataformas suportadas

| Plataforma  | Tipo de conteúdo         | Requer login |
|-------------|--------------------------|:------------:|
| TikTok      | Vídeos públicos          | Não          |
| TikTok      | Vídeos de contas privadas| Sim          |
| Instagram   | Reels                    | Não          |
| Instagram   | Posts de feed            | Não          |
| Instagram   | Stories                  | Sim          |

---

## Métricas do script

| Métrica                        | Valor |
|-------------------------------|-------|
| Linhas de código (LOC)        | 140 |
| Funções                       | 6 (`_fmt_bytes`, `progress_hook`, `is_valid_url`, `is_story_url`, `build_ydl_opts`, `main`) |
| Dependências externas         | 2 (`yt-dlp`, `python-dotenv`) |
| Dependências stdlib           | 4 (`os`, `re`, `sys`, `pathlib`) |
| Domínios aceitos              | 4 |
| Retries por link              | 3 |
| Formato de saída              | MP4 |
| Exit codes                    | `0` = sucesso total, `1` = falha parcial ou total |
| Compatibilidade Python        | 3.10+ |

---

## Tecnologias utilizadas

| Biblioteca      | Versão  | Função |
|-----------------|---------|--------|
| `yt-dlp`        | latest  | Download de vídeos (TikTok e Instagram) |
| `python-dotenv` | latest  | Leitura do arquivo `.env` |

> O `yt-dlp` é utilizado como **biblioteca** (`import yt_dlp`), não via subprocess. Isso garante maior controle de erros e integração nativa com o código Python.

---

## Arquivos do projeto

```
projeto/
├── downloader.py       # script principal
├── requirements.txt    # dependências pip
├── .env.example        # modelo de configuração (versionado)
├── .env                # configuração real (NÃO versionado)
├── .gitignore
└── README.md
```

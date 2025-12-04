"""
Configurações globais do Scanner.
"""

# Configurações de Rede
TIMEOUT = 20
MAX_RETRIES = 3
VERIFY_SSL = False  # Ignora erros de certificado SSL (comum em alvos de recon)

# Headers Padrão (Simula um navegador real para evitar bloqueios simples)
DEFAULT_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
    "Connection": "keep-alive",
    "Upgrade-Insecure-Requests": "1",
}

# Cores para o Output (Rich)
COLOR_SUCCESS = "green"
COLOR_WARNING = "yellow"
COLOR_ERROR = "red"
COLOR_INFO = "cyan"

# Configurações de Execução
MAX_WORKERS = 5
MAX_SUBDOMAINS = 100
CACHE_ENABLED = False
CACHE_TTL = 3600  # segundos

# Configurações de Output
OUTPUT_DIR = "results"
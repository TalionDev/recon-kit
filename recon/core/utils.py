import socket
import tldextract
from rich.console import Console
from recon.config import COLOR_ERROR

console = Console()

def normalize_domain(url_or_domain: str) -> str:
    """
    Remove protocolo (http/s), caminhos e normaliza para 'exemplo.com'.
    """
    extracted = tldextract.extract(url_or_domain)
    # Garante que temos dominio e sufixo
    if extracted.domain and extracted.suffix:
        return f"{extracted.domain}.{extracted.suffix}"
    # Fallback caso tldextract falhe ou seja localhost/IP
    return url_or_domain.replace("https://", "").replace("http://", "").split("/")[0]

def resolve_ip(domain: str) -> str:
    """
    Resolve o IP principal do domínio. Retorna None se falhar.
    """
    try:
        ip = socket.gethostbyname(domain)
        return ip
    except socket.gaierror:
        # Não printamos erro aqui para não sujar a UI, o main trata isso.
        return None
    except Exception as e:
        return None
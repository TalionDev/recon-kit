from recon.core.fetcher import Fetcher
import time

def run(domain, ip=None):
    """
    Coleta subdomínios via Certificate Transparency (crt.sh).
    Resiliente a falhas temporárias do crt.sh (Error 502).
    """
    fetcher = Fetcher()
    url = "https://crt.sh/"
    params = {"q": domain, "output": "json"}
    
    # Crt.sh é instável, tentamos um fetch direto com a config do Fetcher
    data = fetcher.get_json(url, params=params)
    
    subdomains = set()
    
    if data and isinstance(data, list):
        for entry in data:
            name_value = entry.get('name_value', '')
            # Crt.sh pode retornar múltiplas linhas em um certificado
            lines = name_value.split('\n')
            for line in lines:
                # Limpeza básica
                clean = line.strip().lower()
                # Remove wildcards (*.exemplo.com -> exemplo.com)
                clean = clean.replace('*.', '')
                if clean:
                    subdomains.add(clean)
    
    return {
        "source": "crt.sh",
        "count": len(subdomains),
        "subdomains": sorted(list(subdomains))[:100] # Limita a 100 para não poluir o JSON
    }
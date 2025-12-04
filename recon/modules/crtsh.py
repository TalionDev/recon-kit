from recon.modules.base import BaseModule
from recon.config import MAX_SUBDOMAINS
from typing import Optional


class CrtshModule(BaseModule):
    """
    Coleta subdomínios via Certificate Transparency (crt.sh).
    Resiliente a falhas temporárias do crt.sh (Error 502).
    """
    CATEGORY = "passive_recon"
    NAME = "crtsh"
    
    def run(self, domain: str, ip: Optional[str]) -> dict:
        url = "https://crt.sh/"
        params = {"q": domain, "output": "json"}
        
        # Crt.sh é instável, tentamos um fetch direto com a config do Fetcher
        data = self.fetcher.get_json(url, params=params)
        
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
            "subdomains": sorted(list(subdomains))[:MAX_SUBDOMAINS]
        }


# Função de compatibilidade retroativa
def run(domain, ip=None):
    """Wrapper de compatibilidade para chamadas antigas."""
    return CrtshModule().run(domain, ip)
from recon.modules.base import BaseModule
from typing import Optional


class SsllabsModule(BaseModule):
    """
    Consulta API SSL Labs.
    AVISO: V3 depreciada. Tentamos ler do cache (fromCache=on).
    Se não houver cache, não iniciamos scan novo para manter 'passivo' e rápido.
    """
    CATEGORY = "https"
    NAME = "ssllabs"
    
    def run(self, domain: str, ip: Optional[str]) -> dict:
        url = "https://api.ssllabs.com/api/v3/analyze"
        
        params = {
            "host": domain,
            "all": "done",
            "fromCache": "on",  # Apenas dados cacheados
            "maxAge": 48        # Aceita cache de até 48 horas
        }
        
        data = self.fetcher.get_json(url, params=params)
        
        if not data:
            return {"status": "API Unavailable or Timeout"}

        status = data.get("status")
        
        if status == "READY":
            endpoints = data.get("endpoints", [])
            server_info = []
            for e in endpoints:
                server_info.append({
                    "ip": e.get("ipAddress"),
                    "grade": e.get("grade"),
                    "details": e.get("statusMessage")
                })
            return {
                "status": "Cached Report",
                "endpoints": server_info
            }
        else:
            return {"status": "No cached report available (Passive Mode)"}


# Função de compatibilidade retroativa
def run(domain, ip=None):
    """Wrapper de compatibilidade para chamadas antigas."""
    return SsllabsModule().run(domain, ip)
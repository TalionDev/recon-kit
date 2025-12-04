from recon.modules.base import BaseModule


class InternetdbModule(BaseModule):
    """
    Consulta Shodan InternetDB (Gratuito/Sem Key) usando o IP.
    Retorna Portas, CVEs e Tags.
    """
    CATEGORY = "reputation"
    NAME = "internetdb"
    
    def run(self, domain: str, ip: str | None) -> dict:
        if not ip:
            return self.error_response("NO_IP", "IP address is required")

        url = f"https://internetdb.shodan.io/{ip}"
        
        data = self.fetcher.get_json(url)
        
        if not data:
            return {"status": "No data found for this IP"}

        return {
            "ip": data.get("ip"),
            "hostnames": data.get("hostnames", []),
            "ports": data.get("ports", []),
            "cpes": data.get("cpes", []),
            "vulns": data.get("vulns", []),
            "tags": data.get("tags", [])
        }


# Função de compatibilidade retroativa
def run(domain, ip):
    """Wrapper de compatibilidade para chamadas antigas."""
    return InternetdbModule().run(domain, ip)
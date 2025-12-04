from recon.modules.base import BaseModule


class HeadersModule(BaseModule):
    """
    Verifica headers de segurança e informações do servidor.
    Tenta HTTPS primeiro, fallback para HTTP.
    """
    CATEGORY = "headers"
    NAME = "headers"
    
    def run(self, domain: str, ip: str | None) -> dict:
        target = f"https://{domain}"
        
        resp = self.fetcher.head(target)
        if not resp:
            target = f"http://{domain}"
            resp = self.fetcher.head(target)
        
        if not resp:
            return self.error_response("CONNECTION_ERROR", "Could not connect via HTTP/HTTPS")

        h = resp.headers
        
        # Headers críticos de segurança
        sec_headers = {
            "Strict-Transport-Security": h.get("Strict-Transport-Security", "MISSING"),
            "X-Frame-Options": h.get("X-Frame-Options", "MISSING"),
            "X-Content-Type-Options": h.get("X-Content-Type-Options", "MISSING"),
            "Content-Security-Policy": h.get("Content-Security-Policy", "MISSING"),
            "X-XSS-Protection": h.get("X-XSS-Protection", "MISSING"),
        }

        present = sum(1 for v in sec_headers.values() if v != "MISSING")
        
        return {
            "url_tested": target,
            "server": h.get("Server", "Hidden"),
            "powered_by": h.get("X-Powered-By", "Hidden"),
            "security_headers": sec_headers,
            "score": f"{present}/5"
        }


# Função de compatibilidade retroativa
def run(domain, ip=None):
    """Wrapper de compatibilidade para chamadas antigas."""
    return HeadersModule().run(domain, ip)
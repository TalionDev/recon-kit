from recon.modules.base import BaseModule


class ObservatoryModule(BaseModule):
    """
    Consulta Mozilla Observatory.
    Usa o endpoint Analyze com flag rescan=false.
    """
    CATEGORY = "https"
    NAME = "observatory"
    
    def run(self, domain: str, ip: str | None) -> dict:
        url = "https://http-observatory.security.mozilla.org/api/v1/analyze"
        
        params = {
            "host": domain
        }
        
        # Observatory pode retornar 404 se nunca foi scaneado. O fetcher retorna None.
        data = self.fetcher.get_json(url, params=params)
        
        if not data or "error" in data:
            return {"status": "No previous scan found"}

        return {
            "scan_id": data.get("scan_id"),
            "grade": data.get("grade"),
            "score": data.get("score"),
            "tests_passed": data.get("tests_passed"),
            "tests_failed": data.get("tests_failed"),
            "scan_time": data.get("end_time")
        }


# Função de compatibilidade retroativa
def run(domain, ip=None):
    """Wrapper de compatibilidade para chamadas antigas."""
    return ObservatoryModule().run(domain, ip)
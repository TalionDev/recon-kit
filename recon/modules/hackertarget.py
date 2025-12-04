from recon.modules.base import BaseModule


class HackertargetModule(BaseModule):
    """
    Consulta HackerTarget para DNS Lookup e Reverse IP.
    Nota: A API free tem limites estritos.
    """
    CATEGORY = "passive_recon"
    NAME = "hackertarget"
    
    def run(self, domain: str, ip: str | None) -> dict:
        results = {}

        # 1. DNS Lookup (A, AAAA, MX, NS, TXT)
        dns_url = "https://api.hackertarget.com/dnslookup/"
        dns_resp = self.fetcher.get(dns_url, params={"q": domain})
        
        if dns_resp and "error" not in dns_resp.text.lower() and "API count exceeded" not in dns_resp.text:
            records = {}
            for line in dns_resp.text.split('\n'):
                if line.strip():
                    parts = line.split(' : ')
                    if len(parts) >= 2:
                        key = parts[0].strip()
                        val = parts[1].strip()
                        if key not in records: records[key] = []
                        records[key].append(val)
            results["dns_records"] = records
        else:
            results["dns_records"] = "API Limit Exceeded or Error"

        return results


# Função de compatibilidade retroativa
def run(domain, ip=None):
    """Wrapper de compatibilidade para chamadas antigas."""
    return HackertargetModule().run(domain, ip)
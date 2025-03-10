from recon.core.fetcher import Fetcher

def run(domain, ip=None):
    """
    Consulta HackerTarget para DNS Lookup e Reverse IP.
    Nota: A API free tem limites estritos.
    """
    fetcher = Fetcher()
    results = {}

    # 1. DNS Lookup (A, AAAA, MX, NS, TXT)
    dns_url = "https://api.hackertarget.com/dnslookup/"
    dns_resp = fetcher.get(dns_url, params={"q": domain})
    
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
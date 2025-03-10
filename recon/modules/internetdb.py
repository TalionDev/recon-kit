from recon.core.fetcher import Fetcher

def run(domain, ip):
    """
    Consulta Shodan InternetDB (Gratuito/Sem Key) usando o IP.
    Retorna Portas, CVEs e Tags.
    """
    if not ip:
        return {"error": "No IP resolved"}

    fetcher = Fetcher()
    url = f"https://internetdb.shodan.io/{ip}"
    
    data = fetcher.get_json(url)
    
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
from recon.core.fetcher import Fetcher

def run(domain, ip):
    """
    Verifica reputação em GreyNoise (Community API) e gera links para AbuseIPDB.
    Não realiza scraping agressivo no AbuseIPDB para evitar bloqueio.
    """
    if not ip:
        return {"error": "No IP"}

    fetcher = Fetcher()
    results = {}

    # 1. GreyNoise Community API (JSON Free)
    # Retorna se o IP é "Noise" (scanner de internet conhecido) ou "Riot" (serviço benigno comum)
    gn_url = f"https://api.greynoise.io/v3/community/{ip}"
    gn_data = fetcher.get_json(gn_url)
    
    if gn_data:
        results["greynoise"] = {
            "classification": gn_data.get("classification", "unknown"),
            "noise": gn_data.get("noise"),
            "riot": gn_data.get("riot"),
            "message": gn_data.get("message") # Ex: "IP not observed scanning the internet"
        }
    else:
        results["greynoise"] = {"status": "Not found in GreyNoise Community DB"}

    # 2. AbuseIPDB (Link Seguro)
    # Scraping direto é bloqueado por Cloudflare. Geramos o link para verificação manual.
    results["abuseipdb"] = {
        "status": "Manual Check Recommended",
        "link": f"https://www.abuseipdb.com/check/{ip}"
    }

    return results
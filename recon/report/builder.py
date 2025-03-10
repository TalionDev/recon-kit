import json
import os
from datetime import datetime

class ReportBuilder:
    """
    Gera relatórios em JSON (máquina) e Markdown (humano).
    """
    def __init__(self, domain, data):
        self.domain = domain
        self.data = data
        self.timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        self.output_dir = "results"
        
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)

    def save_json(self):
        filename = f"{self.output_dir}/{self.domain}_{self.timestamp}.json"
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(self.data, f, indent=4, ensure_ascii=False)
        return filename

    def save_markdown(self):
        filename = f"{self.output_dir}/{self.domain}_{self.timestamp}.md"
        
        # Extração segura de dados (get com defaults)
        ip = self.data.get('resolved_ip', 'N/A')
        crt = self.data.get('passive_recon', {}).get('crtsh', {})
        idb = self.data.get('reputation', {}).get('internetdb', {})
        head = self.data.get('headers', {})
        ssl = self.data.get('https', {}).get('ssllabs', {})
        
        md = f"# Recon Report: {self.domain}\n"
        md += f"**Data:** {self.timestamp} | **Target IP:** {ip}\n\n"
        
        # Seção 1: Superfície de Ataque
        md += "## 🛡️ Superfície de Ataque & Infra\n"
        md += f"- **Subdomínios (crt.sh):** {crt.get('count', 0)} encontrados\n"
        md += f"- **Portas Abertas (Shodan):** {', '.join(map(str, idb.get('ports', []))) or 'Nenhuma detectada'}\n"
        md += f"- **Vulnerabilidades (CVEs):** {', '.join(idb.get('vulns', [])) or 'Nenhuma listada'}\n"
        
        # Seção 2: Headers
        md += "\n## 🔒 Segurança Web (Headers)\n"
        if "error" not in head:
            md += f"**Server:** {head.get('server')} | **Powered By:** {head.get('powered_by')}\n\n"
            md += "| Header | Status |\n|---|---|\n"
            for k, v in head.get('security_headers', {}).items():
                icon = "✅" if v != "MISSING" else "❌"
                md += f"| {k} | {icon} {v} |\n"
        else:
            md += "Não foi possível conectar ao alvo via HTTP/HTTPS.\n"

        # Seção 3: SSL/Reputação
        md += "\n## 🌐 SSL & Reputação\n"
        md += f"- **SSL Labs Grade:** {ssl.get('endpoints', [{'grade': 'N/A'}])[0].get('grade') if 'endpoints' in ssl else 'N/A'}\n"
        
        gn = self.data.get('reputation', {}).get('greynoise', {})
        md += f"- **GreyNoise:** {gn.get('classification', 'Unknown')}\n"
        
        link = self.data.get('reputation', {}).get('abuseipdb', {}).get('link', '#')
        md += f"- **AbuseIPDB:** [Verificar Manualmente]({link})\n"

        with open(filename, 'w', encoding='utf-8') as f:
            f.write(md)
        return filename
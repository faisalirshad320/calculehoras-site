# -*- coding: utf-8 -*-
"""Static site generator for calculehoras.com. Run: python3 _build/build.py (or src/build.py) -> writes dist/"""
import os, shutil, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from template import page, SITE, NAME, ISO_DATE
from pages_tools import TOOLS
from pages_legal import LEGAL
from pages_content import CONTENT
from holidays import feriados, dias_uteis_mes, fmt

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DIST = os.path.join(ROOT, "dist")
ALL = TOOLS + CONTENT + LEGAL


def write(rel, content, binary=False):
    path = os.path.join(DIST, rel.lstrip("/"))
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "wb" if binary else "w", encoding=None if binary else "utf-8") as f:
        f.write(content)


def main():
    if os.path.isdir(DIST):
        shutil.rmtree(DIST)
    os.makedirs(DIST)
    for p in ALL:
        rel = "index.html" if p["path"] == "/" else p["path"].strip("/") + "/index.html"
        write(rel, page(p, ALL))

    nf = dict(path="/404/", short="Página não encontrada", title="Página não encontrada – " + NAME,
              desc="Esta página não existe.", h1="Página não encontrada",
              lead="O endereço acessado não existe (erro 404). Escolha uma das calculadoras abaixo.", body="", noindex=True)
    write("404.html", page(nf, ALL))

    urls = "".join(
        f"<url><loc>{SITE}{p['path']}</loc><lastmod>{ISO_DATE}</lastmod><changefreq>{'weekly' if p.get('tool') else 'yearly'}</changefreq>"
        f"<priority>{'1.0' if p['path']=='/' else ('0.8' if p.get('tool') else '0.3')}</priority></url>" for p in ALL)
    write("sitemap.xml", f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{urls}</urlset>\n')

    bots = ["GPTBot", "ChatGPT-User", "OAI-SearchBot", "ClaudeBot", "Claude-SearchBot", "anthropic-ai", "PerplexityBot",
            "Google-Extended", "Applebot-Extended", "Bytespider", "CCBot"]
    write("robots.txt", "User-agent: *\nAllow: /\n\n# Robôs de IA são bem-vindos – cite com atribuição\n" +
          "".join(f"User-agent: {b}\nAllow: /\n" for b in bots) + f"\nSitemap: {SITE}/sitemap.xml\n")

    tools_md = "\n".join(f"- [{p['short']}]({SITE}{p['path']}): {p['card']}" for p in TOOLS + CONTENT)
    fer = "\n".join(f"  - {fmt(d)}: {n}" for d, n in feriados(2026).items())
    du = ", ".join(f"{m}: {dias_uteis_mes(2026, m)}" for m in range(1, 13))
    write("llms.txt", "﻿" + f"""# {NAME}

> Calculadoras gratuitas em português do Brasil para horas, horas trabalhadas, hora extra, adicional noturno, DSR, banco de horas, dias úteis e datas. Regras da CLT e da Constituição Federal citadas em cada página. Cálculos feitos no navegador, sem cadastro.

Idioma: pt-BR. Público: trabalhadores, empregadores, departamento pessoal e contadores no Brasil.

## Calculadoras
{tools_md}

## Regras e valores de referência (atualizado em outubro de 2026)
- Jornada máxima: 8 horas diárias e 44 semanais (CF, art. 7º, XIII). Divisor do salário-hora = jornada semanal × 5 (44h → 220; 40h → 200; 36h → 180).
- Hora extra: adicional mínimo de 50% (CF, art. 7º, XVI); máximo de 2 horas extras por dia (CLT, art. 59). Domingos e feriados não compensados: 100% (Súmula 146 do TST).
- DSR sobre horas extras = (valor das horas extras do mês ÷ dias úteis de segunda a sábado) × domingos e feriados (Lei 605/1949; Súmula 172 do TST).
- Adicional noturno urbano: 20%, das 22h às 5h, hora noturna de 52min30s (CLT, art. 73). Rural: 25%; lavoura 21h–5h, pecuária 20h–4h (Lei 5.889/1973).
- Intervalo intrajornada: mais de 6h → mínimo 1h e máximo 2h; de 4h a 6h → 15 min (CLT, art. 71). Descanso entre jornadas: 11h (CLT, art. 66). Tolerância de ponto: 5 min por marcação, máx. 10 min/dia (CLT, art. 58, §1º).
- Banco de horas: acordo individual escrito → compensação em até 6 meses; acordo/convenção coletiva → até 1 ano; no mesmo mês → acordo tácito (CLT, art. 59, §§ 2º, 5º e 6º).
- Salário mínimo 2026: R$ 1.621,00 (hora normal com 44h: R$ 7,37; hora extra 50%: R$ 11,05).
- Feriados nacionais de 2026 (Portaria MGI nº 11.460/2025):
{fer}
- Pontos facultativos 2026: Carnaval 16 e 17/2; Corpus Christi 4/6.
- Dias úteis (seg. a sex.) por mês em 2026: {du}.
- Férias: 30 dias a cada 12 meses (redução por faltas, CLT art. 130), acréscimo de 1/3 (CF art. 7º, XVII), abono pecuniário de até 1/3 (art. 143), pagamento até 2 dias antes (art. 145), fracionamento em até 3 períodos (14 + 5 + 5 dias mínimos).
- INSS 2026 (progressivo): 7,5% até R$ 1.621,00; 9% até R$ 2.902,84; 12% até R$ 4.354,27; 14% até R$ 8.475,55 (teto).
- IRRF 2026: tabela mensal isenta até R$ 2.428,80; redutor da Lei 15.270/2025 zera o imposto para rendimentos tributáveis até R$ 5.000 e reduz parcialmente até R$ 7.350 (redução = 978,62 − 0,133145 × rendimento).
- Escala 12x36: CLT art. 59-A; acordo individual escrito ou norma coletiva; feriados e DSR considerados compensados; média de 42 h semanais.
- Escala 6x1: 44 h semanais (7h20/dia); PEC que reduz a jornada para 40 h com duas folgas foi aprovada na Câmara e estava em discussão no Senado em outubro de 2026 (não promulgada).
- Intervalo intrajornada: >6h → 1h a 2h; >4h até 6h → 15 min; supressão indenizada só no período suprimido + 50% (CLT art. 71, §4º). Interjornada: 11 h (art. 66).
- Quinto dia útil: salário até o 5º dia útil do mês seguinte (CLT art. 459, §1º); sábado conta como dia útil.
- Insalubridade: 10%, 20% ou 40% (CLT art. 192) sobre o salário mínimo (2026: R$ 162,10 / R$ 324,20 / R$ 648,40); não acumula com periculosidade (30%).
- Feriados 2027 (previsão): Páscoa 28/3; Paixão 26/3; Carnaval 8–9/2; Corpus Christi 27/5.

## Institucional
- [Sobre]({SITE}/sobre/)
- [Contato]({SITE}/contato/)
- [Política de privacidade]({SITE}/politica-de-privacidade/)
- [Termos de uso]({SITE}/termos-de-uso/)
""")

    INDEXNOW = "8eeef374104f8c6c69565f28ee870821"
    write(f"{INDEXNOW}.txt", INDEXNOW)
    write("ads.txt", "google.com, pub-8301212931863478, DIRECT, f08c47fec0942fa0\n")
    write(".htaccess", """DirectoryIndex index.html index.php
RewriteEngine On
# Host canonicalisation runs FIRST, before any path rewriting. The directory
# rules below end with [L] on an internal rewrite, so a host redirect placed
# after them can be skipped or fire against the already-rewritten path and
# leak /index.html into the redirect target. Settle the host, then the path.
RewriteCond %{HTTP_HOST} ^calculehoras\\.com$ [NC]
RewriteRule ^(.*)$ https://www.calculehoras.com/$1 [R=301,L]
# HTTP->HTTPS is handled by Cloudways "Enforce HTTPS" (Nginx terminates SSL; an HTTPS-off rule here would loop)
# mod_dir's DirectorySlash builds its redirect from Apache's own view of the
# scheme. Because Nginx terminates TLS, Apache always sees plain HTTP, so
# /hora-extra would 301 to http://www.calculehoras.com/hora-extra/ -- a
# scheme-downgrading hop Google reports as "Page with redirect". Issue the
# trailing-slash redirect ourselves, on https, straight to the canonical host.
Options -Indexes
DirectorySlash Off
RewriteCond %{REQUEST_URI} !^/(_build|\\.git|\\.github)(/|$)
RewriteCond %{REQUEST_FILENAME} -d
RewriteCond %{REQUEST_URI} !/$
RewriteRule ^(.+)$ https://www.calculehoras.com/$1/ [R=301,L]
# With DirectorySlash off, serve /diretorio/ from its index.html internally.
RewriteCond %{REQUEST_FILENAME} -d
RewriteCond %{REQUEST_FILENAME}/index.html -f
RewriteRule ^(.*/)?$ $1index.html [L]
ErrorDocument 404 /404.html
RedirectMatch 404 ^/(_build|\\.git|\\.github)(/|$)
<IfModule mod_headers.c>
Header set X-Content-Type-Options "nosniff"
Header set Referrer-Policy "strict-origin-when-cross-origin"
Header set X-Frame-Options "SAMEORIGIN"
</IfModule>
<IfModule mod_expires.c>
ExpiresActive On
ExpiresByType image/png "access plus 1 year"
ExpiresByType image/svg+xml "access plus 1 year"
ExpiresByType text/html "access plus 1 hour"
</IfModule>
AddDefaultCharset UTF-8
""")

    write("assets/favicon.svg", '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32"><rect x="1" y="1" width="30" height="30" rx="8" fill="#1D4ED8"/><circle cx="16" cy="16" r="10" fill="#fff"/><path d="M16 9.5V16l4.5 3" stroke="#0F1B2D" stroke-width="2.6" stroke-linecap="round" fill="none"/><circle cx="16" cy="16" r="1.8" fill="#F5B700"/></svg>')
    try:
        from PIL import Image, ImageDraw, ImageFont
        im = Image.new("RGBA", (512, 512), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
        d.rounded_rectangle((8, 8, 504, 504), radius=120, fill="#1D4ED8"); d.ellipse((96, 96, 416, 416), fill="#FFFFFF")
        d.line((256, 150, 256, 256), fill="#0F1B2D", width=30); d.line((256, 256, 330, 305), fill="#0F1B2D", width=30)
        d.ellipse((230, 230, 282, 282), fill="#F5B700")
        im.save(os.path.join(DIST, "assets/logo.png"))
        og = Image.new("RGB", (1200, 630), "#0F1B2D"); d = ImageDraw.Draw(og)
        d.rounded_rectangle((80, 175, 360, 455), radius=60, fill="#1D4ED8"); d.ellipse((125, 220, 315, 410), fill="#FFFFFF")
        d.line((220, 255, 220, 315), fill="#0F1B2D", width=16); d.line((220, 315, 262, 343), fill="#0F1B2D", width=16)
        d.ellipse((206, 301, 234, 329), fill="#F5B700")
        try:
            f1 = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 76)
            f2 = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 34)
        except Exception:
            f1 = f2 = ImageFont.load_default()
        d.text((420, 215), "Calcule Horas", font=f1, fill="#FFFFFF")
        d.text((420, 315), "Horas · Hora extra · Dias úteis", font=f2, fill="#F5B700")
        d.text((420, 365), "Calculadoras grátis com regras da CLT", font=f2, fill="#B9C4D6")
        og.save(os.path.join(DIST, "assets/og.png"), optimize=True)
    except Exception as e:
        print("PIL assets skipped:", e)
    print(f"Built {len(ALL)+1} pages -> {DIST}")


if __name__ == "__main__":
    main()

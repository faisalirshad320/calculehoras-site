# Build brief — calculehoras.com (pt-BR)

## Goal
Rank a new DR-0 domain in Google Brasil for tool-intent searches around hours, overtime and working days, and monetise with AdSense. Every page is a working calculator first, explanatory content second.

## Evidence (Ahrefs, Oct 2026)
- "calculadora de horas" 141k/mo KD0 — #1 is calculadora-online.xyz (DR14, 162k visits)
- "calculadora hora extra" 17k KD0 — #1 kazacapital (DR10, 0 backlinks, result gated behind a lead form); #2 DR0
- Weak SERPs confirmed for horas trabalhadas, dias úteis, hora extra clusters

## Topical map (one page per search intent / parent topic)
| URL | Primary keyword | Supporting cluster | ~Vol/mo |
|---|---|---|---|
| / | calculadora de horas | calcular horas, somar horas, calculadora de tempo horas, calculadora de horas online | 160k |
| /horas-trabalhadas/ | calculadora de horas trabalhadas | calcular horas trabalhadas, horas trabalhadas, como calcular horas trabalhadas, contador de horas trabalhadas | 52k |
| /hora-extra/ | calculadora hora extra | calculadora de horas extras, como calcular hora extra, cálculo hora extra, valor da hora extra, hora extra 50 | 110k |
| /adicional-noturno/ | adicional noturno | calculadora adicional noturno, hora noturna reduzida | 41k |
| /dsr-hora-extra/ | calculadora dsr hora extra | calcular dsr, calculadora dsr | 4k |
| /dias-uteis/ | calculadora de dias úteis | dias úteis, contador de dias úteis, quantos dias úteis tem um mês, dias úteis 2026 | 77k |
| /calculadora-de-datas/ | calculadora de datas | anos meses e dias, dias corridos, dias entre datas, somar datas | 52k |
| /quantos-dias-faltam/ | quantos dias faltam | contagem regressiva, dias até o Natal | 10k |
| /banco-de-horas/ | banco de horas | banco de horas como funciona, calcular banco de horas | 16k |
| /horas-em-decimal/ | converter horas em decimal | horas em decimal | 1k |
Legal/trust: /sobre/, /contato/, /politica-de-privacidade/ (LGPD), /termos-de-uso/

## Legal facts used (verify yearly)
- Salário mínimo 2026: R$ 1.621 (decreto federal, vigente 1/1/2026)
- Feriados nacionais 2026 (Portaria MGI 11.460/2025): 1/1, 3/4 Paixão de Cristo, 21/4, 1/5, 7/9, 12/10, 2/11, 15/11, 20/11 Consciência Negra (nacional desde 2024, Lei 14.759/2023), 25/12. Pontos facultativos: Carnaval 16–17/2, Corpus Christi 4/6.
- CLT: jornada 8h/dia, 44h/sem (CF art. 7º XIII); hora extra mín. +50% (CF 7º XVI), máx. 2h/dia (art. 59); domingo/feriado não compensado +100% (Súmula 146 TST); divisor = jornada semanal × 5 (220/200/180)
- Adicional noturno urbano 20%, 22h–5h, hora reduzida 52min30s (art. 73); rural 25% (Lei 5.889/73: lavoura 21h–5h, pecuária 20h–4h)
- DSR sobre horas extras: (HE do mês ÷ dias úteis) × domingos e feriados (Lei 605/49; Súmula 172 TST)
- Intervalo intrajornada: >6h = 1–2h; >4h até 6h = 15 min (art. 71). Interjornada 11h (art. 66). Tolerância 5 min/marcação, máx. 10 min/dia (art. 58 §1)
- Banco de horas: acordo individual escrito → compensação em até 6 meses (art. 59 §5); acordo/convenção coletiva → até 1 ano (§2); mesmo mês → acordo tácito (§6)

## SEO / AEO / GEO requirements
- Title ≤ 60 chars with primary keyword first; meta description with action + benefit; one H1
- Answer-first lead paragraph (citable by AI), formula shown in plain text, worked example, FAQ (FAQPage schema)
- Schema @graph: WebSite, Organization, WebPage, WebApplication (free), BreadcrumbList, FAQPage
- Internal links: every page links contextually to 2–3 siblings + "Outras calculadoras" grid
- robots.txt allows AI crawlers; llms.txt with tool list + key legal facts; sitemap.xml; canonical + hreflang pt-BR
- All calculations client-side; no data sent; LGPD privacy + Consent Mode v2 defaults denied
- Mobile-first, fast (no frameworks), accessible (labels, focus, aria-live results)

## Design
Distinct from stundenrechnen: deep ink + Brazilian-blue primary, warm sun-yellow highlight for results, IBM Plex Sans. Calculator card is the hero; result block big tabular numerals.

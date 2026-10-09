# calculehoras.com

Calculadoras de horas, hora extra, adicional noturno, DSR, banco de horas e dias úteis (pt-BR, AdSense).

- Site estático na raiz do repositório → Cloudways `public_html` via git pull (deploy automático).
- Gerador: `_build/` → `python3 _build/build.py` gera `dist/`; copie `dist/*` para a raiz antes do commit.
- `/_build/` é bloqueado no `.htaccess`.
- Revisar anualmente: salário mínimo, feriados nacionais (portaria MGI), datas em `_build/template.py` (UPDATED/ISO_DATE).

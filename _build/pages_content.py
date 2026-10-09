# -*- coding: utf-8 -*-
"""Content-expansion pages (Oct 2026): feriados, calendário, escalas, férias, idade, intervalo, quinto dia útil, insalubridade."""
import datetime as dt
from holidays import feriados, easter, MESES, fmt, DIAS_SEMANA

SEM = ["D", "S", "T", "Q", "Q", "S", "S"]  # Sunday-first header


def facultativos(y):
    e = easter(y)
    return {e - dt.timedelta(days=48): "Carnaval (ponto facultativo)", e - dt.timedelta(days=47): "Carnaval (ponto facultativo)",
            e - dt.timedelta(days=46): "Quarta-feira de Cinzas (ponto facultativo até 14h)", e + dt.timedelta(days=60): "Corpus Christi (ponto facultativo)"}


def cal_html(y):
    fer, fac = feriados(y), facultativos(y)
    out = []
    for m in range(1, 13):
        d = dt.date(y, m, 1)
        lead = (d.weekday() + 1) % 7  # Sunday=0
        cells = ["<td></td>"] * lead
        notes = []
        while d.month == m:
            cls = []
            if d in fer:
                cls.append("fer"); notes.append(f"<li><b>{d.day}</b> – {fer[d]}</li>")
            elif d in fac:
                cls.append("fac"); notes.append(f"<li><b>{d.day}</b> – {fac[d]}</li>")
            if d.weekday() == 6:
                cls.append("dom")
            cells.append(f'<td{" class=%s" % chr(34) + " ".join(cls) + chr(34) if cls else ""}>{d.day}</td>')
            d += dt.timedelta(days=1)
        while len(cells) % 7:
            cells.append("<td></td>")
        rows = "".join("<tr>" + "".join(cells[i:i + 7]) + "</tr>" for i in range(0, len(cells), 7))
        out.append(f'<div class="mon"><h3>{MESES[m-1].capitalize()} {y}</h3><table><thead><tr>{"".join(f"<th>{s}</th>" for s in SEM)}</tr></thead><tbody>{rows}</tbody></table>'
                   f'{"<ul>" + "".join(notes) + "</ul>" if notes else ""}</div>')
    return '<div class="cal">' + "".join(out) + '</div><p class="hint"><span class="lg fer"></span> feriado nacional &nbsp; <span class="lg fac"></span> ponto facultativo &nbsp; <span style="color:#B42318;font-weight:700">domingos em vermelho</span></p>'


def prolongados(y):
    """Long weekends: holiday/facultativo on Mon/Fri (3 days) or Tue/Thu (possible 4-day 'emenda')."""
    allh = {**facultativos(y), **feriados(y)}
    items = []
    for d, n in sorted(allh.items()):
        if "Cinzas" in n:
            continue
        wd = d.weekday()
        if wd in (0, 4):
            items.append(f"<li><strong>{fmt(d)}</strong> – {n}: fim de semana de 3 dias</li>")
        elif wd in (1, 3):
            br = d - dt.timedelta(days=1) if wd == 1 else d + dt.timedelta(days=1)
            items.append(f"<li><strong>{fmt(d)}</strong> – {n}: feriadão de 4 dias se houver emenda em {br.day:02d}/{br.month:02d}</li>")
    return "<ul>" + "".join(items) + "</ul>"


def fer_table(y):
    rows = ""
    for d, n in sorted({**feriados(y), **facultativos(y)}.items()):
        tipo = "Ponto facultativo" if d in facultativos(y) and d not in feriados(y) else "Feriado nacional"
        rows += f"<tr><td>{d.day:02d}/{d.month:02d}/{y}</td><td>{DIAS_SEMANA[d.weekday()]}</td><td>{n.replace(' (ponto facultativo)', '').replace(' (ponto facultativo até 14h)', '')}</td><td>{tipo}</td></tr>"
    return f'<div class="tw"><table class="t"><thead><tr><th>Data</th><th>Dia da semana</th><th>Feriado</th><th>Tipo</th></tr></thead><tbody>{rows}</tbody></table></div>'


def quinto(y, m):
    hol = feriados(y)
    d, n = dt.date(y, m, 1), 0
    while True:
        if d.weekday() < 6 and d not in hol:
            n += 1
            if n == 5:
                return d
        d += dt.timedelta(days=1)


def quinto_table(y):
    rows = ""
    for m in range(1, 13):
        ref = MESES[m - 2] if m > 1 else "dezembro"
        refy = y if m > 1 else y - 1
        rows += f"<tr><td>Salário de {ref}/{refy}</td><td>{fmt(quinto(y, m))}</td></tr>"
    return f'<div class="tw"><table class="t"><thead><tr><th>Competência</th><th>5º dia útil (prazo de pagamento)</th></tr></thead><tbody>{rows}</tbody></table></div>'


def count_week(y, wd):
    return sum(1 for d in feriados(y) if d.weekday() == wd)


def weekday_holidays(y):
    return sum(1 for d in feriados(y) if d.weekday() < 5)


NEXT_JS = r"""
(function(){var t=new Date();t.setHours(12,0,0,0);var L=[];[t.getFullYear(),t.getFullYear()+1].forEach(function(y){var F=feriados(y);Object.keys(F).sort().forEach(function(k){L.push([k,F[k]])})});
for(var i=0;i<L.length;i++){var d=new Date(L[i][0]+'T12:00:00');if(d>=t){var n=Math.round((d-t)/864e5);document.getElementById('nx').textContent=n===0?'Hoje é feriado!':n+(n===1?' dia':' dias');document.getElementById('nxd').textContent='até '+L[i][1]+' – '+d.toLocaleDateString('pt-BR',{weekday:'long',day:'2-digit',month:'long',year:'numeric'});break}}})();"""

NEXT_BOX = """<div class="calc"><h2>Próximo feriado nacional</h2><div class="result" aria-live="polite"><div class="big" id="nx">–</div><div class="sub" id="nxd"></div></div>
<p class="hint">Contagem a partir da data do seu dispositivo. Para contar dias úteis até uma data, use a <a href="/dias-uteis/">calculadora de dias úteis</a>.</p></div>"""

# ============================================================ Feriados 2026
FER26 = {
    "path": "/feriados-2026/", "short": "Feriados 2026", "tool": True, "group": "cal",
    "card": "Lista oficial dos feriados nacionais e pontos facultativos de 2026, com feriadões.",
    "title": "Feriados 2026 – Lista de Feriados Nacionais e Feriadões",
    "desc": "Todos os feriados nacionais de 2026 com dia da semana, pontos facultativos (Carnaval, Corpus Christi) e a lista de feriadões e emendas do ano. Atualizado conforme a Portaria MGI.",
    "h1": "Feriados 2026: lista completa e feriadões",
    "lead": f"Em 2026 o Brasil tem 10 feriados nacionais, dos quais {weekday_holidays(2026)} caem em dias úteis, além de 4 pontos facultativos. Veja as datas com o dia da semana, os feriados prolongados e quanto falta para o próximo.",
    "sources": ["l662", "l14759", "port26"],
    "body": NEXT_BOX + f"""
<h2>Feriados nacionais e pontos facultativos de 2026</h2>
{fer_table(2026)}
<h2>Feriadões de 2026</h2>
<p>Feriados que caem na segunda ou na sexta-feira garantem fins de semana de três dias; os que caem na terça ou na quinta podem virar feriadão de quatro dias quando a empresa ou o órgão público concede a “emenda”.</p>
{prolongados(2026)}
<div class="note">O Dia da Consciência Negra (20/11) cai em uma sexta-feira em 2026 e é feriado nacional desde 2024 (Lei 14.759/2023). Proclamação da República (15/11) cai em um domingo.</div>
<h2>Feriado nacional, estadual, municipal e ponto facultativo</h2>
<ul>
<li><strong>Feriado nacional:</strong> definido em lei federal; vale em todo o país (Lei 662/1949 e Lei 6.802/1980, entre outras).</li>
<li><strong>Feriado estadual:</strong> a data magna de cada estado, como 9 de julho em São Paulo, 2 de julho na Bahia, 20 de setembro no Rio Grande do Sul e 23 de abril (São Jorge) no Rio de Janeiro.</li>
<li><strong>Feriado municipal:</strong> até quatro por município, incluindo a Sexta-feira da Paixão e o dia do padroeiro (Lei 9.093/1995).</li>
<li><strong>Ponto facultativo:</strong> não é feriado. O governo federal libera seus servidores, mas empresas privadas decidem se haverá expediente — é o caso do Carnaval e de Corpus Christi, salvo lei local.</li>
</ul>
<h2>Trabalhar no feriado: o que diz a lei</h2>
<p>O trabalho em feriado sem folga compensatória deve ser pago em dobro (Lei 605/1949, art. 9º; Súmula 146 do TST). Calcule o valor na <a href="/hora-extra/">calculadora de hora extra</a> com adicional de 100%. Quem trabalha na <a href="/escala-12x36/">escala 12x36</a> tem os feriados considerados compensados (CLT, art. 59-A). Veja também o <a href="/calendario-2026/">calendário 2026</a> completo e os <a href="/feriados-2027/">feriados de 2027</a>.</p>
""",
    "faq": [
        ("Quantos feriados nacionais tem em 2026?", f"São 10 feriados nacionais em 2026; {weekday_holidays(2026)} deles caem de segunda a sexta-feira. Carnaval (16 e 17/2) e Corpus Christi (4/6) são pontos facultativos."),
        ("Carnaval 2026 é feriado?", "Não é feriado nacional. Segunda (16/2) e terça (17/2) de Carnaval são pontos facultativos; alguns estados e municípios, como o Rio de Janeiro, têm lei local que torna a data feriado."),
        ("Quando é a Sexta-feira Santa em 2026?", "Em 3 de abril de 2026. A Páscoa é em 5 de abril."),
        ("Quais são os feriadões de 2026?", "Fins de semana prolongados em 2/1 (emenda), 3/4 (Paixão), 21/4 (terça), 1/5 (sexta), 4/6 (Corpus Christi, quinta), 7/9 (segunda), 12/10 (segunda), 2/11 (segunda), 20/11 (sexta) e 25/12 (sexta)."),
        ("O dia 20 de novembro é feriado em 2026?", "Sim. O Dia Nacional de Zumbi e da Consciência Negra é feriado nacional desde 2024 e cai em uma sexta-feira em 2026."),
        ("Quem trabalha no feriado recebe em dobro?", "Sim, se não houver folga compensatória em outro dia da semana (Súmula 146 do TST). Convenções coletivas podem prever regras próprias."),
    ],
    "js": NEXT_JS,
}

# ============================================================ Feriados 2027
FER27 = {
    "path": "/feriados-2027/", "short": "Feriados 2027", "tool": True, "group": "cal",
    "card": "Previsão dos feriados nacionais de 2027 com dia da semana e feriadões.",
    "title": "Feriados 2027 – Datas dos Feriados Nacionais e Feriadões",
    "desc": "Feriados nacionais de 2027 com o dia da semana, pontos facultativos de Carnaval e Corpus Christi e os feriadões do ano. Páscoa em 28 de março de 2027.",
    "h1": "Feriados 2027: datas e feriadões",
    "lead": f"Os feriados nacionais são fixados por lei, por isso já é possível planejar 2027. A Páscoa cai em 28 de março, o que define a Sexta-feira Santa (26/3), o Carnaval (8 e 9/2) e Corpus Christi (27/5). Em 2027, {weekday_holidays(2027)} dos 10 feriados nacionais caem em dias úteis.",
    "sources": ["l662", "l14759"],
    "body": f"""
<div class="note">Previsão com base na legislação federal. A portaria anual do Ministério da Gestão e da Inovação com o calendário oficial de 2027 (incluindo pontos facultativos) costuma ser publicada no fim do ano anterior; esta página será atualizada quando sair.</div>
<h2>Feriados nacionais e pontos facultativos de 2027</h2>
{fer_table(2027)}
<h2>Feriadões de 2027</h2>
{prolongados(2027)}
<h2>Como as datas móveis são calculadas</h2>
<p>A Páscoa é o primeiro domingo após a primeira lua cheia depois do equinócio de março. A partir dela: Sexta-feira Santa é 2 dias antes, Carnaval 47 e 48 dias antes, e Corpus Christi 60 dias depois. Para 2027, Páscoa = 28/3, logo Sexta-feira Santa = 26/3, Carnaval = 8 e 9/2 e Corpus Christi = 27/5.</p>
<p>Para o ano corrente, veja os <a href="/feriados-2026/">feriados 2026</a> e o <a href="/calendario-2027/">calendário 2027</a> mês a mês. Para prazos, use a <a href="/dias-uteis/">calculadora de dias úteis</a> — ela já considera os feriados nacionais de qualquer ano.</p>
""",
    "faq": [
        ("Quando é o Carnaval de 2027?", "Segunda-feira, 8 de fevereiro, e terça-feira, 9 de fevereiro de 2027 (pontos facultativos). A Quarta-feira de Cinzas é 10/2."),
        ("Quando é a Páscoa de 2027?", "Domingo, 28 de março de 2027. A Sexta-feira Santa é 26 de março."),
        ("Quantos feriados nacionais caem em dia útil em 2027?", f"{weekday_holidays(2027)} dos 10 feriados nacionais caem de segunda a sexta-feira em 2027."),
        ("Quando é Corpus Christi em 2027?", "Quinta-feira, 27 de maio de 2027 (ponto facultativo nacional)."),
    ],
}

# ============================================================ Calendário 2026 / 2027
def _cal_page(y, path, other):
    return {
        "path": path, "short": f"Calendário {y}", "tool": True, "group": "cal",
        "card": f"Calendário {y} mês a mês com feriados nacionais e pontos facultativos.",
        "title": f"Calendário {y} com Feriados – Brasil (para Imprimir)",
        "desc": f"Calendário {y} completo, mês a mês, com os feriados nacionais e pontos facultativos destacados. Pronto para imprimir, com a lista de feriadões do ano.",
        "h1": f"Calendário {y} com feriados",
        "lead": f"Veja os 12 meses de {y} com os feriados nacionais em amarelo e os pontos facultativos em destaque claro. A página é otimizada para impressão: use Ctrl+P (ou Compartilhar → Imprimir no celular).",
        "sources": ["l662", "l14759"] + (["port26"] if y == 2026 else []),
        "body": f"""
<div class="actions" style="margin:0 0 16px"><button class="btn" type="button" onclick="window.print()">Imprimir calendário</button></div>
{cal_html(y)}
<h2>Feriadões de {y}</h2>
{prolongados(y)}
<h2>Datas úteis do calendário {y}</h2>
<ul>
<li>Lista completa com dia da semana: <a href="/feriados-{y}/">feriados {y}</a>.</li>
<li>Dias úteis de cada mês: <a href="/dias-uteis/">calculadora de dias úteis</a>.</li>
<li>Prazo de pagamento do salário: <a href="/quinto-dia-util/">quinto dia útil</a>.</li>
<li>Contagem regressiva para qualquer data: <a href="/quantos-dias-faltam/">quantos dias faltam</a>.</li>
<li>Outro ano: <a href="{other[0]}">{other[1]}</a>.</li>
</ul>
""",
        "faq": [
            (f"Quantos dias tem o ano de {y}?", f"{366 if y % 4 == 0 else 365} dias. {y} {'é' if y % 4 == 0 else 'não é'} ano bissexto."),
            (f"Em que dia da semana começa {y}?", f"{y} começa em uma {DIAS_SEMANA[dt.date(y,1,1).weekday()]} e termina em uma {DIAS_SEMANA[dt.date(y,12,31).weekday()]}."),
            (f"Quando é a Páscoa em {y}?", f"Em {easter(y).day} de {MESES[easter(y).month-1]} de {y}."),
        ],
    }


CAL26 = _cal_page(2026, "/calendario-2026/", ("/calendario-2027/", "calendário 2027"))
CAL27 = _cal_page(2027, "/calendario-2027/", ("/calendario-2026/", "calendário 2026"))

# ============================================================ Escalas (shared generator)
ESC_UI = """
<div class="calc">
<h2>Gerador de escala {nome}</h2>
<div class="grid"><div><label for="esc">Escala</label><select id="esc">{opts}</select></div><div><label for="ini">Primeiro dia de trabalho</label><input type="date" id="ini"></div><div><label for="mes">Mês para visualizar</label><input type="month" id="mes" style="width:100%;font:inherit;font-size:1.05rem;padding:10px 12px;border:1px solid #B7C1D1;border-radius:8px;min-height:46px"></div><div><label for="hd">Horas por plantão/dia</label><input type="number" id="hd" value="{hd}" step="any" min="0" inputmode="decimal"></div></div>
<div class="result" id="res" aria-live="polite"><div class="big" id="nt">–</div><div class="sub" id="ntd"></div>
<dl><dt>Horas no mês</dt><dd id="nh">–</dd><dt>Folgas no mês</dt><dd id="nf">–</dd><dt>Domingos trabalhados</dt><dd id="nd">–</dd><dt>Feriados nacionais trabalhados</dt><dd id="nfe">–</dd></dl>
<div class="actions"><button class="btn sm ghost" type="button" onclick="copyRes('res',this)">Copiar resultado</button></div></div>
<div id="cal" style="margin-top:16px"></div>
<p class="hint">Dias em azul = trabalho; contorno amarelo = feriado nacional. Escalas com folga fixa seguem o calendário; as demais repetem o ciclo a partir do primeiro dia informado.</p>
</div>"""

ESC_OPTS = [("12x36", "12x36 – 12h de trabalho, 36h de descanso"), ("24x48", "24x48 – plantão de 24h, 48h de descanso"),
            ("6x1r", "6x1 – folga em rodízio (a cada 7 dias)"), ("6x1d", "6x1 – folga fixa no domingo"),
            ("5x2", "5x2 – segunda a sexta"), ("4x2", "4x2 – 4 dias de trabalho, 2 de folga"), ("4x3", "4x3 – 4 dias de trabalho, 3 de folga")]


def esc_ui(nome, sel, hd):
    opts = "".join(f'<option value="{v}"{" selected" if v == sel else ""}>{t}</option>' for v, t in ESC_OPTS)
    return ESC_UI.format(nome=nome, opts=opts, hd=hd)


ESC_JS = r"""
(function(){var P={'12x36':[1,0],'24x48':[1,0,0],'6x1r':[1,1,1,1,1,1,0],'4x2':[1,1,1,1,0,0],'4x3':[1,1,1,1,0,0,0]};
var t=new Date();document.getElementById('ini').value=isoD(t);document.getElementById('mes').value=t.getFullYear()+'-'+pad(t.getMonth()+1);
function c(){var e=document.getElementById('esc').value,iv=document.getElementById('ini').value,mv=document.getElementById('mes').value;if(!iv||!mv)return;
var I=new Date(iv+'T12:00:00'),p=mv.split('-'),y=+p[0],m=+p[1]-1,F=feriados(y),d=new Date(y,m,1,12),hd=val('hd'),nt=0,nd=0,nfe=0,tot=0;
var h='<div class="cal" style="grid-template-columns:minmax(0,420px)"><div class="mon"><h3>'+d.toLocaleDateString('pt-BR',{month:'long',year:'numeric'})+'</h3><table><thead><tr><th>D</th><th>S</th><th>T</th><th>Q</th><th>Q</th><th>S</th><th>S</th></tr></thead><tbody><tr>';
for(var i=0;i<d.getDay();i++)h+='<td></td>';
while(d.getMonth()===m){var dw=d.getDay(),w;if(e==='5x2')w=dw>0&&dw<6;else if(e==='6x1d')w=dw>0;else{var pat=P[e],k=Math.round((d-I)/864e5);w=pat[((k%pat.length)+pat.length)%pat.length]===1}
var key=isoD(d),fe=!!F[key];tot++;if(w){nt++;if(dw===0)nd++;if(fe)nfe++}
var cls=(w?'w':'')+(fe?' hol':'')+(dw===0?' dom':'');h+='<td class="'+cls+'" title="'+(fe?F[key]:'')+'">'+d.getDate()+'</td>';if(dw===6)h+='</tr><tr>';d.setDate(d.getDate()+1)}
h+='</tr></tbody></table></div></div>';document.getElementById('cal').innerHTML=h;
document.getElementById('nt').textContent=nt+(nt===1?' dia':' dias')+' de trabalho';document.getElementById('ntd').textContent='na escala '+document.getElementById('esc').selectedOptions[0].text.split(' –')[0];
document.getElementById('nh').textContent=fmtH(nt*hd*60)+' ('+num(nt*hd,2)+' h)';document.getElementById('nf').textContent=(tot-nt);document.getElementById('nd').textContent=nd;document.getElementById('nfe').textContent=nfe}
['esc','ini','mes','hd'].forEach(function(i){document.getElementById(i).addEventListener('input',c)});c()})();"""

E1236 = {
    "path": "/escala-12x36/", "short": "Escala 12x36", "tool": True, "group": "jor",
    "card": "Gerador de escala 12x36 com dias de plantão, horas do mês e regras da CLT.",
    "title": "Escala 12x36: Como Funciona, Horas no Mês e Gerador de Escala",
    "desc": "Entenda a escala 12x36 (CLT, art. 59-A): quantas horas por mês, feriados, adicional noturno e intervalo. Gere a escala do mês com os dias de plantão e o total de horas.",
    "h1": "Escala 12x36: como funciona e gerador de escala",
    "lead": "Na escala 12x36 o profissional trabalha 12 horas seguidas e descansa as 36 horas seguintes. Informe o primeiro plantão e veja o calendário do mês, quantos plantões e quantas horas você vai cumprir.",
    "sources": ["clt", "cf", "tst"],
    "body": esc_ui("12x36", "12x36", 12) + """
<h2>Quantas horas por mês na escala 12x36?</h2>
<p>Como os plantões se alternam dia sim, dia não, o mês tem <strong>15 ou 16 plantões</strong> (14 em fevereiro). Isso dá entre 168 e 192 horas por mês e uma média de <strong>42 horas por semana</strong> — abaixo do limite constitucional de 44 horas semanais.</p>
<div class="formula">Média semanal = 12 h × 3,5 plantões por semana = 42 h &nbsp;·&nbsp; Média mensal ≈ 12 h × 15,2 = 182,5 h</div>
<h2>Regras da escala 12x36 na CLT</h2>
<ul>
<li><strong>Forma de contratação:</strong> desde a Reforma Trabalhista, a escala 12x36 pode ser ajustada por acordo individual escrito, convenção ou acordo coletivo (CLT, art. 59-A). O STF confirmou a validade da regra em 2023 (ADI 5994).</li>
<li><strong>Intervalo:</strong> o intervalo para refeição pode ser usufruído ou indenizado (art. 59-A, caput).</li>
<li><strong>Feriados e DSR:</strong> a remuneração mensal já abrange o descanso semanal e os feriados, que são considerados compensados (art. 59-A, parágrafo único). Convenções coletivas podem prever pagamento em dobro.</li>
<li><strong>Plantão noturno:</strong> as horas entre 22h e 5h têm adicional noturno de 20% e hora reduzida. A prorrogação após as 5h é considerada compensada na 12x36. Calcule em <a href="/adicional-noturno/">adicional noturno</a>.</li>
<li><strong>Hora extra:</strong> trabalhar além das 12 horas do plantão gera hora extra com adicional mínimo de 50% — veja a <a href="/hora-extra/">calculadora de hora extra</a>.</li>
</ul>
<h2>12x36, 24x48 e outras escalas</h2>
<p>A 24x48 (24 horas de trabalho e 48 de descanso) também resulta em média de 56 horas a cada 3 dias e é comum em portarias e brigadas; depende de norma coletiva. Para jornadas semanais, compare com a <a href="/escala-6x1/">escala 6x1</a> e a <a href="/escala-5x2/">escala 5x2</a>. Use o seletor do gerador para visualizar qualquer uma delas.</p>
""",
    "faq": [
        ("Quantos dias trabalha quem faz 12x36?", "15 ou 16 dias por mês (14 em fevereiro), já que os plantões são em dias alternados."),
        ("Quantas horas tem a escala 12x36 por mês?", "Em média 180 a 192 horas, dependendo de quantos plantões caem no mês. A média semanal é de 42 horas."),
        ("Quem trabalha 12x36 recebe feriado em dobro?", "Pela CLT (art. 59-A), não: os feriados são considerados compensados. Convenções coletivas podem garantir o pagamento em dobro."),
        ("A escala 12x36 precisa de acordo coletivo?", "Não necessariamente. Desde 2017 basta acordo individual escrito, convenção ou acordo coletivo (CLT, art. 59-A). Para atividades insalubres, verifique a exigência de licença prévia e a norma coletiva da categoria."),
        ("Tem intervalo na escala 12x36?", "Sim, o intervalo para repouso e alimentação deve ser concedido ou, se não for, indenizado."),
    ],
    "js": ESC_JS,
}

E61 = {
    "path": "/escala-6x1/", "short": "Escala 6x1", "tool": True, "group": "jor",
    "card": "Como funciona a escala 6x1, jornada diária e situação da PEC que acaba com ela.",
    "title": "Escala 6x1: Como Funciona, Jornada e Situação da PEC (2026)",
    "desc": "Escala 6x1 explicada: 6 dias de trabalho e 1 de folga, jornada de 7h20 por dia, regra da folga no domingo e situação da PEC do fim da escala 6x1 no Senado. Gere sua escala do mês.",
    "h1": "Escala 6x1: como funciona e o que muda com a PEC",
    "lead": "Na escala 6x1 o empregado trabalha seis dias e folga um. É a escala mais comum no comércio, em serviços e na indústria. Veja a jornada diária, as regras da folga no domingo, a situação da proposta que pode acabar com ela e gere sua escala do mês.",
    "sources": ["cf", "clt", "l605", "l10101", "senado6x1"],
    "body": esc_ui("6x1", "6x1r", 7.3333) + """
<h2>Jornada na escala 6x1</h2>
<p>Com o limite de 44 horas semanais (Constituição, art. 7º, XIII), a divisão mais comum é de <strong>7 horas e 20 minutos por dia</strong> em seis dias. Outra combinação usual é 8 horas de segunda a sexta e 4 horas no sábado. No gerador acima, 7,3333 horas correspondem a 7h20.</p>
<div class="formula">44 h ÷ 6 dias = 7 h 20 min por dia &nbsp;·&nbsp; 8 h × 5 dias + 4 h = 44 h</div>
<h2>Folga no domingo</h2>
<ul>
<li>O repouso semanal remunerado de 24 horas deve ser <strong>preferencialmente aos domingos</strong> (Constituição, art. 7º, XV; Lei 605/1949; CLT, art. 67).</li>
<li>No <strong>comércio</strong>, a folga deve coincidir com o domingo pelo menos uma vez a cada três semanas (Lei 10.101/2000, art. 6º, parágrafo único).</li>
<li>Para <strong>mulheres</strong> em escala de revezamento, a CLT prevê folga dominical a cada 15 dias (art. 386).</li>
<li>Domingo ou feriado trabalhado sem folga compensatória é pago em dobro (Súmula 146 do TST).</li>
</ul>
<h2>PEC do fim da escala 6x1: situação em outubro de 2026</h2>
<p>A proposta de emenda à Constituição que reduz a jornada máxima de 44 para <strong>40 horas semanais</strong>, com <strong>dois dias de descanso</strong> e sem redução de salário, foi aprovada pela Câmara dos Deputados e está em discussão no plenário do Senado. Em 8 de outubro de 2026 o Senado realizou a terceira das cinco sessões de discussão exigidas antes da votação em primeiro turno; a aprovação depende de 49 dos 81 senadores, em dois turnos. Ainda não há data definida para a votação final.</p>
<div class="note"><strong>Enquanto a PEC não for promulgada, nada muda:</strong> continuam valendo a jornada de até 44 horas semanais e a escala 6x1 nos termos da CLT. Esta página será atualizada quando houver votação.</div>
<p>Se a jornada cair para 40 horas, o divisor do salário-hora passa de 220 para 200, o que aumenta o valor da hora e da hora extra. Simule hoje na <a href="/hora-extra/">calculadora de hora extra</a> escolhendo “40 horas”. Compare com a <a href="/escala-5x2/">escala 5x2</a> e a <a href="/escala-12x36/">escala 12x36</a>.</p>
""",
    "faq": [
        ("O que é a escala 6x1?", "É a escala em que o empregado trabalha seis dias consecutivos e folga um, respeitando o limite de 44 horas semanais."),
        ("Quantas horas por dia na escala 6x1?", "Normalmente 7 horas e 20 minutos (44 h ÷ 6). Também é comum 8 horas de segunda a sexta e 4 horas no sábado."),
        ("A escala 6x1 vai acabar?", "Há uma PEC que reduz a jornada para 40 horas semanais com duas folgas. Ela foi aprovada pela Câmara e está em discussão no Senado (outubro de 2026). Até ser aprovada em dois turnos e promulgada, a escala 6x1 continua permitida."),
        ("Quem trabalha 6x1 tem direito a folgar no domingo?", "O descanso deve ser preferencialmente no domingo. No comércio, a folga precisa cair no domingo pelo menos uma vez a cada três semanas."),
        ("Feriado trabalhado na escala 6x1 é pago em dobro?", "Sim, se não houver folga compensatória (Súmula 146 do TST)."),
    ],
    "js": ESC_JS,
}

E52 = {
    "path": "/escala-5x2/", "short": "Escala 5x2", "tool": True, "group": "jor",
    "card": "Escala 5x2: jornada de 8h ou 8h48, compensação do sábado e gerador mensal.",
    "title": "Escala 5x2: Como Funciona, Jornada de 8h48 e Compensação do Sábado",
    "desc": "Escala 5x2 explicada: cinco dias de trabalho e dois de folga, jornada de 8 horas ou 8h48 com compensação do sábado, regras da CLT e gerador de escala do mês.",
    "h1": "Escala 5x2: jornada, compensação do sábado e gerador",
    "lead": "Na escala 5x2 o empregado trabalha cinco dias e folga dois — normalmente sábado e domingo. Veja como fica a jornada diária com 40 ou 44 horas semanais e gere o calendário do mês.",
    "sources": ["cf", "clt"],
    "body": esc_ui("5x2", "5x2", 8.8) + """
<h2>Jornada na escala 5x2</h2>
<ul>
<li><strong>40 horas semanais:</strong> 8 horas por dia, de segunda a sexta. Divisor do salário-hora: 200.</li>
<li><strong>44 horas semanais:</strong> as 4 horas do sábado são distribuídas nos outros dias, resultando em <strong>8 horas e 48 minutos</strong> por dia. Divisor: 220. No gerador, 8,8 horas = 8h48.</li>
</ul>
<div class="formula">44 h ÷ 5 dias = 8 h 48 min por dia (compensação do sábado)</div>
<h2>Compensação de jornada</h2>
<p>A jornada acima de 8 horas diárias para compensar o sábado é permitida por acordo de compensação (Constituição, art. 7º, XIII; CLT, art. 59, §§ 2º e 6º). A compensação dentro do mesmo mês pode ser feita por acordo individual, inclusive tácito; períodos maiores exigem acordo escrito ou norma coletiva — veja as regras no <a href="/banco-de-horas/">banco de horas</a>. As 2 horas extras diárias continuam sendo o limite (art. 59).</p>
<h2>5x2 x 6x1</h2>
<p>A escala 5x2 é a mais comum em escritórios e na administração pública. A <a href="/escala-6x1/">escala 6x1</a>, típica do comércio, é alvo de uma PEC em tramitação no Senado que prevê 40 horas semanais com dois dias de descanso — na prática, uma jornada no formato 5x2. Para turnos longos, compare com a <a href="/escala-12x36/">escala 12x36</a>.</p>
""",
    "faq": [
        ("O que é escala 5x2?", "É a escala com cinco dias de trabalho e dois de descanso por semana, geralmente de segunda a sexta com folga no sábado e no domingo."),
        ("Quantas horas por dia na escala 5x2?", "8 horas para quem tem jornada de 40 horas semanais, ou 8 horas e 48 minutos para quem tem 44 horas e compensa o sábado."),
        ("Jornada de 8h48 é legal?", "Sim, desde que haja acordo de compensação de jornada. As horas além de 8 por dia servem para compensar o sábado não trabalhado."),
        ("Na escala 5x2, quantos dias úteis tem o mês?", "Entre 19 e 23, dependendo do mês e dos feriados. Veja a tabela na calculadora de dias úteis."),
    ],
    "js": ESC_JS,
}

# ============================================================ Calculadora de férias
FERIAS = {
    "path": "/calculadora-de-ferias/", "short": "Calculadora de férias", "tool": True, "group": "sal",
    "card": "Férias com 1/3 constitucional, abono pecuniário, INSS e IRRF 2026 — valor líquido.",
    "title": "Calculadora de Férias 2026 – Valor Líquido com 1/3, INSS e IR",
    "desc": "Calcule suas férias 2026: salário, médias de horas extras, 1/3 constitucional, venda de 10 dias (abono pecuniário), desconto de INSS e IRRF com a nova isenção até R$ 5 mil. Grátis.",
    "h1": "Calculadora de férias 2026",
    "lead": "Informe o salário bruto, a média de variáveis (horas extras, adicional noturno, comissões) e quantos dias vai tirar. A calculadora soma o terço constitucional, o abono pecuniário se você vender 10 dias e desconta INSS e Imposto de Renda pelas tabelas de 2026.",
    "sources": ["cf", "clt", "inss26", "irrf26"],
    "body": """
<div class="calc">
<h2>Calcular férias</h2>
<div class="grid"><div><label for="sal">Salário bruto mensal (R$)</label><input type="number" id="sal" value="3000" step="50" min="0" inputmode="decimal"></div><div><label for="med">Média de variáveis (R$)</label><input type="number" id="med" value="0" step="10" min="0" inputmode="decimal"></div><div><label for="dias">Dias de direito</label><select id="dias"><option value="30" selected>30 dias (até 5 faltas)</option><option value="24">24 dias (6 a 14 faltas)</option><option value="18">18 dias (15 a 23 faltas)</option><option value="12">12 dias (24 a 32 faltas)</option></select></div><div><label for="dep">Dependentes (IR)</label><input type="number" id="dep" value="0" min="0" inputmode="numeric"></div></div>
<div class="actions"><label class="chk"><input type="checkbox" id="ab"> Vender 1/3 das férias (abono pecuniário)</label></div>
<div class="result" id="res" aria-live="polite"><div class="big" id="liq">R$ 0,00</div><div class="sub">valor líquido das férias</div>
<dl><dt>Dias de descanso</dt><dd id="dg">–</dd><dt>Férias</dt><dd id="vf">–</dd><dt>1/3 constitucional</dt><dd id="vt">–</dd><dt>Abono pecuniário + 1/3</dt><dd id="va">–</dd><dt>Total bruto</dt><dd id="vb">–</dd><dt>INSS</dt><dd id="vi">–</dd><dt>IRRF</dt><dd id="vr">–</dd></dl>
<div class="actions"><button class="btn sm ghost" type="button" onclick="copyRes('res',this)">Copiar resultado</button></div></div>
<p class="hint">INSS progressivo 2026 (teto R$ 8.475,55) e IRRF 2026 com o redutor da Lei 15.270/2025 (isenção para rendimentos até R$ 5.000). Abono pecuniário e seu terço não sofrem INSS nem IR. Pensão alimentícia e outros descontos não estão incluídos.</p>
</div>
<h2>Como calcular as férias</h2>
<div class="formula">Férias = (salário + médias) ÷ 30 × dias de descanso &nbsp;·&nbsp; Terço = férias ÷ 3 &nbsp;·&nbsp; Abono = (salário + médias) ÷ 30 × dias vendidos + 1/3</div>
<p>Exemplo: salário de R$ 3.000, 30 dias de férias, sem vender. Férias = R$ 3.000; terço = R$ 1.000; bruto = R$ 4.000. INSS 2026 sobre R$ 4.000 = R$ 368,60. Como o rendimento tributável fica abaixo de R$ 5.000, o IRRF é zero em 2026. Líquido = <strong>R$ 3.631,40</strong>.</p>
<h2>Regras das férias na CLT</h2>
<ul>
<li><strong>Direito:</strong> 30 dias corridos a cada 12 meses de trabalho (período aquisitivo), reduzidos conforme as faltas injustificadas (CLT, art. 130).</li>
<li><strong>Terço constitucional:</strong> as férias são pagas com acréscimo de 1/3 (Constituição, art. 7º, XVII).</li>
<li><strong>Abono pecuniário:</strong> o empregado pode vender até 1/3 das férias, desde que peça até 15 dias antes do fim do período aquisitivo (art. 143).</li>
<li><strong>Fracionamento:</strong> com concordância do empregado, em até três períodos — um com pelo menos 14 dias e os demais com no mínimo 5 dias (art. 134, §1º).</li>
<li><strong>Pagamento:</strong> até 2 dias antes do início das férias (art. 145).</li>
<li><strong>Início:</strong> não pode começar nos dois dias que antecedem feriado ou o descanso semanal (art. 134, §3º).</li>
<li><strong>Médias:</strong> horas extras, adicional noturno e comissões habituais integram a base — some-as no campo “média de variáveis”. Para chegar à média, use a <a href="/hora-extra/">calculadora de hora extra</a> e o <a href="/adicional-noturno/">adicional noturno</a>.</li>
</ul>
<p>Para marcar a data de volta, some os dias na <a href="/calculadora-de-datas/">calculadora de datas</a>.</p>
""",
    "faq": [
        ("Como calcular o valor das férias?", "Divida o salário (mais a média de variáveis) por 30, multiplique pelos dias de férias e some 1/3 desse valor. Depois desconte INSS e Imposto de Renda."),
        ("Quanto recebe de férias quem ganha um salário mínimo em 2026?", "Com R$ 1.621: férias R$ 1.621 + terço R$ 540,33 = R$ 2.161,33 brutos. INSS R$ 170,20 e IR zero, líquido R$ 1.991,13."),
        ("Vale a pena vender 10 dias de férias?", "O abono pecuniário (10 dias + 1/3) é isento de INSS e de Imposto de Renda, por isso aumenta o valor líquido recebido; em troca, você descansa só 20 dias."),
        ("Férias têm desconto de Imposto de Renda em 2026?", "Sim, mas desde janeiro de 2026 quem tem rendimento tributável de até R$ 5.000 no mês fica isento pelo redutor da Lei 15.270/2025, e há redução parcial até R$ 7.350."),
        ("Quantos dias de férias perco com faltas?", "Até 5 faltas injustificadas: 30 dias. De 6 a 14: 24 dias. De 15 a 23: 18 dias. De 24 a 32: 12 dias. Acima de 32 faltas, o direito é perdido (CLT, art. 130)."),
        ("Quando a empresa deve pagar as férias?", "Até 2 dias antes do início do descanso (CLT, art. 145)."),
    ],
    "js": r"""
function inss26(b){var F=[[1621,.075],[2902.84,.09],[4354.27,.12],[8475.55,.14]],r=0,p=0;for(var i=0;i<F.length;i++){if(b>p){r+=(Math.min(b,F[i][0])-p)*F[i][1]}p=F[i][0]}return Math.round(r*100)/100}
function irrf26(rend,inss,dep){function tab(x){if(x<=2428.80)return 0;if(x<=2826.65)return x*.075-182.16;if(x<=3751.05)return x*.15-394.16;if(x<=4664.68)return x*.225-675.49;return x*.275-908.73}
var leg=tab(rend-inss-dep*189.59),simp=tab(rend-607.20),ir=Math.max(0,Math.min(leg,simp));if(rend<=5000)ir=0;else if(rend<=7350)ir=Math.max(0,ir-(978.62-.133145*rend));return Math.round(ir*100)/100}
(function(){function c(){var b=val('sal')+val('med'),d=parseInt(document.getElementById('dias').value),ab=document.getElementById('ab').checked,dv=ab?Math.floor(d/3):0,dg=d-dv;
var vf=b/30*dg,vt=vf/3,va=b/30*dv*4/3,bru=vf+vt+va,i=inss26(vf+vt),r=irrf26(vf+vt,i,val('dep'));
document.getElementById('dg').textContent=dg+' dias'+(dv?' + '+dv+' vendidos':'');document.getElementById('vf').textContent=brl(vf);document.getElementById('vt').textContent=brl(vt);document.getElementById('va').textContent=brl(va);
document.getElementById('vb').textContent=brl(bru);document.getElementById('vi').textContent='− '+brl(i);document.getElementById('vr').textContent='− '+brl(r);document.getElementById('liq').textContent=brl(bru-i-r)}
['sal','med','dias','dep','ab'].forEach(function(x){document.getElementById(x).addEventListener('input',c)});c()})();""",
}

# ============================================================ Calculadora de idade
IDADE = {
    "path": "/calculadora-de-idade/", "short": "Calculadora de idade", "tool": True, "group": "cal",
    "card": "Idade exata em anos, meses e dias, dias vividos e quanto falta para o aniversário.",
    "title": "Calculadora de Idade – Idade Exata em Anos, Meses e Dias",
    "desc": "Calcule a idade exata a partir da data de nascimento: anos, meses e dias, total de dias e semanas vividos, dia da semana em que nasceu e quantos dias faltam para o próximo aniversário.",
    "h1": "Calculadora de idade",
    "lead": "Informe a data de nascimento para saber a idade exata em anos, meses e dias, quantos dias você já viveu e quanto falta para o próximo aniversário. Também serve para calcular a idade em uma data específica.",
    "sources": [],
    "body": """
<div class="calc">
<h2>Calcular idade</h2>
<div class="grid"><div><label for="nas">Data de nascimento</label><input type="date" id="nas" value="1990-05-15"></div><div><label for="ref">Idade na data</label><input type="date" id="ref"></div></div>
<div class="result" id="res" aria-live="polite"><div class="big" id="ida">–</div><div class="sub" id="idd"></div>
<dl><dt>Total de meses</dt><dd id="tm">–</dd><dt>Total de semanas</dt><dd id="ts">–</dd><dt>Total de dias</dt><dd id="td">–</dd><dt>Nasceu em uma</dt><dd id="wd">–</dd><dt>Próximo aniversário</dt><dd id="pa">–</dd></dl>
<div class="actions"><button class="btn sm ghost" type="button" onclick="copyRes('res',this)">Copiar resultado</button></div></div>
</div>
<h2>Como calcular a idade</h2>
<p>Subtraia o ano de nascimento do ano atual. Se o aniversário deste ano ainda não chegou, diminua 1. Para os meses e dias, avance mês a mês a partir do último aniversário. Exemplo: quem nasceu em 15/05/1990 tem, em 10/10/2026, <strong>36 anos, 4 meses e 25 dias</strong>.</p>
<h2>Idades que importam na lei</h2>
<ul>
<li><strong>16 anos:</strong> idade mínima para trabalhar, salvo como aprendiz a partir dos 14 (Constituição, art. 7º, XXXIII).</li>
<li><strong>18 anos:</strong> maioridade civil e permissão para trabalho noturno, perigoso ou insalubre.</li>
<li><strong>Aposentadoria por idade (INSS):</strong> 65 anos para homens e 62 para mulheres, com tempo mínimo de contribuição, conforme a Emenda Constitucional 103/2019.</li>
<li><strong>60 anos:</strong> pessoa idosa segundo o Estatuto da Pessoa Idosa (Lei 10.741/2003).</li>
</ul>
<p>Para contar o tempo entre outras datas — como tempo de serviço — use a <a href="/calculadora-de-datas/">calculadora de datas</a>. Para uma contagem regressiva, veja <a href="/quantos-dias-faltam/">quantos dias faltam</a>.</p>
""",
    "faq": [
        ("Como calcular minha idade exata?", "Informe sua data de nascimento na calculadora. Ela mostra a idade em anos, meses e dias, além do total de dias e semanas vividos."),
        ("Como calcular a idade em uma data específica?", "Preencha o campo “Idade na data” com a data desejada — por exemplo, a data de um concurso ou da aposentadoria."),
        ("Quantos dias eu já vivi?", "A calculadora mostra o total de dias corridos entre o nascimento e a data de referência."),
        ("Quem nasceu em 29 de fevereiro faz aniversário quando?", "Nos anos não bissextos, a calculadora considera o aniversário em 1º de março para a contagem de dias até o próximo aniversário."),
    ],
    "js": r"""
(function(){document.getElementById('ref').value=isoD(new Date());
function c(){var a=document.getElementById('nas').value,b=document.getElementById('ref').value;if(!a||!b)return;var A=new Date(a+'T12:00:00'),B=new Date(b+'T12:00:00');if(B<A){document.getElementById('ida').textContent='Data inválida';return}
var y=B.getFullYear()-A.getFullYear(),m=B.getMonth()-A.getMonth(),d=B.getDate()-A.getDate();if(d<0){m--;d+=new Date(B.getFullYear(),B.getMonth(),0).getDate()}if(m<0){y--;m+=12}
var tot=Math.round((B-A)/864e5);var N=new Date(B.getFullYear(),A.getMonth(),A.getDate(),12);if(N<=B)N=new Date(B.getFullYear()+1,A.getMonth(),A.getDate(),12);var fal=Math.round((N-B)/864e5);
document.getElementById('ida').textContent=y+(y===1?' ano':' anos');document.getElementById('idd').textContent=m+' mês(es) e '+d+' dia(s)';document.getElementById('tm').textContent=(y*12+m).toLocaleString('pt-BR');
document.getElementById('ts').textContent=Math.floor(tot/7).toLocaleString('pt-BR');document.getElementById('td').textContent=tot.toLocaleString('pt-BR');document.getElementById('wd').textContent=A.toLocaleDateString('pt-BR',{weekday:'long'});
document.getElementById('pa').textContent=N.toLocaleDateString('pt-BR')+' – faltam '+fal+' dia(s), fará '+(N.getFullYear()-A.getFullYear())+' anos'}
['nas','ref'].forEach(function(i){document.getElementById(i).addEventListener('input',c)});c()})();""",
}

# ============================================================ Intervalo intrajornada
INTERV = {
    "path": "/intervalo-intrajornada/", "short": "Intervalo intrajornada", "tool": True, "group": "jor",
    "card": "Intervalo mínimo de almoço pela jornada, indenização do intervalo suprimido e interjornada de 11h.",
    "title": "Intervalo Intrajornada – Regras da CLT e Cálculo do Intervalo Suprimido",
    "desc": "Intervalo intrajornada (CLT, art. 71): 1 a 2 horas para jornadas acima de 6h, 15 minutos de 4h a 6h. Calcule o intervalo mínimo, a indenização do intervalo não concedido e o descanso interjornada de 11h.",
    "h1": "Intervalo intrajornada: regras e cálculo",
    "lead": "Informe o horário de entrada e saída e quanto tempo de intervalo foi concedido. A calculadora mostra o intervalo mínimo exigido pela CLT e, se ele foi suprimido, o valor da indenização com adicional de 50%.",
    "sources": ["clt", "tst"],
    "body": """
<div class="calc">
<h2>Calcular intervalo intrajornada</h2>
<div class="grid"><div><label for="ent">Entrada</label><input type="time" id="ent" value="08:00"></div><div><label for="sai">Saída</label><input type="time" id="sai" value="17:30"></div><div><label for="int">Intervalo concedido (min)</label><input type="number" id="int" value="30" min="0" step="5" inputmode="numeric"></div></div>
<div class="grid" style="margin-top:12px"><div><label for="sal">Salário bruto (R$)</label><input type="number" id="sal" value="2500" step="50" min="0" inputmode="decimal"></div><div><label for="jor">Jornada semanal</label><select id="jor"><option value="44">44h (divisor 220)</option><option value="40">40h (divisor 200)</option><option value="36">36h (divisor 180)</option></select></div><div><label for="dias">Dias no mês com intervalo reduzido</label><input type="number" id="dias" value="22" min="0"></div></div>
<div class="result" id="res" aria-live="polite"><div class="big" id="tot">–</div><div class="sub" id="totd"></div>
<dl><dt>Jornada efetiva</dt><dd id="je">–</dd><dt>Intervalo mínimo pela CLT</dt><dd id="im">–</dd><dt>Intervalo suprimido por dia</dt><dd id="is">–</dd><dt>Indenização por dia</dt><dd id="ind">–</dd></dl>
<div class="actions"><button class="btn sm ghost" type="button" onclick="copyRes('res',this)">Copiar resultado</button></div></div>
<p class="hint">Desde a Reforma Trabalhista (2017), só o período suprimido é indenizado, com acréscimo de 50% sobre o valor da hora normal, e a verba tem natureza indenizatória (CLT, art. 71, §4º).</p>
</div>
<h2>Intervalo mínimo pela duração da jornada</h2>
<div class="tw"><table class="t"><thead><tr><th>Jornada</th><th>Intervalo</th><th>Base legal</th></tr></thead><tbody>
<tr><td>Até 4 horas</td><td>Não obrigatório</td><td>CLT, art. 71</td></tr>
<tr><td>Mais de 4 até 6 horas</td><td>15 minutos</td><td>CLT, art. 71, §1º</td></tr>
<tr><td>Mais de 6 horas</td><td>Mínimo 1 hora, máximo 2 horas</td><td>CLT, art. 71, caput</td></tr>
<tr><td>Mais de 6 horas, com norma coletiva</td><td>Mínimo 30 minutos</td><td>CLT, art. 611-A, III</td></tr>
</tbody></table></div>
<p>O intervalo <strong>não conta</strong> como tempo de trabalho (art. 71, §2º). Para somar as horas efetivamente trabalhadas no dia, use a <a href="/horas-trabalhadas/">calculadora de horas trabalhadas</a>.</p>
<h2>Intervalo interjornada: 11 horas entre jornadas</h2>
<div class="calc">
<div class="grid"><div><label for="f1">Saída no dia anterior</label><input type="time" id="f1" value="22:00"></div><div><label for="i2">Entrada no dia seguinte</label><input type="time" id="i2" value="07:00"></div></div>
<div class="result" aria-live="polite"><div class="big" id="ij">–</div><div class="sub" id="ijd"></div></div>
</div>
<p>Entre duas jornadas deve haver no mínimo <strong>11 horas consecutivas</strong> de descanso (CLT, art. 66). As horas que faltarem são pagas como horas extras, com adicional de 50% (OJ 355 da SDI-1 do TST). Calcule o valor na <a href="/hora-extra/">calculadora de hora extra</a>.</p>
""",
    "faq": [
        ("Qual o intervalo para jornada de 8 horas?", "No mínimo 1 hora e no máximo 2 horas (CLT, art. 71). Convenção ou acordo coletivo pode reduzir para 30 minutos."),
        ("Qual o intervalo para jornada de 6 horas?", "15 minutos, para jornadas acima de 4 e até 6 horas. Se a jornada passar habitualmente de 6 horas, o intervalo passa a ser de 1 hora."),
        ("Como é paga a supressão do intervalo?", "Apenas o tempo suprimido é pago, com acréscimo de 50% sobre a hora normal, como indenização (CLT, art. 71, §4º, após a Reforma Trabalhista)."),
        ("O intervalo de almoço conta como hora trabalhada?", "Não. O intervalo para repouso e alimentação não é computado na jornada."),
        ("Quantas horas de descanso entre uma jornada e outra?", "No mínimo 11 horas consecutivas (CLT, art. 66)."),
    ],
    "js": r"""
(function(){function c(){var a=tmin(document.getElementById('ent').value),b=tmin(document.getElementById('sai').value);if(a===null||b===null)return;var dur=b>a?b-a:b+1440-a,iv=val('int'),ef=Math.max(0,dur-iv);
var min=ef>360?60:(ef>240?15:0);var sup=Math.max(0,min-iv),dv=parseFloat(document.getElementById('jor').value)*5,vh=val('sal')/dv,ind=vh*1.5*sup/60,d=val('dias');
document.getElementById('je').textContent=fmtH(ef);document.getElementById('im').textContent=min===60?'1 hora (máximo 2 horas)':(min===15?'15 minutos':'não obrigatório');
document.getElementById('is').textContent=sup?sup+' min':'nenhum';document.getElementById('ind').textContent=brl(ind);
document.getElementById('tot').textContent=sup?brl(ind*d):'Intervalo regular';document.getElementById('totd').textContent=sup?'indenização em '+d+' dia(s), com adicional de 50%':(iv>120&&ef>360?'atenção: intervalo acima de 2h exige acordo escrito ou norma coletiva':'o intervalo concedido atende ao mínimo da CLT')}
function c2(){var a=tmin(document.getElementById('f1').value),b=tmin(document.getElementById('i2').value);if(a===null||b===null)return;var r=b>a?b-a:b+1440-a,f=Math.max(0,660-r);
document.getElementById('ij').textContent=fmtH(r)+' de descanso';document.getElementById('ijd').textContent=f?'faltam '+fmtH(f)+' para as 11h — pagas como hora extra':'descanso de 11 horas respeitado'}
['ent','sai','int','sal','jor','dias'].forEach(function(i){document.getElementById(i).addEventListener('input',c)});['f1','i2'].forEach(function(i){document.getElementById(i).addEventListener('input',c2)});c();c2()})();""",
}

# ============================================================ Quinto dia útil
QUINTO = {
    "path": "/quinto-dia-util/", "short": "Quinto dia útil", "tool": True, "group": "cal",
    "card": "Data do 5º dia útil de cada mês para pagamento do salário, com sábados contando.",
    "title": "Quinto Dia Útil 2026 e 2027 – Data de Pagamento do Salário",
    "desc": "Quando é o quinto dia útil de cada mês de 2026 e 2027? Tabela com a data-limite de pagamento do salário (CLT, art. 459), contando sábados como dia útil, e calculadora para qualquer mês.",
    "h1": "Quinto dia útil: data de pagamento do salário",
    "lead": "O salário mensal deve ser pago até o quinto dia útil do mês seguinte ao trabalhado (CLT, art. 459, §1º). Para essa contagem, o sábado é dia útil; domingos e feriados não. Veja as datas de 2026 e 2027 ou calcule para qualquer mês.",
    "sources": ["clt", "l662"],
    "body": """
<div class="calc">
<h2>Calcular o quinto dia útil</h2>
<div class="grid"><div><label for="mes">Mês do pagamento</label><input type="month" id="mes" style="width:100%;font:inherit;font-size:1.05rem;padding:10px 12px;border:1px solid #B7C1D1;border-radius:8px;min-height:46px"></div><div><label for="n">Dia útil</label><select id="n"><option value="5" selected>5º dia útil</option><option value="1">1º</option><option value="2">2º</option><option value="3">3º</option><option value="4">4º</option><option value="10">10º</option></select></div></div>
<div class="actions"><label class="chk"><input type="checkbox" id="sab" checked> Sábado conta como dia útil (regra do salário)</label></div>
<div class="result" id="res" aria-live="polite"><div class="big" id="t">–</div><div class="sub" id="td"></div><dl><dt>Dias contados</dt><dd id="lst">–</dd></dl></div>
<p class="hint">Considera os feriados nacionais. Se houver feriado estadual ou municipal no início do mês, a data avança um dia útil.</p>
</div>
<h2>Quinto dia útil 2026</h2>
""" + quinto_table(2026) + """
<h2>Quinto dia útil 2027</h2>
""" + quinto_table(2027) + """
<h2>Regras do pagamento do salário</h2>
<ul>
<li><strong>Prazo:</strong> até o 5º dia útil do mês subsequente ao vencido (CLT, art. 459, §1º).</li>
<li><strong>Sábado é dia útil</strong> para essa contagem, conforme orientação do Ministério do Trabalho (Instrução Normativa nº 1/1989); domingos e feriados são excluídos.</li>
<li><strong>Pagamento em conta:</strong> o valor deve estar disponível ao empregado dentro do prazo.</li>
<li><strong>Atraso:</strong> pode gerar multa prevista em convenção coletiva e correção do valor; atrasos reiterados podem justificar a rescisão indireta (CLT, art. 483, “d”).</li>
<li><strong>Doméstico e outros contratos:</strong> seguem a mesma regra do 5º dia útil, salvo pagamento semanal ou quinzenal.</li>
</ul>
<p>Para contar dias úteis de segunda a sexta entre duas datas, use a <a href="/dias-uteis/">calculadora de dias úteis</a>. Veja também o <a href="/calendario-2026/">calendário 2026</a> com feriados.</p>
""",
    "faq": [
        ("Sábado conta como dia útil para pagamento de salário?", "Sim. Para o prazo do art. 459 da CLT, o sábado é considerado dia útil; apenas domingos e feriados são excluídos."),
        ("Quando é o quinto dia útil de novembro de 2026?", f"{fmt(quinto(2026, 11))}, contando os sábados e descontando o feriado de Finados (2/11)."),
        ("Quando é o quinto dia útil de dezembro de 2026?", f"{fmt(quinto(2026, 12))}."),
        ("Quando é o quinto dia útil de janeiro de 2027?", f"{fmt(quinto(2027, 1))}, já que 1º de janeiro é feriado."),
        ("A empresa pode pagar depois do quinto dia útil?", "Não. O salário mensal deve ser pago até o 5º dia útil do mês seguinte. Convenções coletivas podem fixar prazos menores e multas por atraso."),
    ],
    "js": r"""
(function(){var M=document.getElementById('mes'),t=new Date();M.value=t.getFullYear()+'-'+pad(t.getMonth()+1);
function c(){var p=M.value.split('-');if(p.length<2)return;var y=+p[0],m=+p[1]-1,n=parseInt(document.getElementById('n').value),sab=document.getElementById('sab').checked,F=feriados(y),d=new Date(y,m,1,12),k=0,L=[];
while(k<n&&L.length<40){var dw=d.getDay(),ok=dw!==0&&(sab||dw!==6)&&!F[isoD(d)];if(ok){k++;L.push(d.getDate()+'/'+(m+1))}if(k<n)d.setDate(d.getDate()+1)}
document.getElementById('t').textContent=d.toLocaleDateString('pt-BR');document.getElementById('td').textContent=n+'º dia útil – '+d.toLocaleDateString('pt-BR',{weekday:'long'});document.getElementById('lst').textContent=L.join(' · ')}
['mes','n','sab'].forEach(function(i){document.getElementById(i).addEventListener('input',c)});c()})();""",
}

# ============================================================ Insalubridade
INSAL = {
    "path": "/adicional-de-insalubridade/", "short": "Adicional de insalubridade", "tool": True, "group": "sal",
    "card": "Insalubridade de 10%, 20% ou 40% do salário mínimo 2026 e comparação com periculosidade.",
    "title": "Adicional de Insalubridade 2026 – Cálculo de 10%, 20% e 40%",
    "desc": "Calcule o adicional de insalubridade 2026: grau mínimo (10%), médio (20%) ou máximo (40%) sobre o salário mínimo de R$ 1.621, compare com a periculosidade de 30% e veja os reflexos.",
    "h1": "Calculadora de adicional de insalubridade",
    "lead": "Escolha o grau de insalubridade definido no laudo (NR-15) e informe o salário. A calculadora mostra o adicional sobre o salário mínimo de 2026 e compara com o adicional de periculosidade, já que os dois não podem ser acumulados.",
    "sources": ["clt", "nr15", "tst"],
    "body": """
<div class="calc">
<h2>Calcular insalubridade</h2>
<div class="grid"><div><label for="grau">Grau de insalubridade</label><select id="grau"><option value="10">Mínimo – 10%</option><option value="20" selected>Médio – 20%</option><option value="40">Máximo – 40%</option></select></div><div><label for="base">Base de cálculo (R$)</label><input type="number" id="base" value="1621" step="1" min="0" inputmode="decimal"></div><div><label for="sal">Salário-base (para comparar periculosidade)</label><input type="number" id="sal" value="2500" step="50" min="0" inputmode="decimal"></div></div>
<div class="result" id="res" aria-live="polite"><div class="big" id="tot">–</div><div class="sub" id="totd">adicional de insalubridade por mês</div>
<dl><dt>Salário + insalubridade</dt><dd id="si">–</dd><dt>Periculosidade (30% do salário-base)</dt><dd id="pe">–</dd><dt>Mais vantajoso</dt><dd id="mv">–</dd></dl>
<div class="actions"><button class="btn sm ghost" type="button" onclick="copyRes('res',this)">Copiar resultado</button></div></div>
<p class="hint">A base padrão é o salário mínimo nacional de 2026 (R$ 1.621). Se a convenção coletiva da sua categoria prevê outra base (salário normativo ou salário-base), altere o campo.</p>
</div>
<h2>Valores do adicional de insalubridade em 2026</h2>
<div class="tw"><table class="t"><thead><tr><th>Grau</th><th>Percentual</th><th style="text-align:right">Valor mensal (sobre R$ 1.621)</th></tr></thead><tbody>
<tr><td>Mínimo</td><td>10%</td><td class="num">R$ 162,10</td></tr><tr><td>Médio</td><td>20%</td><td class="num">R$ 324,20</td></tr><tr><td>Máximo</td><td>40%</td><td class="num">R$ 648,40</td></tr>
</tbody></table></div>
<h2>Regras do adicional de insalubridade</h2>
<ul>
<li><strong>Quem tem direito:</strong> quem trabalha exposto a agentes nocivos acima dos limites de tolerância da Norma Regulamentadora 15 (ruído, calor, agentes químicos e biológicos etc.), comprovado por laudo de engenheiro ou médico do trabalho (CLT, arts. 189, 192 e 195).</li>
<li><strong>Percentuais:</strong> 10%, 20% ou 40%, conforme o grau (art. 192).</li>
<li><strong>Base de cálculo:</strong> na prática, o salário mínimo, enquanto não houver lei ou norma coletiva fixando outra base (Súmula Vinculante 4 do STF e decisões posteriores).</li>
<li><strong>Não acumula com periculosidade:</strong> o empregado escolhe o adicional mais vantajoso (art. 193, §2º). A periculosidade é de 30% sobre o salário-base.</li>
<li><strong>EPI:</strong> se o equipamento de proteção eliminar a exposição, o adicional deixa de ser devido (art. 191; Súmula 80 do TST).</li>
<li><strong>Reflexos:</strong> integra a remuneração para férias, 13º salário, FGTS e horas extras enquanto for pago — use a <a href="/calculadora-de-ferias/">calculadora de férias</a> e a <a href="/hora-extra/">calculadora de hora extra</a> com o valor somado.</li>
</ul>
""",
    "faq": [
        ("Qual o valor da insalubridade em 2026?", "Sobre o salário mínimo de R$ 1.621: grau mínimo R$ 162,10, médio R$ 324,20 e máximo R$ 648,40 por mês."),
        ("A insalubridade é calculada sobre o salário mínimo ou sobre o salário?", "Em regra, sobre o salário mínimo, salvo se a convenção coletiva ou o contrato previrem base maior."),
        ("Posso receber insalubridade e periculosidade juntas?", "Não. A CLT (art. 193, §2º) permite apenas um dos adicionais, à escolha do empregado — normalmente o de maior valor."),
        ("Quem define o grau de insalubridade?", "O laudo técnico de engenheiro de segurança ou médico do trabalho, com base nos anexos da NR-15."),
        ("A insalubridade entra nas horas extras?", "Sim. O adicional de insalubridade integra a base de cálculo das horas extras (Súmula 139 do TST, OJ 47 da SDI-1)."),
    ],
    "js": r"""
(function(){function c(){var g=parseFloat(document.getElementById('grau').value),b=val('base'),s=val('sal'),i=b*g/100,p=s*.3;
document.getElementById('tot').textContent=brl(i);document.getElementById('totd').textContent='insalubridade grau '+({10:'mínimo',20:'médio',40:'máximo'}[g])+' ('+g+'%) por mês';
document.getElementById('si').textContent=brl(s+i);document.getElementById('pe').textContent=brl(p);document.getElementById('mv').textContent=i>=p?'Insalubridade (+'+brl(i-p)+')':'Periculosidade (+'+brl(p-i)+')'}
['grau','base','sal'].forEach(function(i){document.getElementById(i).addEventListener('input',c)});c()})();""",
}

CONTENT = [FER26, FER27, CAL26, CAL27, E1236, E61, E52, FERIAS, IDADE, INTERV, QUINTO, INSAL]

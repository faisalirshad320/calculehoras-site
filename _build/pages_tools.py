# -*- coding: utf-8 -*-
from holidays import feriados, dias_uteis_mes, MESES, fmt

DAYS = ["Segunda", "Terça", "Quarta", "Quinta", "Sexta", "Sábado"]

# ============================================================ HOME — Calculadora de horas
HOME = {
    "path": "/", "short": "Calculadora de horas", "tool": True, "group": "jor",
    "card": "Some e subtraia horas e minutos ou calcule o tempo entre dois horários.",
    "title": "Calculadora de Horas Online – Somar e Subtrair Horas",
    "desc": "Calculadora de horas grátis: some e subtraia horas e minutos, calcule o tempo entre dois horários (inclusive após a meia-noite) e veja o resultado em horas e em decimal.",
    "h1": "Calculadora de horas – somar, subtrair e calcular intervalos",
    "lead": "Digite horas e minutos para somar ou subtrair, ou informe dois horários para saber quanto tempo passou entre eles. O resultado aparece em horas:minutos e em formato decimal, pronto para a folha de ponto.",
    "sources": ["clt"],
    "body": """
<div class="calc">
<h2>Somar e subtrair horas</h2>
<div class="rows" id="rows"></div>
<div class="actions"><button class="btn ghost sm" id="add" type="button">+ Adicionar linha</button><button class="btn" id="go" type="button">Calcular total</button><button class="btn ghost" id="reset" type="button">Limpar</button></div>
<div class="result" id="res" aria-live="polite"><div class="big" id="tot">0h00</div><div class="sub" id="totd">0,00 horas em decimal · 0 minutos</div>
<div class="actions"><button class="btn sm ghost" type="button" onclick="copyRes('res',this)">Copiar resultado</button></div></div>
<p class="hint">Escolha “–” para subtrair uma linha. Minutos acima de 59 são convertidos automaticamente em horas.</p>
</div>
<div class="calc">
<h2>Tempo entre dois horários</h2>
<div class="grid"><div><label for="a">Horário inicial</label><input type="time" id="a" value="08:00"></div><div><label for="b">Horário final</label><input type="time" id="b" value="17:48"></div><div><label for="pz">Descontar intervalo (min)</label><input type="number" id="pz" value="0" min="0" step="5"></div></div>
<div class="result" id="res2" aria-live="polite"><div class="big" id="t2">9h48</div><div class="sub" id="t2d">9,80 horas</div></div>
<p class="hint">Se o horário final for menor que o inicial, a calculadora entende que terminou no dia seguinte (ex.: 22:00 às 06:00 = 8 horas).</p>
</div>
<h2>Como somar horas corretamente</h2>
<p>Horas não seguem a base 10: cada hora tem 60 minutos. Por isso 2h45 + 1h30 não é 3h75, e sim <strong>4h15</strong>. A regra é simples:</p>
<ol>
<li>Some as horas e, separadamente, os minutos.</li>
<li>Divida o total de minutos por 60. O quociente vira horas; o resto continua como minutos.</li>
<li>Exemplo: 3h50 + 2h40 → 5 horas e 90 minutos → 90 ÷ 60 = 1 hora e 30 minutos → <strong>6h30</strong>.</li>
</ol>
<p>Para subtrair, faça o caminho inverso: se faltarem minutos, “empreste” 1 hora (60 minutos). Exemplo: 8h10 − 2h45 → 7h70 − 2h45 = <strong>5h25</strong>.</p>
<h2>Horas em decimal: quando usar</h2>
<p>Sistemas de ponto, planilhas e a folha de pagamento costumam trabalhar com horas decimais, porque elas podem ser multiplicadas diretamente pelo valor da hora. 7h30 corresponde a 7,5 horas; 7h45 a 7,75 horas; 7h20 a 7,33 horas. A tabela completa está na página <a href="/horas-em-decimal/">converter horas em decimal</a>.</p>
<h2>Para que serve cada calculadora</h2>
<ul>
<li><strong>Jornada da semana com intervalo:</strong> use a <a href="/horas-trabalhadas/">calculadora de horas trabalhadas</a>, que compara o total com as 44 horas semanais.</li>
<li><strong>Quanto vale a hora extra:</strong> a <a href="/hora-extra/">calculadora de hora extra</a> aplica os adicionais de 50% e 100%.</li>
<li><strong>Trabalho entre 22h e 5h:</strong> a <a href="/adicional-noturno/">calculadora de adicional noturno</a> considera a hora noturna reduzida de 52 minutos e 30 segundos.</li>
</ul>
""",
    "faq": [
        ("Como somar horas e minutos?", "Some as horas e os minutos separadamente. Cada 60 minutos viram 1 hora. Exemplo: 2h45 + 1h30 = 3 horas e 75 minutos = 4h15."),
        ("Como calcular quantas horas tem entre dois horários?", "Subtraia o horário inicial do final. Se o final for menor (virada da meia-noite), some 24 horas. Exemplo: das 22h às 6h são 8 horas."),
        ("Quanto é 1h30 em decimal?", "1,5 hora. Para converter, divida os minutos por 60: 30 ÷ 60 = 0,5."),
        ("Como subtrair horas?", "Subtraia horas e minutos separadamente. Se os minutos ficarem negativos, retire 1 hora e acrescente 60 minutos. Exemplo: 8h10 − 2h45 = 5h25."),
        ("A calculadora guarda meus dados?", "Não. Todos os cálculos são feitos no seu navegador e nada é enviado ou armazenado."),
    ],
    "js": r"""
(function(){var R=document.getElementById('rows');
function row(h,m,neg){var d=document.createElement('div');d.className='row';d.innerHTML='<div><label>Sinal e horas</label><div style="display:flex;gap:6px"><select aria-label="Somar ou subtrair" style="width:64px"><option value="1">+</option><option value="-1"'+(neg?' selected':'')+'>–</option></select><input type="number" min="0" inputmode="numeric" placeholder="h" value="'+(h||'')+'" aria-label="Horas"></div></div><div><label>Minutos</label><input type="number" min="0" inputmode="numeric" placeholder="min" value="'+(m||'')+'" aria-label="Minutos"></div><button class="btn ghost sm" type="button" aria-label="Remover linha" style="margin-bottom:4px">×</button>';
d.querySelector('button').onclick=function(){d.remove();calc()};d.querySelectorAll('input,select').forEach(function(x){x.addEventListener('input',calc)});R.appendChild(d)}
function calc(){var t=0;R.querySelectorAll('.row').forEach(function(r){var s=parseInt(r.querySelector('select').value),i=r.querySelectorAll('input');t+=s*((parseFloat(i[0].value)||0)*60+(parseFloat(i[1].value)||0))});
document.getElementById('tot').textContent=fmtH(t);document.getElementById('totd').textContent=fmtDec(t)+' horas em decimal · '+Math.round(t).toLocaleString('pt-BR')+' minutos'}
document.getElementById('add').onclick=function(){row()};document.getElementById('go').onclick=calc;document.getElementById('reset').onclick=function(){R.innerHTML='';row();row();row();calc()};
row(2,45);row(1,30);row(3,50);calc();
function c2(){var a=tmin(document.getElementById('a').value),b=tmin(document.getElementById('b').value),p=val('pz');if(a===null||b===null)return;var d=b-a;if(d<0)d+=1440;d-=p;if(d<0)d=0;document.getElementById('t2').textContent=fmtH(d);document.getElementById('t2d').textContent=fmtDec(d)+' horas'+(b<a?' · termina no dia seguinte':'')}
['a','b','pz'].forEach(function(i){document.getElementById(i).addEventListener('input',c2)});c2();
})();"""
}

# ============================================================ Horas trabalhadas (cartão de ponto)
rows = "".join(
    f'<tr><td><span class="dl">{d}</span><span class="ds">{d[:3]}</span></td>'
    + "".join(f'<td data-l="{lab.capitalize()}"><input type="time" id="{k}{i}" value="{v if i < 5 else ""}" aria-label="{d} {lab}"></td>'
              for k, v, lab in [("e", "08:00", "entrada"), ("si", "12:00", "saída para intervalo"), ("ri", "13:00", "retorno do intervalo"), ("s", "17:48", "saída")])
    + f'<td class="num" data-l="Total do dia" id="r{i}">–</td></tr>' for i, d in enumerate(DAYS))

TRAB = {
    "path": "/horas-trabalhadas/", "short": "Horas trabalhadas", "tool": True, "group": "jor",
    "card": "Cartão de ponto da semana com intervalo: total, horas extras e saldo.",
    "title": "Calculadora de Horas Trabalhadas com Intervalo",
    "desc": "Calcule as horas trabalhadas da semana pelo cartão de ponto: entrada, intervalo e saída de segunda a sábado. Veja o total, a diferença para 44h e as horas extras.",
    "h1": "Calculadora de horas trabalhadas – cartão de ponto semanal",
    "lead": "Preencha os quatro horários de cada dia — entrada, saída para o almoço, retorno e saída. A calculadora soma as horas trabalhadas, desconta o intervalo e compara o total com a sua jornada semanal (44h por padrão).",
    "sources": ["cf", "clt"],
    "body": f"""
<div class="calc">
<h2>Horas trabalhadas na semana</h2>
<div class="tw"><table class="t pt"><thead><tr><th>Dia</th><th>Entrada</th><th>Saída int.</th><th>Retorno</th><th>Saída</th><th style="text-align:right">Total</th></tr></thead><tbody>{rows}</tbody></table></div>
<div class="actions"><button class="btn" id="go" type="button">Calcular</button><button class="btn ghost" id="reset" type="button">Limpar</button><label class="chk" style="font-weight:500">Jornada semanal (h) <input type="number" id="jor" value="44" step="0.5" min="0" style="width:90px;min-height:38px;padding:6px 8px"></label></div>
<div class="result" id="res" aria-live="polite"><div class="big" id="tot">0h00</div><div class="sub" id="totd">0,00 horas em decimal</div>
<dl><dt>Jornada contratada</dt><dd id="jv">44h00</dd><dt>Diferença</dt><dd id="dif">–</dd><dt>Média por dia trabalhado</dt><dd id="avg">–</dd><dt>Dias acima de 10h</dt><dd id="lim">–</dd></dl>
<div class="actions"><button class="btn sm ghost" type="button" onclick="copyRes('res',this)">Copiar resultado</button></div></div>
<p class="hint">Sem intervalo? Deixe “Saída int.” e “Retorno” em branco. Turnos que viram a meia-noite são reconhecidos.</p>
</div>
<h2>Como calcular as horas trabalhadas</h2>
<div class="formula">Horas do dia = (saída para intervalo − entrada) + (saída − retorno)</div>
<p>Exemplo: entrada 08:00, almoço das 12:00 às 13:00 e saída às 17:48. Manhã: 4h00. Tarde: 4h48. Total: <strong>8h48</strong>. De segunda a sexta isso dá exatamente 44 horas — a jornada máxima semanal prevista no art. 7º, XIII, da Constituição.</p>
<h2>Regras da CLT que afetam o cálculo</h2>
<ul>
<li><strong>Jornada:</strong> até 8 horas diárias e 44 semanais (CF, art. 7º, XIII). O que passar disso é hora extra, limitada a 2 por dia (CLT, art. 59).</li>
<li><strong>Intervalo para almoço:</strong> quem trabalha mais de 6 horas tem direito a no mínimo 1 hora e no máximo 2 horas de intervalo; entre 4 e 6 horas, são 15 minutos (CLT, art. 71). O intervalo não conta como hora trabalhada.</li>
<li><strong>Tolerância no ponto:</strong> variações de até 5 minutos por marcação, no máximo 10 minutos por dia, não são descontadas nem pagas como extra (CLT, art. 58, §1º).</li>
<li><strong>Descanso entre jornadas:</strong> pelo menos 11 horas consecutivas entre o fim de um dia e o início do outro (CLT, art. 66).</li>
</ul>
<div class="note">Passou da jornada? Veja quanto vale a diferença na <a href="/hora-extra/">calculadora de hora extra</a> ou controle o saldo no <a href="/banco-de-horas/">banco de horas</a>.</div>
""",
    "faq": [
        ("Como calcular horas trabalhadas com intervalo de almoço?", "Calcule o período da manhã (saída para o almoço menos entrada) e o da tarde (saída menos retorno) e some os dois. Exemplo: 8h às 12h e 13h às 17h48 = 4h + 4h48 = 8h48."),
        ("Quantas horas por dia para fechar 44 horas semanais?", "De segunda a sexta, 8h48 por dia. Com expediente aos sábados, são 8 horas de segunda a sexta e 4 horas no sábado."),
        ("O intervalo de almoço conta como hora trabalhada?", "Não. O intervalo intrajornada (CLT, art. 71) não é computado na jornada. Se ele não for concedido, o período suprimido deve ser pago com acréscimo de 50%."),
        ("Quantas horas extras posso fazer por dia?", "No máximo 2 horas extras por dia, conforme o art. 59 da CLT, o que leva a jornada a até 10 horas."),
        ("Os 5 minutos de atraso são descontados?", "Não, se ficarem dentro da tolerância de 5 minutos por marcação e 10 minutos por dia (CLT, art. 58, §1º). Acima disso, todo o tempo é considerado."),
    ],
    "js": r"""
(function(){var N=6;function seg(a,b){if(a===null||b===null)return 0;var d=b-a;if(d<0)d+=1440;return d}
function calc(){var tot=0,days=0,over=0;for(var i=0;i<N;i++){var e=tmin(document.getElementById('e'+i).value),si=tmin(document.getElementById('si'+i).value),ri=tmin(document.getElementById('ri'+i).value),s=tmin(document.getElementById('s'+i).value),c=document.getElementById('r'+i);
if(e===null||s===null){c.textContent='–';continue}var d=(si!==null&&ri!==null)?seg(e,si)+seg(ri,s):seg(e,s);tot+=d;days++;if(d>600)over++;c.textContent=fmtH(d)}
var j=val('jor')*60;document.getElementById('tot').textContent=fmtH(tot);document.getElementById('totd').textContent=fmtDec(tot)+' horas em decimal';document.getElementById('jv').textContent=fmtH(j);
var df=tot-j;document.getElementById('dif').textContent=(df>=0?'+':'')+fmtH(df)+(df>0?' (horas extras)':df<0?' (horas a menos)':' (jornada exata)');
document.getElementById('avg').textContent=days?fmtH(tot/days):'–';document.getElementById('lim').textContent=over?over+' dia(s) acima do limite de 10h':'nenhum'}
document.getElementById('go').onclick=calc;document.getElementById('jor').oninput=calc;document.querySelectorAll('table.t input').forEach(function(x){x.addEventListener('change',calc)});
document.getElementById('reset').onclick=function(){document.querySelectorAll('table.t input').forEach(function(x){x.value=''});calc()};calc()})();"""
}

# ============================================================ Hora extra
HE = {
    "path": "/hora-extra/", "short": "Hora extra", "tool": True, "group": "sal",
    "card": "Valor da hora extra com adicional de 50% e 100%, divisor da CLT e DSR.",
    "title": "Calculadora de Hora Extra 2026 – 50% e 100% (CLT)",
    "desc": "Calculadora de hora extra grátis: informe salário, jornada e horas extras para ver o valor da hora normal, da hora extra 50% e 100% e o reflexo no DSR, conforme a CLT.",
    "h1": "Calculadora de hora extra – 50%, 100% e DSR",
    "lead": "Informe o salário bruto, a jornada semanal e as horas extras do mês. A calculadora encontra o valor da hora normal pelo divisor da CLT, aplica os adicionais de 50% e 100% e estima o reflexo no descanso semanal remunerado (DSR).",
    "sources": ["cf", "clt", "l605", "tst"],
    "body": """
<div class="calc">
<h2>Calcular hora extra</h2>
<div class="grid"><div><label for="sal">Salário bruto mensal (R$)</label><input type="number" id="sal" value="3000" step="50" min="0" inputmode="decimal"></div><div><label for="jor">Jornada semanal</label><select id="jor"><option value="44" selected>44 horas (divisor 220)</option><option value="40">40 horas (divisor 200)</option><option value="36">36 horas (divisor 180)</option><option value="30">30 horas (divisor 150)</option></select></div></div>
<h3>Horas extras no mês</h3>
<div class="grid"><div><label for="h50">Dias úteis – horas</label><input type="number" id="h50" value="10" min="0" inputmode="numeric"></div><div><label for="m50">minutos</label><input type="number" id="m50" value="0" min="0" inputmode="numeric"></div><div><label for="p50">Adicional (%)</label><input type="number" id="p50" value="50" min="50" step="5"></div></div>
<div class="grid" style="margin-top:12px"><div><label for="h100">Domingos e feriados – horas</label><input type="number" id="h100" value="0" min="0" inputmode="numeric"></div><div><label for="m100">minutos</label><input type="number" id="m100" value="0" min="0" inputmode="numeric"></div><div><label for="p100">Adicional (%)</label><input type="number" id="p100" value="100" min="50" step="5"></div></div>
<h3>Reflexo no DSR (opcional)</h3>
<div class="grid"><div><label for="du">Dias úteis no mês (seg. a sáb.)</label><input type="number" id="du" value="25" min="1"></div><div><label for="df">Domingos e feriados no mês</label><input type="number" id="df" value="5" min="0"></div></div>
<div class="result" id="res" aria-live="polite"><div class="big" id="tot">R$ 0,00</div><div class="sub" id="totd">total de horas extras + DSR (valor bruto)</div>
<dl><dt>Valor da hora normal</dt><dd id="vh">–</dd><dt>Hora extra a 50%</dt><dd id="v50">–</dd><dt>Hora extra a 100%</dt><dd id="v100">–</dd><dt>Total das horas extras</dt><dd id="the">–</dd><dt>DSR sobre horas extras</dt><dd id="dsr">–</dd></dl>
<div class="actions"><button class="btn sm ghost" type="button" onclick="copyRes('res',this)">Copiar resultado</button></div></div>
<p class="hint">Valores brutos, antes de INSS e IRRF. Convenções coletivas podem prever adicionais maiores — ajuste os percentuais.</p>
</div>
<h2>Fórmula da hora extra</h2>
<div class="formula">Valor da hora = salário ÷ divisor &nbsp;·&nbsp; Hora extra 50% = valor da hora × 1,5 &nbsp;·&nbsp; Hora extra 100% = valor da hora × 2</div>
<p>O <strong>divisor</strong> é a jornada semanal multiplicada por 5: 44h → 220, 40h → 200, 36h → 180. Exemplo com salário de R$ 3.000 e 44 horas semanais:</p>
<ul>
<li>Valor da hora normal: R$ 3.000 ÷ 220 = <strong>R$ 13,64</strong></li>
<li>Hora extra a 50%: R$ 13,64 × 1,5 = <strong>R$ 20,45</strong></li>
<li>10 horas extras no mês: 10 × R$ 20,45 = <strong>R$ 204,55</strong></li>
<li>DSR (25 dias úteis, 5 domingos/feriados): R$ 204,55 ÷ 25 × 5 = <strong>R$ 40,91</strong></li>
</ul>
<h2>O que diz a lei</h2>
<ul>
<li><strong>Adicional mínimo de 50%</strong> sobre a hora normal (Constituição, art. 7º, XVI; CLT, art. 59, §1º).</li>
<li><strong>Domingos e feriados</strong> trabalhados e não compensados são pagos em dobro, ou seja, com 100% (Súmula 146 do TST).</li>
<li><strong>Limite diário:</strong> no máximo 2 horas extras por dia (CLT, art. 59).</li>
<li><strong>DSR:</strong> horas extras habituais refletem no descanso semanal remunerado (Lei 605/1949; Súmula 172 do TST). Para calcular só essa parte, use a <a href="/dsr-hora-extra/">calculadora de DSR</a>.</li>
<li><strong>Hora extra noturna:</strong> entre 22h e 5h, some também o <a href="/adicional-noturno/">adicional noturno</a> de 20%.</li>
</ul>
<div class="note">Não sabe quantas horas extras fez? Some o cartão de ponto na <a href="/horas-trabalhadas/">calculadora de horas trabalhadas</a>. Se a empresa usa compensação, confira o <a href="/banco-de-horas/">banco de horas</a>. Trabalha em plantões? Veja a <a href="/escala-12x36/">escala 12x36</a>.</div>
""",
    "faq": [
        ("Como calcular o valor da hora extra?", "Divida o salário pelo divisor da jornada (220 para 44 horas semanais) para achar o valor da hora. Multiplique por 1,5 para a hora extra a 50% ou por 2 para a de 100%."),
        ("Quanto é a hora extra de quem ganha um salário mínimo em 2026?", "Com salário mínimo de R$ 1.621 e jornada de 44 horas: hora normal = R$ 1.621 ÷ 220 = R$ 7,37; hora extra a 50% = R$ 11,05; a 100% = R$ 14,74."),
        ("Hora extra no domingo é 100%?", "Sim, quando o domingo ou feriado trabalhado não é compensado com folga em outro dia, a remuneração é em dobro (Súmula 146 do TST). Convenções coletivas podem prever outro percentual."),
        ("Qual é o divisor para 40 horas semanais?", "200. O divisor é a jornada semanal multiplicada por 5: 40 × 5 = 200."),
        ("Hora extra entra no DSR?", "Sim. Horas extras habituais geram reflexo no descanso semanal remunerado: valor das horas extras do mês ÷ dias úteis × domingos e feriados."),
        ("Posso fazer quantas horas extras por dia?", "Até 2 horas extras por dia, segundo o art. 59 da CLT, salvo situações excepcionais de força maior."),
    ],
    "js": r"""
(function(){function c(){var s=val('sal'),j=parseFloat(document.getElementById('jor').value),dv=j*5,vh=dv?s/dv:0;
var m50=val('h50')*60+val('m50'),m100=val('h100')*60+val('m100'),r50=vh*(1+val('p50')/100),r100=vh*(1+val('p100')/100);
var t50=r50*m50/60,t100=r100*m100/60,the=t50+t100,du=val('du'),df=val('df'),dsr=du?the/du*df:0;
document.getElementById('vh').textContent=brl(vh)+' (divisor '+dv+')';document.getElementById('v50').textContent=brl(r50)+' por hora · '+fmtH(m50)+' = '+brl(t50);
document.getElementById('v100').textContent=brl(r100)+' por hora · '+fmtH(m100)+' = '+brl(t100);document.getElementById('the').textContent=brl(the);document.getElementById('dsr').textContent=brl(dsr);
document.getElementById('tot').textContent=brl(the+dsr)}
['sal','jor','h50','m50','p50','h100','m100','p100','du','df'].forEach(function(i){document.getElementById(i).addEventListener('input',c)});c()})();"""
}

# ============================================================ Adicional noturno
NOT = {
    "path": "/adicional-noturno/", "short": "Adicional noturno", "tool": True, "group": "sal",
    "card": "Horas noturnas (22h–5h), hora reduzida de 52min30s e valor do adicional de 20%.",
    "title": "Calculadora de Adicional Noturno – 20% e Hora Reduzida",
    "desc": "Calcule o adicional noturno: informe o horário de trabalho e o salário para ver as horas noturnas entre 22h e 5h, a hora reduzida de 52min30s e o valor do adicional de 20% (CLT).",
    "h1": "Calculadora de adicional noturno",
    "lead": "Informe o horário do turno, o salário e quantos dias trabalhou no mês. A calculadora separa as horas entre 22h e 5h, aplica a hora noturna reduzida de 52 minutos e 30 segundos e calcula o adicional de 20% (ou 25% no trabalho rural).",
    "sources": ["clt", "l5889", "tst"],
    "body": """
<div class="calc">
<h2>Calcular adicional noturno</h2>
<div class="grid"><div><label for="ini">Início do turno</label><input type="time" id="ini" value="22:00"></div><div><label for="fim">Fim do turno</label><input type="time" id="fim" value="06:00"></div><div><label for="dias">Dias trabalhados no mês</label><input type="number" id="dias" value="22" min="0"></div></div>
<div class="grid" style="margin-top:12px"><div><label for="sal">Salário bruto (R$)</label><input type="number" id="sal" value="2500" step="50" min="0" inputmode="decimal"></div><div><label for="jor">Jornada semanal</label><select id="jor"><option value="44">44h (divisor 220)</option><option value="40">40h (divisor 200)</option><option value="36">36h (divisor 180)</option></select></div><div><label for="tipo">Tipo de trabalho</label><select id="tipo"><option value="urb">Urbano – 20%, 22h às 5h</option><option value="lav">Rural lavoura – 25%, 21h às 5h</option><option value="pec">Rural pecuária – 25%, 20h às 4h</option></select></div></div>
<div class="actions"><label class="chk"><input type="checkbox" id="prorr" checked> Contar horas após o horário noturno quando o turno começa à noite (Súmula 60, II, do TST)</label></div>
<div class="result" id="res" aria-live="polite"><div class="big" id="tot">R$ 0,00</div><div class="sub" id="totd">adicional noturno no mês (bruto)</div>
<dl><dt>Horas noturnas por dia (relógio)</dt><dd id="hr">–</dd><dt>Horas noturnas por dia (reduzidas)</dt><dd id="hf">–</dd><dt>Valor da hora normal</dt><dd id="vh">–</dd><dt>Adicional por dia</dt><dd id="ad">–</dd></dl>
<div class="actions"><button class="btn sm ghost" type="button" onclick="copyRes('res',this)">Copiar resultado</button></div></div>
<p class="hint">A hora reduzida só se aplica ao trabalho urbano. No rural, a hora noturna tem 60 minutos e o adicional é de 25%.</p>
</div>
<h2>Como funciona o adicional noturno</h2>
<p>No trabalho urbano, é noturno o período entre <strong>22h e 5h</strong>. A hora trabalhada nesse horário vale 20% a mais e é contada como se tivesse <strong>52 minutos e 30 segundos</strong> (CLT, art. 73). Na prática, 7 horas de relógio entre 22h e 5h equivalem a 8 horas noturnas.</p>
<div class="formula">Horas reduzidas = minutos noturnos ÷ 52,5 &nbsp;·&nbsp; Adicional = valor da hora × horas reduzidas × 20%</div>
<p>Exemplo: turno das 22h às 5h, salário de R$ 2.500 e 44h semanais. Valor da hora: R$ 2.500 ÷ 220 = R$ 11,36. Horas reduzidas: 420 ÷ 52,5 = 8. Adicional por noite: R$ 11,36 × 8 × 20% = <strong>R$ 18,18</strong>. Em 22 noites: <strong>R$ 400,00</strong>.</p>
<h2>Regras importantes</h2>
<ul>
<li><strong>Prorrogação:</strong> se a jornada é cumprida no período noturno e se estende após as 5h, as horas seguintes também recebem o adicional (Súmula 60, II, do TST).</li>
<li><strong>Rural:</strong> adicional de 25%, sem hora reduzida — lavoura das 21h às 5h; pecuária das 20h às 4h (Lei 5.889/1973, art. 7º).</li>
<li><strong>Hora extra noturna:</strong> o adicional noturno integra a base da hora extra. Calcule a hora extra na <a href="/hora-extra/">calculadora de hora extra</a> usando o valor da hora já acrescido de 20%.</li>
<li><strong>Turno que vira a noite:</strong> para saber a duração total do turno, use a <a href="/">calculadora de horas</a>.</li>
</ul>
""",
    "faq": [
        ("Qual o horário do adicional noturno?", "Para trabalhadores urbanos, das 22h às 5h. No campo, das 21h às 5h na lavoura e das 20h às 4h na pecuária."),
        ("Quanto é o adicional noturno?", "No mínimo 20% sobre a hora diurna para trabalhadores urbanos (CLT, art. 73) e 25% para rurais (Lei 5.889/1973). Convenções coletivas podem prever percentuais maiores."),
        ("O que é hora noturna reduzida?", "É a regra que considera cada hora noturna urbana como 52 minutos e 30 segundos. Assim, 7 horas de relógio entre 22h e 5h valem 8 horas noturnas."),
        ("Quem trabalha das 22h às 6h recebe adicional depois das 5h?", "Sim, quando a jornada é cumprida integralmente no período noturno e prorrogada, as horas após as 5h também recebem o adicional (Súmula 60, II, do TST)."),
        ("Como calcular o adicional noturno de quem ganha um salário mínimo?", "Com R$ 1.621 e 44h semanais, a hora vale R$ 7,37. O adicional é de R$ 1,47 por hora noturna reduzida. Uma noite completa das 22h às 5h (8 horas reduzidas) rende R$ 11,79 de adicional."),
    ],
    "js": r"""
(function(){var W={urb:[1320,300,.2,true],lav:[1260,300,.25,false],pec:[1200,240,.25,false]};
function c(){var a=tmin(document.getElementById('ini').value),b=tmin(document.getElementById('fim').value);if(a===null||b===null)return;var t=document.getElementById('tipo').value,w=W[t];
var end=b<=a?b+1440:b,nm=0;for(var m=a;m<end;m++){var x=m%1440;var inN=w[0]>w[1]?(x>=w[0]||x<w[1]):(x>=w[0]&&x<w[1]);if(inN)nm++}
if(document.getElementById('prorr').checked){var wEnd=(a>=w[0]?w[1]+1440:w[1]);var startsNight=(a>=w[0]||a<w[1]);if(startsNight&&end>wEnd){nm+=end-wEnd}}
var red=w[3]?nm/52.5:nm/60,s=val('sal'),dv=parseFloat(document.getElementById('jor').value)*5,vh=s/dv,ad=vh*red*w[2],d=val('dias');
document.getElementById('hr').textContent=fmtH(nm);document.getElementById('hf').textContent=num(red,2)+' h'+(w[3]?' (hora de 52min30s)':' (sem redução)');
document.getElementById('vh').textContent=brl(vh);document.getElementById('ad').textContent=brl(ad)+' ('+Math.round(w[2]*100)+'%)';document.getElementById('tot').textContent=brl(ad*d);document.getElementById('totd').textContent='adicional noturno em '+d+' dia(s) (bruto)'}
['ini','fim','dias','sal','jor','tipo','prorr'].forEach(function(i){document.getElementById(i).addEventListener('input',c)});c()})();"""
}

# ============================================================ DSR
DSR = {
    "path": "/dsr-hora-extra/", "short": "DSR sobre hora extra", "tool": True, "group": "sal",
    "card": "Reflexo das horas extras no descanso semanal remunerado, com dias do mês automáticos.",
    "title": "Calculadora de DSR sobre Hora Extra – Fórmula e Exemplo",
    "desc": "Calcule o DSR sobre horas extras: escolha o mês para contar dias úteis, domingos e feriados automaticamente e veja o valor do reflexo no descanso semanal remunerado.",
    "h1": "Calculadora de DSR sobre hora extra",
    "lead": "O descanso semanal remunerado (DSR) também deve refletir as horas extras habituais. Escolha o mês para a calculadora contar os dias úteis, domingos e feriados nacionais, e informe o valor das horas extras.",
    "sources": ["l605", "tst", "l662"],
    "body": """
<div class="calc">
<h2>Calcular o DSR</h2>
<div class="grid"><div><label for="mes">Mês de referência</label><input type="month" id="mes" style="width:100%;font:inherit;font-size:1.05rem;padding:10px 12px;border:1px solid #B7C1D1;border-radius:8px;min-height:46px"></div><div><label for="vhe">Total de horas extras no mês (R$)</label><input type="number" id="vhe" value="500" step="10" min="0" inputmode="decimal"></div></div>
<div class="grid" style="margin-top:12px"><div><label for="du">Dias úteis (seg. a sáb.)</label><input type="number" id="du" min="1"></div><div><label for="df">Domingos e feriados</label><input type="number" id="df" min="0"></div></div>
<div class="result" id="res" aria-live="polite"><div class="big" id="tot">R$ 0,00</div><div class="sub" id="totd">DSR sobre horas extras</div><dl><dt>Feriados nacionais no mês</dt><dd id="fer">–</dd><dt>Total com DSR</dt><dd id="tt">–</dd></dl></div>
<p class="hint">Os dias são preenchidos pelo mês escolhido com base nos feriados nacionais. Inclua manualmente feriados estaduais e municipais.</p>
</div>
<h2>Fórmula do DSR sobre horas extras</h2>
<div class="formula">DSR = (valor das horas extras do mês ÷ dias úteis) × domingos e feriados</div>
<p>Para o DSR, <strong>dias úteis incluem o sábado</strong> (de segunda a sábado, exceto feriados). Exemplo: R$ 500 em horas extras em um mês com 25 dias úteis e 5 domingos e feriados → R$ 500 ÷ 25 × 5 = <strong>R$ 100,00</strong> de DSR.</p>
<h2>Base legal</h2>
<p>A Lei 605/1949 garante o repouso semanal remunerado, e a Súmula 172 do TST determina que as horas extras habitualmente prestadas sejam computadas no seu cálculo. O valor das horas extras você obtém na <a href="/hora-extra/">calculadora de hora extra</a>; para contar dias úteis de qualquer período, use a <a href="/dias-uteis/">calculadora de dias úteis</a>.</p>
""",
    "faq": [
        ("Como calcular o DSR sobre horas extras?", "Divida o valor total das horas extras do mês pelo número de dias úteis (segunda a sábado) e multiplique pelo número de domingos e feriados do mês."),
        ("Sábado conta como dia útil no DSR?", "Sim. Para o cálculo do DSR, consideram-se dias úteis de segunda a sábado, excluindo feriados."),
        ("O DSR incide sobre todas as horas extras?", "Incide sobre as horas extras habituais (Súmula 172 do TST). Horas extras eventuais podem não gerar reflexo, dependendo do caso."),
        ("Quantos domingos e feriados tem o mês?", "Depende do mês. Escolha o mês na calculadora: ela conta domingos e feriados nacionais automaticamente."),
    ],
    "js": r"""
(function(){var M=document.getElementById('mes'),n=new Date();M.value=n.getFullYear()+'-'+pad(n.getMonth()+1);
function fill(){var p=M.value.split('-');if(p.length<2)return;var y=+p[0],m=+p[1]-1,F=feriados(y),d=new Date(y,m,1),du=0,df=0,names=[];while(d.getMonth()===m){var k=isoD(d),dw=d.getDay();if(dw===0||F[k]){df++;if(F[k])names.push(d.getDate()+'/'+(m+1)+' '+F[k])}else du++;d.setDate(d.getDate()+1)}
document.getElementById('du').value=du;document.getElementById('df').value=df;document.getElementById('fer').textContent=names.length?names.join(' · '):'nenhum';c()}
function c(){var v=val('vhe'),du=val('du'),df=val('df'),r=du?v/du*df:0;document.getElementById('tot').textContent=brl(r);document.getElementById('tt').textContent=brl(v+r)}
M.addEventListener('input',fill);['vhe','du','df'].forEach(function(i){document.getElementById(i).addEventListener('input',c)});fill()})();"""
}

# ============================================================ Dias úteis
def _tabela_uteis(y):
    rows = "".join(f"<tr><td>{MESES[m-1].capitalize()}</td><td class=\"num\">{dias_uteis_mes(y, m)}</td><td class=\"num\">{dias_uteis_mes(y, m, True)}</td></tr>" for m in range(1, 13))
    tot = sum(dias_uteis_mes(y, m) for m in range(1, 13))
    tot6 = sum(dias_uteis_mes(y, m, True) for m in range(1, 13))
    return rows + f'<tr><td><strong>Total {y}</strong></td><td class="num">{tot}</td><td class="num">{tot6}</td></tr>', tot


def _lista_feriados(y):
    return "".join(f"<li>{fmt(d)} – {n}</li>" for d, n in feriados(y).items())


T26, TOT26 = _tabela_uteis(2026)
UTEIS = {
    "path": "/dias-uteis/", "short": "Dias úteis", "tool": True, "group": "cal",
    "card": "Conte dias úteis entre duas datas com os feriados nacionais de qualquer ano.",
    "title": "Calculadora de Dias Úteis 2026 – com Feriados Nacionais",
    "desc": "Conte os dias úteis entre duas datas descontando sábados, domingos e feriados nacionais. Veja quantos dias úteis tem cada mês de 2026 e a lista oficial de feriados.",
    "h1": "Calculadora de dias úteis",
    "lead": f"Informe a data inicial e a final para contar os dias úteis, já descontando fins de semana e feriados nacionais. Em 2026, o ano tem {TOT26} dias úteis de segunda a sexta.",
    "sources": ["l662", "l14759"],
    "body": f"""
<div class="calc">
<h2>Contar dias úteis entre duas datas</h2>
<div class="grid"><div><label for="d1">Data inicial</label><input type="date" id="d1"></div><div><label for="d2">Data final</label><input type="date" id="d2"></div></div>
<div class="actions"><label class="chk"><input type="checkbox" id="sab"> Sábado é dia útil</label><label class="chk"><input type="checkbox" id="car"> Descontar Carnaval</label><label class="chk"><input type="checkbox" id="cor"> Descontar Corpus Christi</label><label class="chk"><input type="checkbox" id="inc" checked> Incluir a data inicial</label></div>
<div class="result" id="res" aria-live="polite"><div class="big" id="t">– dias úteis</div><div class="sub" id="td"></div><dl><dt>Dias corridos</dt><dd id="dc">–</dd><dt>Fins de semana</dt><dd id="fs">–</dd><dt>Feriados no período</dt><dd id="fp">–</dd></dl>
<div class="actions"><button class="btn sm ghost" type="button" onclick="copyRes('res',this)">Copiar resultado</button></div></div>
<p class="hint">Feriados estaduais e municipais não são descontados. Carnaval e Corpus Christi são pontos facultativos nacionais — marque se não houver expediente.</p>
</div>
<h2>Quantos dias úteis tem cada mês de 2026</h2>
<div class="tw"><table class="t"><thead><tr><th>Mês</th><th style="text-align:right">Seg. a sex.</th><th style="text-align:right">Seg. a sáb.</th></tr></thead><tbody>{T26}</tbody></table></div>
<p class="hint">Considera os feriados nacionais. Carnaval (16 e 17/2) e Corpus Christi (4/6) contam como dias úteis por serem pontos facultativos.</p>
<h2>Feriados nacionais de 2026</h2>
<p>Veja todos os detalhes e feriadões em <a href="/feriados-2026/">feriados 2026</a>, o <a href="/calendario-2026/">calendário 2026</a> e o prazo do salário no <a href="/quinto-dia-util/">quinto dia útil</a>.</p>
<ul>{_lista_feriados(2026)}</ul>
<p>Pontos facultativos: Carnaval em 16 e 17 de fevereiro, Quarta-feira de Cinzas até as 14h (18/2) e Corpus Christi em 4 de junho (Portaria MGI nº 11.460/2025). O Dia Nacional de Zumbi e da Consciência Negra (20/11) é feriado nacional desde 2024 (Lei 14.759/2023).</p>
<h2>Como contar dias úteis</h2>
<ol><li>Conte todos os dias do período (dias corridos).</li><li>Retire os sábados e domingos.</li><li>Retire os feriados que caem de segunda a sexta.</li></ol>
<p>Precisa somar ou subtrair dias corridos, ou saber a diferença em anos, meses e dias? Use a <a href="/calculadora-de-datas/">calculadora de datas</a>. Para contar quanto falta para uma data, veja <a href="/quantos-dias-faltam/">quantos dias faltam</a>.</p>
""",
    "faq": [
        ("Quantos dias úteis tem 2026?", f"{TOT26} dias úteis de segunda a sexta, considerando os feriados nacionais. Carnaval e Corpus Christi são pontos facultativos e estão incluídos como dias úteis nessa conta."),
        ("Sábado é dia útil?", "Para prazos bancários e a maioria das empresas, não. Para o cálculo do DSR e alguns prazos trabalhistas, sim. Marque a opção “Sábado é dia útil” quando for o seu caso."),
        ("Carnaval é feriado nacional?", "Não. Carnaval é ponto facultativo nacional. Em alguns estados e municípios ele é feriado por lei local."),
        ("Quais são os feriados nacionais de 2026?", "1/1, 3/4 (Paixão de Cristo), 21/4, 1/5, 7/9, 12/10, 2/11, 15/11, 20/11 (Consciência Negra) e 25/12."),
        ("Quantos dias úteis tem um mês?", "Em média 21 a 22 dias úteis de segunda a sexta. O número exato depende dos fins de semana e feriados — veja a tabela de 2026 nesta página."),
    ],
    "js": r"""
(function(){var t=new Date();document.getElementById('d1').value=isoD(t);var e=new Date(t);e.setDate(e.getDate()+30);document.getElementById('d2').value=isoD(e);
function c(){var a=document.getElementById('d1').value,b=document.getElementById('d2').value;if(!a||!b)return;var A=new Date(a+'T12:00:00'),B=new Date(b+'T12:00:00');if(B<A){var x=A;A=B;B=x}
var sab=document.getElementById('sab').checked,opt={carnaval:document.getElementById('car').checked,corpus:document.getElementById('cor').checked},inc=document.getElementById('inc').checked;
var cur=new Date(A);if(!inc)cur.setDate(cur.getDate()+1);var u=0,f=0,fw=0,tot=0,names=[],cache={};
while(cur<=B){var y=cur.getFullYear();if(!cache[y])cache[y]=feriados(y,opt);var k=isoD(cur),dw=cur.getDay(),we=dw===0||(dw===6&&!sab);tot++;if(we)fw++;else if(cache[y][k]){f++;names.push(cur.getDate()+'/'+(cur.getMonth()+1)+' '+cache[y][k])}else u++;cur.setDate(cur.getDate()+1)}
document.getElementById('t').textContent=u.toLocaleString('pt-BR')+' dias úteis';document.getElementById('td').textContent=A.toLocaleDateString('pt-BR')+' a '+B.toLocaleDateString('pt-BR');
document.getElementById('dc').textContent=tot;document.getElementById('fs').textContent=fw;document.getElementById('fp').textContent=f?f+' — '+names.join(' · '):'nenhum'}
['d1','d2','sab','car','cor','inc'].forEach(function(i){document.getElementById(i).addEventListener('input',c)});c()})();"""
}

# ============================================================ Calculadora de datas
DATAS = {
    "path": "/calculadora-de-datas/", "short": "Calculadora de datas", "tool": True, "group": "cal",
    "card": "Diferença entre datas em anos, meses e dias; somar e subtrair dias corridos.",
    "title": "Calculadora de Datas – Dias Entre Datas e Somar Dias",
    "desc": "Calculadora de datas online: descubra quantos dias, semanas, meses e anos há entre duas datas e some ou subtraia dias, meses ou anos de uma data. Grátis e sem cadastro.",
    "h1": "Calculadora de datas – dias entre datas e soma de dias",
    "lead": "Descubra a diferença exata entre duas datas em dias corridos, semanas e anos-meses-dias, ou some e subtraia dias, meses e anos de qualquer data.",
    "sources": [],
    "body": """
<div class="calc">
<h2>Diferença entre duas datas</h2>
<div class="grid"><div><label for="d1">Data inicial</label><input type="date" id="d1"></div><div><label for="d2">Data final</label><input type="date" id="d2"></div></div>
<div class="result" id="res" aria-live="polite"><div class="big" id="t">–</div><div class="sub" id="td"></div><dl><dt>Em anos, meses e dias</dt><dd id="amd">–</dd><dt>Em semanas</dt><dd id="sem">–</dd><dt>Em horas</dt><dd id="hrs">–</dd></dl>
<div class="actions"><button class="btn sm ghost" type="button" onclick="copyRes('res',this)">Copiar resultado</button></div></div>
</div>
<div class="calc">
<h2>Somar ou subtrair tempo de uma data</h2>
<div class="grid"><div><label for="d3">Data</label><input type="date" id="d3"></div><div><label for="op">Operação</label><select id="op"><option value="1">+ Somar</option><option value="-1">– Subtrair</option></select></div><div><label for="nd">Dias</label><input type="number" id="nd" value="90" min="0"></div><div><label for="nm">Meses</label><input type="number" id="nm" value="0" min="0"></div><div><label for="ny">Anos</label><input type="number" id="ny" value="0" min="0"></div></div>
<div class="result" id="res2" aria-live="polite"><div class="big" id="t2">–</div><div class="sub" id="t2d"></div></div>
</div>
<h2>Como calcular dias entre datas</h2>
<p>A diferença entre duas datas em <strong>dias corridos</strong> conta todos os dias do calendário, incluindo fins de semana e feriados. Entre 1º e 31 de janeiro há 30 dias de diferença; se você incluir o primeiro e o último dia, são 31 dias.</p>
<p>Na forma <strong>anos, meses e dias</strong>, a calculadora avança mês a mês do calendário, como se faz para calcular idade ou tempo de serviço. Exemplo: de 15/03/2020 a 10/10/2026 são 6 anos, 6 meses e 25 dias.</p>
<h2>Prazos em dias corridos x dias úteis</h2>
<p>Prazos contratuais e de entrega muitas vezes são em dias corridos; prazos processuais trabalhistas e bancários costumam ser em dias úteis. Para descontar fins de semana e feriados, use a <a href="/dias-uteis/">calculadora de dias úteis</a>. Para uma contagem regressiva até um evento, veja <a href="/quantos-dias-faltam/">quantos dias faltam</a>.</p>
""",
    "faq": [
        ("Como calcular quantos dias tem entre duas datas?", "Subtraia a data inicial da final em dias de calendário. A calculadora faz isso automaticamente e também mostra o resultado em semanas e em anos, meses e dias."),
        ("Quantos dias são 90 dias a partir de hoje?", "Escolha a data de hoje em “Somar ou subtrair tempo”, informe 90 dias e a calculadora mostra a data final com o dia da semana."),
        ("O que são dias corridos?", "São todos os dias do calendário, sem descontar sábados, domingos ou feriados."),
        ("Como calcular tempo de serviço em anos, meses e dias?", "Informe a data de admissão e a data final. O campo “anos, meses e dias” mostra o tempo de serviço completo."),
    ],
    "js": r"""
(function(){var t=new Date();document.getElementById('d1').value='2020-03-15';document.getElementById('d2').value=isoD(t);document.getElementById('d3').value=isoD(t);
var fmtL=function(d){return d.toLocaleDateString('pt-BR',{weekday:'long',day:'2-digit',month:'long',year:'numeric'})};
function c1(){var a=document.getElementById('d1').value,b=document.getElementById('d2').value;if(!a||!b)return;var A=new Date(a+'T12:00:00'),B=new Date(b+'T12:00:00'),neg=B<A;if(neg){var x=A;A=B;B=x}
var d=Math.round((B-A)/864e5);var y=B.getFullYear()-A.getFullYear(),m=B.getMonth()-A.getMonth(),dd=B.getDate()-A.getDate();if(dd<0){m--;dd+=new Date(B.getFullYear(),B.getMonth(),0).getDate()}if(m<0){y--;m+=12}
document.getElementById('t').textContent=(neg?'−':'')+d.toLocaleString('pt-BR')+' dias';document.getElementById('td').textContent=fmtL(A)+' até '+fmtL(B);
document.getElementById('amd').textContent=y+' ano(s), '+m+' mês(es) e '+dd+' dia(s)';document.getElementById('sem').textContent=Math.floor(d/7)+' semanas e '+(d%7)+' dia(s)';document.getElementById('hrs').textContent=(d*24).toLocaleString('pt-BR')+' horas'}
function c2(){var a=document.getElementById('d3').value;if(!a)return;var A=new Date(a+'T12:00:00'),s=parseInt(document.getElementById('op').value);A.setFullYear(A.getFullYear()+s*val('ny'));A.setMonth(A.getMonth()+s*val('nm'));A.setDate(A.getDate()+s*val('nd'));document.getElementById('t2').textContent=A.toLocaleDateString('pt-BR');document.getElementById('t2d').textContent=fmtL(A)}
['d1','d2'].forEach(function(i){document.getElementById(i).addEventListener('input',c1)});['d3','op','nd','nm','ny'].forEach(function(i){document.getElementById(i).addEventListener('input',c2)});c1();c2()})();"""
}

# ============================================================ Quantos dias faltam
FALTAM = {
    "path": "/quantos-dias-faltam/", "short": "Quantos dias faltam", "tool": True, "group": "cal",
    "card": "Contagem regressiva em dias corridos e úteis até qualquer data ou feriado.",
    "title": "Quantos Dias Faltam? Contagem Regressiva para Qualquer Data",
    "desc": "Descubra quantos dias faltam para o Natal, o Ano Novo, o próximo feriado ou qualquer data: contagem regressiva em dias corridos, dias úteis e semanas.",
    "h1": "Quantos dias faltam?",
    "lead": "Escolha uma data ou um evento e veja na hora quantos dias faltam — em dias corridos, dias úteis e semanas. A contagem parte de hoje.",
    "sources": ["l662"],
    "body": """
<div class="calc">
<h2>Contagem regressiva</h2>
<div class="grid"><div><label for="ev">Evento</label><select id="ev"><option value="custom">Escolher uma data</option><option value="natal">Natal</option><option value="ano">Ano Novo</option><option value="feriado">Próximo feriado nacional</option><option value="carnaval">Carnaval</option><option value="ferias">Fim do ano letivo (20/12)</option></select></div><div><label for="dt">Data</label><input type="date" id="dt"></div></div>
<div class="result" id="res" aria-live="polite"><div class="big" id="t">–</div><div class="sub" id="td"></div><dl><dt>Dias úteis (seg. a sex.)</dt><dd id="du">–</dd><dt>Semanas</dt><dd id="sm">–</dd><dt>Fins de semana até lá</dt><dd id="fs">–</dd></dl></div>
</div>
<h2>Datas mais procuradas</h2>
<ul id="lista"></ul>
<h2>Como a contagem é feita</h2>
<p>A calculadora conta os dias a partir de hoje, sem incluir o dia de hoje, até a data escolhida. Os dias úteis descontam sábados, domingos e feriados nacionais. Para contar entre duas datas quaisquer, use a <a href="/calculadora-de-datas/">calculadora de datas</a> ou a <a href="/dias-uteis/">calculadora de dias úteis</a>.</p>
""",
    "faq": [
        ("Quantos dias faltam para o Natal?", "A contagem muda todos os dias. Selecione “Natal” na calculadora para ver quantos dias corridos e úteis faltam a partir de hoje."),
        ("Quantos dias faltam para o Ano Novo?", "Selecione “Ano Novo” na calculadora: ela mostra os dias até 1º de janeiro do próximo ano."),
        ("Qual é o próximo feriado nacional?", "Escolha “Próximo feriado nacional” e a calculadora mostra qual é o feriado e quantos dias faltam."),
        ("A contagem inclui o dia de hoje?", "Não. A contagem começa amanhã e inclui a data final."),
    ],
    "js": r"""
(function(){var T=new Date();T.setHours(12,0,0,0);var Y=T.getFullYear();
function nextHoliday(){for(var y=Y;y<=Y+1;y++){var F=feriados(y);var ks=Object.keys(F).sort();for(var i=0;i<ks.length;i++){var d=new Date(ks[i]+'T12:00:00');if(d>T)return [d,F[ks[i]]]}}}
function target(v){if(v==='natal'){var d=new Date(Y,11,25,12);if(d<=T)d=new Date(Y+1,11,25,12);return [d,'Natal']}if(v==='ano')return [new Date(Y+1,0,1,12),'Ano Novo'];if(v==='feriado')return nextHoliday();
if(v==='carnaval'){var e=easter(Y),c=new Date(e);c.setDate(c.getDate()-47);c.setHours(12);if(c<=T){e=easter(Y+1);c=new Date(e);c.setDate(c.getDate()-47);c.setHours(12)}return [c,'Carnaval']}if(v==='ferias'){var f=new Date(Y,11,20,12);if(f<=T)f=new Date(Y+1,11,20,12);return [f,'20 de dezembro']}return null}
function count(D){var n=Math.round((D-T)/864e5),du=0,fs=0,cur=new Date(T),cache={};for(var i=0;i<n;i++){cur.setDate(cur.getDate()+1);var y=cur.getFullYear();if(!cache[y])cache[y]=feriados(y);var w=cur.getDay();if(w===0||w===6)fs++;else if(!cache[y][isoD(cur)])du++}return [n,du,fs]}
function c(){var v=document.getElementById('ev').value,D,name;if(v==='custom'){var x=document.getElementById('dt').value;if(!x)return;D=new Date(x+'T12:00:00');name=D.toLocaleDateString('pt-BR')}else{var r=target(v);D=r[0];name=r[1];document.getElementById('dt').value=isoD(D)}
var k=count(D);document.getElementById('t').textContent=(k[0]<0?'Já passou: ':'Faltam ')+Math.abs(k[0]).toLocaleString('pt-BR')+' dias';document.getElementById('td').textContent='até '+name+' – '+D.toLocaleDateString('pt-BR',{weekday:'long',day:'2-digit',month:'long',year:'numeric'});
document.getElementById('du').textContent=k[0]>0?k[1]:'–';document.getElementById('sm').textContent=k[0]>0?Math.floor(k[0]/7)+' semanas e '+(k[0]%7)+' dia(s)':'–';document.getElementById('fs').textContent=k[0]>0?Math.round(k[2]/2)+' (aprox.)':'–'}
document.getElementById('ev').addEventListener('input',c);document.getElementById('dt').addEventListener('input',function(){document.getElementById('ev').value='custom';c()});
document.getElementById('ev').value='natal';c();
var L=[['natal','Natal'],['ano','Ano Novo'],['feriado','próximo feriado'],['carnaval','Carnaval']],ul=document.getElementById('lista');L.forEach(function(x){var r=target(x[0]),k=count(r[0]);var li=document.createElement('li');li.innerHTML='Quantos dias faltam para o <strong>'+x[1]+(x[0]==='feriado'?' ('+r[1]+')':'')+'</strong>: '+k[0]+' dias ('+r[0].toLocaleDateString('pt-BR')+')';ul.appendChild(li)})})();"""
}

# ============================================================ Banco de horas
BANCO = {
    "path": "/banco-de-horas/", "short": "Banco de horas", "tool": True, "group": "jor",
    "card": "Saldo do banco de horas com créditos e débitos, prazos da CLT e valor estimado.",
    "title": "Banco de Horas: Como Funciona e Calculadora de Saldo",
    "desc": "Entenda como funciona o banco de horas na CLT (prazos de 6 meses e 1 ano) e calcule o saldo somando horas extras e descontando folgas e atrasos.",
    "h1": "Banco de horas – como funciona e calculadora de saldo",
    "lead": "Lance as horas a mais (crédito) e as folgas ou saídas antecipadas (débito) para ver o saldo do seu banco de horas. Abaixo, as regras da CLT sobre prazos de compensação e pagamento.",
    "sources": ["clt"],
    "body": """
<div class="calc">
<h2>Calcular saldo do banco de horas</h2>
<div class="grid"><div><label for="sh">Saldo anterior – horas</label><input type="number" id="sh" value="0"></div><div><label for="sm">minutos</label><input type="number" id="sm" value="0" min="0"></div><div><label for="vh">Valor da hora normal (R$, opcional)</label><input type="number" id="vh" value="13.64" step="0.01" min="0" inputmode="decimal"></div></div>
<h3>Lançamentos</h3>
<div class="rows" id="rows"></div>
<div class="actions"><button class="btn ghost sm" id="add" type="button">+ Adicionar lançamento</button><button class="btn ghost" id="reset" type="button">Limpar</button></div>
<div class="result" id="res" aria-live="polite"><div class="big" id="tot">0h00</div><div class="sub" id="totd"></div><dl><dt>Total de créditos</dt><dd id="cr">–</dd><dt>Total de débitos</dt><dd id="db">–</dd><dt>Se o saldo positivo for pago como hora extra (50%)</dt><dd id="pg">–</dd></dl>
<div class="actions"><button class="btn sm ghost" type="button" onclick="copyRes('res',this)">Copiar resultado</button></div></div>
</div>
<h2>Como funciona o banco de horas</h2>
<p>No banco de horas, as horas trabalhadas além da jornada não são pagas como extra: viram um crédito que o empregado compensa depois com folgas ou saídas antecipadas. A CLT (art. 59) define três modalidades:</p>
<div class="tw"><table class="t"><thead><tr><th>Modalidade</th><th>Como é feito</th><th>Prazo para compensar</th></tr></thead><tbody>
<tr><td>Acordo coletivo ou convenção</td><td>Negociado com o sindicato</td><td>Até 12 meses (art. 59, §2º)</td></tr>
<tr><td>Acordo individual escrito</td><td>Entre empresa e empregado</td><td>Até 6 meses (art. 59, §5º)</td></tr>
<tr><td>Compensação no mesmo mês</td><td>Acordo individual, inclusive tácito</td><td>Dentro do mesmo mês (art. 59, §6º)</td></tr>
</tbody></table></div>
<h2>O que acontece com o saldo</h2>
<ul>
<li><strong>Saldo positivo não compensado no prazo</strong> deve ser pago como hora extra, com adicional mínimo de 50%. O mesmo vale na rescisão do contrato (art. 59, §3º).</li>
<li><strong>Limite diário:</strong> mesmo com banco de horas, a jornada não pode passar de 10 horas por dia.</li>
<li><strong>Saldo negativo:</strong> a forma de desconto deve estar prevista no acordo; na falta de previsão, a compensação do saldo negativo é discutível judicialmente.</li>
</ul>
<p>Para somar o cartão de ponto da semana, use a <a href="/horas-trabalhadas/">calculadora de horas trabalhadas</a>; para valorar o saldo, a <a href="/hora-extra/">calculadora de hora extra</a>.</p>
""",
    "faq": [
        ("Como funciona o banco de horas?", "As horas trabalhadas além da jornada viram crédito para ser compensado com folgas. Se não forem compensadas no prazo (6 meses no acordo individual, 12 meses no coletivo), devem ser pagas como hora extra."),
        ("Banco de horas vence em quanto tempo?", "No acordo individual escrito, em até 6 meses; por acordo ou convenção coletiva, em até 1 ano; no acordo para o mesmo mês, dentro do próprio mês (CLT, art. 59)."),
        ("O que acontece com o banco de horas na demissão?", "O saldo positivo não compensado deve ser pago como hora extra, calculado sobre o valor da remuneração na data da rescisão (CLT, art. 59, §3º)."),
        ("Banco de horas precisa de acordo por escrito?", "O banco de até 6 meses exige acordo individual escrito. O de até 1 ano exige acordo ou convenção coletiva. A compensação no mesmo mês pode ser por acordo tácito."),
    ],
    "js": r"""
(function(){var R=document.getElementById('rows');
function row(t,h,m){var d=document.createElement('div');d.className='row';d.innerHTML='<div><label>Tipo e horas</label><div style="display:flex;gap:6px"><select aria-label="Crédito ou débito" style="width:120px"><option value="1">Crédito +</option><option value="-1"'+(t<0?' selected':'')+'>Débito –</option></select><input type="number" min="0" placeholder="h" value="'+(h||'')+'" aria-label="Horas"></div></div><div><label>Minutos</label><input type="number" min="0" placeholder="min" value="'+(m||'')+'" aria-label="Minutos"></div><button class="btn ghost sm" type="button" aria-label="Remover lançamento" style="margin-bottom:4px">×</button>';
d.querySelector('button').onclick=function(){d.remove();c()};d.querySelectorAll('input,select').forEach(function(x){x.addEventListener('input',c)});R.appendChild(d)}
function c(){var base=val('sh')*60+(val('sh')<0?-1:1)*val('sm'),cr=0,db=0;R.querySelectorAll('.row').forEach(function(r){var s=parseInt(r.querySelector('select').value),i=r.querySelectorAll('input'),m=(parseFloat(i[0].value)||0)*60+(parseFloat(i[1].value)||0);if(s>0)cr+=m;else db+=m});
var t=base+cr-db,vh=val('vh');document.getElementById('tot').textContent=(t>0?'+':'')+fmtH(t);document.getElementById('totd').textContent=t>0?'saldo positivo (crédito do empregado)':t<0?'saldo negativo (horas devidas à empresa)':'saldo zerado';
document.getElementById('cr').textContent='+'+fmtH(cr);document.getElementById('db').textContent='−'+fmtH(db);document.getElementById('pg').textContent=(t>0&&vh)?brl(vh*1.5*t/60):'–'}
document.getElementById('add').onclick=function(){row(1)};document.getElementById('reset').onclick=function(){R.innerHTML='';row(1);row(-1);c()};['sh','sm','vh'].forEach(function(i){document.getElementById(i).addEventListener('input',c)});
row(1,2,30);row(1,1,15);row(-1,4,0);c()})();"""
}

# ============================================================ Horas em decimal
dec_rows = "".join(
    f'<tr><td>{m} min</td><td class="num">{str(round(m/60,2)).replace(".",",")}</td><td>{m+30} min</td><td class="num">{str(round((m+30)/60,2)).replace(".",",")}</td></tr>'
    for m in range(0, 30))
DEC = {
    "path": "/horas-em-decimal/", "short": "Horas em decimal", "tool": True, "group": "jor",
    "card": "Converta horas e minutos em decimal e vice-versa, com tabela completa.",
    "title": "Converter Horas em Decimal – Tabela e Calculadora",
    "desc": "Converta horas e minutos em horas decimais (7h45 = 7,75) e decimal em horas e minutos. Tabela de conversão de minutos para a folha de ponto e o cálculo de salário.",
    "h1": "Converter horas em decimal",
    "lead": "7 horas e 45 minutos correspondem a 7,75 horas decimais. Use o conversor nos dois sentidos e consulte a tabela de minutos para preencher folhas de ponto e planilhas.",
    "sources": [],
    "body": f"""
<div class="calc">
<h2>Horas e minutos → decimal</h2>
<div class="grid"><div><label for="h">Horas</label><input type="number" id="h" value="7" min="0"></div><div><label for="m">Minutos</label><input type="number" id="m" value="45" min="0"></div></div>
<div class="result" id="res" aria-live="polite"><div class="big" id="t">7,75</div><div class="sub" id="td">horas decimais · 465 minutos</div></div>
</div>
<div class="calc">
<h2>Decimal → horas e minutos</h2>
<div class="grid"><div><label for="d">Horas decimais</label><input type="number" id="d" value="8.3" step="0.01" min="0"></div></div>
<div class="result" id="res2" aria-live="polite"><div class="big" id="t2">8h18</div><div class="sub" id="t2d">8 horas e 18 minutos</div></div>
</div>
<h2>Tabela de minutos em horas decimais</h2>
<div class="tw"><table class="t"><thead><tr><th>Minutos</th><th style="text-align:right">Decimal</th><th>Minutos</th><th style="text-align:right">Decimal</th></tr></thead><tbody>{dec_rows}</tbody></table></div>
<h2>Fórmula</h2>
<ul><li><strong>Minutos → decimal:</strong> minutos ÷ 60. Ex.: 45 ÷ 60 = 0,75.</li><li><strong>Decimal → minutos:</strong> parte decimal × 60. Ex.: 0,3 × 60 = 18 minutos.</li></ul>
<p>O formato decimal permite multiplicar as horas direto pelo valor da hora: 7,75 h × R$ 13,64 = R$ 105,71. Para somar várias marcações, use a <a href="/">calculadora de horas</a>.</p>
""",
    "faq": [
        ("Quanto é 7h30 em decimal?", "7,5 horas, porque 30 minutos ÷ 60 = 0,5."),
        ("Como transformar 8,5 horas em horas e minutos?", "8 horas e 30 minutos: 0,5 × 60 = 30."),
        ("Quanto é 20 minutos em decimal?", "0,33 hora (20 ÷ 60 = 0,333...)."),
        ("Por que usar horas decimais?", "Porque o valor decimal pode ser multiplicado diretamente pelo valor da hora no cálculo do salário e das horas extras."),
    ],
    "js": r"""
(function(){function c1(){var t=val('h')*60+val('m');document.getElementById('t').textContent=fmtDec(t);document.getElementById('td').textContent='horas decimais · '+Math.round(t)+' minutos'}
function c2(){var t=Math.round(val('d')*60);document.getElementById('t2').textContent=fmtH(t);document.getElementById('t2d').textContent=Math.floor(t/60)+' horas e '+(t%60)+' minutos'}
['h','m'].forEach(function(i){document.getElementById(i).addEventListener('input',c1)});document.getElementById('d').addEventListener('input',c2);c1();c2()})();"""
}

TOOLS = [HOME, TRAB, HE, NOT, DSR, UTEIS, DATAS, FALTAM, BANCO, DEC]

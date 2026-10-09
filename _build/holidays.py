# -*- coding: utf-8 -*-
"""Brazilian national holidays (server-side, used to pre-render static tables). Mirrors feriados() in template JS."""
import datetime as dt

MESES = ["janeiro", "fevereiro", "março", "abril", "maio", "junho", "julho", "agosto", "setembro", "outubro", "novembro", "dezembro"]


def easter(y):
    a, b, c = y % 19, y // 100, y % 100
    d, e = b // 4, b % 4
    f = (b + 8) // 25
    g = (b - f + 1) // 3
    h = (19 * a + b - d - g + 15) % 30
    i, k = c // 4, c % 4
    l = (32 + 2 * e + 2 * i - h - k) % 7
    m = (a + 11 * h + 22 * l) // 451
    mo = (h + l - 7 * m + 114) // 31
    da = ((h + l - 7 * m + 114) % 31) + 1
    return dt.date(y, mo, da)


def feriados(y, carnaval=False, corpus=False):
    fixed = [(1, 1, "Confraternização Universal"), (4, 21, "Tiradentes"), (5, 1, "Dia do Trabalho"),
             (9, 7, "Independência do Brasil"), (10, 12, "Nossa Senhora Aparecida"), (11, 2, "Finados"),
             (11, 15, "Proclamação da República"), (12, 25, "Natal")]
    if y >= 2024:
        fixed.append((11, 20, "Dia Nacional de Zumbi e da Consciência Negra"))
    out = {dt.date(y, m, d): n for m, d, n in fixed}
    e = easter(y)
    out[e - dt.timedelta(days=2)] = "Paixão de Cristo (Sexta-feira Santa)"
    if carnaval:
        out[e - dt.timedelta(days=48)] = "Carnaval (ponto facultativo)"
        out[e - dt.timedelta(days=47)] = "Carnaval (ponto facultativo)"
    if corpus:
        out[e + dt.timedelta(days=60)] = "Corpus Christi (ponto facultativo)"
    return dict(sorted(out.items()))


def dias_uteis_mes(y, m, sabado=False):
    hol = feriados(y)
    d = dt.date(y, m, 1)
    n = 0
    while d.month == m:
        if d.weekday() < (6 if sabado else 5) and d not in hol:
            n += 1
        d += dt.timedelta(days=1)
    return n


DIAS_SEMANA = ["segunda-feira", "terça-feira", "quarta-feira", "quinta-feira", "sexta-feira", "sábado", "domingo"]


def fmt(d):
    return f"{d.day:02d}/{d.month:02d}/{d.year} ({DIAS_SEMANA[d.weekday()]})"

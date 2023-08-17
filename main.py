import requests
import math
from bs4 import BeautifulSoup

def scraping_in(url): 
    response = requests.get(url)
    html_content = response.text

    return BeautifulSoup(html_content, 'html.parser')

def tabla_matriz(url, nombre_table):
    tabla = scraping_in(url).find(class_=nombre_table)
    elementos_tabla = tabla.find_all('tr')
    td_m = []

    for el in elementos_tabla[1:]:
        td_arr = []

        for td in el.find_all('td'): 
            td_arr.append(td.get_text())
        
        if td_arr[0] != 'A Conf.':
            td_m.append(td_arr)
    
    return td_m

def ultimos_resultados(equipo):
    ultimos_partidos = tabla_matriz(f'https://www.promiedos.com.ar/club={equipo}', 'fixclub')

    ga = 0 
    gc = 0 

    pg = 0
    pp = 0
    pe = 0

    resultados_ultimos_partidos = [elem[4] for elem in ultimos_partidos]

    for res in resultados_ultimos_partidos: 

        if res != '-':
            rival = int(res.split(" - ")[1])
            tm = int(res.split(" - ")[0])
        
            ga += tm 
            gc += rival

            if rival > tm: 
                pp += 1
            elif rival < tm: 
                pg += 1
            else: 
                pe += 1

    return ( pg, pp, pe, ga, gc )

def ultimos_resultados_detallado(equipo):
    ultimos_partidos = tabla_matriz(f'https://www.promiedos.com.ar/club={equipo}', 'fixclub')

    # goles a favor/contra de local
    gf_local, gc_local = 0, 0
    # goles a fav/cont visitante
    gf_visitante, gc_visitante = 0, 0
    # p ganados local/visitante
    pgl, pgv = 0, 0
    # p perdidos local/visitante
    ppl, ppv = 0, 0
    # p emp local/visitante
    pel, pev = 0, 0

    resultados_ultimos_partidos = [(elem[2], elem[4]) for elem in ultimos_partidos if elem[4] != '-']

    for data in resultados_ultimos_partidos: 
        res = data[1].replace(' ', '').split('-')
        tm = int(res[0])
        riv = int(res[1])

        if data[0] == 'L': 
            if tm > riv: # equipo ganó 
                pgl += 1 
                gf_local += tm
                gc_local += riv
            elif tm < riv: # equipo perdió 
                ppl += 1 
                gf_local += tm
                gc_local += riv
            else: 
                pel += 1 
                gf_local += tm
                gc_local += riv
        else:
            if tm > riv: # equipo ganó 
                pgv += 1 
                gf_visitante += tm
                gc_visitante += riv
            elif tm < riv: # equipo perdió 
                ppv += 1 
                gf_visitante += tm
                gc_visitante += riv
            else: 
                pev += 1 
                gf_visitante += tm
                gc_visitante += riv

    total_pl = (pgl + ppl + pel) 
    total_pv = (pgv + ppv + pev)

    return ( 
        gf_local / total_pl, 
        gf_visitante / total_pv, 
        gc_local / total_pl, 
        gc_visitante / total_pv, 
        (pgl, pgv), 
        (ppl, ppv), 
        (pel, pev))

def get_fuerzas(equipo, gfl, gcl, gfv, gcv):
    f_ata_loc = equipo[0] / gfl
    f_def_loc = equipo[2] / gcl
    f_ata_vis = equipo[0] / gfv
    f_def_vis = equipo[2] / gcv

    return ( f_ata_loc, f_def_loc, f_ata_vis, f_def_vis )

def promedios_equipos(equipo_a, equipo_b): 

    prom_gf_local = (equipo_a[0] + equipo_b[0]) / 2
    prom_gc_local = (equipo_a[2] + equipo_b[2]) / 2
    prom_gf_vis = (equipo_a[1] + equipo_b[1]) / 2
    prom_gc_vis = (equipo_a[3] + equipo_b[3]) / 2

    fuerzas_equipo_a = get_fuerzas(equipo_a, prom_gf_local, prom_gc_local, prom_gf_vis, prom_gc_vis)
    fuerzas_equipo_b = get_fuerzas(equipo_b, prom_gf_local, prom_gc_local, prom_gf_vis, prom_gc_vis)

    media_goles_a = fuerzas_equipo_a[0] * fuerzas_equipo_b[3]
    media_goles_b = fuerzas_equipo_b[2] * fuerzas_equipo_a[1]

    return media_goles_a, media_goles_b



if __name__ == "__main__": 

    equipos = {
        "river": 18,
        "san lorenzo": 19,
        "talleres": 52, 
        "defensa y justicia": 29,
        "estudiantes": 8,
        "rosario central": 35,
        "lanus": 13,
        "belgrano": 26,
        "godoy cruz": 10,
        "argentinos": 3,
        "boca": 6,
        "sarmiento": 81,
        "newells": 14,
        "platense": 45,
        "tigre": 20,
        "barracas": 82,
        "gimnasia": 9,
        "instituto": 33,
        "central": 78,
        "colon": 7,
        "independiente": 12, 
        "huracan": 11,
        "atletico tucuman": 25,
        "racing club": 17,
        "velez": 21, 
        "banfield": 5,
        "arsenal": 4,
        "union": 39
    }

    print(promedios_equipos(
        ultimos_resultados_detallado(equipos["boca"]),
        ultimos_resultados_detallado(equipos["huracan"])
        ))
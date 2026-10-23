"""
TP3 - Crímenes en Chicago (2001 - presente)
Fuente: https://data.cityofchicago.org/resource/ijzp-q8t2  (API Socrata / SoQL)

El dataset completo tiene ~8.6 millones de filas. En vez de bajar todo crudo,
se le pide al servidor que agregue (GROUP BY) sobre TODOS los años y se bajan
solo las tablas resumen. Se guardan en data/ para no repetir las consultas.

Preguntas:
  1) ¿Hay estacionalidad en los crímenes?
  2) ¿Qué lugares de Chicago son más peligrosos?
  3) ¿Qué tipos de crímenes son los más frecuentes?

RESPUESTAS (8.648.866 registros, 2001-01-01 a 2026-09-26; figuras en figs/)

1) SÍ hay estacionalidad, y es muy consistente (figs 1a-1d).
   - Los crímenes suben en verano y bajan en invierno. Julio está ~12% por
     encima del promedio del año y febrero ~17% por debajo (julio supera a
     febrero en ~35%). En 22 de 25 años el pico cayó entre mayo y agosto.
   - Parte del mínimo de febrero se debe a que tiene menos días, pero diciembre
     y enero (31 días) también quedan ~6-9% por debajo: el frío pesa.
   - Excepción visible: 2020 (abril mínimo histórico por la cuarentena COVID).
   - También hay ciclo diario: mínimo a las 5 h, máximo a la noche y a las
     12 h. El pico de las 0 h está inflado porque cuando se desconoce la hora
     se registra 00:00; lo mismo pasa (en menor medida) con las 12:00. Los
     fines de semana tienen más actividad de madrugada.
   - Tendencia de largo plazo: los crímenes bajaron a menos de la mitad entre
     2001 y 2025 (fig 1a).

2) Lugares más peligrosos (figs 2a-2c):
   - Austin es por lejos la community area con más crímenes (~491 mil) y con
     más crímenes violentos (~167 mil). Le siguen, en violentos: South Shore,
     West Englewood, North Lawndale y Englewood (West Side y South Side).
   - Near North Side y Near West Side (centro/Loop) tienen muchos crímenes en
     total, pero sobre todo robos/hurtos; en violentos bajan en el ranking.
   - Las 10 áreas con más crímenes (de 77) concentran el 33% del total.
   - El mapa por beat muestra los focos en el West Side, el South Side y el
     centro; el norte (lakefront) y el extremo noroeste son mucho más tranquilos.
   - Por tipo de lugar: la mayoría ocurre en la calle (STREET), seguida de
     residencias, departamentos y veredas.
   - Ojo: son conteos absolutos y no están normalizados por población.

3) Tipos más frecuentes (figs 3a-3b):
   THEFT (21%), BATTERY (18%), CRIMINAL DAMAGE (11%), NARCOTICS (9%) y
   ASSAULT (7%), que juntos suman el 66% del total. NARCOTICS cayó muchísimo
   (de ~56 mil en 2005 a ~7 mil en 2025, con un salto fuerte en
   2015-2016), mientras que THEFT y BATTERY se mantienen arriba
   todo el período.
"""
import os
from io import StringIO

import matplotlib.pyplot as plt
import pandas as pd
import requests
import seaborn as sns

BASE = "https://data.cityofchicago.org/resource/ijzp-q8t2.csv"
AREAS = "https://data.cityofchicago.org/resource/igwz-8jzy.csv"
HERE = os.getcwd()  # en Colab no existe __file__
DATA = os.path.join(HERE, "data")
FIGS = os.path.join(HERE, "figs")
os.makedirs(DATA, exist_ok=True)
os.makedirs(FIGS, exist_ok=True)
sns.set_theme(style="whitegrid")

VIOLENTOS = ["HOMICIDE", "ROBBERY", "BATTERY", "ASSAULT", "CRIMINAL SEXUAL ASSAULT",
             "CRIM SEXUAL ASSAULT", "KIDNAPPING", "WEAPONS VIOLATION"]


def soql(nombre, url=BASE, **params):
    """Ejecuta una consulta SoQL y cachea el resultado en data/<nombre>.csv."""
    path = os.path.join(DATA, f"{nombre}.csv")
    if os.path.exists(path):
        return pd.read_csv(path)
    params = {f"${k}": v for k, v in params.items()}
    params.setdefault("$limit", 500000)
    print(f"Consultando {nombre} ...")
    r = requests.get(url, params=params, timeout=600)
    r.raise_for_status()
    df = pd.read_csv(StringIO(r.text))
    df.to_csv(path, index=False)
    return df


# --------------------------------------------------------------------------
# Descarga de agregados (todos los años)
# --------------------------------------------------------------------------
total = soql("total", select="count(*) AS n, min(date) AS desde, max(date) AS hasta")
print(total.to_string(index=False))

anio_mes = soql("anio_mes",
                select="year, date_extract_m(date) AS mes, count(*) AS n",
                group="year, date_extract_m(date)")
dow_hora = soql("dow_hora",
                select="date_extract_dow(date) AS dow, date_extract_hh(date) AS hora, count(*) AS n",
                group="date_extract_dow(date), date_extract_hh(date)")
tipo_anio = soql("tipo_anio",
                 select="primary_type, year, count(*) AS n",
                 group="primary_type, year")
area = soql("community_area",
            select="community_area, count(*) AS n",
            where="community_area IS NOT NULL",
            group="community_area")
lista_violentos = ", ".join(f"'{t}'" for t in VIOLENTOS)
area_viol = soql("community_area_violentos",
                 select="community_area, count(*) AS n",
                 where=f"community_area IS NOT NULL AND primary_type IN ({lista_violentos})",
                 group="community_area")
beat = soql("beat",
            select="beat, count(*) AS n, avg(latitude) AS lat, avg(longitude) AS lon",
            where="latitude IS NOT NULL AND latitude > 41",
            group="beat")
lugar = soql("location_description",
             select="location_description, count(*) AS n",
             group="location_description", order="n DESC", limit=30)
nombres = soql("areas_nombres", url=AREAS, select="area_numbe, community")

# Algunos tipos cambiaron de nombre a lo largo de los años
tipo_anio["primary_type"] = tipo_anio["primary_type"].replace({
    "CRIM SEXUAL ASSAULT": "CRIMINAL SEXUAL ASSAULT",
    "NON - CRIMINAL": "NON-CRIMINAL",
    "NON-CRIMINAL (SUBJECT SPECIFIED)": "NON-CRIMINAL",
})
ultimo_anio = int(anio_mes["year"].max())
completos = anio_mes[anio_mes["year"] < ultimo_anio]  # el año en curso está incompleto

# ==========================================================================
# 1) ESTACIONALIDAD
# ==========================================================================
MESES = ["Ene", "Feb", "Mar", "Abr", "May", "Jun", "Jul", "Ago", "Sep", "Oct", "Nov", "Dic"]
DIAS = ["Dom", "Lun", "Mar", "Mié", "Jue", "Vie", "Sáb"]

# Serie mensual completa
serie = anio_mes.assign(fecha=pd.to_datetime(dict(year=anio_mes.year, month=anio_mes.mes, day=1)))
serie = serie.sort_values("fecha")
fig, ax = plt.subplots(figsize=(14, 4))
ax.plot(serie.fecha, serie.n, lw=1)
ax.set(title="Crímenes por mes en Chicago (2001 - presente)", ylabel="Crímenes / mes")
fig.tight_layout(); fig.savefig(os.path.join(FIGS, "1a_serie_mensual.png"), dpi=120)
plt.show()

# Para separar la estacionalidad de la tendencia de largo plazo (los crímenes
# bajaron mucho desde 2001), cada mes se expresa como % del promedio de su año.
completos = completos.copy()
completos["rel"] = completos.n / completos.groupby("year").n.transform("mean") * 100
tabla = completos.pivot(index="year", columns="mes", values="rel")
tabla.columns = MESES

fig, axes = plt.subplots(1, 2, figsize=(15, 6), gridspec_kw={"width_ratios": [1, 1.4]})
sns.boxplot(data=completos, x="mes", y="rel", ax=axes[0], color="steelblue")
axes[0].axhline(100, color="k", ls="--", lw=1)
axes[0].set(xticks=range(12), xticklabels=MESES, xlabel="",
            ylabel="% del promedio mensual del año",
            title="Perfil estacional (cada punto = un año)")
sns.heatmap(tabla, cmap="RdBu_r", center=100, ax=axes[1], cbar_kws={"label": "% del promedio anual"})
axes[1].set(title="Mes vs año (relativo al promedio del año)", ylabel="")
fig.tight_layout(); fig.savefig(os.path.join(FIGS, "1b_estacionalidad_mes.png"), dpi=120)
plt.show()

# Día de la semana x hora
dh = dow_hora.pivot(index="dow", columns="hora", values="n")
dh.index = DIAS
fig, ax = plt.subplots(figsize=(14, 4))
sns.heatmap(dh / 1000, cmap="rocket_r", ax=ax, cbar_kws={"label": "miles de crímenes"})
ax.set(title="Crímenes por día de la semana y hora (todos los años)", xlabel="Hora", ylabel="")
fig.tight_layout(); fig.savefig(os.path.join(FIGS, "1c_dia_hora.png"), dpi=120)
plt.show()

# Estacionalidad por tipo (top 6): ¿todos los tipos tienen el mismo patrón?
top6 = tipo_anio.groupby("primary_type").n.sum().nlargest(6).index
tipo_mes = soql("tipo_mes",
                select="primary_type, date_extract_m(date) AS mes, count(*) AS n",
                where=f"year < {ultimo_anio}",
                group="primary_type, date_extract_m(date)")
tm = tipo_mes[tipo_mes.primary_type.isin(top6)].copy()
tm["rel"] = tm.n / tm.groupby("primary_type").n.transform("mean") * 100
fig, ax = plt.subplots(figsize=(10, 5))
sns.lineplot(data=tm, x="mes", y="rel", hue="primary_type", marker="o", ax=ax)
ax.axhline(100, color="k", ls="--", lw=1)
ax.set(xticks=range(1, 13), xticklabels=MESES, xlabel="", ylabel="% del promedio mensual",
       title="Estacionalidad por tipo de crimen")
fig.tight_layout(); fig.savefig(os.path.join(FIGS, "1d_estacionalidad_tipo.png"), dpi=120)
plt.show()

perfil = completos.groupby("mes").rel.mean()
print("\n=== 1) ESTACIONALIDAD ===")
print("Promedio de cada mes como % del promedio anual:")
print(perfil.round(1).set_axis(MESES).to_string())
print(f"Mes pico: {MESES[perfil.idxmax() - 1]} ({perfil.max():.0f}%), "
      f"mes mínimo: {MESES[perfil.idxmin() - 1]} ({perfil.min():.0f}%)")
print(f"Julio supera a Febrero en {(perfil[7] / perfil[2] - 1) * 100:.0f}% en promedio.")
print(f"Años en que el pico cayó entre mayo y agosto: "
      f"{(tabla.idxmax(axis=1).isin(MESES[4:8])).sum()} de {len(tabla)}")
hora_pico = dh.sum().idxmax()
print(f"Hora con más crímenes: {hora_pico} h, hora con menos: {dh.sum().idxmin()} h")

# ==========================================================================
# 2) LUGARES MÁS PELIGROSOS
# ==========================================================================
nombres["area_numbe"] = nombres.area_numbe.astype(int)
nombres = nombres.drop_duplicates("area_numbe").set_index("area_numbe").community.str.title()
for d in (area, area_viol):
    d.drop(d[d.community_area == 0].index, inplace=True)
    d["nombre"] = d.community_area.astype(int).map(nombres)

fig, axes = plt.subplots(1, 2, figsize=(15, 7))
for ax, d, titulo, color in [(axes[0], area, "Todos los crímenes", "steelblue"),
                             (axes[1], area_viol, "Crímenes violentos", "firebrick")]:
    t = d.nlargest(15, "n")
    sns.barplot(data=t, y="nombre", x=t.n / 1000, ax=ax, color=color)
    ax.set(title=f"{titulo}: top 15 community areas", xlabel="miles (2001 - presente)", ylabel="")
fig.tight_layout(); fig.savefig(os.path.join(FIGS, "2a_community_areas.png"), dpi=120)
plt.show()

# "Mapa": cada punto es un beat policial (~270), ubicado en el promedio de sus coordenadas
fig, ax = plt.subplots(figsize=(8, 10))
sc = ax.scatter(beat.lon, beat.lat, c=beat.n / 1000, s=beat.n / beat.n.max() * 250,
                cmap="inferno_r", alpha=0.85, edgecolor="k", lw=0.3)
plt.colorbar(sc, ax=ax, label="miles de crímenes")
for _, r in beat.nlargest(8, "n").iterrows():
    ax.annotate(f"beat {int(r.beat)}", (r.lon, r.lat), fontsize=8, xytext=(5, 5),
                textcoords="offset points")
ax.set(title="Crímenes por beat policial (2001 - presente)", xlabel="Longitud", ylabel="Latitud",
       aspect=1 / 0.745)  # corrige la escala lon/lat a 42° N
fig.tight_layout(); fig.savefig(os.path.join(FIGS, "2b_mapa_beats.png"), dpi=120)
plt.show()

# Tipo de lugar
fig, ax = plt.subplots(figsize=(9, 7))
t = lugar.dropna().head(15)
sns.barplot(data=t, y="location_description", x=t.n / 1000, ax=ax, color="darkorange")
ax.set(title="Tipo de lugar donde ocurren los crímenes (top 15)", xlabel="miles", ylabel="")
fig.tight_layout(); fig.savefig(os.path.join(FIGS, "2c_tipo_lugar.png"), dpi=120)
plt.show()

print("\n=== 2) LUGARES MÁS PELIGROSOS ===")
print("Top 5 community areas (todos los crímenes):")
print(area.nlargest(5, "n")[["nombre", "n"]].to_string(index=False))
print("Top 5 community areas (crímenes violentos):")
print(area_viol.nlargest(5, "n")[["nombre", "n"]].to_string(index=False))
top10 = area.nlargest(10, "n").n.sum() / area.n.sum() * 100
print(f"Las 10 áreas con más crímenes (de 77) concentran el {top10:.0f}% del total.")
print("Tipos de lugar más frecuentes:")
print(lugar.dropna().head(5).to_string(index=False))

# ==========================================================================
# 3) TIPOS DE CRÍMENES MÁS FRECUENTES
# ==========================================================================
por_tipo = tipo_anio.groupby("primary_type").n.sum().sort_values(ascending=False)

fig, ax = plt.subplots(figsize=(9, 7))
t = por_tipo.head(15)
sns.barplot(y=t.index, x=t.values / 1e6, ax=ax, color="seagreen")
for i, v in enumerate(t.values):
    ax.text(v / 1e6, i, f" {v / por_tipo.sum() * 100:.1f}%", va="center", fontsize=8)
ax.set(title="Tipos de crímenes más frecuentes (2001 - presente)", xlabel="millones", ylabel="")
fig.tight_layout(); fig.savefig(os.path.join(FIGS, "3a_tipos.png"), dpi=120)
plt.show()

# Evolución anual de los principales tipos
top8 = por_tipo.head(8).index
ev = tipo_anio[tipo_anio.primary_type.isin(top8) & (tipo_anio.year < ultimo_anio)]
fig, ax = plt.subplots(figsize=(12, 6))
sns.lineplot(data=ev, x="year", y="n", hue="primary_type", marker="o", ax=ax)
ax.set(title="Evolución anual de los 8 tipos más frecuentes", xlabel="Año", ylabel="Crímenes / año")
fig.tight_layout(); fig.savefig(os.path.join(FIGS, "3b_tipos_evolucion.png"), dpi=120)
plt.show()

print("\n=== 3) TIPOS MÁS FRECUENTES ===")
print((por_tipo.head(10).to_frame("n")
       .assign(pct=lambda d: (d.n / por_tipo.sum() * 100).round(1))).to_string())
print(f"Los 5 tipos más frecuentes suman el {por_tipo.head(5).sum() / por_tipo.sum() * 100:.0f}% del total.")
print(f"\nFiguras guardadas en {FIGS}")

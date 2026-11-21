# IID

Trabajos prácticos y trabajo final de la materia IID.

## Trabajo final (ClinVar)

Variantes germinales de ClinVar (`variant_summary` 2026-10, GRCh38): extracción, limpieza, normalización hasta 4NF, base OLTP en SQLite, data warehouse en copo de nieve y visualización interactiva en Streamlit.

**Archivos que forman parte del trabajo final:**

| Archivo | Contenido |
|---|---|
| `notebooks/TrabajoFinal_IID.ipynb` | Notebook completo: ETL, normalización, OLTP, DW y código de la app Streamlit |
| `src/diagrams/snowflake_clinvar_dw.png` | Diagrama del DW en copo de nieve |
| `src/diagrams/visualizacion_streamlit_clinvar.pdf` | Gráficos de la app Streamlit (8 páginas) |
| `requirements.txt` | Dependencias |

Al ejecutar el notebook se generan estos archivos, que no se suben al repositorio (`.gitignore`):

- `data/processed/clinvar_oltp.db`: base transaccional (OLTP)
- `data/processed/clinvar_dw.db`: data warehouse
- `notebooks/app_clinvar.py`: app Streamlit, escrita por las celdas `%%writefile` (`streamlit run app_clinvar.py`)

## Resto del repositorio (trabajos anteriores)

```
README.md, LICENSE, .gitignore
data/raw/data_chicago/        CSV agregados de crímenes de Chicago (actividad complementaria del TP3)
notebooks/
  PrimeraClase.ipynb          Primera clase
  tp1_ID.ipynb                TP1: ingesta de GDELT 2.0
  TP3.ipynb                   TP3: análisis multivariante de GDELT
  TP4_IID.ipynb               TP4
  utilities_tp4/              Notebooks de referencia para el TP4 (outliers, espacio latente)
  Demo ETL Taxi.ipynb         Demo de ingesta a gran escala (material de clase)
src/
  diagrama_er_oltp.xml.md     TP2: diagrama ER de la OLTP de GDELT (draw.io)
  diagrams/
    tp2.*, tp2_starscheme.*   TP2: diagramas ER y esquema estrella (draw.io, PNG, HTML)
    starscheme.png            TP2: esquema estrella
    1a_…3b_*.png              Gráficos de crímenes de Chicago (actividad complementaria del TP3)
  scripts/
    chicago_crimes*.py        Scripts de la actividad de Chicago (local y Colab)
```

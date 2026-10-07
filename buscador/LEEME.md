# Buscador de Recetas

Abre `Buscador_Recetas.html` (en la carpeta principal) con doble clic. No necesita internet ni instalar nada.

1. Escribe el nombre del plato, de la receta base o el código.
2. Usa los filtros: Carta (fotos), Postres, Recetas venta, Recetas base o una categoría.
3. Haz clic en una receta para verla con sus sub-recetas desplegables.
4. Agrégala con **+** y luego **Descargar Excel**, o usa **Excel solo de esta**.

El Excel trae las hojas **Resumen**, **Recetas** (las elegidas, con insumos) y **Recetas Base**
(todas las sub-recetas que necesitan, en cualquier nivel, con la columna "Usada en").

## Actualizar con nuevos reportes de Inforest

```
pip install xlrd openpyxl
python buscador/actualizar_buscador.py recetas_base_2026.xls recetas_venta_2026.xls
```

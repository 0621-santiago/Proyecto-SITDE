"""Lectura de la plantilla Excel con Pandas (SITDE-26).

El parser solo revisa la ESTRUCTURA del archivo (que existan las hojas y
las columnas) y convierte cada fila en un diccionario. La revisión de
tipos y duplicados fila por fila la hace el módulo de validaciones
(SITDE-27), y la carga a PostgreSQL se hace después con bulk_create.
"""
import unicodedata
from datetime import datetime
from pathlib import Path

import pandas as pd

from .plantilla import HOJAS


class ErrorPlantilla(Exception):
    """El archivo no tiene la estructura de la plantilla SITDE."""

    def __init__(self, errores):
        self.errores = errores
        super().__init__('; '.join(errores))


def normalizar_columna(nombre):
    """'Fecha Vencimiento ' -> 'fecha_vencimiento' (sin tildes ni espacios)."""
    texto = unicodedata.normalize('NFKD', str(nombre)).encode('ascii', 'ignore').decode()
    return '_'.join(texto.strip().lower().replace('%', 'pct').split())


def _limpiar_valor(valor):
    if valor is None or (not isinstance(valor, str) and pd.isna(valor)):
        return None
    if isinstance(valor, pd.Timestamp):
        return valor.date()
    if isinstance(valor, datetime):
        return valor.date()
    if isinstance(valor, str):
        valor = valor.strip()
        return valor or None
    if hasattr(valor, 'item'):  # tipos numéricos de numpy
        return valor.item()
    return valor


def leer_plantilla(ruta):
    """Lee la plantilla y devuelve {'Hoja': [ {columna: valor, 'fila': n}, ... ]}.

    `fila` es el número de fila en Excel, para poder decirle al usuario
    exactamente dónde está un error. Las filas vacías se ignoran.
    Lanza ErrorPlantilla si faltan hojas o columnas.
    """
    ruta = Path(ruta)
    if not ruta.exists():
        raise ErrorPlantilla([f'No se encontró el archivo {ruta.name}.'])
    if ruta.suffix.lower() != '.xlsx':
        raise ErrorPlantilla([f'El archivo {ruta.name} no es un Excel .xlsx.'])

    try:
        hojas_excel = pd.read_excel(ruta, sheet_name=None, dtype=object)
    except Exception as exc:  # archivo dañado o protegido
        raise ErrorPlantilla([f'No se pudo leer el archivo: {exc}']) from exc

    errores = []
    resultado = {}
    for nombre_hoja, columnas_esperadas in HOJAS.items():
        if nombre_hoja not in hojas_excel:
            errores.append(f'Falta la hoja "{nombre_hoja}".')
            continue

        tabla = hojas_excel[nombre_hoja]
        tabla.columns = [normalizar_columna(c) for c in tabla.columns]
        faltantes = [c for c in columnas_esperadas if c not in tabla.columns]
        if faltantes:
            errores.append(f'En la hoja "{nombre_hoja}" faltan las columnas: {", ".join(faltantes)}.')
            continue

        registros = []
        for indice, fila in tabla[columnas_esperadas].iterrows():
            registro = {col: _limpiar_valor(fila[col]) for col in columnas_esperadas}
            if all(valor is None for valor in registro.values()):
                continue
            registro['fila'] = indice + 2  # +1 por el encabezado, +1 porque Excel cuenta desde 1
            registros.append(registro)
        resultado[nombre_hoja] = registros

    if errores:
        raise ErrorPlantilla(errores)
    return resultado

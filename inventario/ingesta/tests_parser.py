import tempfile
from datetime import date
from pathlib import Path

from django.test import SimpleTestCase
from openpyxl import Workbook

from .parser import ErrorPlantilla, leer_plantilla, normalizar_columna
from .plantilla import HOJAS, crear_plantilla


class ParserTests(SimpleTestCase):
    """Pruebas del parser de plantillas Excel (SITDE-26)."""

    def setUp(self):
        self.carpeta = tempfile.TemporaryDirectory()
        self.dir = Path(self.carpeta.name)

    def tearDown(self):
        self.carpeta.cleanup()

    def test_lee_la_plantilla_de_ejemplo(self):
        ruta = crear_plantilla(self.dir / 'plantilla.xlsx')
        datos = leer_plantilla(ruta)
        self.assertEqual(set(datos), set(HOJAS))
        self.assertEqual(len(datos['Lotes']), 2)
        lote = datos['Lotes'][0]
        self.assertEqual(lote['codigo_lote'], 'L-001')
        self.assertIsInstance(lote['fecha_vencimiento'], date)
        self.assertEqual(lote['fila'], 2)

    def test_plantilla_vacia_no_trae_registros(self):
        ruta = crear_plantilla(self.dir / 'vacia.xlsx', con_ejemplos=False)
        datos = leer_plantilla(ruta)
        self.assertTrue(all(len(r) == 0 for r in datos.values()))

    def test_reporta_hojas_y_columnas_faltantes(self):
        libro = Workbook()
        hoja = libro.active
        hoja.title = 'Lotes'
        hoja.append(['codigo_lote', 'producto'])
        ruta = self.dir / 'incompleta.xlsx'
        libro.save(ruta)

        with self.assertRaises(ErrorPlantilla) as contexto:
            leer_plantilla(ruta)
        mensajes = ' '.join(contexto.exception.errores)
        self.assertIn('Falta la hoja "Recepciones"', mensajes)
        self.assertIn('fecha_vencimiento', mensajes)

    def test_rechaza_archivos_que_no_son_xlsx(self):
        ruta = self.dir / 'datos.csv'
        ruta.write_text('a,b')
        with self.assertRaises(ErrorPlantilla):
            leer_plantilla(ruta)

    def test_normaliza_encabezados(self):
        self.assertEqual(normalizar_columna(' Fecha Vencimiento '), 'fecha_vencimiento')
        self.assertEqual(normalizar_columna('Grasa %'), 'grasa_pct')
        self.assertEqual(normalizar_columna('Código Lote'), 'codigo_lote')

from django.core.management.base import BaseCommand, CommandError

from inventario.ingesta.parser import ErrorPlantilla, leer_plantilla


class Command(BaseCommand):
    help = 'Lee una plantilla Excel de SITDE y muestra cuántos registros trae cada hoja.'

    def add_arguments(self, parser):
        parser.add_argument('ruta', help='Ruta del archivo .xlsx')

    def handle(self, *args, **opciones):
        try:
            datos = leer_plantilla(opciones['ruta'])
        except ErrorPlantilla as error:
            for mensaje in error.errores:
                self.stderr.write(self.style.ERROR(f'✗ {mensaje}'))
            raise CommandError('La plantilla no tiene la estructura esperada.')

        for hoja, registros in datos.items():
            self.stdout.write(f'{hoja}: {len(registros)} registros leídos')

        # Pendiente: validar tipos y duplicados (SITDE-27) y cargar con
        # bulk_create a PostgreSQL cuando estén los modelos (SITDE-25).
        self.stdout.write(self.style.WARNING(
            'Lectura terminada. La validación y la carga a la base de datos '
            'se conectan cuando estén listos los modelos y las validaciones.'
        ))

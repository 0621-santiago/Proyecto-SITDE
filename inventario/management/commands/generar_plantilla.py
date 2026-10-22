from django.core.management.base import BaseCommand

from inventario.ingesta.plantilla import crear_plantilla


class Command(BaseCommand):
    help = 'Crea la plantilla Excel que llenan las PYMES para cargar sus datos.'

    def add_arguments(self, parser):
        parser.add_argument('ruta', nargs='?', default='plantilla_sitde.xlsx')
        parser.add_argument('--vacia', action='store_true', help='Sin filas de ejemplo.')

    def handle(self, *args, **opciones):
        ruta = crear_plantilla(opciones['ruta'], con_ejemplos=not opciones['vacia'])
        self.stdout.write(self.style.SUCCESS(f'Plantilla creada: {ruta}'))

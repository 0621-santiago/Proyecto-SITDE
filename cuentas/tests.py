from django.contrib.auth.models import Group, User
from django.test import TestCase
from django.urls import reverse

from .roles import ADMINISTRADOR, EMPRESARIO


class InicioSesionTests(TestCase):
    """Criterios de aceptación de la HU-01 (SITDE-4)."""

    def setUp(self):
        self.empresario = User.objects.create_user('empresario', password='ClaveSegura123')
        self.empresario.groups.add(Group.objects.get(name=EMPRESARIO))
        self.admin = User.objects.create_user('admin', password='ClaveSegura123')
        self.admin.groups.add(Group.objects.get(name=ADMINISTRADOR))

    def test_los_grupos_existen(self):
        self.assertTrue(Group.objects.filter(name=ADMINISTRADOR).exists())
        self.assertTrue(Group.objects.filter(name=EMPRESARIO).exists())

    def test_ac1_datos_validos_llevan_al_menu_principal(self):
        respuesta = self.client.post(
            reverse('iniciar_sesion'),
            {'username': 'empresario', 'password': 'ClaveSegura123'},
        )
        self.assertRedirects(respuesta, reverse('inicio'))

    def test_ac2_contrasena_incorrecta_muestra_error(self):
        respuesta = self.client.post(
            reverse('iniciar_sesion'),
            {'username': 'empresario', 'password': 'equivocada'},
        )
        self.assertEqual(respuesta.status_code, 200)
        self.assertContains(respuesta, 'Intente nuevamente')
        self.assertNotIn('_auth_user_id', self.client.session)

    def test_inicio_exige_sesion(self):
        respuesta = self.client.get(reverse('inicio'))
        self.assertRedirects(respuesta, reverse('iniciar_sesion') + '?next=/')

    def test_menu_cambia_segun_el_rol(self):
        self.client.force_login(self.empresario)
        respuesta = self.client.get(reverse('inicio'))
        self.assertContains(respuesta, 'Empresario')
        self.assertNotContains(respuesta, 'Usuarios y roles')

        self.client.force_login(self.admin)
        respuesta = self.client.get(reverse('inicio'))
        self.assertContains(respuesta, 'Administrador')
        self.assertContains(respuesta, 'Usuarios y roles')

    def test_cerrar_sesion(self):
        self.client.force_login(self.empresario)
        respuesta = self.client.post(reverse('cerrar_sesion'))
        self.assertRedirects(respuesta, reverse('iniciar_sesion'))
        self.assertNotIn('_auth_user_id', self.client.session)

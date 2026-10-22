# SITDE

Sistema inteligente de apoyo a la toma de decisiones empresariales para PYMES del sector lácteo de la provincia de Ubaté (Cundinamarca).

Proyecto de Ingeniería de Sistemas y Computación, Universidad de Cundinamarca, sede Ubaté.
Autores: Manuel Santiago Garzón Rodríguez y Nicolás Ramírez Montero.

## Tecnologías

- Python 3.12 o superior
- Django 6
- PostgreSQL
- Pandas y openpyxl para la carga de plantillas Excel

## Cómo correr el proyecto

1. Clonar el repositorio y entrar a la carpeta:

   ```
   git clone https://github.com/0621-santiago/Proyecto-SITDE.git
   cd Proyecto-SITDE
   ```

2. Crear y activar el entorno virtual:

   ```
   python -m venv venv
   venv\Scripts\activate          (Windows)
   source venv/bin/activate       (Linux o Mac)
   ```

3. Instalar las dependencias:

   ```
   pip install -r requirements.txt
   ```

4. Crear el archivo de configuración: copiar `.env.example` como `.env` y poner los datos de tu PostgreSQL. El `.env` no se sube a Git; cada integrante tiene el suyo.

5. Crear la base de datos `DB_SITDE` en PostgreSQL y aplicar las migraciones:

   ```
   python manage.py migrate
   ```

6. Crear un usuario administrador y arrancar el servidor:

   ```
   python manage.py createsuperuser
   python manage.py runserver
   ```

7. Abrir http://127.0.0.1:8000 e iniciar sesión.

## Pruebas

```
python manage.py test
```

## Organización del trabajo

- Tablero en Jira: proyecto SITDE.
- Ramas:
  - `main`: versión estable. Solo recibe cambios cuando todo está probado y funcionando.
  - `develop`: integración. Aquí se juntan los avances de los dos integrantes.
  - `dev-nicolas` y `dev-santiago`: ramas de trabajo de cada integrante. Salen de `develop` y vuelven a ella con un pull request.
- Flujo: `dev-<nombre>` → pull request a `develop` → revisión del compañero → `develop` → `main` cuando todo funciona.
- Antes de trabajar, actualizar la rama propia con lo último de `develop` (`git pull origin develop`).
- Cada mensaje de commit lleva la clave de Jira, por ejemplo: `SITDE-22: configuración con variables de entorno`.

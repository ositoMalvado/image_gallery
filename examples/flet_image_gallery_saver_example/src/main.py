import flet as ft
import requests
from io import BytesIO
from flet_image_gallery_saver import FletImageGallerySaver


def main(page: ft.Page):
    page.title = "Ejemplo de FletImageGallerySaver"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.padding = 20

    # Crear un control de texto para mostrar mensajes
    status_text = ft.Text("Estado: Listo para guardar imágenes", size=16)

    # Crear una instancia del control FletImageGallerySaver
    gallery_saver = FletImageGallerySaver()

    # Función para manejar cuando se completa el guardado
    def on_save_completed(e):
        status_text.value = f"✅ Guardado completado: {e.data}"
        status_text.color = ft.Colors.GREEN
        page.update()

    # Función para manejar cuando falla el guardado
    def on_save_failed(e):
        status_text.value = f"❌ Error al guardar: {e.data}"
        status_text.color = ft.Colors.RED
        page.update()

    # Asignar los manejadores de eventos
    gallery_saver.on_save_completed = on_save_completed
    gallery_saver.on_save_failed = on_save_failed

    # Función para guardar una imagen de ejemplo desde bytes
    def save_sample_image(e):
        status_text.value = "Guardando imagen de ejemplo..."
        status_text.color = ft.Colors.BLUE
        page.update()

        # Crear una imagen de ejemplo (un cuadrado rojo)
        try:
            from PIL import Image

            img = Image.new("RGB", (100, 100), color="red")
            buffer = BytesIO()
            img.save(buffer, format="JPEG")
            image_bytes = buffer.getvalue()

            # Guardar la imagen
            gallery_saver.save_image(
                image_bytes=image_bytes, quality=90, name="cuadrado_rojo.jpg"
            )
        except ImportError:
            status_text.value = "❌ Error: Se requiere la biblioteca PIL/Pillow"
            status_text.color = ft.Colors.RED
            page.update()

    # Función para guardar una imagen desde URL
    def save_image_from_url(e):
        status_text.value = "Descargando imagen desde URL..."
        status_text.color = ft.Colors.BLUE
        page.update()

        try:
            # URL de una imagen de ejemplo
            url = "https://picsum.photos/200"
            response = requests.get(url)
            if response.status_code == 200:
                # Guardar la imagen descargada
                gallery_saver.save_image(
                    image_bytes=response.content,
                    quality=85,
                    name="imagen_desde_url.jpg",
                )
            else:
                status_text.value = (
                    f"❌ Error al descargar la imagen: {response.status_code}"
                )
                status_text.color = ft.Colors.RED
                page.update()
        except Exception as ex:
            status_text.value = f"❌ Error: {str(ex)}"
            status_text.color = ft.Colors.RED
            page.update()

    # Crear botones para las acciones
    btn_save_sample = ft.ElevatedButton(
        "Guardar imagen de ejemplo",
        icon=ft.Icons.IMAGE,
        on_click=save_sample_image,
        style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10)),
    )

    btn_save_from_url = ft.ElevatedButton(
        "Guardar imagen desde URL",
        icon=ft.Icons.CLOUD_DOWNLOAD,
        on_click=save_image_from_url,
        style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10)),
    )

    # Crear la interfaz
    page.add(
        ft.Container(
            content=ft.Column(
                [
                    ft.Text(
                        "Ejemplo de FletImageGallerySaver",
                        size=24,
                        weight=ft.FontWeight.BOLD,
                    ),
                    ft.Text(
                        "Guarda imágenes en la galería del dispositivo",
                        size=16,
                        italic=True,
                    ),
                    ft.Divider(),
                    gallery_saver,  # El control está oculto pero funcional
                    ft.Container(height=20),  # Espaciador
                    ft.Row(
                        [btn_save_sample, btn_save_from_url],
                        alignment=ft.MainAxisAlignment.CENTER,
                        spacing=20,
                    ),
                    ft.Container(height=20),  # Espaciador
                    status_text,
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=10,
            ),
            width=400,
            padding=20,
            border_radius=10,
            bgcolor=ft.Colors.PRIMARY_CONTAINER,
        )
    )


ft.app(main)

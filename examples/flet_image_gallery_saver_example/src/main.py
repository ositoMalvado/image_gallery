import flet as ft
from io import BytesIO
from flet_image_gallery_saver import ImageGallerySaver


def main(page: ft.Page):
    page.title = "ImageGallerySaver Example"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.padding = 20

    # Create a text control to display messages
    status_text = ft.Text("Status: Ready to save images", size=16)

    # Create an instance of ImageGallerySaver control
    gallery_saver = ImageGallerySaver()
    # Insert the control in overlay, as it's a non-visual control
    page.overlay.append(gallery_saver)

    # Function to handle when saving is completed
    def on_save_completed(e):
        status_text.value = f"✅ Save completed: {e.data}"
        status_text.color = ft.Colors.GREEN
        page.update()

    # Function to handle when saving fails
    def on_save_failed(e):
        status_text.value = f"❌ Error saving: {e.data}"
        status_text.color = ft.Colors.RED
        page.update()

    # Assign event handlers
    gallery_saver.on_save_completed = on_save_completed
    gallery_saver.on_save_failed = on_save_failed

    # Function to save a sample image from bytes
    def save_sample_image(e):
        status_text.value = "Saving sample image..."
        status_text.color = ft.Colors.BLUE
        page.update()

        # Create a sample image (a red square)
        try:
            from PIL import Image

            img = Image.new("RGB", (100, 100), color="red")
            buffer = BytesIO()
            img.save(buffer, format="JPEG")
            image_bytes = buffer.getvalue()

            # Save the image
            gallery_saver.save_image(
                image_bytes=image_bytes, quality=90, name="red_square.jpg"
            )
        except ImportError:
            status_text.value = "❌ Error: PIL/Pillow library is required"
            status_text.color = ft.Colors.RED
            page.update()

    # Function to save an image from URL
    def save_image_from_url(e):
        try:
            import requests

            status_text.value = "Downloading image from URL..."
            status_text.color = ft.Colors.BLUE
            page.update()

            try:
                # Sample image URL
                url = "https://picsum.photos/200"
                response = requests.get(url)
                if response.status_code == 200:
                    # Save the downloaded image
                    gallery_saver.save_image(
                        image_bytes=response.content,
                        quality=85,
                        name="image_from_url.jpg",
                    )
                else:
                    status_text.value = (
                        f"❌ Error downloading image: {response.status_code}"
                    )
                    status_text.color = ft.Colors.RED
                    page.update()
            except Exception as ex:
                status_text.value = f"❌ Error: {str(ex)}"
                status_text.color = ft.Colors.RED
                page.update()

        except ImportError:
            status_text.value = "❌ Error: requests library is required"
            status_text.color = ft.Colors.RED
            page.update()

    # Create buttons for actions
    btn_save_sample = ft.ElevatedButton(
        "Save Sample Image",
        icon=ft.Icons.IMAGE,
        on_click=save_sample_image,
        style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10)),
    )

    btn_save_from_url = ft.ElevatedButton(
        "Save Image from URL",
        icon=ft.Icons.CLOUD_DOWNLOAD,
        on_click=save_image_from_url,
        style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10)),
    )

    # Create the interface
    page.add(
        ft.Container(
            content=ft.Column(
                [
                    ft.Text(
                        "ImageGallerySaver Example",
                        size=24,
                        weight=ft.FontWeight.BOLD,
                    ),
                    ft.Text(
                        "Save images to the device gallery",
                        size=16,
                        italic=True,
                    ),
                    ft.Divider(),
                    ft.Container(height=20),  # Spacer
                    ft.Column(
                        [btn_save_sample, btn_save_from_url],
                        alignment=ft.MainAxisAlignment.CENTER,
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    ),
                    ft.Container(height=20),  # Spacer
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

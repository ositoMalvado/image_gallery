from enum import Enum
from typing import Any, Optional, Union, Callable, Dict

from flet.core.constrained_control import ConstrainedControl
from flet.core.control import OptionalNumber, Control
from flet.core.types import OptionalControlEventCallable
from flet.core.ref import Ref


class FletImageGallerySaver(Control):
    """
    Un control para guardar imágenes y archivos en la galería del dispositivo.

    Este control permite guardar imágenes desde bytes o archivos directamente en la galería
    del dispositivo móvil, con soporte para configurar la calidad y el nombre del archivo.

    Ejemplo:
    ```python
    import flet as ft

    def main(page):
        def on_save_completed(e):
            print(f"Guardado completado: {e.data}")

        def on_save_failed(e):
            print(f"Error al guardar: {e.data}")

        def save_image_clicked(e):
            # Guardar una imagen desde bytes
            gallery_saver.save_image(
                image_bytes=image_bytes,
                quality=90,
                name="mi_imagen.jpg"
            )

        def save_file_clicked(e):
            # Guardar un archivo desde una ruta
            gallery_saver.save_file(
                file_path="/ruta/al/archivo.jpg"
            )

        gallery_saver = ft.FletImageGallerySaver(
            on_save_completed=on_save_completed,
            on_save_failed=on_save_failed
        )

        page.add(
            gallery_saver,
            ft.ElevatedButton("Guardar imagen", on_click=save_image_clicked),
            ft.ElevatedButton("Guardar archivo", on_click=save_file_clicked)
        )

    ft.app(target=main)
    ```
    """

    def __init__(
        self,
        #
        # Control
        #
        ref=None,
        disabled=None,
        visible=None,
        data=None,
        #
        # FletImageGallerySaver specific
        #
        on_save_completed: OptionalControlEventCallable = None,
        on_save_failed: OptionalControlEventCallable = None,
    ):
        Control.__init__(
            self,
            ref=ref,
            disabled=disabled,
            visible=visible,
            data=data,
        )

        self.on_save_completed = on_save_completed
        self.on_save_failed = on_save_failed

    def _get_control_name(self):
        return "flet_image_gallery_saver"

    # on_save_completed
    @property
    def on_save_completed(self) -> OptionalControlEventCallable:
        """
        Evento que se dispara cuando se completa el guardado de una imagen o archivo.

        El evento contiene información sobre el resultado en el campo `data`.
        """
        return self._get_event_handler("save_completed")

    @on_save_completed.setter
    def on_save_completed(self, handler: OptionalControlEventCallable):
        self._add_event_handler("save_completed", handler)

    # on_save_failed
    @property
    def on_save_failed(self) -> OptionalControlEventCallable:
        """
        Evento que se dispara cuando falla el guardado de una imagen o archivo.

        El evento contiene información sobre el error en el campo `data`.
        """
        return self._get_event_handler("save_failed")

    @on_save_failed.setter
    def on_save_failed(self, handler: OptionalControlEventCallable):
        self._add_event_handler("save_failed", handler)

    def save_image(
        self, image_bytes: bytes, quality: int = 80, name: Optional[str] = None
    ) -> None:
        """
        Guarda una imagen en la galería del dispositivo a partir de bytes.

        Args:
            image_bytes: Los bytes de la imagen a guardar.
            quality: La calidad de la imagen (0-100), por defecto 80.
            name: Nombre opcional para el archivo guardado.
        """
        args = {}

        # Convertir bytes a string de enteros separados por comas
        if isinstance(image_bytes, bytes):
            bytes_str = ",".join([str(b) for b in image_bytes])
            args["bytes"] = bytes_str
        else:
            raise ValueError("image_bytes debe ser de tipo bytes")

        if quality is not None:
            args["quality"] = str(quality)

        if name is not None:
            args["name"] = name

        self._invoke_method("save_image", args)

    def save_file(self, file_path: str, is_return_path_of_ios: bool = False) -> None:
        """
        Guarda un archivo en la galería del dispositivo a partir de una ruta de archivo.

        Args:
            file_path: Ruta al archivo que se guardará en la galería.
            is_return_path_of_ios: Si es True, devuelve la ruta del archivo en iOS.
        """
        args = {}

        args["filePath"] = file_path
        args["isReturnPathOfIOS"] = str(is_return_path_of_ios).lower()

        self._invoke_method("save_file", args)

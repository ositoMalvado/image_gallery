from typing import Optional
from flet.core.control import Control
from flet.core.types import OptionalControlEventCallable


class ImageGallerySaver(Control):
    """
    A control for saving images and files to the device gallery.

    This control allows saving images from bytes or files directly to the mobile device's
    gallery, with support for configuring quality and filename.

    Example:
    ```python
    import flet as ft

    def main(page):
        def on_save_completed(e):
            print(f"Save completed: {e.data}")

        def on_save_failed(e):
            print(f"Save failed: {e.data}")

        def save_image_clicked(e):
            # Save an image from bytes
            gallery_saver.save_image(
                image_bytes=image_bytes,
                quality=90,
                name="my_image.jpg"
            )

        def save_file_clicked(e):
            # Save a file from a path
            gallery_saver.save_file(
                file_path="/path/to/file.jpg"
            )

        gallery_saver = ft.FletImageGallerySaver(
            on_save_completed=on_save_completed,
            on_save_failed=on_save_failed
        )

        page.add(
            gallery_saver,
            ft.ElevatedButton("Save image", on_click=save_image_clicked),
            ft.ElevatedButton("Save file", on_click=save_file_clicked)
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
        """
        Initialize a new ImageGallerySaver control.

        Args:
            ref: Reference to the control.
            disabled: Whether the control is disabled.
            visible: Whether the control is visible.
            data: Additional data associated with the control.
            on_save_completed: Event handler triggered when saving completes successfully.
            on_save_failed: Event handler triggered when saving fails.
        """
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
        """
        Get the internal control name for the Flet runtime.

        Returns:
            str: The control name.
        """
        return "flet_image_gallery_saver"

    # on_save_completed
    @property
    def on_save_completed(self) -> OptionalControlEventCallable:
        """
        Event that fires when an image or file is successfully saved.

        The event contains information about the result in the `data` field.

        Returns:
            OptionalControlEventCallable: The current event handler.
        """
        return self._get_event_handler("save_completed")

    @on_save_completed.setter
    def on_save_completed(self, handler: OptionalControlEventCallable):
        """
        Set the handler for the save_completed event.

        Args:
            handler: The function to call when saving completes successfully.
        """
        self._add_event_handler("save_completed", handler)

    # on_save_failed
    @property
    def on_save_failed(self) -> OptionalControlEventCallable:
        """
        Event that fires when saving an image or file fails.

        The event contains error information in the `data` field.

        Returns:
            OptionalControlEventCallable: The current event handler.
        """
        return self._get_event_handler("save_failed")

    @on_save_failed.setter
    def on_save_failed(self, handler: OptionalControlEventCallable):
        """
        Set the handler for the save_failed event.

        Args:
            handler: The function to call when saving fails.
        """
        self._add_event_handler("save_failed", handler)

    def save_image(
        self, image_bytes: bytes, quality: int = 80, name: Optional[str] = None
    ) -> None:
        """
        Save an image to the device gallery from bytes.

        This method converts the provided image bytes to a format that can be saved
        in the device's gallery. The quality parameter affects the compression level
        for formats that support it, like JPEG.

        Args:
            image_bytes: The image bytes to save.
            quality: The image quality (0-100), default is 80.
            name: Optional name for the saved file.

        Raises:
            ValueError: If image_bytes is not of type bytes.
        """
        args = {}

        # Convert bytes to comma-separated string of integers
        if isinstance(image_bytes, bytes):
            bytes_str = ",".join([str(b) for b in image_bytes])
            args["bytes"] = bytes_str
        else:
            raise ValueError("image_bytes must be of type bytes")

        if quality is not None:
            args["quality"] = str(quality)

        if name is not None:
            args["name"] = name

        self.invoke_method("save_image", args)

    def save_file(self, file_path: str, is_return_path_of_ios: bool = False) -> None:
        """
        Save a file to the device gallery from a file path.

        This method allows saving existing files to the device gallery by providing
        the file path. This is useful for saving files that are already on the device
        but not yet in the gallery.

        Args:
            file_path: Path to the file that will be saved to the gallery.
            is_return_path_of_ios: If True, returns the file path on iOS devices.
        """
        args = {}

        args["filePath"] = file_path
        args["isReturnPathOfIOS"] = str(is_return_path_of_ios).lower()

        self.invoke_method("save_file", args)
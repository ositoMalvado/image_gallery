# Introduction

FletImageGallerySaver for Flet.

## Examples

```
import flet as ft

from flet_image_gallery_saver import FletImageGallerySaver


def main(page: ft.Page):
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    page.add(

                ft.Container(height=150, width=300, alignment = ft.alignment.center, bgcolor=ft.Colors.PURPLE_200, content=FletImageGallerySaver(
                    tooltip="My new FletImageGallerySaver Control tooltip",
                    value = "My new FletImageGallerySaver Flet Control", 
                ),),

    )


ft.app(main)
```

## Classes

[FletImageGallerySaver](FletImageGallerySaver.md)



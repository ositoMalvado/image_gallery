# flet-image-gallery-saver
ImageGallerySaver control for Flet

## Compatibility

Compatible only with iOS and Android.

## Installation

Add dependency to `pyproject.toml` of your Flet app:

* **Git dependency**

Link to git repository:

```
dependencies = [
  "flet-image-gallery-saver @ git+https://github.com/ositoMalvado/image-gallery",
  "flet>=0.28.2",
]
```

## Permission required

```
[tool.flet]
permissions = ["photo_library"]
```

Build your app:
```
flet build macos -v
```

## Documentation

[Link to documentation](https://ositoMalvado.github.io/image-gallery/)

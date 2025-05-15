import 'package:flet/flet.dart';

import 'flet_image_gallery_saver.dart';

CreateControlFactory createControl = (CreateControlArgs args) {
  switch (args.control.type) {
    case "flet_image_gallery_saver":
      return FletImageGallerySaverControl(
        parent: args.parent,
        control: args.control,
        backend: args.backend,
      );
    default:
      return null;
  }
};

void ensureInitialized() {
  // nothing to initialize
}

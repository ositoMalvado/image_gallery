import 'package:flet/flet.dart';
import 'package:flutter/material.dart';
import 'package:image_gallery_saver/image_gallery_saver.dart';
import 'dart:typed_data';

class FletImageGallerySaverControl extends StatefulWidget {
  final Control? parent;
  final Control control;
  final FletControlBackend backend;

  const FletImageGallerySaverControl({
    super.key,
    required this.parent,
    required this.control,
    required this.backend,
  });

  @override
  State<FletImageGallerySaverControl> createState() =>
      _FletImageGallerySaverControlState();
}

class _FletImageGallerySaverControlState
    extends State<FletImageGallerySaverControl> {
  @override
  void initState() {
    super.initState();
    widget.backend.subscribeMethods(widget.control.id, _handleMethodCall);
  }

  @override
  void dispose() {
    widget.backend.unsubscribeMethods(widget.control.id);
    super.dispose();
  }

  Future<String?> _handleMethodCall(
      String methodName, Map<String, String> args) async {
    switch (methodName) {
      case "save_image":
        return _handleSaveImage(args);
      case "save_file":
        return _handleSaveFile(args);
      default:
        return null;
    }
  }

  Future<String?> _handleSaveImage(Map<String, String> args) async {
    final imageBytes = args["bytes"];
    if (imageBytes == null || imageBytes.isEmpty) {
      return "error: No image data provided";
    }

    try {
      // Decode base64 string to Uint8List
      final Uint8List bytes = Uint8List.fromList(
          imageBytes.split(',').map((e) => int.parse(e)).toList());

      // Optional parameters
      final quality = int.tryParse(args["quality"] ?? "100");
      final name = args["name"];

      final result = await ImageGallerySaver.saveImage(
        bytes,
        quality: quality ?? 80,
        name: name,
      );

      _handleSaveResult(result);
      return result.toString();
    } catch (e) {
      debugPrint("Save image error: $e");
      return "error: $e";
    }
  }

  Future<String?> _handleSaveFile(Map<String, String> args) async {
    final filePath = args["filePath"];
    if (filePath == null || filePath.isEmpty) {
      return "error: No file path provided";
    }

    try {
      final isReturnPathOfIOS = args["isReturnPathOfIOS"] == "true";

      final result = await ImageGallerySaver.saveFile(
        filePath,
        isReturnPathOfIOS: isReturnPathOfIOS,
      );

      _handleSaveResult(result);
      return result.toString();
    } catch (e) {
      debugPrint("Save file error: $e");
      return "error: $e";
    }
  }

  void _handleSaveResult(dynamic result) {
    if (result != null) {
      if (result is Map &&
          result.containsKey('isSuccess') &&
          result['isSuccess']) {
        widget.backend.triggerControlEvent(
            widget.control.id, "save_completed", result.toString());
      } else {
        widget.backend.triggerControlEvent(
            widget.control.id, "save_failed", result.toString());
      }
    }
  }

  @override
  Widget build(BuildContext context) {
    // This is a non-visual control, return an empty container
    return const SizedBox.shrink();
  }
}

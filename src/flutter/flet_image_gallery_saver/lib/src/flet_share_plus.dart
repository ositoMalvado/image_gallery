import 'package:flet/flet.dart';
import 'package:flutter/material.dart';
import 'package:share_plus/share_plus.dart';

class SharePlusControl extends StatefulWidget {
  final Control control;
  final FletControlBackend backend;

  const SharePlusControl({
    Key? key,
    required this.control,
    required this.backend,
  }) : super(key: key);

  @override
  State<SharePlusControl> createState() => _SharePlusControlState();
}

class _SharePlusControlState extends State<SharePlusControl> {
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
      case "share_text":
        return _handleShareText(args);
      case "share_files":
        return _handleShareFiles(args);
      case "share_uri":
        return _handleShareUri(args);
      default:
        return null;
    }
  }

  Future<String?> _handleShareText(Map<String, String> args) async {
    final text = args["text"] ?? "";
    final subject = args["subject"] ?? "";

    try {
      final result = await Share.share(
        text,
        subject: subject,
      );

      _handleShareResult(result);
      return result.status.name;
    } catch (e) {
      debugPrint("Share error: $e");
      return "error: $e";
    }
  }

  Future<String?> _handleShareFiles(Map<String, String> args) async {
    final filePaths = (args["filePaths"] ?? "")
        .split(",")
        .where((path) => path.isNotEmpty)
        .toList();
    final text = args["text"] ?? "";

    if (filePaths.isEmpty) {
      return "error: No files to share";
    }

    try {
      final files = filePaths.map((path) => XFile(path)).toList();
      final result = await Share.shareXFiles(
        files,
        text: text,
      );

      _handleShareResult(result);
      return result.status.name;
    } catch (e) {
      debugPrint("Share files error: $e");
      return "error: $e";
    }
  }

  Future<String?> _handleShareUri(Map<String, String> args) async {
    final uriString = args["uri"] ?? "";
    
    if (uriString.isEmpty) {
      return "error: URI is empty";
    }

    try {
      final uri = Uri.parse(uriString);
      final result = await Share.shareUri(uri);

      _handleShareResult(result);
      return result.status.name;
    } catch (e) {
      debugPrint("Share URI error: $e");
      return "error: $e";
    }
  }
  
  void _handleShareResult(ShareResult result) {
    if (result.status == ShareResultStatus.success) {
      widget.backend.triggerControlEvent(
          widget.control.id, "share_completed", result.raw);
    } else if (result.status == ShareResultStatus.dismissed) {
      widget.backend.triggerControlEvent(
          widget.control.id, "share_dismissed", result.raw);
    }
  }

  @override
  Widget build(BuildContext context) {
    // This is a non-visual control, return an empty container
    return const SizedBox.shrink();
  }
}
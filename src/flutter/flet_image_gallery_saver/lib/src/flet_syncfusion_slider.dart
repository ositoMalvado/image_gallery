import 'package:flet/flet.dart';
import 'package:flutter/material.dart';
import 'package:syncfusion_flutter_sliders/sliders.dart';
import 'package:syncfusion_flutter_sliders/src/slider_shapes.dart';
import 'package:intl/intl.dart' show DateFormat, NumberFormat;
import 'package:syncfusion_flutter_core/theme.dart';
import 'utils/flet_syncfusion_utils.dart';
import 'dart:convert';

class FletSyncfusionSliderControl extends StatefulWidget {
  final Control? parent;
  final Control control;
  final List<Control> children;
  final bool parentDisabled;
  final bool? parentAdaptive;
  final FletControlBackend backend;

  const FletSyncfusionSliderControl({
    super.key,
    required this.parent,
    required this.control,
    required this.children,
    required this.parentDisabled,
    required this.parentAdaptive,
    required this.backend,
  });

  @override
  State<FletSyncfusionSliderControl> createState() =>
      _FletSyncfusionSliderControlState();
}

class _FletSyncfusionSliderControlState
    extends State<FletSyncfusionSliderControl> {
  double _value = 0.0;
  final _debouncer = Debouncer(milliseconds: isDesktopPlatform() ? 10 : 100);

  @override
  void initState() {
    super.initState();
    _value = widget.control.attrDouble("value", 0.0)!;
    debugPrint("SyncfusionSlider initState: Initial value=$_value");
  }

  @override
  void dispose() {
    _debouncer.dispose();
    super.dispose();
  }

  @override
  void didUpdateWidget(covariant FletSyncfusionSliderControl oldWidget) {
    super.didUpdateWidget(oldWidget);
    double newValue = widget.control.attrDouble("value", 0.0)!;
    if ((_value - newValue).abs() > 0.00001) {
      debugPrint(
          "SyncfusionSlider didUpdateWidget: Value changed externally from $_value to $newValue");
      _value = newValue;
    }
  }

  void handleChange(dynamic value) {
    double newValue = value as double;
    debugPrint("SyncfusionSlider onChanged: New value=$newValue");

    setState(() {
      _value = newValue;
    });

    var props = {"value": newValue.toString()};
    widget.backend.updateControlState(widget.control.id, props, server: false);

    _debouncer.run(() {
      widget.backend.updateControlState(widget.control.id, props);
      widget.backend.triggerControlEvent(
          widget.control.id, "change", newValue.toString());
    });
  }

  void handleChangeStart(dynamic startValue) {
    double value = startValue as double;
    debugPrint("SyncfusionSlider onChangeStart: Value=$value");
    widget.backend.triggerControlEvent(
        widget.control.id, "change_start", value.toString());
  }

  void handleChangeEnd(dynamic endValue) {
    double value = endValue as double;
    debugPrint("SyncfusionSlider onChangeEnd: Value=$value");
    widget.backend
        .triggerControlEvent(widget.control.id, "change_end", value.toString());
  }

  @override
  Widget build(BuildContext context) {
    debugPrint(
        "FletSyncfusionSliderControl build: ${widget.control.id}, Current internal value=$_value");

    // Basic properties
    double min = widget.control.attrDouble("min", 0.0)!;
    double max = widget.control.attrDouble("max", 100.0)!;
    double interval = widget.control
        .attrDouble("interval", (max > min ? (max - min) / 10 : 10.0))!;
    if (interval <= 0) interval = 10.0;
    double? stepSize = widget.control.attrDouble("step_size");

    // Visualization properties
    bool showTicks = widget.control.attrBool("show_ticks", false)!;
    bool showLabels = widget.control.attrBool("show_labels", false)!;
    bool showDividers = widget.control.attrBool("show_dividers", false)!;
    bool enableTooltip = widget.control.attrBool("enable_tooltip", true)!;
    bool shouldAlwaysShowTooltip =
        widget.control.attrBool("should_always_show_tooltip", false)!;
    int minorTicksPerInterval =
        widget.control.attrInt("minor_ticks_per_interval", 0)!;

    // Orientation and direction
    bool isVertical = widget.control.attrBool("vertical", false)!;
    bool isInversed = widget.control.attrBool("inversed", false)!;

    // Colors
    Color? activeColor =
        widget.control.attrColor("active_color", context) ?? null;
    Color? inactiveColor =
        widget.control.attrColor("inactive_color", context) ?? null;

    // Label and tooltip settings
    String labelPlacementStr =
        widget.control.attrString("label_placement", "onTicks")!;
    LabelPlacement labelPlacement = LabelPlacement.onTicks;
    if (labelPlacementStr == "betweenTicks") {
      labelPlacement = LabelPlacement.betweenTicks;
    }

    String edgeLabelPlacementStr =
        widget.control.attrString("edge_label_placement", "auto")!;
    EdgeLabelPlacement edgeLabelPlacement = EdgeLabelPlacement.auto;
    if (edgeLabelPlacementStr == "inside") {
      edgeLabelPlacement = EdgeLabelPlacement.inside;
    } else if (edgeLabelPlacementStr == "auto") {
      edgeLabelPlacement = EdgeLabelPlacement.auto;
    }

    // Shapes
    SfTooltipShape tooltipShape = const SfRectangularTooltipShape();
    String tooltipShapeStr =
        widget.control.attrString("tooltip_shape", "rectangular")!;
    if (tooltipShapeStr == "paddle") {
      tooltipShape = const SfPaddleTooltipShape();
    }

    SfTrackShape trackShape = const SfTrackShape();
    SfDividerShape dividerShape = const SfDividerShape();
    SfOverlayShape overlayShape = const SfOverlayShape();
    SfThumbShape thumbShape = const SfThumbShape();
    SfTickShape tickShape = const SfTickShape();

    SfTickShape? minorTickShape;
    String? minorTickShapeType = widget.control.attrString("minor_tick_shape");
    if (minorTickShapeType == "SfTickShape") {
      minorTickShape = const SfTickShape();
    } else {
      minorTickShape = const SfMinorTickShape();
    }

    // icon and tooltip position
    var contentCtrls =
        widget.children.where((c) => c.name == "thumb_icon" && c.isVisible);

    bool? adaptive =
        widget.control.attrBool("adaptive") ?? widget.parentAdaptive;
    bool disabled = widget.control.isDisabled || widget.parentDisabled;

    Widget? thumbIcon = null;
    if (contentCtrls.isNotEmpty) {
      thumbIcon = createControl(widget.control, contentCtrls.first.id, disabled,
          parentAdaptive: adaptive);
    }

    SliderTooltipPosition tooltipPosition;
    if (widget.control.attrString("tooltip_position") == "left") {
      tooltipPosition = SliderTooltipPosition.left;
    } else {
      tooltipPosition = SliderTooltipPosition.right;
    }

    // last

    NumberFormat? numberFormat = null;
    DateFormat? dateFormat = null;
    DateIntervalType? dateIntervalType = null;

    // Clamp value within current min/max
    double currentValue = _value.clamp(min, max);
    if ((_value - currentValue).abs() > 0.00001) {
      debugPrint(
          "SyncfusionSlider build: Clamping internal value from $_value to $currentValue based on min=$min, max=$max");
      _value = currentValue;
    }

    SfSliderThemeData themeStyle = SfSliderThemeData();
    String? styleName = widget.control.attrString("sf_slider_theme");
    if (styleName != null) {
      Map<String, dynamic> json = jsonDecode(styleName);
      themeStyle = sfSliderThemeDataFromJSON(Theme.of(context), json)!;
    }
    // parseButtonStyle(theme, control, propName)
    Widget sliderWidget;
    if (isVertical) {
      sliderWidget = SfSliderTheme(
          data: themeStyle,
          child: SfSlider.vertical(
            min: min,
            max: max,
            value: currentValue,
            interval: interval,
            stepSize: stepSize,
            minorTicksPerInterval: minorTicksPerInterval,
            showTicks: showTicks,
            showLabels: showLabels,
            showDividers: showDividers,
            enableTooltip: enableTooltip,
            shouldAlwaysShowTooltip: shouldAlwaysShowTooltip,
            activeColor: activeColor,
            inactiveColor: inactiveColor,
            labelPlacement: labelPlacement,
            edgeLabelPlacement: edgeLabelPlacement,

            // * shapes
            trackShape: trackShape,
            dividerShape: dividerShape,
            overlayShape: overlayShape,
            thumbShape: thumbShape,
            tickShape: tickShape,
            minorTickShape: minorTickShape,
            tooltipShape: tooltipShape,

            // * icon and tooltip position
            thumbIcon: thumbIcon,
            tooltipPosition: tooltipPosition,

            // last
            numberFormat: numberFormat,
            dateFormat: dateFormat,
            dateIntervalType: dateIntervalType,
            // labelFormatterCallback
            // tooltipTextFormatterCallback
            // semanticFormatterCallback

            // * inversed and handlers
            isInversed: isInversed,
            onChanged: !disabled ? handleChange : null,
            onChangeStart: !disabled ? handleChangeStart : null,
            onChangeEnd: !disabled ? handleChangeEnd : null,
          ));
    } else {
      sliderWidget = SfSliderTheme(
          data: themeStyle,
          child: SfSlider(
            min: min,
            max: max,
            value: currentValue,
            interval: interval,
            stepSize: stepSize,
            minorTicksPerInterval: minorTicksPerInterval,
            showTicks: showTicks,
            showLabels: showLabels,
            showDividers: showDividers,
            enableTooltip: enableTooltip,
            shouldAlwaysShowTooltip: shouldAlwaysShowTooltip,
            activeColor: activeColor,
            inactiveColor: inactiveColor,
            labelPlacement: labelPlacement,
            edgeLabelPlacement: edgeLabelPlacement,

            // * shapes
            trackShape: trackShape,
            dividerShape: dividerShape,
            overlayShape: overlayShape,
            thumbShape: thumbShape,
            tickShape: tickShape,
            minorTickShape: minorTickShape,
            tooltipShape: tooltipShape,

            // * icon and tooltip position
            thumbIcon: thumbIcon,

            // last
            numberFormat: numberFormat,
            dateFormat: dateFormat,
            dateIntervalType: dateIntervalType,
            // labelFormatterCallback
            // tooltipTextFormatterCallback
            // semanticFormatterCallback

            // * inversed and handlers
            onChanged: !disabled ? handleChange : null,
            onChangeStart: !disabled ? handleChangeStart : null,
            onChangeEnd: !disabled ? handleChangeEnd : null,
          ));
    }

    return constrainedControl(
        context, sliderWidget, widget.parent, widget.control);
  }
}

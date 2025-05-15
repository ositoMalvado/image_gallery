from enum import Enum
from typing import Any, Optional, Union
import json
from flet.core.adaptive_control import AdaptiveControl
from flet.core.animation import AnimationValue
from flet.core.badge import BadgeValue
from flet.core.constrained_control import ConstrainedControl
from flet.core.control import OptionalNumber, Control
from flet.core.ref import Ref
from flet.core.tooltip import TooltipValue
from flet.core.types import (
    ColorEnums,
    ColorValue,
    ControlStateValue,
    MouseCursor,
    OffsetValue,
    OptionalControlEventCallable,
    ResponsiveNumber,
    RotateValue,
    ScaleValue,
    PaddingValue,
)

from flet_syncfusion_slider.flet_syncfusion_slider_theme import SfSliderTheme


class SyncfusionSlider(ConstrainedControl, AdaptiveControl):
    """
    A Syncfusion slider provides advanced slider features with customizable appearance,
    interactive elements like ticks and labels, and extensive event handling.

    Use this slider when you need more advanced functionalities than the basic slider,
    such as interval ticks, custom formatting, and more.

    Example:
    ```
    import flet as ft

    def main(page):
        def slider_changed(e):
            print(f"Slider changed to {e.control.value}")

        page.add(
            ft.Text("Syncfusion Slider with value:"),
            ft.SyncfusionSlider(
                value=30,
                min=0,
                max=100,
                interval=10,
                show_ticks=True,
                show_labels=True,
                on_change=slider_changed
            )
        )

    ft.app(target=main)
    ```
    """

    def __init__(
        self,
        value: OptionalNumber = None,
        min: OptionalNumber = None,
        max: OptionalNumber = None,
        interval: OptionalNumber = None,
        step_size: OptionalNumber = None,
        show_ticks: Optional[bool] = None,
        show_labels: Optional[bool] = None,
        show_dividers: Optional[bool] = None,
        enable_tooltip: Optional[bool] = None,
        should_always_show_tooltip: Optional[bool] = None,
        tooltip_shape: Optional[str] = None,
        minor_tick_shape: Optional[str] = None,
        tooltip_position: Optional[str] = None,
        minor_ticks_per_interval: Optional[int] = None,
        inversed: Optional[bool] = None,
        active_color: Optional[ColorValue] = None,
        inactive_color: Optional[ColorValue] = None,
        thumb_icon: Optional[Control] = None,
        # tooltip_text_format: Optional[str] = None,
        # label_format: Optional[str] = None,
        label_placement: Optional[str] = None,
        edge_label_placement: Optional[str] = None,
        sf_slider_theme: Optional[SfSliderTheme] = None,
        on_change: OptionalControlEventCallable = None,
        on_change_start: OptionalControlEventCallable = None,
        on_change_end: OptionalControlEventCallable = None,
        #
        # ConstrainedControl and AdaptiveControl
        #
        ref: Optional[Ref] = None,
        key: Optional[str] = None,
        width: OptionalNumber = None,
        height: OptionalNumber = None,
        left: OptionalNumber = None,
        top: OptionalNumber = None,
        right: OptionalNumber = None,
        bottom: OptionalNumber = None,
        expand: Union[None, bool, int] = None,
        expand_loose: Optional[bool] = None,
        col: Optional[ResponsiveNumber] = None,
        opacity: OptionalNumber = None,
        rotate: Optional[RotateValue] = None,
        scale: Optional[ScaleValue] = None,
        offset: Optional[OffsetValue] = None,
        aspect_ratio: OptionalNumber = None,
        animate_opacity: Optional[AnimationValue] = None,
        animate_size: Optional[AnimationValue] = None,
        animate_position: Optional[AnimationValue] = None,
        animate_rotation: Optional[AnimationValue] = None,
        animate_scale: Optional[AnimationValue] = None,
        animate_offset: Optional[AnimationValue] = None,
        on_animation_end: OptionalControlEventCallable = None,
        tooltip: Optional[TooltipValue] = None,
        badge: Optional[BadgeValue] = None,
        visible: Optional[bool] = None,
        disabled: Optional[bool] = None,
        data: Any = None,
        adaptive: Optional[bool] = None,
    ):
        ConstrainedControl.__init__(
            self,
            ref=ref,
            key=key,
            width=width,
            height=height,
            left=left,
            top=top,
            right=right,
            bottom=bottom,
            expand=expand,
            expand_loose=expand_loose,
            col=col,
            opacity=opacity,
            rotate=rotate,
            scale=scale,
            offset=offset,
            aspect_ratio=aspect_ratio,
            animate_opacity=animate_opacity,
            animate_size=animate_size,
            animate_position=animate_position,
            animate_rotation=animate_rotation,
            animate_scale=animate_scale,
            animate_offset=animate_offset,
            on_animation_end=on_animation_end,
            tooltip=tooltip,
            badge=badge,
            visible=visible,
            disabled=disabled,
            data=data,
        )

        AdaptiveControl.__init__(self, adaptive=adaptive)

        self.value = value
        self.min = min
        self.max = max
        self.interval = interval
        self.step_size = step_size
        self.show_ticks = show_ticks
        self.show_labels = show_labels
        self.show_dividers = show_dividers
        self.enable_tooltip = enable_tooltip
        self.should_always_show_tooltip = should_always_show_tooltip
        self.tooltip_shape = tooltip_shape
        self.minor_tick_shape = minor_tick_shape
        self.tooltip_position = tooltip_position
        self.thumb_icon = thumb_icon
        self.minor_ticks_per_interval = minor_ticks_per_interval
        self.inversed = inversed
        self.active_color = active_color
        self.inactive_color = inactive_color
        # self.tooltip_text_format = tooltip_text_format
        # self.label_format = label_format
        self.label_placement = label_placement
        self.edge_label_placement = edge_label_placement
        self.sf_slider_theme = sf_slider_theme
        self.on_change = on_change
        self.on_change_start = on_change_start
        self.on_change_end = on_change_end

    def _get_control_name(self):
        return "flet_syncfusion_slider"

    def before_update(self):
        super().before_update()
        assert self.min is None or self.max is None or self.min <= self.max, (
            "min must be less than or equal to max"
        )
        assert self.min is None or self.value is None or (self.value >= self.min), (
            "value must be greater than or equal to min"
        )
        assert self.max is None or self.value is None or (self.value <= self.max), (
            "value must be less than or equal to max"
        )

        # Procesar el tema del slider si está definido
        if self.sf_slider_theme is not None:
            self._set_attr("sf_slider_theme", str(self.sf_slider_theme))

    # value
    @property
    def value(self) -> float:
        return self._get_attr("value", data_type="float", def_value=self.min or 0.0)

    @value.setter
    def value(self, value: OptionalNumber):
        self._set_attr("value", value)

    # min
    @property
    def min(self) -> float:
        return self._get_attr("min", data_type="float", def_value=0.0)

    @min.setter
    def min(self, value: OptionalNumber):
        self._set_attr("min", value)

    # max
    @property
    def max(self) -> float:
        return self._get_attr("max", data_type="float", def_value=100.0)

    @max.setter
    def max(self, value: OptionalNumber):
        self._set_attr("max", value)

    # interval
    @property
    def interval(self) -> float:
        if self.max is not None and self.min is not None:
            default_interval = (self.max - self.min) / 10
        else:
            default_interval = 10.0
        return self._get_attr("interval", data_type="float", def_value=default_interval)

    @interval.setter
    def interval(self, value: OptionalNumber):
        self._set_attr("interval", value)

    # step_size
    @property
    def step_size(self) -> OptionalNumber:
        return self._get_attr("step_size", data_type="float")

    @step_size.setter
    def step_size(self, value: OptionalNumber):
        self._set_attr("step_size", value)

    # show_ticks
    @property
    def show_ticks(self) -> bool:
        return self._get_attr("show_ticks", data_type="bool", def_value=False)

    @show_ticks.setter
    def show_ticks(self, value: Optional[bool]):
        self._set_attr("show_ticks", value)

    # show_labels
    @property
    def show_labels(self) -> bool:
        return self._get_attr("show_labels", data_type="bool", def_value=False)

    @show_labels.setter
    def show_labels(self, value: Optional[bool]):
        self._set_attr("show_labels", value)

    # show_dividers
    @property
    def show_dividers(self) -> bool:
        return self._get_attr("show_dividers", data_type="bool", def_value=False)

    @show_dividers.setter
    def show_dividers(self, value: Optional[bool]):
        self._set_attr("show_dividers", value)

    # enable_tooltip
    @property
    def enable_tooltip(self) -> bool:
        return self._get_attr("enable_tooltip", data_type="bool", def_value=True)

    @enable_tooltip.setter
    def enable_tooltip(self, value: Optional[bool]):
        self._set_attr("enable_tooltip", value)

    # should_always_show_tooltip
    @property
    def should_always_show_tooltip(self) -> bool:
        return self._get_attr(
            "should_always_show_tooltip", data_type="bool", def_value=False
        )

    @should_always_show_tooltip.setter
    def should_always_show_tooltip(self, value: Optional[bool]):
        self._set_attr("should_always_show_tooltip", value)

    # minor_ticks_per_interval
    @property
    def minor_ticks_per_interval(self) -> int:
        return self._get_attr("minor_ticks_per_interval", data_type="int", def_value=0)

    @minor_ticks_per_interval.setter
    def minor_ticks_per_interval(self, value: Optional[int]):
        self._set_attr("minor_ticks_per_interval", value)

    # inversed
    @property
    def inversed(self) -> bool:
        return self._get_attr("inversed", data_type="bool", def_value=False)

    @inversed.setter
    def inversed(self, value: Optional[bool]):
        self._set_attr("inversed", value)

    # active_color
    @property
    def active_color(self) -> Optional[ColorValue]:
        return self.__active_color

    @active_color.setter
    def active_color(self, value: Optional[ColorValue]):
        self.__active_color = value
        self._set_enum_attr("active_color", value, ColorEnums)

    # inactive_color
    @property
    def inactive_color(self) -> Optional[ColorValue]:
        return self.__inactive_color

    @inactive_color.setter
    def inactive_color(self, value: Optional[ColorValue]):
        self.__inactive_color = value
        self._set_enum_attr("inactive_color", value, ColorEnums)

    # tooltip_shape
    @property
    def tooltip_shape(self) -> Optional[str]:
        return self._get_attr("tooltip_shape")

    @tooltip_shape.setter
    def tooltip_shape(self, value: Optional[str]):
        self._set_attr("tooltip_shape", value)

    # minor_tick_shape
    @property
    def minor_tick_shape(self) -> Optional[str]:
        return self._get_attr("minor_tick_shape")

    @minor_tick_shape.setter
    def minor_tick_shape(self, value: Optional[str]):
        self._set_attr("minor_tick_shape", value)

    # tooltip_position
    @property
    def tooltip_position(self) -> Optional[str]:
        return self._get_attr("tooltip_position")

    @tooltip_position.setter
    def tooltip_position(self, value: Optional[str]):
        self._set_attr("tooltip_position", value)

    @property
    def thumb_icon(self) -> Optional[Control]:
        return self.__content

    @thumb_icon.setter
    def thumb_icon(self, value: Optional[Control]):
        self.__content = value

    def _get_children(self):
        children = []
        if self.__content is not None:
            self.__content._set_attr_internal("n", "thumb_icon")
            children.append(self.__content)
        return children

    # tooltip_text_format
    # @property
    # def tooltip_text_format(self) -> Optional[str]:
    #     return self._get_attr("tooltip_text_format")

    # @tooltip_text_format.setter
    # def tooltip_text_format(self, value: Optional[str]):
    #     self._set_attr("tooltip_text_format", value)

    # label_format
    # @property
    # def label_format(self) -> Optional[str]:
    #     return self._get_attr("label_format")

    # @label_format.setter
    # def label_format(self, value: Optional[str]):
    #     self._set_attr("label_format", value)

    # label_placement
    @property
    def label_placement(self) -> Optional[str]:
        return self._get_attr("label_placement")

    @label_placement.setter
    def label_placement(self, value: Optional[str]):
        self._set_attr("label_placement", value)

    # edge_label_placement
    @property
    def edge_label_placement(self) -> Optional[str]:
        return self._get_attr("edge_label_placement")

    @edge_label_placement.setter
    def edge_label_placement(self, value: Optional[str]):
        self._set_attr("edge_label_placement", value)

    # sf_slider_theme
    @property
    def sf_slider_theme(self) -> Optional[SfSliderTheme]:
        return self.__sf_slider_theme

    @sf_slider_theme.setter
    def sf_slider_theme(self, value: Optional[SfSliderTheme]):
        self.__sf_slider_theme = value
        if value is not None:
            # Usar to_dict() para convertir el tema a un diccionario con claves en snake_case
            # que es lo que espera el lado de Dart
            self._set_attr("sf_slider_theme", value.to_dict())
            print("value: ", value)
            print("value to dict: ", value.to_dict())
        else:
            self._set_attr("sf_slider_theme", None)

    # on_change
    @property
    def on_change(self) -> OptionalControlEventCallable:
        return self._get_event_handler("change")

    @on_change.setter
    def on_change(self, handler: OptionalControlEventCallable):
        self._add_event_handler("change", handler)

    # on_change_start
    @property
    def on_change_start(self) -> OptionalControlEventCallable:
        return self._get_event_handler("change_start")

    @on_change_start.setter
    def on_change_start(self, handler: OptionalControlEventCallable):
        self._add_event_handler("change_start", handler)

    # on_change_end
    @property
    def on_change_end(self) -> OptionalControlEventCallable:
        return self._get_event_handler("change_end")

    @on_change_end.setter
    def on_change_end(self, handler: OptionalControlEventCallable):
        self._add_event_handler("change_end", handler)


class SyncfusionVerticalSlider(SyncfusionSlider):
    """
    A vertical version of the Syncfusion slider with all the same features but in vertical orientation.

    Example:
    ```
    import flet as ft

    def main(page):
        def slider_changed(e):
            print(f"Vertical slider changed to {e.control.value}")

        page.add(
            ft.Text("Syncfusion Vertical Slider with value:"),
            ft.SyncfusionVerticalSlider(
                value=30,
                min=0,
                max=100,
                interval=10,
                show_ticks=True,
                show_labels=True,
                on_change=slider_changed
            )
        )

    ft.app(target=main)
    ```
    """

    def __init__(
        self,
        value: OptionalNumber = None,
        min: OptionalNumber = None,
        max: OptionalNumber = None,
        interval: OptionalNumber = None,
        step_size: OptionalNumber = None,
        show_ticks: Optional[bool] = None,
        show_labels: Optional[bool] = None,
        show_dividers: Optional[bool] = None,
        enable_tooltip: Optional[bool] = None,
        should_always_show_tooltip: Optional[bool] = None,
        tooltip_shape: Optional[str] = None,
        minor_tick_shape: Optional[str] = None,
        tooltip_position: Optional[str] = None,
        minor_ticks_per_interval: Optional[int] = None,
        inversed: Optional[bool] = None,
        active_color: Optional[ColorValue] = None,
        inactive_color: Optional[ColorValue] = None,
        thumb_icon: Optional[Control] = None,
        label_placement: Optional[str] = None,
        edge_label_placement: Optional[str] = None,
        on_change: OptionalControlEventCallable = None,
        on_change_start: OptionalControlEventCallable = None,
        on_change_end: OptionalControlEventCallable = None,
        #
        # ConstrainedControl and AdaptiveControl
        #
        ref: Optional[Ref] = None,
        key: Optional[str] = None,
        width: OptionalNumber = None,
        height: OptionalNumber = None,
        left: OptionalNumber = None,
        top: OptionalNumber = None,
        right: OptionalNumber = None,
        bottom: OptionalNumber = None,
        expand: Union[None, bool, int] = None,
        expand_loose: Optional[bool] = None,
        col: Optional[ResponsiveNumber] = None,
        opacity: OptionalNumber = None,
        rotate: Optional[RotateValue] = None,
        scale: Optional[ScaleValue] = None,
        offset: Optional[OffsetValue] = None,
        aspect_ratio: OptionalNumber = None,
        animate_opacity: Optional[AnimationValue] = None,
        animate_size: Optional[AnimationValue] = None,
        animate_position: Optional[AnimationValue] = None,
        animate_rotation: Optional[AnimationValue] = None,
        animate_scale: Optional[AnimationValue] = None,
        animate_offset: Optional[AnimationValue] = None,
        on_animation_end: OptionalControlEventCallable = None,
        tooltip: Optional[TooltipValue] = None,
        badge: Optional[BadgeValue] = None,
        visible: Optional[bool] = None,
        disabled: Optional[bool] = None,
        data: Any = None,
        adaptive: Optional[bool] = None,
    ):
        super().__init__(
            value=value,
            min=min,
            max=max,
            interval=interval,
            step_size=step_size,
            show_ticks=show_ticks,
            show_labels=show_labels,
            show_dividers=show_dividers,
            enable_tooltip=enable_tooltip,
            should_always_show_tooltip=should_always_show_tooltip,
            tooltip_shape=tooltip_shape,
            minor_tick_shape=minor_tick_shape,
            tooltip_position=tooltip_position,
            minor_ticks_per_interval=minor_ticks_per_interval,
            inversed=inversed,
            active_color=active_color,
            inactive_color=inactive_color,
            thumb_icon=thumb_icon,
            label_placement=label_placement,
            edge_label_placement=edge_label_placement,
            on_change=on_change,
            on_change_start=on_change_start,
            on_change_end=on_change_end,
            ref=ref,
            key=key,
            width=width,
            height=height,
            left=left,
            top=top,
            right=right,
            bottom=bottom,
            expand=expand,
            expand_loose=expand_loose,
            col=col,
            opacity=opacity,
            rotate=rotate,
            scale=scale,
            offset=offset,
            aspect_ratio=aspect_ratio,
            animate_opacity=animate_opacity,
            animate_size=animate_size,
            animate_position=animate_position,
            animate_rotation=animate_rotation,
            animate_scale=animate_scale,
            animate_offset=animate_offset,
            on_animation_end=on_animation_end,
            tooltip=tooltip,
            badge=badge,
            visible=visible,
            disabled=disabled,
            data=data,
            adaptive=adaptive,
        )
        self._set_attr("vertical", True)

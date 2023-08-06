#!/usr/bin/env python3

"""Definition of some types for mypy."""


#  pylint: disable=invalid-name

from typing import Optional, Tuple, Callable, Any, Union, Literal, Dict
from typing import TypedDict, List, get_args, TYPE_CHECKING
import pygame as pg
if TYPE_CHECKING:
    from . import Node


abs_size_t = Tuple[int, int]
anchor_t = Tuple[
    Literal['left', 'center', 'right'],
    Literal['top', 'center', 'bottom']
]
animation_callback_t = Callable[[], None]
animation_t = Literal[
    'fade', 'fadein', 'fadeout', 'fill', 'grow', 'glow', 'popin',
    'popout', 'scroll'
]
background_t = Literal['color', 'image']
border_t = Literal['color', 'image']
color_t = Union[
    str,
    Tuple[int, int, int],
    Tuple[int, int, int, int]
]
floating_pos_type_t = Literal['relative', 'absolute']
font_size_rel_t = Literal[
    'xx-small', 'x-small', 'small', 'normal', 'large', 'x-large', 'xx-large'
]
pos_opt_t = Tuple[Optional[int], Optional[int]]
pos_t = Tuple[int, int]
floating_pos_t = Tuple[floating_pos_type_t, anchor_t, pos_t]
font_size_t = Union[int, font_size_rel_t]
halign_t = Literal['center', 'left', 'right']
node_pred_t = Callable[['Node'], bool]
opt_pos_opt_t = Optional[pos_opt_t]
opt_pos_t = Optional[pos_t]
orientation_t = Literal['vertical', 'horizontal']
padding_t = Union[int, Tuple[int, int]]
push_dest_t = Literal['bottom', 'top']
rect_t = Tuple[int, int, int, int]
size_t = Tuple[Optional[Union[str, int]], Optional[Union[str, int]]]
user_key_proc_t = Callable[[], None]
link_t = Callable[[], bool]
event_proc_t = Callable[[pg.event.Event], bool]
valign_t = Literal['bottom', 'center', 'top']
media_t = Literal['font', 'image', 'sound']

#  style class
sc_context_type_t = Literal['class', 'event', 'parentclass', 'status', 'value']
sc_context_t = Dict[sc_context_type_t, Any]
all_sc_contexts = get_args(sc_context_type_t)

#  keys
key_action_t = Literal[
    'activate',
    'close-window',
    'move-focus-forward',
    'move-focus-backward',
    'move-focus-north',
    'move-focus-east',
    'move-focus-south',
    'move-focus-west',
    'user-defined'
]
all_key_actions = get_args(key_action_t)


event_t = Literal[
    #  the node has been activated
    'on-activate',
    #  the value of the node has changed
    'on-change',
    #  the node get the clicked status
    'on-clicked',
    #  left-click up on the node
    'on-click-up',
    #  left-click down on the node
    'on-click-down',
    #  right-click down on the node
    'on-click-down-right',
    #  right-click up on the node
    'on-click-up-right',
    #  the node window is closed
    'on-close',
    #  the node has been disabled
    'on-disable',
    #  the node has been enabled
    'on-enable',
    #  the node received the focus
    'on-focus',
    #  a key has been pressed
    'on-key',
    #  the mouse wheel has been used over the node
    'on-mouse-wheel',
    #  the node window is opened
    'on-open',
    #  the cursor just moved over the node
    'on-over',
    #  the cursor was previously on the node, and is still over it
    'on-over-again',
    #  the node has been selected
    'on-select',
    #  the node has lost the focus
    'on-unfocus',
    #  the cursor is not over the node anymore
    'on-unover',
    #  the node has been unselected
    'on-unselect',
    #  the node get the unclicked status
    'on-unclicked'
]

all_events = list(get_args(event_t))


status_t = Literal[
    #  base status
    'base',
    #  the node is being left-clicked (i.e., the cursor is over it and
    #  the user has the left mouse button pressed)
    'clicked',
    #  the node is disabled
    'disabled',
    #  the node has the focus
    'focus',
    #  the cursor is over the node
    'overed',
    #  the node is being selected
    'selected'
]
all_status = list(get_args(status_t))

style_attr_t = Literal[
    'animation', 'animation-arguments', 'background', 'background-color',
    'background-image', 'border', 'border-color', 'border-images',
    'border-width', 'color', 'corner', 'cursor-image', 'expand', 'font',
    'font-size', 'frame-bar-background-color', 'frame-bar-color',
    'frame-bar-corner', 'frame-bar-width', 'frame-vbar-images',
    'gauge-label-class', 'gauge-label-format', 'grid-row-size',
    'halign', 'hspacing', 'input-text-allowed', 'input-text-max-size',
    'input-text-placeholder', 'opacity', 'orientation', 'padding', 'pos',
    'pos-list', 'range-acceleration', 'range-bar-color', 'range-bar-corner',
    'range-bar-size', 'range-bullet-color', 'range-bullet-radius',
    'range-label-class', 'range-label-distance', 'range-label-format',
    'range-step', 'rule-images', 'scale', 'select-cyclic', 'select-hide-links',
    'select-next-class', 'select-next-label', 'select-prev-class',
    'select-prev-label', 'select-wheel-units', 'size', 'sound',
    'text-board-push-dest', 'text-board-rows', 'underline', 'valign',
    'vspacing', 'window-cross-image'
]

style_t = TypedDict('style_t', {
    'animation': animation_t,
    'animation-arguments': Dict[str, Any],
    'background': background_t,
    'background-color': color_t,
    'background-image': str,
    'border': border_t,
    'border-color': color_t,
    'border-images': Tuple[str, str, str, str, str, str],
    'border-width': int,
    'color': color_t,
    'corner': int,
    'cursor-image': str,
    'expand': bool,
    'font': str,
    'font-size': font_size_t,
    'frame-bar-background-color': color_t,
    'frame-bar-color': color_t,
    'frame-bar-corner': int,
    'frame-bar-width': int,
    'frame-vbar-images': Tuple[str, str, str, str, str, str],
    'gauge-label-class': str,
    'gauge-label-format': str,
    'grid-row-size': int,
    'halign': halign_t,
    'hspacing': int,
    'input-text-allowed': str,
    'input-text-max-size': int,
    'input-text-placeholder': str,
    'opacity': float,
    'orientation': orientation_t,
    'padding': padding_t,
    'pos': floating_pos_t,
    'pos-list': List[floating_pos_t],
    'range-acceleration': int,
    'range-bar-color': color_t,
    'range-bar-corner': int,
    'range-bar-size': abs_size_t,
    'range-bullet-color': color_t,
    'range-bullet-radius': int,
    'range-label-class': str,
    'range-label-distance': int,
    'range-label-format': str,
    'range-step': int,
    'rule-images': Tuple[str, str, str],
    'scale': float,
    'select-cyclic': bool,
    'select-hide-links': bool,
    'select-next-class': str,
    'select-next-label': str,
    'select-prev-class': str,
    'select-prev-label': str,
    'select-wheel-units': int,
    'size': size_t,
    'sound': str,
    'text-board-push-dest': push_dest_t,
    'text-board-rows': int,
    'underline': bool,
    'valign': valign_t,
    'vspacing': int,
    'window-cross-image': str
}, total=False)

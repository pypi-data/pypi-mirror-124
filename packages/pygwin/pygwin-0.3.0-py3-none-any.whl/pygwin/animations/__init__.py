#!/usr/bin/env python3

"""Import all predefined animations here."""

from .animation_sequence import AnimationSequence
from .sleep_animation import SleepAnimation
from .node_animation import NodeAnimation
from .fade import FadeAnimation, FadeInAnimation, FadeOutAnimation
from .fill import FillAnimation
from .glow import GlowAnimation
from .grow import GrowAnimation, PopInAnimation, PopOutAnimation
from .scroll import ScrollAnimation

__all__ = [
    'AnimationSequence',
    'FadeAnimation',
    'FadeInAnimation',
    'FadeOutAnimation',
    'FillAnimation',
    'GlowAnimation',
    'GrowAnimation',
    'PopInAnimation',
    'PopOutAnimation',
    'SleepAnimation',
    'ScrollAnimation'
]

#!/usr/bin/env python3

"""Definition of class NodeAnimation."""

from abc import ABC
from typing import Any, Callable, Optional, TYPE_CHECKING

from .. import Animation
if TYPE_CHECKING:
    from .. import Node


class NodeAnimation(Animation, ABC):
    """A NodeAnimation periodically update the style of a Node."""

    def __init__(
            self,
            node: 'Node',
            prog: Any,
            handler: Callable[[Any], Any],
            **kwargs: Any
    ):
        """Initialize self.

        Argument node is the Node object on which self will operate.

        kwarg period is the period of the animation (default = 1).

        If kwarg persistent is False then the node recovers its
        original style when the animation ends.  Otherwise, the
        updates of the style made by the animation are permanent.
        Default is False.

        The animation is started after initialisation.

        """
        Animation.__init__(
            self,
            prog,
            handler,
            node.get_window(),
            period=kwargs.get('period', 1)
        )
        self.__node = node
        self.__tmp_class: Optional[str]
        if kwargs.get('persistent', False):
            self.__tmp_class = None
        else:
            self.__tmp_class = self.node._new_tmp_style_class()
        node.set_animation(self)

    @property
    def node(self) -> 'Node':
        """Get the node animated by self."""
        return self.__node

    @property
    def tmp_class(self) -> Optional[str]:
        """Get the temporary style class created for the node.

        None is returned if self has been initialized with keyword
        persistent=True.

        The temporary style class lives as long as the animation has
        not been stopped.

        """
        return self.__tmp_class

    def stop(self) -> None:
        super().stop()
        if self.node.animation == self:
            self.node.set_animation(None)
        if self.tmp_class is not None:
            self.node._del_tmp_style_class(self.tmp_class)
            self.__tmp_class = None

#!/usr/bin/env python3

"""Definition of class Box."""

from typing import Iterator, List, Optional, Tuple, Any, Literal

from . import types, Pos, Node, Label


class Box(Node):
    """Box nodes are containers for other nodes."""

    AVAILABLE_STYLES = {
        'hspacing',
        'orientation',
        'vspacing'
    }

    def __init__(self, *nodes: Node, **kwargs: Any):
        """Initialise a Box node with nodes inside."""
        Node.__init__(self, **kwargs)
        self.__children: List[Node] = list()
        for node in nodes:
            self.pack(node)

    def __len__(self) -> int:
        """Get the number of nodes in the box."""
        return len(self.children)

    def __iter__(self) -> Iterator[Node]:
        """Iterate on all the nodes inside the box."""
        yield from self.children

    def __getitem__(self, i: int) -> Node:
        """Get the ith node inside the Box.

        Raise IndexError if i >= length of the box.

        """
        return self.__children[i]

    @property
    def children(self) -> List[Node]:
        """Get the list of nodes insides of the box."""
        return self.__children

    def is_empty(self) -> bool:
        """Check if the box is empty."""
        return self.__children == []

    def empty(self) -> None:
        """Empty the box."""
        children = list(self.__children)
        for child in children:
            self._del_child(child)

    def pack(self, node: Node) -> None:
        """Append node to the box children."""
        self.insert(len(self.__children), node)

    def remove(self, i: int) -> None:
        """Remove the ith child node of the box.

        Raise IndexError if i >= length of the box.

        """
        self.replace(i, None)

    def remove_node(self, node: Node) -> None:
        """Remove Node node from the box.

        Raise ValueError if node is not in the box.  If the removed
        node had the focus, then the focus is given to the node at the
        same position in the box after removal (or the last one if the
        removed node was the last children).

        """
        idx = self.children.index(node)
        had_focus = node.has_focus()
        self.remove(idx)
        if had_focus and self.children != []:
            idx = min(len(self.children) - 1, idx)
            self.children[idx].get_focus()

    def replace(self, i: int, node: Optional[Node]) -> None:
        """Replace the ith child of the box by node.

        Raise IndexError if i >= length of the box.

        """
        lg = len(self.children)
        if i >= lg:
            msg = f'tried to replace {i}-th child of a {lg}-node box'
            raise IndexError(msg)
        old = self.__children[i]
        self._del_child(old)
        if node is not None:
            self.insert(i, Label.node_of(node))

    def _del_child(self, node: Node) -> None:
        super()._del_child(node)
        self.__children.remove(node)
        self._reset_size()

    def insert(self, i: int, node: Node) -> None:
        """Insert node in the box at ith position.

        Raise IndexError if i > length of the box.

        """
        node = Label.node_of(node)
        self.__children.insert(i, node)
        self._add_child(node)
        self._reset_size()

    def __expanded_child_size(
            self,
            expanded: Node,
            size: types.pos_t
    ) -> types.pos_t:
        hspacing = self.get_style('hspacing')
        vspacing = self.get_style('vspacing')
        orientation = self.get_style('orientation')
        if orientation == 'vertical':
            hsum = (len(self.children) - 1) * vspacing
            for node in self.children:
                if node != expanded:
                    hsum += node.size_[1]
            result = size[0], size[1] - hsum
        else:
            wsum = (len(self.children) - 1) * hspacing
            for node in self.children:
                if node != expanded:
                    wsum += node.size_[0]
            result = size[0] - wsum, size[1]
        return result

    def _precompute_inner_size(self) -> types.pos_opt_t:
        sw, sh = (None, None) if self.size is None else self.size
        if sw is not None:
            sw -= self._get_inner_diff()[0]
        if sh is not None:
            sh -= self._get_inner_diff()[1]
        return sw, sh

    def _compute_inner_size(self) -> types.pos_t:
        def compute_dim(
                sizes: List[types.pos_t],
                sumed: int,
                maxed: int,
                spacing: Literal['vspacing', 'hspacing']
        ) -> types.pos_t:
            m = max(sizes, key=lambda wh: wh[maxed], default=(0, 0))[maxed]
            s = sum(map(lambda wh: wh[sumed], sizes))
            if len(sizes) > 1:
                s += (len(sizes) - 1) * self.get_style(spacing)
            return m, s

        def compute_sizes() -> Tuple[List[types.pos_t], types.pos_t]:
            sizes = list(
                map(lambda child: child._compute_size(), self.children)
            )
            if orientation == 'vertical':
                w, h = compute_dim(sizes, 1, 0, 'vspacing')
            else:
                h, w = compute_dim(sizes, 0, 1, 'hspacing')
            result = Pos.check(Pos.combine((sw, sh), (w, h)))
            return sizes, result

        orientation = self.get_style('orientation')
        sw, sh = self._precompute_inner_size()
        sizes, result = compute_sizes()

        #  set the container sizes of all children
        expanded = next(
            (child for child in self.__children if child.get_style('expand')),
            None
        )
        for child, (cw, ch) in zip(self.__children, sizes):
            if child != expanded:
                csize = (
                    (result[0], ch)
                    if orientation == 'vertical'
                    else (cw, result[1])
                )
            else:
                csize = self.__expanded_child_size(expanded, result)
            child._set_container_size(csize)

        #  we have to recompute self's inner size since the update of
        #  a child container size may have changed its size if it has
        #  a relative size and hence self's inner size
        _, size = compute_sizes()
        return Pos.check(size)

    def _position(self, pos: types.pos_t) -> None:
        orientation = self.get_style('orientation')
        if orientation == 'vertical':
            spacing = self.get_style('vspacing')
            for child in self.children:
                child.position(pos)
                pos = Pos.sum(pos, (0, spacing + child.size_[1]))
        else:
            spacing = self.get_style('hspacing')
            for child in self.children:
                child.position(pos)
                pos = Pos.sum(pos, (spacing + child.size_[0], 0))

    def _iter_tree(
            self, rec: bool = True, traverse: bool = False
    ) -> Iterator[Node]:
        if rec:
            for child in self.children:
                yield from child.iter_tree(rec=True, traverse=traverse)
        else:
            yield from self.children

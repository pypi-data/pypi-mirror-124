#!/usr/bin/env python3

"""Definition of class Table."""

from typing import Dict, Optional, Tuple, Any, Iterator

from . import types, Node, Label


class Table(Node):  # pylint: disable=R0902
    """Table nodes are two-dimensional arrays of nodes."""

    AVAILABLE_STYLES = {
        'hspacing',
        'vspacing'
    }

    def __init__(
            self,
            cells: Optional[Dict[types.pos_t, Node]] = None,
            colspan: Optional[Dict[types.pos_t, int]] = None,
            rowspan: Optional[Dict[types.pos_t, int]] = None,
            **kwargs: Any):
        """Initialise a table Node.

        The table is initially empty if kwarg cells is None. If not
        None, kwarg cells must be an {(int,int): Node} dictionary with
        key=coordinate of the cell and value=content of the cell.
        Cells of which coordinates do not appear in the dictionary are
        empty. If not None, kwarg colspan (resp. rowspan) is an
        {(int,int): int} dict, indicating for each cell the number of
        columns (rows) the cell spans.

        """
        Node.__init__(self, **kwargs)

        self.__cells: Dict[types.pos_t, Node] = dict()
        self.__rowspan: Dict[types.pos_t, int] = dict()
        self.__colspan: Dict[types.pos_t, int] = dict()
        self.__cols: int = 0
        self.__rows: int = 0
        self.__widths: Optional[Dict[int, int]] = None
        self.__heights: Optional[Dict[int, int]] = None

        #  cells initialisation
        if cells is None:
            cells = dict()
        if colspan is None:
            colspan = dict()
        if rowspan is None:
            rowspan = dict()
        for ij in cells:
            self.set_cell(
                ij, cells[ij],
                colspan=colspan.get(ij, 1),
                rowspan=rowspan.get(ij, 1)
            )

    def __len__(self) -> int:
        """Get the number of cells in the table."""
        return len(self.__cells)

    def new_row(
            self,
            cells: Dict[int, Node],
            colspan: Optional[Dict[int, int]] = None,
            rowspan: Optional[Dict[int, int]] = None
    ) -> None:
        """Add a row composed of cells at the bottom of the table.

        Cells must be a dictionary of {int: Node} with key=column
        number, value=cell content. If not None, colspan and rowspan
        must be dictionaries of {int: int} with key=column number and
        value=colspan or rowspan of the cell.

        """
        i = self.__rows
        for j in cells:
            cs = colspan[j] if colspan is not None and j in colspan else 1
            rs = rowspan[j] if rowspan is not None and j in rowspan else 1
            self.set_cell((i, j), cells[j], colspan=cs, rowspan=rs)

    def set_span(
            self,
            ij: types.pos_t,
            colspan: int = 1,
            rowspan: int = 1
    ) -> None:
        """Set the colspan and rowspan of the ij cell of the table.

        Raise ValueError if the cell does not exist.

        """
        if ij not in self.__cells:
            raise ValueError(f'{ij} not in cells')
        if colspan > 1:
            self.__colspan[ij] = colspan
        if rowspan > 1:
            self.__rowspan[ij] = rowspan
        self._reset_size()

    def set_cell(
            self,
            ij: types.pos_t,
            node: Node,
            colspan: int = 1,
            rowspan: int = 1
    ) -> None:
        """Put node in the ij cell of the table.

        The cell is given the specified colspan and rowspan.

        """
        if ij in self.__cells:
            self.__cells[ij]._unref()
        node = Label.node_of(node)
        self.__cells[ij] = node
        self.set_span(ij, colspan=colspan, rowspan=rowspan)
        i, j = ij
        self.__rows = max(self.__rows, i + self.__cell_rows(ij))
        self.__cols = max(self.__cols, j + self.__cell_cols(ij))
        self._add_child(node)
        self._reset_size()

    def empty(self) -> None:
        """Remove all cells from self."""
        children = list(self.__cells.values())
        for child in children:
            self._del_child(child)
        self.__cols = 0
        self.__rows = 0
        self.__cells = dict()
        self.__rowspan = dict()
        self.__colspan = dict()

    def _compute_inner_size(self) -> types.pos_t:
        hspacing = self.get_style('hspacing')
        vspacing = self.get_style('vspacing')

        self.__widths = {j: 0 for j in range(self.__cols)}
        self.__heights = {i: 0 for i in range(self.__rows)}

        #  compute sizes of all cells
        s = {
            ij: cell._compute_size()
            for ij, cell in self.__cells.items()
        }

        self.__compute_column_widths(s)

        #  compute max cell height for each row
        for i in range(self.__rows):
            for j in range(self.__cols):
                if (i, j) in self.__cells:
                    _, min_h = self.__cells[i, j].size_
                    self.__heights[i] = max(
                        min_h, self.__heights[i], s[i, j][1]
                    )

        #  set the container size of all cells
        for i, j in self.__cells:
            width = 0
            cols = self.__cell_cols((i, j))
            for k in range(cols):
                width += self.__widths[j + k]
            width += (cols - 1) * hspacing
            csize = (width, self.__heights[i])
            self.__cells[i, j]._set_container_size(csize)

        #  compute the final result
        w = 0
        j = 0
        while j < self.__cols:
            cols = self.__cell_cols((0, j))
            for k in range(cols):
                w += self.__widths[j + k]
            w += cols
            j += cols
        h = sum(self.__heights[i] for i in range(self.__rows))
        if self.__cols > 1:
            w += (self.__cols - 1) * hspacing
        if self.__rows > 1:
            h += (self.__rows - 1) * vspacing

        return w, h

    def _position(self, pos: types.pos_t) -> None:
        if self.__widths is None or self.__heights is None:
            raise ValueError('widths and heights of table not computed')
        hspacing = self.get_style('hspacing')
        vspacing = self.get_style('vspacing')
        h = 0
        i = 0
        while i < self.__rows:
            w = 0
            j = 0
            while j < self.__cols:
                if (i, j) in self.__cells:
                    cell = self.__cells[i, j]
                    cell.position((pos[0] + w, pos[1] + h))
                    w += cell.container_size_[0]
                else:
                    w += self.__widths[j]
                w += hspacing
                j += self.__cell_cols((i, j))
            h += self.__heights[i] + vspacing
            i += 1

    def __cell_cols(self, ij: types.pos_t) -> int:
        if ij in self.__colspan:
            return self.__colspan[ij]
        return 1

    def __cell_rows(self, ij: types.pos_t) -> int:
        if ij in self.__rowspan:
            return self.__rowspan[ij]
        return 1

    def __compute_column_widths(
            self,
            sizes: Dict[types.pos_t, types.pos_t]
    ) -> None:
        hspacing = self.get_style('hspacing')
        notdone: Dict[int, Tuple[types.pos_t, int, int]] = dict()
        for j in range(self.__cols):
            wmax = 0

            #  traverse cells of this column that spans a single
            #  column
            for i in range(self.__rows):
                if (i, j) in self.__cells:
                    cell = self.__cells[i, j]
                    if self.__cell_cols((i, j)) == 1:
                        wmax = max(wmax, cell.size_[0])

            #  check closed cells
            for i, nd in notdone.items():
                _, cw, ccols = nd
                if ccols == 1:
                    wmax = max(cw, wmax)

            #  update opened cells
            for i, nd in notdone.items():
                cij, cw, ccols = nd
                notdone[i] = cij, cw - wmax - hspacing, ccols - 1

            #  remove closing cells
            notdone = {k: v for k, v in notdone.items() if v[2] > 0}

            #  open new cells
            for i in range(self.__rows):
                if (i, j) in self.__cells:
                    cell = self.__cells[i, j]
                    cols = self.__cell_cols((i, j))
                    if cols > 1:
                        notdone[i] = \
                            (i, j), sizes[i, j][0] - wmax - hspacing, cols - 1

            assert self.__widths is not None
            self.__widths[j] = wmax

    def _iter_tree(
            self, rec: bool = True, traverse: bool = False
    ) -> Iterator[Node]:
        if rec:
            for cell in self.__cells.values():
                yield from cell.iter_tree(rec=True, traverse=traverse)
        else:
            yield from self.__cells.values()

    def _del_child(self, node: Node) -> None:
        super()._del_child(node)
        ij = next(ij for ij, n in self.__cells.items() if n == node)
        del self.__cells[ij]
        for d in (self.__rowspan, self.__colspan):
            if ij in d:
                del d[ij]
        self._reset_size()

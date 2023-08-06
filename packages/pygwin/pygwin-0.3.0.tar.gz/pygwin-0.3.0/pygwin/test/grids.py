#!/usr/bin/env python3

"""Document this method."""

from pygwin import Grid, Label, Window, Image, Media, TextBoard, Box, Frame


TITLE = 'grids'.title()


def get_window(win_sys):
    """grids window"""
    def add(img):
        def fun():
            def link():
                new.set_selected(not new.is_selected())
                return True
            new = Image(img.surface, link=link)
            grid.insert(0, new)
            return True
        return fun

    def delete():
        to_del = [img for img in grid if img.is_selected()]
        for node in to_del:
            grid.remove_node(node)
        return True
    size = 64, 64
    imgs = [
        Image(Media.get_image(f, scale=size))
        for f in ['elf.png', 'orc.png', 'dragon.png']
    ]
    for img in imgs:
        img.set_link(add(img))
    grid = Grid(style={'size': ('100%', None)})
    board = TextBoard(style={'size': ('100%', None)})
    board.push_text("""Click on an image to add it in the frame.  You can then
select images in the frame and click on delete to remove them from the frame.
The box in the frame will not hold more than 5 images per row.  Deletion will
automatically rearrange the box.""")
    box_main = Box(
        board,
        Box(*imgs,
            Label('delete', link=delete, style={'valign': 'center'}),
            style={'orientation': 'horizontal', 'halign': 'center'}),
        Frame(grid, style={'size': (400, 400)}))
    return Window(win_sys, box_main, title=TITLE)

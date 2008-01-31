#!/usr/bin/python

__all__ = ("Renderer", "ButtonRenderer", "BasicRenderer", "TextRenderer",
           "KineticRenderer", "KineticTextRenderer", "MultiImageRenderer",
           "EdjeKineticRenderer", )

import core
from kinetic import Kinetic
import evas
import edje


class Renderer(object):
    """Factory/updater for Evas Objects that represents a cell.

    You should either override C{render()} or use the default and implement
    C{create_cell()}, C{update_cell()} and C{show_cell()}.
    """
    def render(self, cell, row, list, x, y, w, h):
        self.list = list
        if cell is None:
            canvas = list.scroll_contents.toplevel_evas
            cell = self.create_cell(canvas)

        cell.data["row"] = row
        if row:
            self.update_cell(cell, row)

        self.show_cell(cell, x, y, w, h)
        return cell

    def create_cell(self, canvas):
        raise TypeError("create_cell() must be implemented by renderer")

    def update_cell(self, cell, row):
        raise TypeError("update_cell() must be implemented by renderer")

    def show_cell(self, cell, x, y, w, h):
        raise TypeError("show_cell() must be implemented by renderer")

    def delete(self):
        self.list = None


class KineticRenderer(Renderer):
    """Kinetic-aware base renderer.

    It will call the press() method when mouse down event happens, release()
    when the mouse goes up or the click was cancelled by a mouse move, and
    click() when a click in the cell happens.
    """
    def __init__(self, *a, **ka):
        Renderer.__init__(self, *a, **ka)

    def render(self, cell, row, list, x, y, w, h):
        self.list = list
        if cell is None:
            canvas = list.scroll_contents.toplevel_evas
            cell = self.create_cell(canvas)
            cell.on_mouse_down_add(self._mouse_down)
            cell.on_mouse_move_add(self._mouse_move)
            cell.on_mouse_up_add(self._mouse_up)
            cell.data["last_y"] = -1
            cell.data["cancel"] = False
            cell.propagate_events = True

        cell.data["row"] = row
        if row:
            self.update_cell(cell, row)

        self.show_cell(cell, x, y, w, h)
        return cell

    def _mouse_down(self, cell, ev, *a, **ka):
        cell.data["last_y"] = ev.position.canvas.y
        cell.data["cancel"] = False
        self.press(cell, cell.data["row"])

    def _mouse_move(self, cell, ev, *a, **ka):
        if (ev.buttons & 1) == 1:
            last_y = cell.data["last_y"]
            if last_y == -1:
                return
            if abs(last_y - ev.position.canvas.y) > Kinetic.threshold:
                cell.data["cancel"] = True
                self.release(cell, cell.data["row"])

    def _mouse_up(self, cell, ev, *a, **ka):
        cell.data["last_y"] = -1
        if not cell.data["cancel"]:
            row = cell.data["row"]
            self.click(cell, row)
            self.update_cell(cell, row)
            self.release(cell, row)

    def show_cell(self, cell, x, y, w, h):
        cell.move(x, y)
        cell.resize(w, h)
        cell.show()

    def press(self, cell, row):
        pass

    def release(self, cell, row):
        pass

    def click(self, cell, row):
        pass


class EdjeKineticRenderer(Renderer):
    """Kinetic-aware base renderer for Edje objects.

    It will call the press() method when mouse down event happens, release()
    when the mouse goes up or the click was cancelled by a mouse move, and
    click() when a click in the cell happens. It passes the part that
    triggered the event as argument also.
    """
    def __init__(self, *a, **ka):
        Renderer.__init__(self, *a, **ka)

    def render(self, cell, row, list, x, y, w, h):
        self.list = list
        if cell is None:
            canvas = list.scroll_contents.toplevel_evas
            cell = self.create_cell(canvas)
            cell.signal_callback_add("mouse,down,1", "*", self._mouse_down)
            cell.signal_callback_add("mouse,move", "*", self._mouse_move)
            cell.signal_callback_add("mouse,up,1", "*", self._mouse_up)
            cell.propagate_events = True
            cell.data["last_y"] = -1
            cell.data["cancel"] = False

        cell.data["row"] = row
        if row:
            self.update_cell(cell, row)

        self.show_cell(cell, x, y, w, h)
        return cell

    def _get_position(self, cell):
        return cell.evas.pointer_canvas_xy

    def _is_button_down(self, cell):
        return (cell.evas.pointer_button_down_mask & 1) == 1

    def _mouse_down(self, cell, emission, src):
        x, y = self._get_position(cell)
        cell.data["last_y"] = y
        cell.data["cancel"] = False
        self.press(cell, src, cell.data["row"])

    def _mouse_move(self, cell, emission, src):
        if self._is_button_down(cell):
            x, y = self._get_position(cell)
            last_y = cell.data["last_y"]
            if last_y == -1:
                return
            if abs(last_y - y) > Kinetic.threshold:
                cell.data["cancel"] = True
                self.release(cell, src, cell.data["row"])

    def _mouse_up(self, cell, emission, src):
        cell.data["last_y"] = -1
        if not cell.data["cancel"]:
            row = cell.data["row"]
            self.click(cell, src, row)
            self.update_cell(cell, row)
            self.release(cell, src, row)

    def show_cell(self, cell, x, y, w, h):
        cell.move(x, y)
        cell.resize(w, h)
        cell.show()

    def press(self, cell, part, row):
        pass

    def release(self, cell, part, row):
        pass

    def click(self, cell, part, row):
        pass


class ButtonRenderer(KineticRenderer):
    def __init__(self, label="", theme="button", label_theme="label",
                 click=None, *a, **ka):
        KineticRenderer.__init__(self)
        if not callable(click):
            raise ValueError("must supply a callable callback for click")
        self.click_cb = click
        self.label = label
        self.args = a
        self.kargs = ka
        self.theme = theme
        self.label_theme = label_theme

    def create_cell(self, canvas):
        cell = edje.Edje(canvas)
        core.theme_edje_object_set(cell, self.list.theme_file, self.theme)

        l = edje.Edje(canvas)
        core.theme_edje_object_set(l, self.list.theme_file, self.label_theme,
                                   "tree/button")
        l.part_text_set("etk.text.label", self.label)
        cell.data["label"] = l

        cell.part_swallow("etk.swallow.content", l)
        return cell

    def press(self, cell, row):
        cell.signal_emit("etk,state,pressed", "etk")

    def release(self, cell, row):
        cell.signal_emit("etk,state,released", "etk")

    def update_cell(self, cell, row):
        pass

    def show_cell(self, cell, x, y, w, h):
        cell.resize(w - 10, h - 10)
        cell.move(int(x + 5), int(y + 5))
        cell.show()

    def click(self, cell, row):
        self.click_cb(row, *self.args, **self.kargs)


class BasicRenderer(Renderer):
    def __init__(self, slot=None, theme=None, *a, **ka):
        Renderer.__init__(self, *a, **ka)
        if slot is None:
            raise ValueError("must supply a slot")
        self.slot = slot
        self.theme = theme


class TextRenderer(BasicRenderer):
    def __init__(self, *a, **ka):
        BasicRenderer.__init__(self, *a, **ka)
        if self.theme is None:
            self.theme = "text"

    def create_cell(self, canvas):
        cell = edje.Edje(canvas)
        core.theme_edje_object_set_from_parent(cell, self.theme, self.list)
        cell.pass_events = True
        return cell

    def update_cell(self, cell, row):
        cell.part_text_set("etk.text.label", row[self.slot].__str__())

    def show_cell(self, cell, x, y, w, h):
        min_w, min_h = cell.size_min_calc()
        cell.resize(min_w, min_h)
        cell.move(x, y + ((h - min_h) / 2))
        cell.show()


class ImageRenderer(KineticRenderer):
    def __init__(self, file_slot, key_slot=None, click=None, *a, **ka):
        KineticRenderer.__init__(self)
        self.file_slot = file_slot
        self.key_slot = key_slot
        self.click_cb = click
        self.args = a
        self.kargs = ka

    def create_cell(self, canvas):
        return canvas.FilledImage()

    def update_cell(self, cell, row):
        if self.key_slot:
            key = row[self.key_slot]
        else:
            key = None
        cell.file_set(row[self.file_slot], key)

    def click(self, cell, row):
        if self.click_cb:
            self.click_cb(row, *self.args, **self.kargs)


class KineticTextRenderer(KineticRenderer):
    def __init__(self, theme="text", slot=0, click=None, *a, **ka):
        KineticRenderer.__init__(self)
        self.click_cb = click
        self.slot = slot
        self.theme = theme
        self.args = a
        self.kargs = ka

    def create_cell(self, canvas):
        cell = edje.Edje(canvas)
        core.theme_edje_object_set_from_parent(cell, self.theme, self.list)
        return cell

    def update_cell(self, cell, row):
        cell.part_text_set("etk.text.label", row[self.slot].__str__())

    def show_cell(self, cell, x, y, w, h):
        min_w, min_h = cell.size_min_calc()
        cell.resize(int(w), min_h)
        cell.move(x, y + ((h - min_h) / 2))
        cell.show()

    def click(self, cell, row):
        if self.click_cb:
            self.click_cb(row, *self.args, **self.kargs)


class MultiImageRenderer(KineticRenderer):
    def __init__(self, images=[], state_slot=0, align=(0.0, 0.5), click=None,
                 *a, **ka):
        if not images:
            raise ValueError("must supply images")
        KineticRenderer.__init__(self)
        self.images = images
        self.state_slot = state_slot
        self.align = align
        self.click_cb = click
        self.args = a
        self.kargs = ka

    def create_cell(self, canvas):
        return canvas.FilledImage()

    def update_cell(self, cell, row):
        state = row[self.state_slot]
        file, key = self.images[state]
        cell.file_set(file, key)

    def show_cell(self, cell, x, y, w, h):
        iw, ih = cell.image_size
        ix = x + self.align[0] * (w - iw)
        iy = y + self.align[1] * (h - ih)
        cell.resize(iw, ih)
        cell.move(int(ix), int(iy))
        cell.show()

    def click(self, cell, row):
        if self.click_cb:
            self.click_cb(row, *self.args, **self.kargs)

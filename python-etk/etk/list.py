#!/usr/bin/python

__all__ = ("ListModel", "ListModelMixin", "List", "Kinetic", )

import core

from kinetic import Kinetic
import evas
import evas.decorators
import edje
import ecore

import math


class CallbackMixin(object):
    "Simple callback support for objects."
    def __init__(self):
        # Only one class in the hierarchy needs to call CallbackMixin.__init__()
        self._callbacks = []
        count = len([x for x in dir(self) if x.endswith("_CALLBACK")])

        for i in xrange(count):
            self._callbacks.append([])

        # TODO: automatic creation of on_NAME_add()/_del() helpers.

    def _emit(self, signal, *args):
        for c, a, ka in self._callbacks[signal]:
            c(self, *(args + a), **ka)

    def callback_add(self, signal, func, *a, **ka):
        self._callbacks[signal].append((func, a, ka))

    def callback_del(self, signal, func, *a, **ka):
        self._callbacks[signal].remove((func, a, ka))


class ListModelMixin(CallbackMixin):
    "Helper mixin to make easy implementation of model classes usable by List"

    MODEL_ADDED_CALLBACK, MODEL_REMOVED_CALLBACK, MODEL_CHANGED_CALLBACK = range(3)
    def __init__(self):
        CallbackMixin.__init__(self)

    def _elements_get(self):
        return self.elements_get()

    def elements_get(self):
        raise TypeError("No implementation for getting elements from ListModel")

    elements = property(_elements_get)

    def on_model_added(self, callback, *a, **ka):
        self.callback_add(self.MODEL_ADDED_CALLBACK, callback, *a, **ka)

    def on_model_removed(self, callback, *a, **ka):
        self.callback_add(self.MODEL_REMOVED_CALLBACK, callback, *a, **ka)

    def on_model_changed(self, callback, *a, **ka):
        self.callback_add(self.MODEL_CHANGED_CALLBACK, callback, *a, **ka)

    def emit_model_added(self, *a, **ka):
        self._emit(self.MODEL_ADDED_CALLBACK, *a, **ka)

    def emit_model_removed(self, *a, **ka):
        self._emit(self.MODEL_REMOVED_CALLBACK, *a, **ka)

    def emit_model_changed(self, *a, **ka):
        self._emit(self.MODEL_CHANGED_CALLBACK, *a, **ka)


class ListModel(ListModelMixin):
    "A list with callbacks for notifying about changes"

    def __init__(self, *a, **ka):
        self._elements = []
        ListModelMixin.__init__(self)

    def elements_get(self):
        return self._elements

    def __getitem__(self, i):
        return self._elements[i]

    def __setitem__(self, i, v):
        self._elements[i] = v
        self.emit_model_changed(i, v)

    def append(self, v):
        self._elements.append(v)
        self.emit_model_added(len(self._elements) - 1, v)

    def prepend(self, v):
        self._elements.insert(0, v)
        self.emit_model_added(0, v)

    def insert(self, i, v):
        self._elements.insert(i, v)
        self.emit_model_added(i, v)

    def remove(self, v):
        i = -1
        try:
            i = self._elements.index(v)
        except ValueError:
            return

        del self._elements[i]
        self.emit_model_removed(i, v)


class ListColumn(object):
    def __init__(self, width, renderer, expandable):
        self.width = width
        self.renderer = renderer
        self.expandable = expandable
        self.real_width = width


class ListVisibleRow(evas.ClippedSmartObject):
    def __init__(self, list, *a, **ka):
        evas.ClippedSmartObject.__init__(self, list.toplevel_evas)

        self.list = list
        self.sc = self.list.scroll_contents
        self.sc.member_object_add(self)

        self.clip = self.sc.content_clip

        # XXX: group
        self.bg = edje.Edje(self.evas_get())
        core.theme_edje_object_set_from_parent(self.bg, self.list.row_theme,
                                               self.list)
        self.bg.propagate_events = True
        self.member_add(self.bg)

        self.mask = self.evas_get().Rectangle()
        self.mask.propagate_events = True
        self.mask.color = (0, 0, 0, 0)
        self.member_add(self.mask)
        self.mask.raise_()

        self.cells = [None, ] * len(self.list.cols)
        self.row = None

    @evas.decorators.event_callback(evas.EVAS_CALLBACK_MOUSE_DOWN)
    def _mouse_down(self, ev):
        self.sc.kinetic.mouse_down(ev.position.canvas.y)

    @evas.decorators.event_callback(evas.EVAS_CALLBACK_MOUSE_MOVE)
    def _mouse_move(self, ev):
        if not (ev.buttons & 0x1) or \
                (ev.position.canvas.y == ev.prev_position.canvas.y):
            return
        self.sc.kinetic.mouse_move(ev.prev_position.canvas.y,
                                   ev.position.canvas.y)

    @evas.decorators.event_callback(evas.EVAS_CALLBACK_MOUSE_UP)
    def _mouse_up(self, ev):
        if self.sc.kinetic.mouse_up(ev.position.canvas.y):
            self.click()

    def show(self):
        evas.ClippedSmartObject.show(self)
        x, y, w, h = self.geometry
        self.bg.resize(w, h)
        self.bg.show()
        self.mask.resize(w, h)

        selected = self.row in self.list.selected_rows

        if selected:
            self.signal_emit("etk,state,selected")
        else:
            self.signal_emit("etk,state,unselected")

        cx = x
        for i, c in enumerate(self.list.cols):
            old_cell = self.cells[i]
            cell = c.renderer.render(old_cell, self.row, self.list, cx, y,
                                     c.real_width, h)
            if cell != old_cell:
                if old_cell:
                    old_cell.delete()
                self.cells[i] = cell
                self.member_add(self.cells[i])
            if isinstance(cell, edje.Edje):
                if selected:
                    cell.signal_emit("cell,state,selected", "")
                else:
                    cell.signal_emit("cell,state,unselected", "")
            cx += c.real_width

        self.mask.raise_()

    def hide(self):
        try:
            self.bg.hide()
        except AttributeError:
            return
        self.mask.hide()
        for c in self.cells:
            if c:
                c.hide()

    def resize(self, w, h):
        pass

    def click(self):
        self.list._emit(List.ROW_CLICKED_CALLBACK, self.row)
        if self.list.selectable != List.NOT_SELECTABLE:
            if self.row in self.list.selected_rows:
                self.list.unselect_row(self.row)
            else:
                self.list.select_row(self.row)

    def signal_emit(self, signal):
        self.bg.signal_emit(signal, "etk")

    def move_relative(self, dx=0, dy=0):
        x, y = self.pos
        self.move(x + dx, y + dy)


class ListScrollContents(core.Widget):
    def __init__(self, list, row_height, **kargs):
        core.Widget.__init__(self, **kargs)
        self.internal = True
        self.repeat_mouse_events = True
        self.list = list
        self.content_clip = None
        self.row_height = row_height
        self.on_realized(self.create_content_clip) # XXX: decorators
        self.visible_rows = []
        self.scroll_y = 0
        self.kinetic = Kinetic(self._kinetic_move, self._kinetic_state_change)
        self.on_destroyed(self._on_destroyed)

    def _on_destroyed(self, *ignored):
        for vr in self.visible_rows:
            vr.delete()
        self.visible_rows = []
        self.list = None
        self.kinetic = None
        return True

    def _kinetic_move(self, offset):
        if offset == 0:
            return False
        self.list.scrolled_view.vscrollbar.value -= offset
        return True

    def _show_scrollbar(self):
        self.list.scrolled_view.policy = (core.ScrolledView.HIDE,
                                          core.ScrolledView.SHOW)

    def _hide_scrollbar(self):
            self.list.scrolled_view.policy = (core.ScrolledView.HIDE,
                                              core.ScrolledView.HIDE)

    def _kinetic_state_change(self, scrolling):
        self._set_mask_visible_rows(scrolling)
        if scrolling:
            self._show_scrollbar()
        else:
            self._hide_scrollbar()

    def visible_range(self):
        if not self.list.rows:
            return (0, 0)

        first_row = self.visible_rows[0].row
        first = self.list.rows.index(first_row)
        h = self.geometry[3]
        count = int(math.ceil(float(h) / self.row_height))
        return (first, first + count - 1)

    def create_content_clip(self, obj, *a, **ka):
        self.content_clip = self.toplevel_evas.Rectangle()
        self.list.scrolled_view.member_object_add(self.content_clip)
        return True

    # XXX
    def _get_fixed_content_geometry(self):
        hpolicy, vpolicy = self.list.scrolled_view.policy
        x, y, w, h = self.geometry

        if vpolicy == core.ScrolledView.SHOW:
            sw, sh = self.list.scrolled_view.vscrollbar.size_request()
            w += sw

        return (x, y, w, h)

    def _size_allocate(self, x, y, w, h):
        if self.list._change_animator.running:
            return

        fx, fy, fw, fh = self._get_fixed_content_geometry()

        self.content_clip.move(fx, fy)
        self.content_clip.resize(w, fh)
        self.content_clip.show()

        self._create_visible_rows(h)
        self._update_visible_rows(fx, fy, fw, fh)

    def _scroll(self, x, y):
        if self.list._change_animator.running:
            self.scroll_y = y
            return
        dy = y - self.scroll_y
        self._move_visible_rows(dy)

    def _scroll_size_get(self, scrollview_w, scrollview_h, scrollbar_w,
                         scrollbar_h):
        return (self.list.real_width, len(self.list.rows) * self.row_height)

    def _create_visible_rows(self, h):
        count = len(self.visible_rows)
        new_count = (h / self.row_height) + 2

        if new_count == count:
            return
        elif new_count < count:
            for vr in self.visible_rows[new_count:count]:
                vr.delete()
            del self.visible_rows[new_count:count]
        else:
            for i in xrange(new_count - count):
                self.visible_rows.append(ListVisibleRow(self.list))

    def _update_visible_rows(self, x, y, w, h):
        rh = self.row_height
        delta_y = self.scroll_y % rh
        first = self.scroll_y / rh
        pos_y = y - delta_y

        rows = self.list.rows[first:(first + len(self.visible_rows))]
        rows_count = len(rows)

        for i, vr in enumerate(self.visible_rows):
            vr.geometry = (x, pos_y, w, rh)
            if i < rows_count:
                vr.row = rows[i]
                vr.show()
            else:
                vr.row = None
                vr.hide()
            pos_y += rh

    def _move_visible_rows(self, dy):
        first_before = self.scroll_y / self.row_height
        self.scroll_y += dy
        first_after = self.scroll_y / self.row_height

        dif = first_after - first_before
        if dif == 0:
            for vr in self.visible_rows:
                vr.move_relative(0, -dy)
        elif abs(dif) <= 2:
            self._move_visible_rows_swapping(dy, dif)
        else:
            self.redraw()

    def _move_visible_rows_swapping(self, dy, dif):
        if dy > 0:
            swaps = self.visible_rows[:dif]
            keeps = self.visible_rows[dif:]
            self.visible_rows = keeps + swaps
        else:
            swaps = self.visible_rows[dif:]
            keeps = self.visible_rows[:dif]
            self.visible_rows = swaps + keeps

        for vr in keeps:
            vr.move_relative(0, -dy)

        if dy > 0:
            new_x, new_y = keeps[-1].pos
            new_y += self.row_height
            row_idx = (self.scroll_y / self.row_height) + len(keeps)
        else:
            new_x, new_y = keeps[0].pos
            new_y -= self.row_height * len(swaps)
            row_idx = self.scroll_y / self.row_height

        for vr in swaps:
            if row_idx < len(self.list.rows):
                vr.row = self.list.rows[row_idx]
            else:
                vr.row = None
            vr.move(new_x, new_y)
            vr.show()
            new_y += self.row_height
            row_idx += 1

    def _set_mask_visible_rows(self, mask, propagate=True):
        if mask:
            for vr in self.visible_rows:
                vr.mask.propagate_events = propagate
                vr.mask.show()
        else:
            for vr in self.visible_rows:
                vr.mask.propagate_events = propagate
                vr.mask.hide()

    def redraw(self):
        self._update_visible_rows(*self.geometry)


class ChangeAnimator(object):
    step = 8

    def __init__(self, list):
        self.list = list
        self.running = False
        self.animator = None

    def stop(self):
        pass

    def run(self):
        if self.running:
            return

        self.running = True
        self.list.scroll_contents._set_mask_visible_rows(True, False)
        self._prepare()

    def _prepare(self):
        if not self.list._change_queue:
            self.running = False
            self.list.scroll_contents._hide_scrollbar()
            self.list.scroll_contents._set_mask_visible_rows(False)
            return

        self.pos, self.row, self.added = self.list._change_queue.pop(0)

        first, last = self.list.scroll_contents.visible_range()
        self.rel_pos = self.pos - first

        if self.pos < first:
            self._start(self._offscreen_animation, True)
        elif self.pos > last:
            self._start(self._offscreen_animation, False)
        else:
            self._start(self._animation)


    def _start(self, func, *a):
        if self.animator is not None or not self.running:
            return

        self.remaining = -1
        self.animator = ecore.animator_add(func, *a)

    def _setup_visible_row(self):
        visible_rows = self.list.scroll_contents.visible_rows

        if self.added:
            vr = visible_rows.pop()
            vr.row = self.row

            x, y, w, h = visible_rows[self.rel_pos].geometry

            vr.geometry = x, y - self.list.row_height, w, h
            vr.lower()
            vr.show()

            visible_rows.insert(self.rel_pos, vr)
            self.vr = vr
        else:
            # XXX: fill the first hidden VR because it will show up during
            # the animation
            vr = visible_rows.pop(self.rel_pos)
            vr.geometry = visible_rows[-1].geometry
            vr.row = None
            vr.hide()
            visible_rows.append(vr)
            self.vr = vr

    def _offscreen_animation(self, update_position, *ignored):
        # Setup a new animation
        if self.remaining == -1:
            self.list.scroll_contents._show_scrollbar()
            if self.added:
                self.list._add_row(self.pos, self.row)
            else:
                self.list._remove_row(self.pos, self.row)
            self.remaining = self.list.row_height
            return True

        # Animation ended
        elif self.remaining == 0:
            self.list.redraw_queue()
            self.animator = None
            self._prepare()
            return False

        if self.remaining < self.step:
            step = self.remaining
        else:
            step = self.step

        self._update_scrollbar(step, update_position)

        self.remaining -= step
        return True

    def _update_scrollbar(self, step, update_position):
        lower, upper = self.list.scrolled_view.vscrollbar.range

        if self.added:
            if update_position:
                self.list.scrolled_view.vscrollbar.value += step
            self.list.scrolled_view.vscrollbar.range = lower, upper + step
        else:
            if update_position:
                self.list.scrolled_view.vscrollbar.value -= step
            self.list.scrolled_view.vscrollbar.range = lower, upper - step

    def _animation(self, *ignored):
        # Setup a new animation
        if self.remaining == -1:
            self.list.scroll_contents._hide_scrollbar()
            if self.added:
                self.list._add_row(self.pos, self.row)
            self._setup_visible_row()
            self.remaining = self.list.row_height
            return True

        # Animation ended
        elif self.remaining == 0:
            if not self.added:
                self.list._remove_row(self.pos, self.row)
            self.list.redraw_queue()
            self.animator = None
            self._prepare()
            return False

        if self.remaining < self.step:
            step = self.remaining
        else:
            step = self.step

        if self.added:
            self._animation_added(step)
        else:
            self._animation_removed(step)

        self.remaining -= step
        return True

    def _animation_added(self, step):
        self.vr.move_relative(0, step)
        after = self.list.scroll_contents.visible_rows[(self.rel_pos + 1):]
        for v in after:
            v.move_relative(0, step)

    def _animation_removed(self, step):
        after = self.list.scroll_contents.visible_rows[self.rel_pos:]
        for v in after:
            v.move_relative(0, -step)


class List(core.Widget, CallbackMixin):
    NOT_SELECTABLE, SINGLE_SELECTABLE, MULTI_SELECTABLE = range(3)
    ROW_SELECTED_CALLBACK, ROW_UNSELECTED_CALLBACK, ROW_CLICKED_CALLBACK = range(3)

    def __init__(self, model=None, columns=[], selectable=0,
                 row_height=60, theme_group="tree", row_theme="row",
                 animated_changes=False, **kargs):
        core.Widget.__init__(self, **kargs)
        CallbackMixin.__init__(self)
        self._init_scrolled_view()
        self._init_scroll_contents(row_height)
        self._init_columns(columns)

        self.frozen = False

        self._model = None
        self._change_animator = ChangeAnimator(self)
        self._animated_changes = animated_changes
        self._model_set(model)

        self.selectable = selectable
        self.selected_rows = []

        self.focusable = True
        self.theme_group = theme_group
        self.row_theme = row_theme

        # Focus on Click
        self.on_mouse_down(self._get_focus)

        self.on_destroyed(self._on_destroyed)

    def _on_destroyed(self, obj):
        self.scroll_contents.kinetic.stop()
        if self._model is not None:
            self._model.callback_del(ListModel.MODEL_ADDED_CALLBACK,
                                     self._on_model_added)
            self._model.callback_del(ListModel.MODEL_REMOVED_CALLBACK,
                                     self._on_model_removed)
            self._model.callback_del(ListModel.MODEL_CHANGED_CALLBACK,
                                     self._on_model_changed)
        self._model = None
        self._change_animator.stop()
        self._change_animator = None

        for c in self.cols:
            c.renderer.delete()

        self.cols = None
        self.selected_rows = None

        self.scrolled_view = None
        self.scroll_contents = None

        return True

    def _get_focus(self, *ignored):
        self.focus = True
        return True

    def _init_scrolled_view(self):
        sv = core.ScrolledView(policy=(core.ScrolledView.HIDE,
                                       core.ScrolledView.HIDE))
        sv.parent = self
        sv.theme_parent = self
        sv.internal = True
        sv.repeat_mouse_events = True
        sv.show()
        self.scrolled_view = sv

    def _init_scroll_contents(self, row_height):
        sc = ListScrollContents(self, row_height) # XXX: get from theme
        self.scrolled_view.add(sc)
        sc.show()
        self.scroll_contents = sc

    def _init_columns(self, cols):
        self.cols = []
        self.width = 0
        self.real_width = 0
        for w, r, e in cols:
            self.column_add(w, r, e)

    def column_add(self, width, renderer, expandable=True):
        self.cols.append(ListColumn(width, renderer, expandable))
        self.width += width

    def _size_request(self):
        (vs_w, vs_h) = self.scrolled_view.vscrollbar.size_request(0) # XXX
        return (self.width + vs_w, self.row_height)

    def _size_allocate(self, x, y, w, h):
        self._update_cols_real_width(w)
        self.scrolled_view.size_allocate(x, y, w, h)

    def _update_cols_real_width(self, total):
        fixed = 0
        for c in self.cols:
            if not c.expandable:
                fixed += c.width
        if self.width == fixed:
            return

        proportion = float(total - fixed) / float(self.width - fixed)
        for c in self.cols:
            if c.expandable:
                c.real_width = c.width * proportion
            else:
                c.real_width = c.width
        self.real_width = total

    def _row_height_set(self, rh):
        self.scroll_contents.row_height = rh

    def _row_height_get(self):
        return self.scroll_contents.row_height

    row_height = property(_row_height_get, _row_height_set) # XXX: doc

    def select_row(self, row):
        if self.selectable == self.NOT_SELECTABLE:
            return
        self._select_row(row)
        self.scroll_contents.redraw()

    def _select_row(self, row):
        if row in self.selected_rows:
            return
        if self.selectable == self.SINGLE_SELECTABLE:
            self._unselect_all_rows()
        self.selected_rows.append(row)
        self._emit(self.ROW_SELECTED_CALLBACK, row)

    def unselect_row(self, row):
        if self.selectable == self.NOT_SELECTABLE:
            return
        self._unselect_row(row)
        self.scroll_contents.redraw()

    def _unselect_row(self, row):
        if row in self.selected_rows:
            self.selected_rows.remove(row)
            self._emit(self.ROW_UNSELECTED_CALLBACK, row)

    def unselect_all_rows(self):
        if self.selectable == self.NOT_SELECTABLE:
            return
        self._unselect_all_rows()
        self.scroll_contents.redraw()

    def _unselect_all_rows(self):
        for row in self.selected_rows:
            self.selected_rows.remove(row)
            self._emit(self.ROW_UNSELECTED_CALLBACK, row)

    def on_row_selected(self, callback, *a, **ka):
        self.callback_add(self.ROW_SELECTED_CALLBACK, callback, *a, **ka)

    def on_row_unselected(self, callback, *a, **ka):
        self.callback_add(self.ROW_UNSELECTED_CALLBACK, callback, *a, **ka)

    def on_row_clicked(self, callback, *a, **ka):
        self.callback_add(self.ROW_CLICKED_CALLBACK, callback, *a, **ka)

    def freeze(self):
        #if self.frozen:
        #    return
        self.frozen = True

    def thaw(self):
        if not self.frozen:
            return
        self._change_queue_flush()
        self.scroll_contents.redraw()
        self.frozen = False

    def _add_row(self, pos, row):
        self.rows.insert(pos, row)

    def _remove_row(self, pos, row):
        if row in self.selected_rows:
            self.selected_rows.remove(row)
        del self.rows[pos]

    def _queue_row(self, pos, row, added):
        self._change_queue.append((pos, row, added))

    def _change_queue_flush(self):
        for pos, row, added in self._change_queue:
            if added:
                self._add_row(pos, row)
            else:
                self._remove_row(pos, row)
        self._change_queue = []

    def _on_model_added(self, model, pos, row):
        if self.animated_changes:
            self._queue_row(pos, row, added=True)
            if not self.frozen:
                self._change_animator.run()
        else:
            self._add_row(pos, row)
            if not self.frozen:
                self.scroll_contents.redraw()

    def _on_model_removed(self, model, pos, row):
        if self.animated_changes:
            self._queue_row(pos, row, added=False)
            if not self.frozen:
                self._change_animator.run()
        else:
            self._remove_row(pos, row)
            if not self.frozen:
                self.scroll_contents.redraw()

    def _on_model_changed(self, model, pos, row):
        if not self.frozen:
            self.scroll_contents.redraw()

    def _model_get(self):
        return self._model

    def _model_set(self, model):
        if self._model is not None:
            self._model.callback_del(ListModel.MODEL_ADDED_CALLBACK,
                                     self._on_model_added)
            self._model.callback_del(ListModel.MODEL_REMOVED_CALLBACK,
                                     self._on_model_removed)
            self._model.callback_del(ListModel.MODEL_CHANGED_CALLBACK,
                                     self._on_model_changed)

        self._model = model

        self._change_animator.stop()
        self._change_queue = []
        self.rows = list(self._model.elements)

        self._model.on_model_added(self._on_model_added)
        self._model.on_model_removed(self._on_model_removed)
        self._model.on_model_changed(self._on_model_changed)
        self.scrolled_view.vscrollbar.value = 0
        self.redraw_queue()

    model = property(_model_get, _model_set)

    def _animated_changes_get(self):
        return self._animated_changes

    def _animated_changes_set(self, v):
        if self._animated_changes == v:
            return

        self._animated_changes = v
        if not self._animated_changes:
            self._change_queue_flush()
            if not self.frozen:
                self.scroll_contents.redraw()

    animated_changes = property(_animated_changes_get, _animated_changes_set)

    def _scroll_to(self, row, interval, pos_offset, y_offset):
        try:
            pos = self.rows.index(row)
        except ValueError:
            return

        to_y = (self.row_height * (pos + pos_offset)) + y_offset
        if to_y < 0:
            to_y = 0

        self.scroll_contents.kinetic.force_move( \
            self.scroll_contents.scroll_y, to_y, interval)

    def scroll_top_to(self, row, interval=0.5):
        self._scroll_to(row, interval, 0, 0)

    def scroll_middle_to(self, row, interval=0.5):
        x, y, w, h = self.scroll_contents.geometry
        y_offset = -((h / 2) - (self.row_height / 2))
        self._scroll_to(row, interval, 0, y_offset)

    def scroll_bottom_to(self, row, interval=0.5):
        x, y, w, h = self.scroll_contents.geometry
        pos_offset = -((h / self.row_height) - 1)
        y_offset = -(h % self.row_height)
        self._scroll_to(row, interval, pos_offset, y_offset)

import ecore


class Kinetic(object):
    accel_constant = 0.7
    min_movement = 0.1
    min_speed = 10.0
    threshold = 20
    drag_only_threshold = 3

    def __init__(self, move_offset, state_change=None):
        """Creates a new state object to simulate kinetic scroll behaviour.

        C{move_offset} is a function to be called when some movement should
        happen because of a drag or kinetic scroll. Return True if the
        movement happened or False if no scrolling is possible, which will
        stop the animation.

        C{state_change} is a function called whenever scrolling state change,
        so you can show/hide UI elements that only show up in scrolling state.
        """
        self.move_offset = move_offset
        self.state_change = state_change
        self.animation = None

        self.first_value = 0
        self.base_value = 0

        self.time = 0.0
        self.speed = 0.0
        self.accel = 0.0

        self.cancel_kinetic = False
        self.cancel_click = False

        self.forced = False
        self.forced_goal = 0

    def mouse_down(self, value):
        """Feeds object with a mouse down event at value.

        @return: False if the animation stopped, otherwise True.
        """
        scrolling = True
        self.cancel_kinetic = self.cancel_click = False

        if self.animation:
            self.animation.stop()
            self.animation = None
            scrolling = False
            self.cancel_kinetic = self.cancel_click = True

        self.first_value = self.base_value = value
        self.time = ecore.time_get()

        return scrolling

    def stop(self):
        "Stops the animation if it's happening."
        if self.animation:
            self.animation.stop()
            self.animation = None
            if self.state_change:
                self.state_change(False)

    def _animation(self):
        "Calculates an offset to move and calls the move_offset."
        t = ecore.time_get()
        dt = t - self.time
        ddv = (self.speed * dt) + (0.5 * self.accel * dt * dt)
        dv = int(ddv)

        if dt < ecore.animator_frametime_get() / 2.0:
            return True

        if self.forced:
            if self.forced_goal == 0:
                self.stop()
                return False

            if -1 < dv < 1:
                dv = int(self.speed / abs(self.speed))

            if self.forced_goal < abs(dv):
                if dv < 0:
                    dv = -(self.forced_goal)
                else:
                    dv = self.forced_goal
                self.forced_goal = 0
            else:
                self.forced_goal -= abs(dv)

        else: # not forced
            if abs(ddv) < self.min_movement and \
                    abs(self.speed) < self.min_speed:
                self.stop()
                return False

        self.speed = self.speed + (self.accel * dt)
        self.time = t

        moved = self.move_offset(dv)

        # Stop animation if move_offset couldn't move anymore or if already
        # crossed speed zero (stop) line.
        if not moved or (self.speed * self.accel) > 0:
            self.stop()
            return False

        return True

    def mouse_up(self, value):
        """Feeds object with mouse up event at value.

        @return: True if a click happened, False otherwise.
        """
        # If it's just a small movement and click was not cancelled yet,
        # this is a click.
        delta_first = value - self.first_value
        if abs(delta_first) < self.threshold and not self.cancel_click:
            if self.state_change:
                self.state_change(False)
            self.cancel_click = False
            return True

        # A very slow drag cause the kinetic scroll to stop.
        if self.cancel_kinetic:
            if self.animation:
                self.animation.stop()
                self.animation = None
            if self.state_change:
                self.state_change(False)
            return False

        # Set the values and create the animation
        t = ecore.time_get()
        dt = t - self.time
        dv = value - self.base_value

        self.time = t
        self.speed = dv / dt
        self.accel = -(self.speed * self.accel_constant)
        self.forced = False

        if not self.animation:
            if self.state_change:
                self.state_change(True)
            self.animation = ecore.animator_add(self._animation)

        return False

    def mouse_move(self, prev_value, value):
        "Feeds object with mouse move event from prev_value to value."
        # A very slow drag (identified by a small mouse_move event) will
        # cause the kinetic scroll to be cancelled when the mouse goes up.
        dv = value - prev_value
        self.cancel_kinetic = (abs(dv) < self.drag_only_threshold)

        self.move_offset(dv)

        # If you drag over the threshold, it's a way to cancel a click
        # before mouse goes up.
        delta_first = value - self.first_value
        if not self.cancel_click and abs(delta_first) > self.threshold:
            if self.state_change:
                self.state_change(True)
            self.cancel_click = True

        # If movement changed orientation, reset kinetic information.
        delta_base = value - self.base_value
        if dv * delta_base < 0:
            self.base_value = prev_value
            self.time = ecore.time_get()

    def force_move(self, from_value, to_value, interval):
        """Animate movement from one value to another in some interval.

        This function will try to calculate the correct speed for the animation
        to respect the interval.
        """
        if from_value == to_value:
            if self.state_change:
                self.state_change(False)
            return

        # Note that we invert things here because other functions usually
        # take the MOUSE GESTURE and move the other way around
        dv = from_value - to_value
        self.speed = dv / (interval * \
                               (1 - (0.5 * self.accel_constant * interval)))
        self.accel = -(self.speed * self.accel_constant)
        self.time = ecore.time_get()
        self.cancel_click = True

        self.forced_goal = abs(dv)
        self.forced = True

        if not self.animation:
            if self.state_change:
                self.state_change(True)
            self.animation = ecore.animator_add(self._animation)

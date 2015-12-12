# -*- coding: utf-8 -*-
"""
Created on Fri Dec 04 22:39:16 2015

@author: H.Gens
"""
import matplotlib.pyplot as plt
from screeninfo import get_monitors



class GridCreator(object):
    """
    Defines a class that creates a grid of matplotlib figures.
    """

    def __init__(self, rows=3, cols=6, monitor_start=0, prop={}):
        """
        Initializes the grid.

        'rows' is the number of rows in the grid.  It can also be
        thought of as the number of figures in one column.

        'cols' is the number of columns in the grid.  It can also be
        thought of as the number of figures in one row.

        'monitor_start' is either a list of indicies or a single
        integer index.  The values correspond to the positions within
        the list returned by the get_monitors() function.  If it's a
        list, then these are the monitors to use.  If it's an integer,
        this is the monitor where the figure grid begins.  The grid
        grows toward larger indexed monitors and then wraps back
        around.

        'prop' is a dict that provides minor tweaks to how figure
        dimensions are calculated.  The defaults should be sufficient
        for most cases.  It describes the OS-dependent container
        (titlebar, borders) drawn around each window.  It also
        describes the Windows Start Menu placement/dimensions, which
        are used to ensure the grid's figures aren't obscured by the
        Start Menu.
        """
        # Argument validation.
        self.monitors = GridCreator.validate_inputs(
            cols, rows, monitor_start
        )
        self.rows = rows
        self.cols = cols

        # Each window has an OS-dependent container that occupies
        # space.  This must be accounted for when creating the figure.
        # The values below are appropriate for the Windows 7 Aero theme
        # and are in pixels.
        self.container_x_left = prop.get('container x left', 8)
        self.container_x_right = prop.get('container x right', 8)
        self.container_y_top = prop.get('container y top', 30)
        self.container_y_bot = prop.get('container y bot', 8)
        # Height of the Windows 7 start menu in pixels.  This portion
        # of the monitor is considered unavailable and assumed located
        # at the bottom of the monitor.  What is that?  You have it
        # located somewhere else?  YOU'RE CRAZY!
        self.start_menu_y = prop.get('start menu y', 36)


    @staticmethod
    def validate_figures(figures):
        """
        This function validates the argument to create().  It also
        redefines the 'figures' arg if it's not a list.
        """
        # 'figures' must be an integer or a list of integers.
        error_string = 'figures arg must be integers or list of integers'
        if isinstance(figures, int):
            figures = range(1, figures + 1)
        elif isinstance(figures, list) or isinstance(figures, tuple):
            if len(figures) == 0:
                raise ValueError(error_string)
            for value in figures:
                if not isinstance(value, int):
                    raise ValueError(error_string)
        else:
            raise ValueError(error_string)
        return figures


    @staticmethod
    def validate_inputs(rows, cols, monitor_start):
        """
        This function validates the arguments to __init__().  It also
        returns a sorted 'monitors' list containing monitor details.
        """
        # Get the monitor information from screeninfo.get_monitors().
        monitors = get_monitors()
        # It's necessary to sort the result so that the far left monitor is
        # positioned first.
        monitors = sorted(monitors, key=lambda monitor: monitor.x)

        # 'rows', 'cols' must be real, positive numbers.
        if isinstance(rows, int) or isinstance(rows, float):
            if rows < 1:
                raise ValueError('rows arg must be greater than unity')
        else:
            raise ValueError('rows arg must be a numeric')
        if isinstance(cols, int) or isinstance(cols, float):
            if cols < 1:
                raise ValueError('cols arg must be greater than unity')
        else:
            raise ValueError('cols arg must be a numeric')

        # 'monitor_start' must be a single integer or a list of integers.
        error_string = (
            'monitor_start arg must be an integer or list of integers'
        )
        if isinstance(monitor_start, int):
            if monitor_start > len(monitors) - 1:
                error_string = (
                    'only %d monitors detected but monitor_start says to '
                    'start on monitor %d' % (len(monitors), monitor_start + 1)
                )
                raise ValueError(error_string)
        elif isinstance(monitor_start, list) or \
                isinstance(monitor_start, tuple):
            if len(monitor_start) == 0:
                raise ValueError(error_string)
            for value in monitor_start:
                if not isinstance(value, int):
                    raise ValueError(error_string)
                elif value > len(monitors) - 1:
                    error_string = (
                        'only %d monitors detected but monitor_start contains '
                        'monitor %d' % (len(monitors), value + 1)
                    )
                    raise ValueError(error_string)
        else:
            raise ValueError(error_string)

        # Rearrange or reduce the 'monitors' list depending on the value of
        # 'monitor_start'.
        if isinstance(monitor_start, int):
            monitors = monitors[monitor_start: ] + monitors[0: monitor_start]
        else:
            monitors = [monitors[i] for i in monitor_start]

        return monitors


    def close(self, figures=None):
        """
        Closes open matplotlib windows by calling pyplot.close().

        'figures' is an integer, list of integers, or None.  If an
        integer, then that specific window is closed.  If a list, then
        all figures in that list are closed.  If None, then all open
        figures are closed.
        """
        if figures is None:
            plt.close('all')
            return

        if isinstance(figures, int):
            plt.close(figures)
            return

        if isinstance(figures, list) or isinstance(figures, tuple):
            for figure in figures:
                if isinstance(figure, int):
                    plt.close(figure)


    def create(self, figures):
        """
        Creates a uniform grid of matplotlib figures across multiple
        monitors, depending on how the class was initialized.

        If 'figures' is an integer, figures 1 through 'figures' are
        created.  Otherwise, 'figures' should be a list of integer
        figure numbers.
        """
        # Argument validation.
        figures = GridCreator.validate_figures(figures)

        # Get the required instance variables.
        rows = self.rows
        cols = self.cols
        monitors = self.monitors
        container_x_left = self.container_x_left
        container_x_right = self.container_x_right
        container_y_top = self.container_y_top
        container_y_bot = self.container_y_bot
        start_menu_y = self.start_menu_y

        # Maximum number of figures per monitor.
        max_fpm = rows * cols

        # Create each figure and figure out where it belongs.
        for i, fig in enumerate(figures):
            # Pivot to a new monitor if we've run out of space.  The
            # modulus expression sets monitor_index to [0, ..., N, 0,
            # ..., N, 0, ...], where N is the length of 'monitors'.
            # Without the modulus expression, 'monitor_index' would
            # grow unchecked.
            monitor_index = int(i / max_fpm) % len(monitors)
            monitor = monitors[monitor_index]

            # Determine the dimensions of the figure within the given
            # monitor.  These dimensions are a function of the
            # monitor's resolution.
            monitor_res_x = monitor.width
            monitor_res_y = monitor.height - start_menu_y
            width = monitor_res_x / (cols * 1.0)
            height = monitor_res_y / (rows * 1.0)

            # Compute the local figure number as if the other monitors
            # didn't exist.  This number is 0-indexed and varies from 0
            # to max_fpm-1.
            fignum_local = i % max_fpm

            # Compute the current row and column to which the figure
            # belongs.  Together, these define the coordinates of the
            # current figure.  These variables are zero-indexed, and
            # the (0, 0) position is in the top left corner of the
            # monitor.
            current_row = int(fignum_local / cols)
            current_col = fignum_local - int(current_row * cols)

            # Get the monitor's origin, which is the top left corner of
            # the monitor.
            x, y = monitor.x, monitor.y

            # Calculate the x/y coordinates of the to-be-created
            # window.  The coordinates passed to setGeometry() are the
            # top left corner of the window excluding the container.
            x += current_col * width + container_x_left
            y += current_row * height + container_y_top

            plt.figure(fig)
            m = plt.get_current_fig_manager()
            # Some notes about setGeometry():
            # - x, y are not the true top left corner of the window.
            #   Instead, they indicate the top left corner of the
            #   inner, non-container window.
            # - The window's container (e.g., titlebar) does not count
            #   towards the total requested width/height.  The OS is
            #   responsible for adding the container.
            m.window.setGeometry(
                x, y,
                width - (container_x_left + container_x_right),
                height - (container_y_top + container_y_bot)
            )


# ------------------
# standalone use
# ------------------
if __name__ == '__main__':
    figures = 8
    rows, cols = 2, 3
    plt.close('all')

    gc = GridCreator(rows, cols)
    gc.create(figures)

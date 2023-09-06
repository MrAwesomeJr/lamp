import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from mpl_toolkits.axes_grid1 import make_axes_locatable
from cycler import cycler
import time


class Plot:
    # displays on matplotlib
    # mostly thanks to Kai Wong

    # what does n_colors do?
    def __init__(self, leds=50, **kwargs):

        self.strip = None
        self._fig, self._ax = plt.subplots( figsize = (10,10))
        self._fig.suptitle( __class__.__name__ )

        # Construct left and top axes
        # ref https://matplotlib.org/3.1.0/gallery/axes_grid1/scatter_hist_locatable_axes.html#sphx-glr-gallery-axes-grid1-scatter-hist-locatable-axes-py

        divider = make_axes_locatable( self._ax)
        self._top_ax = divider.append_axes( "top", 1.2, pad=0.2, sharex= self._ax)
        self._left_ax = divider.append_axes( "left", 1.2, pad=0.2, sharey= self._ax )

        # Customize axes

        self._ax.set_xlabel( 'time')
        self._ax.set_ylabel( 'pixel')
        self._ax.yaxis.set_ticks_position('right')
        self._ax.yaxis.set_label_position('right')

        self._top_ax.set_xlabel('time')
        self._top_ax.set_ylabel('color')
        self._top_ax.xaxis.set_ticks_position('top')
        self._top_ax.xaxis.set_label_position('top')

        self._left_ax.set_xlabel('color')
        self._left_ax.set_ylabel('pixel')

        custom_cycler = cycler(color=['r', 'g', 'b'] )
        self._top_ax.set_prop_cycle(custom_cycler)
        self._left_ax.set_prop_cycle(custom_cycler)

        # Get line objects for set_data on mouse move

        self._center_v_line = self._ax.axvline(np.nan, color ='k', linewidth = 1, alpha = 0.5)
        self._center_h_line = self._ax.axhline(np.nan, color ='k', linewidth = 1, alpha = 0.5)
        self._left_h_line = self._left_ax.axhline(np.nan, color ='k', linewidth = 1, alpha = 0.5)
        self._top_v_line = self._top_ax.axvline(np.nan, color ='k', linewidth = 1, alpha = 0.5)

        # Event handler

        self._fig.canvas.mpl_connect('motion_notify_event', lambda e: self._on_move(e))

        # Initialise data

        self._data = np.empty(shape = (  leds, 0, 3 ), dtype = int ) # need int here otherwise imshow would think it is float and rgb range 0-1

    def _on_move(self, event):

        # ref https://stackoverflow.com/questions/59144464/plotting-two-cross-section-intensity-at-the-same-time-in-one-figure

        if event.inaxes is self._ax :
                cur_x = event.xdata
                cur_y = event.ydata

                self._center_v_line.set_xdata([cur_x, cur_x])
                self._center_h_line.set_ydata([cur_y, cur_y])
                self._left_h_line.set_ydata([cur_y, cur_y])
                self._top_v_line.set_xdata([cur_x, cur_x])


                for i, line in enumerate(self._left_lines):
                    line.set_xdata(self._data[ :, int(cur_x), i])

                for i, line in enumerate( self._top_lines ) :
                    line.set_ydata(  self._data[ int(cur_y), :, i ])

    def show(self, strip, **kwargs):
        self.start_time = time.perf_counter()

        self.strip = strip

        # add existing info to self._data
        self._data = np.transpose(np.array(list(update.color for update in self.strip.buffer)), axes=(1, 0, 2))

        self._im = self._ax.imshow( self._data, interpolation = 'none' )
        self._ax.set_aspect('auto')

        t = 0
        p = 0

        self._left_lines = self._left_ax.plot( self._data[:, t],  range( 0, self._data.shape[0] ), drawstyle='steps-post' )
        self._top_lines = self._top_ax.plot( range( 0, self._data.shape[1] ), self._data[ p, : ], drawstyle='steps-post',)

        # animation object for consistent updates

        self._animation = FuncAnimation(self._fig, self._update, blit=True, cache_frame_data=False)

        # plt.show() is a blocking call?

        plt.show()

    def _update(self, frame):
        # returns the value for matplotlib's animation frame

        self._data = np.transpose(np.array(list(update.color for update in self.strip.buffer)), axes=(1, 0, 2))
        self._im.set_data(self._data)

        self.strip.set_timestamp(time.perf_counter() - self.start_time)


        return self._top_lines + self._left_lines + [self._im, self._center_v_line, self._center_h_line, self._left_h_line, self._top_v_line]

    def __call__(self, values ) :

        self._data = np.insert( self._data, self._data.shape[1], values, axis=1)
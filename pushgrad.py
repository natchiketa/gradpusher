#!/usr/bin/env python

# GIMP Python plug-in to generate call to the pushgrad SCSS mixin.
# Copyright 2012 Sal Lara <sal.lara@gmail.com>
#
#   This program is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation; either version 3 of the License, or
#   (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with this program.  If not, see <http://www.gnu.org/licenses/>.

#
# Note: gimpfu.py is the most up-to-date list of UI items.

from gimpfu import *
import gtk

GRADIENT_TYPES           = ('linear', 'radial')
GRADIENT_SHAPES          = ('ellipse', 'circle')
RADIAL_GRADIENT_SIZES    = ("closest-side", "farthest-side", "closest-corner", "farthest-corner")

def pushgrad(
        gradient_type, gradient_shape, angle, image, radial_pos_horiz, radial_pos_vert,
        radial_size, use_gradient_name, gradient_name, prefix, gradient
    ):

    img = image
    sel = pdb.gimp_selection_bounds(img)
    left, top = sel[1], sel[2]
    width = sel[3] - left
    height = sel[4] - top

    # map parameter indices to their respective string values
    gradient_type  = GRADIENT_TYPES[gradient_type]
    gradient_shape = GRADIENT_SHAPES[gradient_shape]
    radial_size    = RADIAL_GRADIENT_SIZES[radial_size]

    # save the current gradient for resetting after finished
    current_gradient = pdb.gimp_context_get_gradient()
    pdb.gimp_context_set_gradient(gradient)
    if use_gradient_name:
        active_gradient_name = pdb.gimp_context_get_gradient(img).replace(prefix, '')
        grad_colors = {'linear':active_gradient_name,'radial':active_gradient_name}
    else:
        grad_colors = {'linear':gradient_name,'radial':gradient_name}

    # set the active gradient back to what it was before we changed it
    pdb.gimp_context_set_gradient(current_gradient)

    # append 'deg' to the angle value to match the linear-gradient parameter syntax
    angle = '%sdeg' % angle

    # concatenate to build the whole radial-gradient position value
    grad_position  = '%s %s' % (radial_pos_horiz, radial_pos_vert)
    grad_linear    = 'ling(%s, (%s)' % (angle, grad_colors[gradient_type])
    grad_radial    = 'radg(%s, %s, %s, (%s)' % (gradient_shape, radial_size, grad_position, grad_colors[gradient_type])
    grad_types     = {'linear': grad_linear, 'radial': grad_radial}

    pushgrad_call = '$gv: pushgrad(%s, (%dpx %dpx), (%dpx %dpx), $s));' % (grad_types[gradient_type], left, top, width, height)

    # get the clipboard
    clipboard = gtk.clipboard_get()
    # set the clipboard text data
    clipboard.set_text(pushgrad_call)

    pdb.gimp_progress_set_text(pushgrad_call)

    return

register(
    "python_fu_pushgrad",
     "Generate call to the pushgrad SCSS mixin",
     "Generate call to the pushgrad SCSS mixin",
     "Sal Lara", "Sal Lara",
     "2012",
     "Pushgrad mixin call...",
    "",      # Alternately use RGB, RGB*, GRAY*, INDEXED etc.
    [
        (PF_OPTION, "gradient_type", "Gradient Type:", 0, GRADIENT_TYPES ),
        (PF_OPTION, "gradient_shape", "Gradient Shape:", 0, GRADIENT_SHAPES ),

        (PF_FLOAT, "angle", "Angle", 90),

        (PF_IMAGE, "image", "Input image", None),

        # USED WHEN RADIAL GRADIENTS ARE SELECTED
        # POSITION
        (PF_RADIO, "radial_pos_horiz", "radial-gradient: horiz. pos", "left",
          (("left", "left"), ("center", "center"), ("right", "right"))),
        (PF_RADIO, "radial_pos_vert", "radial-gradient: vert. pos", "top",
          (("top", "top"), ("center", "center"), ("bottom", "bottom"))),
        # SIZE
        (PF_OPTION, "radial_size", "radial-gradient: size", 0, RADIAL_GRADIENT_SIZES),


        (PF_BOOL, "use_gradient_name", "Use name of a GIMP Gradient", True),
        (PF_STRING, "gradient_name", "If No to above specify here:", "natcss_"),
        (PF_STRING, "prefix", "Prefix to remove from GIMP gradient name:", "natcss_"),
        (PF_GRADIENT, "gradient", "Gradient", None),
    ],
    [],
    pushgrad, menu="<Image>/Filters/Languages/Python-Fu" )

main()


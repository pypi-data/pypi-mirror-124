# Copyright CNRS/Inria/UCA
# Contributor(s): Eric Debreuve (since 2019)
#
# eric.debreuve@cnrs.fr
#
# This software is governed by the CeCILL  license under French law and
# abiding by the rules of distribution of free software.  You can  use,
# modify and/ or redistribute the software under the terms of the CeCILL
# license as circulated by CEA, CNRS and INRIA at the following URL
# "http://www.cecill.info".
#
# As a counterpart to the access to the source code and  rights to copy,
# modify and redistribute granted by the license, users are provided only
# with a limited warranty  and the software's author,  the holder of the
# economic rights,  and the successive licensors  have only  limited
# liability.
#
# In this respect, the user's attention is drawn to the risks associated
# with loading,  using,  modifying and/or developing or reproducing the
# software by the user in light of its specific status of free software,
# that may mean  that it is complicated to manipulate,  and  that  also
# therefore means  that it is reserved for developers  and  experienced
# professionals having in-depth computer knowledge. Users are therefore
# encouraged to load and test the software's suitability as regards their
# requirements in conditions enabling the security of their systems and/or
# data to be ensured and,  more generally, to use and operate it in the
# same conditions as regards security.
#
# The fact that you are presently reading this means that you have had
# knowledge of the CeCILL license and that you accept its terms.

from typing import Tuple

import numpy as nmpy
import scipy.ndimage as spim


array_t = nmpy.ndarray


def DetectionWithTolerance(detection: array_t, tolerance: int, /) -> array_t:
    """"""
    output = nmpy.zeros_like(detection)

    distance_map = spim.distance_transform_edt(detection != 1)
    output[distance_map <= tolerance] = 1

    for label in range(2, nmpy.amax(detection) + 1):
        current_map = spim.distance_transform_edt(detection != label)
        closer_bmap = current_map < distance_map
        output[nmpy.logical_and(closer_bmap, current_map <= tolerance)] = label
        distance_map[closer_bmap] = current_map[closer_bmap]

    return output


def ShiftedVersion(image: array_t, shift_r_x_c: Tuple[int, int], /) -> array_t:
    """"""
    shifted_img = nmpy.roll(image, shift_r_x_c[0], axis=0)
    output = nmpy.roll(shifted_img, shift_r_x_c[1], axis=1)

    if shift_r_x_c[0] > 0:
        output[: shift_r_x_c[0], :] = 0
    elif shift_r_x_c[0] < 0:
        output[shift_r_x_c[0] :, :] = 0
    if shift_r_x_c[1] > 0:
        output[:, : shift_r_x_c[1]] = 0
    elif shift_r_x_c[1] < 0:
        output[:, shift_r_x_c[1] :] = 0

    return output

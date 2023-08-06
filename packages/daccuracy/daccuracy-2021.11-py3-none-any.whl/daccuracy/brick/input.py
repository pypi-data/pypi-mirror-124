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

import glob
import sys as sstm
from collections import defaultdict as default_dict_t
from csv import reader as csv_reader_t
from pathlib import Path as path_t
from typing import Callable, Optional, Sequence, Tuple

import imageio as mgio
import numpy as nmpy

import daccuracy.brick.csv_io as csio
import daccuracy.brick.image as imge
from daccuracy.brick.csv_io import row_transform_h


array_t = nmpy.ndarray

img_shape_h = Tuple[int, ...]
gt_loading_fct_h = Callable[
    [path_t, img_shape_h, Sequence[int], row_transform_h], array_t
]


# See at the end of module
GT_LOADING_FOR_EXTENSION = default_dict_t(lambda: GroundTruthFromImage)
DN_LOADING_FOR_EXTENSION = default_dict_t(lambda: DetectionFromImage)


def GroundTruthFromImage(
    path: path_t,
    _: img_shape_h = None,
    __: Sequence[int] = None,
    ___: row_transform_h = None,
    /,
) -> Optional[array_t]:
    """"""
    return _ImageFromPath(
        path, _ImageFromImagePath, None, "image or unreadable by imageio"
    )


def GroundTruthFromNumpy(
    path: path_t,
    _: img_shape_h = None,
    __: Sequence[int] = None,
    ___: row_transform_h = None,
    /,
) -> Optional[array_t]:
    """"""
    return _ImageFromPath(path, _ImageFromNumpyPath, None, "Numpy file or unreadable")


def GroundTruthFromCSV(
    path: path_t,
    shape: img_shape_h,
    rc_idc: Tuple[int, int],
    row_transform: row_transform_h,
    /,
) -> Optional[array_t]:
    """"""
    output = nmpy.zeros(shape, dtype=nmpy.uint8)

    if row_transform is None:
        row_transform = lambda f_idx: csio.SymmetrizedRow(f_idx, float(shape[0]))

    try:
        with open(path) as csv_accessor:
            csv_reader = csv_reader_t(csv_accessor)
            # Do not enumerate csv_reader below since some rows might be dropped
            label = 1
            for line in csv_reader:
                coords = csio.CSVLineToCoords(line, rc_idc, row_transform)
                if coords is not None:
                    if output[coords] > 0:
                        print(
                            f"{path}: Multiple GTs at same position (due to rounding or duplicates)"
                        )
                        output = None
                        break
                    else:
                        output[coords] = label
                        label += 1
    except BaseException as exc:
        print(f"{path}: Error while reading or unreadable\n({exc})", file=sstm.stderr)
        output = None

    return output


def GroundTruthForDetection(
    detection_name: str,  # Without extension
    detection_shape: img_shape_h,
    ground_truth_path: path_t,
    ground_truth_folder: path_t,
    ground_truth: Optional[array_t],
    rc_idc: Tuple[int, int],
    row_transform: row_transform_h,
    mode: str,
    /,
) -> Tuple[Optional[array_t], Optional[path_t]]:
    """"""
    if mode == "one-to-one":
        ground_truth_path = None
        pattern = ground_truth_folder / (detection_name + ".*")
        for path in glob.iglob(pattern):
            ground_truth_path = path
            break
        if ground_truth_path is None:
            ground_truth = None
        else:
            gt_loading_fct = GT_LOADING_FOR_EXTENSION[ground_truth_path.suffix.lower()]
            ground_truth = gt_loading_fct(
                ground_truth_path, detection_shape, rc_idc, row_transform
            )
    elif ground_truth is None:  # mode = 'one-to-many'
        gt_loading_fct = GT_LOADING_FOR_EXTENSION[ground_truth_path.suffix.lower()]
        ground_truth = gt_loading_fct(
            ground_truth_path, detection_shape, rc_idc, row_transform
        )

    return ground_truth, ground_truth_path


def DetectionFromImage(
    path: path_t, /, *, shift_r_x_c: Tuple[int, int] = None
) -> Optional[array_t]:
    """"""
    return _ImageFromPath(
        path, _ImageFromImagePath, shift_r_x_c, "image or unreadable by imageio"
    )


def DetectionFromNumpy(
    path: path_t, /, *, shift_r_x_c: Tuple[int, int] = None
) -> Optional[array_t]:
    """"""
    return _ImageFromPath(
        path, _ImageFromNumpyPath, shift_r_x_c, "Numpy file or unreadable"
    )


def LabeledImageIsValid(image: Optional[array_t], /) -> Tuple[bool, Optional[str]]:
    """"""
    if image is None:
        return False, None

    unique_values = nmpy.unique(image)
    expected_values = range(nmpy.amax(image) + 1)

    is_valid = (unique_values.__len__() > 1) and nmpy.array_equal(
        unique_values, expected_values
    )

    if is_valid:
        issues = None
    elif unique_values.__len__() == 1:
        issues = f"Only one value present in image: {unique_values[0]}; Expected=at least 0 and 1"
    else:
        if unique_values[0] > 0:
            issues = ["0?"]  # Zero is missing
        else:
            issues = [str(unique_values[0])]
        for v_m_1_idx, label in enumerate(unique_values[1:]):
            previous = unique_values[v_m_1_idx]
            label_as_str = str(label)
            if label == previous:
                issues.append("=" + label_as_str)
            elif label > previous + 1:
                issues.extend(("...?", label_as_str))
            else:
                issues.append(label_as_str)
        issues = ", ".join(issues)

    return is_valid, issues


def _ImageFromPath(
    path: path_t,
    LoadingFunction: Callable[[path_t], array_t],
    shift_r_x_c: Optional[Tuple[int, int]],
    message: str,
    /,
) -> Optional[array_t]:
    """"""
    try:
        output = LoadingFunction(path)
        if shift_r_x_c is not None:
            output = imge.ShiftedVersion(output, shift_r_x_c)

        is_valid, issues = LabeledImageIsValid(output)
        if not is_valid:
            print(
                f"{path}: Incorrectly labeled image:\n    {issues}",
                file=sstm.stderr,
            )
            output = None
    except BaseException as exc:
        print(
            f"{path}: Not a valid {message}\n({exc})",
            file=sstm.stderr,
        )
        output = None

    return output


def _ImageFromImagePath(path: path_t, /) -> array_t:
    """"""
    return mgio.imread(str(path))


def _ImageFromNumpyPath(path: path_t, /) -> array_t:
    """"""
    output = nmpy.load(str(path))

    if hasattr(output, "keys"):
        first_key = tuple(output.keys())[0]
        output = output[first_key]

    return output


GT_LOADING_FOR_EXTENSION |= {
    ".csv": GroundTruthFromCSV,
    ".npy": GroundTruthFromNumpy,
    ".npz": GroundTruthFromNumpy,
}
DN_LOADING_FOR_EXTENSION |= {".npy": DetectionFromNumpy, ".npz": DetectionFromNumpy}

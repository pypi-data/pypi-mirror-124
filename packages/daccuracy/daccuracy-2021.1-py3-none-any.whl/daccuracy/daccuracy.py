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

import sys as sstm
from pathlib import Path as path_t
from typing import Tuple

import daccuracy.brick.arguments as rgmt
import daccuracy.brick.csv_io as csio
import daccuracy.brick.input as inpt
import daccuracy.brick.measures as msre
import daccuracy.brick.output as otpt
from daccuracy.brick.input import DN_LOADING_FOR_EXTENSION, row_transform_h
from daccuracy.brick.measures import measure_fct_h


def _ComputeAndOutputMeasures(
    ground_truth_path: path_t,
    detection_path: path_t,
    measure_fct: measure_fct_h,
    rc_idc: Tuple[int, int],
    row_transform: row_transform_h,
    shift_r_x_c: Tuple[int, int],
    should_exclude_border: bool,
    tolerance: int,
    output_format: str,
    should_show_image: bool,
    output_accessor,
) -> None:
    """"""
    if ground_truth_path.is_file():
        mode = "one-to-many"
        ground_truth_folder = None
    else:
        mode = "one-to-one"
        ground_truth_folder = ground_truth_path
    ground_truth = None

    if detection_path.is_file():
        detection_folder = detection_path.parent
        detection_name = detection_path.name
    else:
        detection_folder = detection_path
        detection_name = None

    header = csio.HeaderRow(measure_fct(None, None))
    if output_format == "csv":
        print(csio.COL_SEPARATOR.join(header), file=output_accessor)
        name_field_len = 0
    else:
        name_field_len = max(elm.__len__() for elm in header)

    for document in detection_folder.iterdir():
        if document.is_file() and (
            (detection_name is None) or (document.name == detection_name)
        ):
            dn_loading_fct = DN_LOADING_FOR_EXTENSION[document.suffix.lower()]
            detection = dn_loading_fct(document, shift_r_x_c=shift_r_x_c)
            if detection is None:
                continue

            ground_truth, ground_truth_path = inpt.GroundTruthForDetection(
                document.stem,
                detection.shape,
                ground_truth_path,
                ground_truth_folder,
                ground_truth,
                rc_idc,
                row_transform,
                mode,
            )
            if ground_truth is None:
                continue

            measures = msre.AccuracyMeasures(
                ground_truth,
                detection,
                measure_fct,
                should_exclude_border,
                tolerance,
            )
            measures_as_str = msre.MeasuresAsStrings(measures)
            output_row = [ground_truth_path.name, document.name] + measures_as_str

            if output_format == "csv":
                print(csio.COL_SEPARATOR.join(output_row), file=output_accessor)
            else:
                for name, value in zip(header, output_row):
                    print(f"{name:>{name_field_len}} = {value}", file=output_accessor)
            if should_show_image:
                otpt.PrepareMixedGTDetectionImage(ground_truth, detection)

    if should_show_image:
        otpt.ShowPreparedImages()


def Main() -> None:
    """"""
    *args, std_args = rgmt.ProcessedArguments(sstm.argv)

    std_args_but_1 = (
        std_args.shift_r_x_c,
        std_args.should_exclude_border,
        std_args.tolerance,
        std_args.output_format,
        std_args.should_show_image,
        std_args.output_accessor,
    )

    if std_args.should_show_usage_notice:
        print(
            "!!!! USAGE NOTICE !!!!\n"
            "Remember that, WITH MOST IMAGE FORMATS, ground-truth and detection CANNOT CONTAIN MORE THAN 255 OBJECTS.\n"
            "If they do, DAccuracy will complain about the image being incorrectly labeled.\n"
            "This constraint will be relaxed in a future version (it cannot be simply removed when using fixed-length\n"
            "representations of integers) by allowing to pass files of Numpy arrays and unlabeled images.\n\n"
            'This notice is silenced by the "--no-usage-notice" option.\n'
            "!!!!\n",
            file=sstm.stderr,
        )
    _ComputeAndOutputMeasures(*args, *std_args_but_1)

    if std_args.output_accessor is not sstm.stdout:
        std_args.output_accessor.close()


if __name__ == "__main__":
    #
    Main()

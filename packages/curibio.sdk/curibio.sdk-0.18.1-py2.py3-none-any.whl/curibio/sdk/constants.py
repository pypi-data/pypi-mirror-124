# -*- coding: utf-8 -*-
"""Docstring."""
from collections import OrderedDict
from typing import Dict
from typing import Tuple
from typing import Union
import uuid

from immutabledict import immutabledict
from labware_domain_models import LabwareDefinition
from mantarray_file_manager import MANTARRAY_SERIAL_NUMBER_UUID
from mantarray_file_manager import METADATA_UUID_DESCRIPTIONS
from mantarray_file_manager import PLATE_BARCODE_UUID
from mantarray_file_manager import TISSUE_SAMPLING_PERIOD_UUID
from mantarray_file_manager import UTC_BEGINNING_RECORDING_UUID
from mantarray_file_manager import WELL_NAME_UUID
from mantarray_waveform_analysis import AMPLITUDE_UUID
from mantarray_waveform_analysis import AUC_UUID
from mantarray_waveform_analysis import BESSEL_LOWPASS_10_UUID
from mantarray_waveform_analysis import BUTTERWORTH_LOWPASS_30_UUID
from mantarray_waveform_analysis import CENTIMILLISECONDS_PER_SECOND
from mantarray_waveform_analysis import CONTRACTION_VELOCITY_UUID
from mantarray_waveform_analysis import FRACTION_MAX_UUID
from mantarray_waveform_analysis import IRREGULARITY_INTERVAL_UUID
from mantarray_waveform_analysis import RELAXATION_VELOCITY_UUID
from mantarray_waveform_analysis import TIME_DIFFERENCE_UUID
from mantarray_waveform_analysis import TWITCH_FREQUENCY_UUID
from mantarray_waveform_analysis import TWITCH_PERIOD_UUID

try:  # adapted from https://packaging.python.org/guides/single-sourcing-package-version/
    from importlib import metadata
except ImportError:  # pragma: no cover
    # Running on pre-3.8 Python; use importlib-metadata package
    import importlib_metadata as metadata  # type: ignore # Eli (9/1/20): for some reason mypy is giving weird errors for this
PACKAGE_VERSION = metadata.version("curibio.sdk")  # type: ignore # Eli (9/1/20): for some reason mypy is giving weird errors for this

TWENTY_FOUR_WELL_PLATE = LabwareDefinition(row_count=4, column_count=6)

MICROSECONDS_PER_CENTIMILLISECOND = 10
MICRO_TO_BASE_CONVERSION = 1e6
METADATA_EXCEL_SHEET_NAME = "metadata"
METADATA_RECORDING_ROW_START = 0
METADATA_INSTRUMENT_ROW_START = METADATA_RECORDING_ROW_START + 4
METADATA_OUTPUT_FILE_ROW_START = METADATA_INSTRUMENT_ROW_START + 6

CONTINUOUS_WAVEFORM_SHEET_NAME = "continuous-waveforms"
AGGREGATE_METRICS_SHEET_NAME = "aggregate-metrics"
PER_TWITCH_METRICS_SHEET_NAME = "per-twitch-metrics"
NUMBER_OF_PER_TWITCH_METRICS = 45
SNAPSHOT_CHART_SHEET_NAME = "continuous-waveform-snapshots"
FULL_CHART_SHEET_NAME = "full-continuous-waveform-plots"
TWITCH_FREQUENCIES_CHART_SHEET_NAME = "twitch-frequencies-plots"
FORCE_FREQUENCY_RELATIONSHIP_SHEET = "force-frequency-relationship"

INTERPOLATED_DATA_PERIOD_SECONDS = 1 / 100
INTERPOLATED_DATA_PERIOD_CMS = INTERPOLATED_DATA_PERIOD_SECONDS * CENTIMILLISECONDS_PER_SECOND
TSP_TO_DEFAULT_FILTER_UUID = {  # Tissue Sampling Period (centi-milliseconds) to default Pipeline Filter UUID
    960: BESSEL_LOWPASS_10_UUID,
    160: BUTTERWORTH_LOWPASS_30_UUID,
}

DEFAULT_CELL_WIDTH = 64
CHART_HEIGHT = 300
CHART_BASE_WIDTH = 120
CHART_HEIGHT_CELLS = 15
CHART_FIXED_WIDTH_CELLS = 8
CHART_FIXED_WIDTH = DEFAULT_CELL_WIDTH * CHART_FIXED_WIDTH_CELLS
PEAK_VALLEY_COLUMN_START = 100
CHART_WINDOW_NUM_SECONDS = 10
CHART_WINDOW_NUM_DATA_POINTS = CHART_WINDOW_NUM_SECONDS / INTERPOLATED_DATA_PERIOD_SECONDS
SECONDS_PER_CELL = 2.5

CALCULATED_METRIC_DISPLAY_NAMES: Dict[uuid.UUID, Union[str, Tuple[int, str]]] = immutabledict(
    OrderedDict(
        [
            (TWITCH_PERIOD_UUID, "Twitch Period (seconds)"),
            (TWITCH_FREQUENCY_UUID, "Twitch Frequency (Hz)"),
            (AMPLITUDE_UUID, "Active Twitch Force (μN)"),
            (FRACTION_MAX_UUID, "Fraction of Maximum Active Twitch Force (μN)"),
            (AUC_UUID, "Energy (μJ)"),
            (
                CONTRACTION_VELOCITY_UUID,
                "Twitch Contraction Velocity (μN/second)",
            ),
            (
                RELAXATION_VELOCITY_UUID,
                "Twitch Relaxation Velocity (μN/second)",
            ),
            (IRREGULARITY_INTERVAL_UUID, "Twitch Interval Irregularity (seconds)"),
            (TIME_DIFFERENCE_UUID, "Time Difference (seconds)"),
        ]
    )
)

TWITCH_WIDTH_METRIC_DISPLAY_NAMES: Dict[int, str] = immutabledict(
    [
        (90, "Twitch Width 90 (seconds)"),
        (75, "Twitch Width 75 (seconds)"),
        (50, "Twitch Width 50 (seconds)"),
        (25, "Twitch Width 25 (seconds)"),
        (10, "Twitch Width 10 (seconds)"),
    ]
)

CONTRACTION_COORDINATES_DISPLAY_NAMES: Dict[int, str] = immutabledict(
    [
        (90, "Contraction Coordinates 90"),
        (75, "Contraction Coordinates 75"),
        (50, "Contraction Coordinates 50"),
        (25, "Contraction Coordinates 25"),
        (10, "Contraction Coordinates 10"),
    ]
)

RELAXATION_COORDINATES_DISPLAY_NAMES: Dict[int, str] = immutabledict(
    [
        (10, "Relaxation Coordinates 10"),
        (25, "Relaxation Coordinates 25"),
        (50, "Relaxation Coordinates 50"),
        (75, "Relaxation Coordinates 75"),
        (90, "Relaxation Coordinates 90"),
    ]
)

CONTRACTION_TIME_DIFFERENCE_DISPLAY_NAMES: Dict[int, str] = immutabledict(
    [
        (90, "Time From Contraction 90 to Peak (seconds)"),
        (75, "Time From Contraction 75 to Peak (seconds)"),
        (50, "Time From Contraction 50 to Peak (seconds)"),
        (25, "Time From Contraction 25 to Peak (seconds)"),
        (10, "Time From Contraction 10 to Peak (seconds)"),
    ]
)

RELAXATION_TIME_DIFFERENCE_DISPLAY_NAMES: Dict[int, str] = immutabledict(
    [
        (10, "Time From Peak to Relaxation 10 (seconds)"),
        (25, "Time From Peak to Relaxation 25 (seconds)"),
        (50, "Time From Peak to Relaxation 50 (seconds)"),
        (75, "Time From Peak to Relaxation 75 (seconds)"),
        (90, "Time From Peak to Relaxation 90 (seconds)"),
    ]
)
ALL_FORMATS = immutabledict({"CoV": {"num_format": "0.00%"}})

TWITCHES_POINT_UP_UUID = uuid.UUID("97f69f56-f1c6-4c50-8590-7332570ed3c5")
INTERPOLATION_VALUE_UUID = uuid.UUID("466d0131-06b7-4f0f-ba1e-062a771cb280")
mutable_metadata_uuid_descriptions = dict(
    METADATA_UUID_DESCRIPTIONS
)  # create a mutable version to add in the new values specific to the SDK (.update is an in-place operation that doesn't return the dictionary, so chaining is difficult)
mutable_metadata_uuid_descriptions.update(
    {
        TWITCHES_POINT_UP_UUID: "Flag indicating whether or not the twitches in the data point up or not",
        INTERPOLATION_VALUE_UUID: "Desired value for optical well data interpolation",
    }
)
METADATA_UUID_DESCRIPTIONS = immutabledict(mutable_metadata_uuid_descriptions)

EXCEL_OPTICAL_METADATA_CELLS = immutabledict(
    {
        WELL_NAME_UUID: "E2",
        UTC_BEGINNING_RECORDING_UUID: "E3",
        PLATE_BARCODE_UUID: "E4",
        TISSUE_SAMPLING_PERIOD_UUID: "E5",
        TWITCHES_POINT_UP_UUID: "E6",
        MANTARRAY_SERIAL_NUMBER_UUID: "E7",
        INTERPOLATION_VALUE_UUID: "E8",
    }
)

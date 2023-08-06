#  Copyright (c) 2021 ETH Zurich, SIS ID and HVL D-ITET
#

"""
Sensors that are used by the devices implemented in the CCB
"""

import logging
from abc import ABC, abstractmethod
from dataclasses import dataclass

import numpy as np
from scipy.interpolate import interp1d  # type: ignore

from hvl_ccb.utils.conversion_unit import Temperature, preserve_type
from hvl_ccb.utils.typing import ConvertableTypes
from hvl_ccb.utils.validation import validate_number

logger = logging.getLogger(__name__)


@dataclass  # type: ignore
class Sensor(ABC):

    @abstractmethod
    def __setattr__(self, name, value):
        pass

    @abstractmethod
    @preserve_type
    def convert(self, value: ConvertableTypes) -> ConvertableTypes:
        pass


@dataclass
class LEM4000S(Sensor):
    """
    Converts the output voltage (V) to the measured current (A)
    when using a LEM Current transducer LT 4000-S

    """
    CONVERSION = 5000
    shunt: float = 1.2
    calibration_factor: float = 1

    def __setattr__(self, name, value):
        if name == 'CONVERSION':
            raise AttributeError(
                "Attribute 'CONVERSION' is a constant and cannot be changed, "
                "the sensor can be calibrated with the attribute 'calibration_factor'."
            )
        if name == 'shunt':
            # ensure positive value, but also allow a very small shunt
            validate_number('shunt', value, (1e-6, None))
        if name == "calibration_factor":
            # ensure a value close to 1, but also allow negative values
            # for a reversed current sensor
            validate_number("calibration_factor", abs(value), (0.9, 1.1))
        self.__dict__[name] = value

    @preserve_type
    def convert(self, value: ConvertableTypes) -> ConvertableTypes:
        value = value / self.shunt * self.CONVERSION  # type: ignore
        return value


@dataclass
class LMT70A(Sensor):
    """
    Converts the output voltage (V) to the measured temperature (default °C)
    when using a TI Precision Analog Temperature Sensor LMT70(A)

    """
    temperature_unit: Temperature = Temperature.CELSIUS

    # look up table from datasheet
    # first column: temperature in degree celsius
    # second column: voltage in volt
    # https://www.ti.com/lit/ds/symlink/lmt70a.pdf?ts=1631590373860
    LUT = np.array(
        [
            [-55., 1.375219],
            [-50., 1.350441],
            [-40., 1.300593],
            [-30., 1.250398],
            [-20., 1.199884],
            [-10., 1.14907],
            [0., 1.097987],
            [10., 1.046647],
            [20., 0.99505],
            [30., 0.943227],
            [40., 0.891178],
            [50., 0.838882],
            [60., 0.78636],
            [70., 0.733608],
            [80., 0.680654],
            [90., 0.62749],
            [100., 0.574117],
            [110., 0.520551],
            [120., 0.46676],
            [130., 0.412739],
            [140., 0.358164],
            [150., 0.302785]
        ]
    )

    def __setattr__(self, name, value):
        if name == 'temperature_unit':
            Temperature(value)
        if name == 'LUT':
            raise AttributeError("Attribute 'LUT' is a constant and cannot be changed")
        self.__dict__[name] = value

    @preserve_type
    def convert(self, value: ConvertableTypes) -> ConvertableTypes:
        """
        NaN is returned for values that are not covered by the look up table
        :param value: output voltage of the sensor.
        :raise TypeError: for non convertable data types
        :return: measured temperature (default °C)
        """
        try:
            validate_number(
                "value", value, (self.LUT[-1, 1], self.LUT[0, 1]), logger=logger
            )
        except ValueError:
            mask = np.any([value < self.LUT[-1, 1], value > self.LUT[0, 1]], axis=0)
            value[mask] = np.NaN  # type: ignore
        logging.info(
            "Use linear interpolation of lookup table provided in datasheet"
        )
        piecewise_linear_interp = interp1d(
            self.LUT[:, 1], self.LUT[:, 0], kind='linear'
        )
        return Temperature.convert(
            piecewise_linear_interp(value),
            source=Temperature.CELSIUS,
            target=self.temperature_unit
        )

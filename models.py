"""Represent models for near-Earth objects and their close approaches.

The `NearEarthObject` class represents a near-Earth object. Each has a unique
primary designation, an optional unique name, an optional diameter, and a flag
for whether the object is potentially hazardous.

The `CloseApproach` class represents a close approach to Earth by an NEO. Each
has an approach datetime, a nominal approach distance, and a relative approach
velocity.

A `NearEarthObject` maintains a collection of its close approaches, and a
`CloseApproach` maintains a reference to its NEO.

The functions that construct these objects use information extracted from the
data files from NASA, so these objects should be able to handle all of the
quirks of the data set, such as missing names and unknown diameters.

You'll edit this file in Task 1.
"""
from helpers import cd_to_datetime, datetime_to_str
import re


class NearEarthObject:
    """A near-Earth object (NEO).

    An NEO encapsulates semantic and physical parameters about the object, such
    as its primary designation (required, unique), IAU name (optional), diameter
    in kilometers (optional - sometimes unknown), and whether it's marked as
    potentially hazardous to Earth.

    A `NearEarthObject` also maintains a collection of its close approaches -
    initialized to an empty collection, but eventually populated in the
    `NEODatabase` constructor.
    """
    def __init__(self, **info):
        """Create a new `NearEarthObject`.

        :param info: A dictionary of excess keyword arguments supplied to the constructor.
        """
        # Assign information from the arguments passed to the constructor
        # onto attributes named `designation`, `name`, `diameter`, and `hazardous`.
        # Coerce these values to their appropriate data type and handle any edge cases,
        # such as an empty name being represented by `None` and a missing diameter
        # being represented by `float('nan')`.
        self.designation = info.get('pdes')
        self.name = info.get('name') if info.get('name') else None
        self.diameter = float(info.get('diameter')) if info.get('diameter') else float('nan')
        self.hazardous = True if info.get('pha') == 'Y' else False

        # Create an empty initial collection of linked approaches.
        self.approaches = []

    @property
    def fullname(self):
        """Return a representation of the full name of this NEO."""
        # Use self.designation and self.name to build a fullname for this object.
        if self.name:
            return f'{self.designation} ({self.name})'
        return f'{self.designation}'

    def __str__(self):
        """Return `str(self)`."""
        # Use this object's attributes to return a human-readable string representation.
        # The project instructions include one possibility. Peek at the __repr__
        # method for examples of advanced string formatting.
        hazardous_status = "is potentially hazardous" if self.hazardous else "is not potentially hazardous"
        diameter_str = f"of diameter {self.diameter:.3f} km" if not float('nan') else "with an unknown diameter"
        return f"NEO {self.fullname} {diameter_str} and {hazardous_status}."

    def __repr__(self):
        """Return `repr(self)`, a computer-readable string representation of this object."""
        return f"NearEarthObject(designation={self.designation!r}, name={self.name!r}, " \
               f"diameter={self.diameter:.3f}, hazardous={self.hazardous!r})"

    def numerical_pde(self, pde):
        """Extracts the numerical part from a primary designation.

        This method is not directly used in the __init__ for `self.designation`
        as `designation` should typically be the full primary designation.
        It's included as it was in the original code.
        """
        if pde:
            # Get the first part of the string (e.g., '249P')
            pdes_str_part = pde.split()[0]

            # Use a regular expression to find all digits in the string
            # and join them to form a new string
            numeric_part = ''.join(re.findall(r'\d+', pdes_str_part))

            if numeric_part:  # Check if any digits were found
                return int(numeric_part)
            else:
                return ''  # Or 0, or None, depending on your logic
        else:
            return ''


class CloseApproach:
    """A close approach to Earth by an NEO.

    A `CloseApproach` encapsulates information about the NEO's close approach to
    Earth, such as the date and time (in UTC) of closest approach, the nominal
    approach distance in astronomical units, and the relative approach velocity
    in kilometers per second.

    A `CloseApproach` also maintains a reference to its `NearEarthObject` -
    initially, this information (the NEO's primary designation) is saved in a
    private attribute, but the referenced NEO is eventually replaced in the
    `NEODatabase` constructor.
    """
    def __init__(self, **info):
        """Create a new `CloseApproach`.

        :param info: A dictionary of excess keyword arguments supplied to the constructor.
        """
        # Assign information from the arguments passed to the constructor
        # onto attributes named `_designation`, `time`, `distance`, and `velocity`.
        # Coerce these values to their appropriate data type and handle any edge cases.
        # The `cd_to_datetime` function will be useful.
        self._designation = info.get('des')  # Primary designation of the associated NEO
        self.time = cd_to_datetime(info.get('cd'))  # Use the cd_to_datetime function
        self.distance = float(info.get('dist')) if info.get('dist') else 0.0
        self.velocity = float(info.get('v_rel')) if info.get('v_rel') else 0.0

        # Create an attribute for the referenced NEO, originally None.
        self.neo = None

    @property
    def time_str(self):
        """Return a formatted representation of this `CloseApproach`'s approach time.

        The value in `self.time` should be a Python `datetime` object. While a
        `datetime` object has a string representation, the default representation
        includes seconds - significant figures that don't exist in our input
        data set.

        The `datetime_to_str` method converts a `datetime` object to a
        formatted string that can be used in human-readable representations and
        in serialization to CSV and JSON files.
        """
        # Use this object's `.time` attribute and the `datetime_to_str` function to
        # build a formatted representation of the approach time.
        return datetime_to_str(self.time)

    def __str__(self):
        """Return `str(self)`."""
        # Use this object's attributes to return a human-readable string representation.
        # The project instructions include one possibility. Peek at the __repr__
        # method for examples of advanced string formatting.
        neo_fullname = self.neo.fullname if self.neo else self._designation
        return f"At {self.time_str}, '{neo_fullname}' approaches Earth at a distance of " \
               f"{self.distance:.2f} au and a velocity of {self.velocity:.2f} km/s."

    def __repr__(self):
        """Return `repr(self)`, a computer-readable string representation of this object."""
        return f"CloseApproach(time={self.time_str!r}, distance={self.distance:.2f}, " \
               f"velocity={self.velocity:.2f}, neo={self.neo!r})"

"""
Miscellaneous  functionality relating to metadata.
"""

import datetime


class MetadataItem:
    """
    Convenience class for working with a metadata element.

    Parameters
    ----------
    key : str
        The key for the metadata item.
    value : various
        The value for the metadata item.
    units : str or None
        The units associated with the metadata item.
    annotation : str or None
        An annotation (comment) associated with the metadata item.
    type : str or None
        The type of value.  Must be one of self.VALID_TYPES.
    """
    # Non-link types will be based on XML types.
    VALID_TYPES = {
        'link', 'string', 'boolean', 'decimal', 'integer', 'dateTime'
    }
    DATE_CLASSES = {datetime.datetime, datetime.date, datetime.time}

    # Reference:  https://numpy.org/doc/stable/user/basics.types.html
    NUMPY_INT_CLASS_NAMES = {
        'short', 'ushort',
        'intc', 'uintc',
        'int_', 'uint',
        'longlong', 'ulonglong',
        'int8', 'int16', 'int32', 'int64',
        'uint8', 'uint16', 'uint32', 'uint64',
        'intp', 'uintp',
    }
    NUMPY_FLOAT_CLASS_NAMES = {
        'half', 'float16', 'single', 'double', 'longdouble', 'csingle',
        'cdouble', 'clongdouble',
        'float32', 'float64', 'float_'
    }
    # NOTE:  Complex numbers currently not parseable.
    NUMPY_STRING_CLASSES = {
        'byte', 'ubyte', 'str_',
    }
    NUMPY_BOOL_CLASS = 'bool_'

    def __init__(self, key, value, units=None, annotation=None, type_=None):
        self.key = key

        # Convert from Numpy types.
        # NOTE:  Use value, not self.value, since the former will be used to
        #        determine the type.
        if type(value).__name__ in self.NUMPY_INT_CLASS_NAMES:
            value = int(value)
        elif type(value).__name__ in self.NUMPY_FLOAT_CLASS_NAMES:
            value = float(value)
        elif type(value).__name__ in self.NUMPY_STRING_CLASSES:
            value = str(value)
        elif type(value).__name__ == self.NUMPY_BOOL_CLASS:
            value = bool(value)

        self.value = value
        self.units = units
        self.annotation = annotation

        if type_ is None:
            value_type = type(value)

            if value_type == int:
                type_ = 'integer'
            elif value_type == float:
                type_ = 'decimal'
            elif value_type == str:
                type_ = 'string'
            elif value_type == bool:
                type_ = 'boolean'
            elif value_type in self.DATE_CLASSES:
                type_ = 'dateTime'
            else:
                raise ValueError(f"Unknown value type: {value_type}")

        self.type = type_

    @property
    def key(self):
        return self._key

    @key.setter
    def key(self, value):
        if not isinstance(value, str) or not value:
            raise ValueError("key must be a non-empty string")

        self._key = value

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        if value is None:
            raise ValueError("value must not be None")

        self._value = value

    @property
    def units(self):
        return self._units

    @units.setter
    def units(self, value):
        if value is not None and not isinstance(value, str):
            raise ValueError("units must be None or a string")

        self._units = value

    @property
    def annotation(self):
        return self._annotation

    @annotation.setter
    def annotation(self, value):
        if value is not None and not isinstance(value, str):
            raise ValueError("annotation must be None or a string")

        self._annotation = value

    @property
    def type(self):
        return self._type

    @type.setter
    def type(self, value):
        if value not in self.VALID_TYPES:
            raise ValueError(
                f"type_ must be one of {', '.join(self.VALID_TYPES)}")

        self._type = value

    def to_api_format(self):
        """
        Translate item data to the format expected by the API.

        Returns
        -------
        A dict that can be appended to a list of metadata items and passed to
        an endpoint.
        """

        def convert_value():
            if self.value.__class__ in self.DATE_CLASSES:
                return self.value.isoformat()
            else:
                return self.value

        output = {
            'keyName': self.key,
            'value': {
                'type': self.type,
                'link': convert_value(),
            }
        }

        if self.units is not None:
            # 'unit' should be singular per the API.
            output['unit'] = self.units

        if self.annotation is not None:
            output['annotation'] = self.annotation

        return output

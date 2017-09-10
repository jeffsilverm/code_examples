#! /usr/bin/python
# -*- coding: utf-8 -*-
#
# classmethod demonstration
#
# This program demonstrates how to use classmethods to encapsulate an object
# and protect it from changes

import sys

python3 = sys.version_info.major == 3


class Thingy(object):
    """This class implements a class of ''thingys'' that have different 
    'flavors' """

    _thingy_list = []
    _class_serial_number = 0
    _flavor = None
    _name = None

    @classmethod
    def __init__(cls, flavor, name):
        """This method creates thingy objects"""

        cls._flavor = flavor
        cls._class_serial_number = cls._class_serial_number
        cls._thingy_list.append(cls)
        cls._name = name

        cls._class_serial_number += 1

    @classmethod
    def __str__(cls):
        """This method converts an object of type Thingy to a string"""
        s = "CLASS: flavor: {} CLASS: serial number {:d} name {}".format(
            cls.key_to_string(cls._flavor),
                                cls._class_serial_number, cls._name )
        return s

    @classmethod
    def __repr__(cls):
        """return a revisible representation of an object of type Thingy"""
        return "In class method __repr__:\n  flavor:{}".format(cls._flavor) + \
            "\n  class serial number: {:d}".format(cls._class_serial_number) + \
            "\n  class thingy list: {}".format(cls._thingy_list)

    @classmethod
    def validate(cls, value, lower_limit, upper_limit):
        """You'll notice that while this a class method, it doesn't actually
        reference the class.  You see this in various other places, such as
        the math module which has math.sqrt() """

        assert isinstance(value, int ), "Value is not an integer, actually {}".\
            format(type(value))
        assert lower_limit <= value <= upper_limit, \
            "Value {} is out of the allowed range {}..{}".format(value,
                                        lower_limit, upper_limit)

    @classmethod
    def class_iterator(self):
        """This method returns an iterator, for looping over the object list"""

        a = iter(self._thingy_list)
        return a

    @classmethod
    def key_to_string(cls, key):
        """This method MUST be defined by any subclass"""
        raise NotImplemented("You didn't subclass the key_to_string method"\
                             "did you?")


class GrayThingy(Thingy):
    """This class implements a class of 'thingys' that have different gray scales """

    WHITE = 0
    LIGHTGRAY = 1
    GRAY = 2
    DARKGRAY = 3
    BLACK = 4
    values_table=dict()
    values_table[0]="White"
    values_table[1]="Lightgray"
    values_table[2]="Gray"
    values_table[3]="Darkgray"
    values_table[4]="Black"

    object_serial_number = 0

    def __init__(self, gray_scale, name):
        """This creates GrayThingy objects"""

        self.validate(gray_scale, GrayThingy.WHITE, GrayThingy.BLACK)
        self._obj_flavor = gray_scale
        self._obj_serial_number = GrayThingy.object_serial_number
        GrayThingy.object_serial_number += 1
        if python3:
            super().__init__(flavor=gray_scale, name=name)
        else:
            super(Thingy, self).__init__()

    def __str__(self):
        """This method converts an object of type GrayThingy to a string"""
        s = "Instance: gray_scale: {} Instance: serial number {:d} name {}".\
            format( self.key_to_string(self._flavor),
                                self._class_serial_number, self._name )
        return s

    def __repr__(self):
        return "In instance method __repr__:" + self.__str__()

    def key_to_string(self, key):
        """This method converts a key to a gray value"""
        return self.values_table[key]


class ColoredThingy(Thingy):
    RED = 0
    ORANGE = 1
    YELLOW = 2
    GREEN = 3
    BLUE = 4
    INDIGO = 5
    VIOLET = 6
    colors_table = dict()
    colors_table[RED] = "RED"
    colors_table[ORANGE] = "ORANGE"
    colors_table[YELLOW] = "YELLOW"
    colors_table[GREEN] = "GREEN"
    colors_table[BLUE] = "BLUE"
    colors_table[INDIGO] = "INDIGO"
    colors_table[VIOLET] = "VIOLET"

    object_serial_number = 0

    def __init__(self, color, name):

        self.validate(color, ColoredThingy.RED, ColoredThingy.VIOLET)
        self._obj_flavor = color
        self._obj_serial_number = ColoredThingy.object_serial_number
        ColoredThingy.object_serial_number += 1
        if python3:
            super().__init__(flavor=color, name=name)
        else:
            super(Thingy, self).__init__()

    def key_to_string(self, key):
        """This method converts a key to a gray value"""
        return self.colors_table[key]

# Note that this class does *not* implement __str__.  What happens?


if __name__ == "__main__":

    red_thingy = ColoredThingy(ColoredThingy.RED, 'red')
    yellow_thingy = ColoredThingy(ColoredThingy.YELLOW, 'yellow')
    white_thingy = GrayThingy(GrayThingy.WHITE, 'white')
    lightgray_thingy = GrayThingy(GrayThingy.LIGHTGRAY, 'light gray')
    gray_thingy = GrayThingy(GrayThingy.GRAY, 'gray')
    black_thingy = GrayThingy(GrayThingy.BLACK, 'black')


    print("The white thingy instance iterator")
    for thingy in white_thingy.class_iterator():
        s=str(thingy)
        print(s)
        t=thingy._name
        print("Thingy name: {}".format(t) )

    print("The Thingy class iterator")
    for thingy in Thingy.class_iterator():
        s=str(thingy)
        print(s)
        t=thingy._name
        print("Thingy name: {}".format(t) )

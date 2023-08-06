raise NotImplementedError("This package isn't ready yet.")

import datetime
from copy import copy
from typing import Any

__version__ = "0.0.1.b"

class undefined:
    def __repr__(self):
        return "<undefined>"
    def __str__(self):
        return "--"
    def __bool__(self):
        return False

class FreeAgent(undefined):
    def __repr__(self):
        return "free agent"
    def __str__(self):
        return "free agent"

PLAYER_STAT_NAMES = [
    'acceleration',
    'aggression',
    'agility',
    'attacking_position',
    'balance',
    'ball_control',
    'composure',
    'crossing',
    'curve',
    'defending',
    'dribbling',
    'finishing',
    'free_kick',
    'heading',
    'interceptions',
    'jumping',
    'long_passing',
    'long_shots',
    'marking',
    'pace',
    'passing',
    'penalties',
    'physical',
    'reactions',
    'shooting',
    'short_passing',
    'shot_power',
    'sliding_tangle',
    'sprint_speed',
    'stamina',
    'standing_tackle',
    'strength',
    'vision',
    'volleys',
]

GOALKEEPER_STAT_NAMES = [
    'diving',
    'handling',
    'kicking',
    'gk_positioning',
    'reflexes',
    'speed'
]
ALL_STAT_NAMES = PLAYER_STAT_NAMES + GOALKEEPER_STAT_NAMES

ALL_POSITIONS = [
    "GK",
    "LWB",
    "LB",
    "LCB",
    "CB",
    "RCB",
    "RB",
    "RWB",
    "LDM",
    "CDM",
    "RDM",
    "LM",
    "LCM",
    "CM",
    "RCM",
    "RM",
    "LAM",
    "CAM",
    "RAM",
    "LW",
    "LF",
    "CF",
    "RF",
    "RW",
    "LS",
    "ST",
    "RS",
]

def isposition(x):
    """Returns whether x is a position."""
    return x in ALL_POSITIONS

def isplayerstat(x):
    """Returns whether x is a player stat."""
    return x in PLAYER_STAT_NAMES

def isgkstat(x):
    """Returns whether x is a GK stat."""
    return x in GOALKEEPER_STAT_NAMES

def isstat(x):
    """Returns whether x is a stat."""
    return x in ALL_STAT_NAMES

class _helpers:
    """a bunch of tools crammed into an object as staticmethods. these aren't for use"""

    @staticmethod
    def check_if_undefined(func):
        def inner(self, *args, **kwargs):
            if self.value is undefined:
                try:
                    fname = eval(func.__name__.strip("__"))
                except NameError:
                    fname = func.__name__
                finally:
                    fname += "()"
                    raise ValueError(f"{fname} operation failed with undefined stat")
            return func(self, *args, **kwargs)
        return inner

class Profile:
    def _set_dob(self, dob):
        if dob is undefined:
            return
        if not isinstance(dob, datetime.datetime):
            raise ValueError("date_of_birth must be an instance of datetime.datetime")
        self.date_of_birth = dob

    def __init__(self, **kwargs):
        self.age = kwargs.pop("age", undefined)
        self.nationality = kwargs.pop("nationality", undefined)
        self._set_dob(kwargs.pop("date_of_birth", undefined))

class PlayerStat:
    """An object used to represent a stat on a player.
    
    Whilst this object was only built for internals, there's no reason
    why you can't use it yourself. Initialize with (name, value), representing
    the name and value of the stat. These are checked on initialization to make
    sure they are valid.
    """

    def __init__(self, name, value):
        if not isstat(name):
            raise ValueError(name + " was not a recognized stat")
        self.name = name
        self.clean_name = name.replace("_", " ").capitalize()
        if value not in range(1, 101) or value is not undefined:
            raise ValueError(f"PlayerStat '{name}' value <{name}> must be in range(1, 101), or undefined")
        self.value = value

    def __repr__(self):
        return f"<{self.name} {self.value}>"

    def __str__(self):
        return str(self.value)

    def __bool__(self):
        return self.value is not undefined

    def copy(self):
        return copy(self)

    def undefine(self) -> None:
        self.value = undefined

    @_helpers.check_if_undefined
    def __int__(self):
        return self.value

    @_helpers.check_if_undefined
    def __eq__(self, other):
        return self.value == other
    
    @_helpers.check_if_undefined
    def __ne__(self, other):
        return self.value != other

    @_helpers.check_if_undefined
    def __gt__(self, other):
        return self.value > other
    
    @_helpers.check_if_undefined
    def __lt__(self, other):
        return self.value < other

    @_helpers.check_if_undefined
    def __add__(self, n):
        return self.value + n

    @_helpers.check_if_undefined
    def __sub__(self, n):
        return self.value - n

    @_helpers.check_if_undefined
    def __truediv__(self, n):
        return self.value / n

    @_helpers.check_if_undefined
    def __floordiv__(self, n):
        return self.value // n

    @_helpers.check_if_undefined
    def __divmod__(self, n):
        return (self.value // n, self.value % n)

    @_helpers.check_if_undefined
    def __mod__(self, n):
        return self.__divmod__(n)[1]

    @_helpers.check_if_undefined
    def __pow__(self, n):
        return self.value ** n

    @_helpers.check_if_undefined
    def __float__(self):
        return float(self.value)
    
    @_helpers.check_if_undefined
    def __complex__(self):
        return complex(self.value)

    @_helpers.check_if_undefined
    def __abs__(self):
        return abs(self.value)

    @_helpers.check_if_undefined
    def __invert__(self):
        return ~self.value

    @_helpers.check_if_undefined
    def __index__(self):
        return self.value

    @_helpers.check_if_undefined
    def __or__(self, n):
        return self.value | n

    @_helpers.check_if_undefined
    def __xor__(self, n):
        return self.value ^ n

    @_helpers.check_if_undefined
    def __ior__(self, n):
        if 100 < self.value | n < 0:
            raise ValueError(f"'{self.name}' stat must be between 0 and 100")
        self.value |= n

    @_helpers.check_if_undefined
    def __ixor__(self, n):
        if 100 < self.value ^ n < 0:
            raise ValueError(f"'{self.name}' stat must be between 0 and 100")
        self.value ^= n

    @_helpers.check_if_undefined
    def __ipow__(self, n):
        if 100 < self.value ** n < 0:
            raise ValueError(f"'{self.name}' stat must be between 0 and 100")
        self.value **= n

    @_helpers.check_if_undefined
    def __imod__(self, n):
        if 100 < self.value % n < 0:
            raise ValueError(f"'{self.name}' stat must be between 0 and 100")
        self.value %= n

    @_helpers.check_if_undefined
    def __iadd__(self, n):
        if self.value + n > 100:
            raise ValueError(f"'{self.name}' stat cannot exceed 100")
        self.value += n

    @_helpers.check_if_undefined
    def __isub__(self, n):
        if self.value - n < 0:
            raise ValueError(f"'{self.name}' stat cannot fall below 0")
        self.value -= n

    @_helpers.check_if_undefined
    def __imul__(self, n):
        if 100 < self.value * n < 0:
            raise ValueError(f"'{self.name}' stat must be between 0 and 100")
        self.value *= n

    @_helpers.check_if_undefined
    def __itruediv__(self, n):
        if 100 < self.value / n < 0:
            raise ValueError(f"'{self.name}' stat must be between 0 and 100")
        self.value /= n

    @_helpers.check_if_undefined
    def __ifloordiv__(self, n):
        if 100 < self.value // n < 0:
            raise ValueError(f"'{self.name}' stat must be between 0 and 100")
        self.value //= n


# class PlayerStatIterator:
#     def __init__(self, stat_dict):
#         self.stat_dict = stat_dict

#     def __iter__(self):
#         return iter(self.stat_dict)

#     def __repr__(self):
#         return f"PlayerStatIterator <{len(self.stat_dict)}>"

#     def __len__(self):
#         return len(self.stat_dict)


class BasePlayer:
    """A base for players (Player, GoalKeeper).
    
    In the same way as BaseException and Exception, you should
    only use Player and GoalKeeper, do not use this base.
    """

    isgk = False

    def __init__(self, player_name, *, settings):
        self.player_name = player_name
        self.profile = undefined  # settable with Player(...).set_profile()
        self.club = settings.get("club", undefined)
        self.kit_number = settings.get("kit_number", undefined)
        self._add_wage(settings.get("wage", undefined))
        self._add_positions(settings.get("preferred_positions", undefined))
        if self.isgk:
            stats = ALL_STAT_NAMES
        else:
            stats = PLAYER_STAT_NAMES
        self.stat_dict = {stat: PlayerStat(settings.get(stat, undefined)) for stat in stats}

    def __str__(self):
        return self.player_name

    def __repr__(self):
        if self.isgk:
            player = "goalkeeper"
        else:
            player = "player"
        return player + f" <{self.player_name}"

    def __iter__(self):
        return iter(self.stat_dict)

    def __init_subclass__(cls, goalkeeper: bool = False) -> None:
        cls.isgk = goalkeeper

    def _add_positions(self, positions):
        if positions is undefined:
            return
        if not isinstance(positions, (list, tuple)):
            raise ValueError("preferred_positions must be a list or tuple")
        for pos in positions:
            if not isposition(pos):
                raise ValueError(f"Position '{pos}' invalid")
        self.preferred_positions = positions

    def _add_wage(self, wage):
        if wage is undefined:
            return
        if not isinstance(wage, int) or wage < 0:
            raise ValueError("Wage must be a positive int")
        self.wage = wage

    def __getattr__(self, attr) -> PlayerStat:
        try:
            return self.stat_dict[attr]
        except KeyError:
            raise AttributeError(f"'Player' object has no attribute or stat named '{attr}'") from None

    def __getitem__(self, item) -> PlayerStat:
        self.__getattr__(item)
    
    def __delitem__(self, item) -> None:
        self.__delattr__(item)
    
    def __delattr__(self, attr) -> None:
        self.__getattr__(attr)
        self.stat_dict[attr] = PlayerStat(undefined)

    def __dir__(self):
        return ["__class__", "__doc__", "__module__"] + list(self.stat_dict.keys())

    def set_profile(self, profile: Profile = None):
        if profile is None:
            self.profile = undefined
            return
        if not isinstance(profile, Profile):
            raise ValueError("profile must be an instance of Profile")
        self.profile = profile

        
class Player(BasePlayer):
    """A representation of a player."""

class GoalKeeper(BasePlayer, goalkeeper=True):
    """A representation of a goalkeeper."""

from enum import Enum


class FormatType(Enum):
    SINGLE_ELIMINATION = "single_elimination"
    DOUBLE_ELIMINATION = "double_elimination"
    GROUP_KNOCKOUT = "group_knockout"


class TournamentStatus(Enum):
    REGISTRATION = "registration"
    ACTIVE = "active"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class BracketType(Enum):
    GROUP = "group"
    WINNERS = "winners"
    LOSERS = "losers"
    FINAL = "final"


class MatchStatus(Enum):
    PENDING = "pending"
    PLAYING = "playing"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class PlayerStatus(Enum):
    REGISTERED = "registered"
    ELIMINATED = "eliminated"
    QUALIFIED = "qualified"
    WINNER = "winner"


class TiebreakRule(Enum):
    GOAL_DIFF = "goal_diff"
    HEAD_TO_HEAD = "head_to_head"
    RANDOM = "random"


class GroupName(Enum):
    """User groups for authorization and permissions"""
    ADMIN = "admin"
    MODERATOR = "moderator"
    USER = "user"
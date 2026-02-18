"""
Tournament Models
Supports: Single Elimination, Double Elimination, Group Stage + Knockout
"""

from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
import uuid

from utils.base_model import BaseModel
from utils.enums import (
    FormatType,
    TournamentStatus,
    BracketType,
    MatchStatus,
    PlayerStatus,
    TiebreakRule,
)


# ============================================================================
# 1️⃣ BASE TOURNAMENT MODEL
# ============================================================================

class Tournament(BaseModel):
    """
    Base tournament model. Parent for all tournament types.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    game_title = models.CharField(max_length=255)  # e.g., Mortal Kombat
    
    format_type = models.CharField(
        max_length=50,
        choices=[(fmt.value, fmt.value) for fmt in FormatType],
        default=FormatType.SINGLE_ELIMINATION.value
    )
    
    max_players = models.PositiveIntegerField(validators=[MinValueValidator(2)])
    current_player_count = models.PositiveIntegerField(default=0)
    
    status = models.CharField(
        max_length=50,
        choices=[(status.value, status.value) for status in TournamentStatus],
        default=TournamentStatus.REGISTRATION.value
    )
    
    registration_deadline = models.DateTimeField()
    start_date = models.DateTimeField()
    
    class Meta:
        db_table = "tournaments"
        ordering = ["-created_at"]
    
    def __str__(self):
        return f"{self.name} ({self.format_type})"


# ============================================================================
# 2️⃣ TOURNAMENT SETTINGS MODEL
# ============================================================================

class TournamentSettings(BaseModel):
    """
    Core configuration that applies regardless of format.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    tournament = models.OneToOneField(
        Tournament,
        on_delete=models.CASCADE,
        related_name="settings"
    )
    
    seeding_enabled = models.BooleanField(default=True)
    shuffle_players = models.BooleanField(default=False)
    number_of_consoles = models.PositiveIntegerField(default=1)
    match_duration_minutes = models.PositiveIntegerField(default=15)
    third_place_match = models.BooleanField(default=False)
    auto_generate_fixtures = models.BooleanField(default=True)
    lock_settings = models.BooleanField(default=False)
    
    class Meta:
        db_table = "tournament_settings"
    
    def __str__(self):
        return f"Settings for {self.tournament.name}"


# ============================================================================
# 3️⃣ FORMAT-SPECIFIC SETTINGS MODELS
# ============================================================================

class SingleEliminationSettings(BaseModel):
    """
    Configuration for Single Elimination format.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    tournament = models.OneToOneField(
        Tournament,
        on_delete=models.CASCADE,
        related_name="single_elim_settings"
    )
    
    allow_byes = models.BooleanField(default=True)
    auto_balance_bracket = models.BooleanField(default=True)
    
    class Meta:
        db_table = "single_elimination_settings"
    
    def __str__(self):
        return f"Single Elim Settings: {self.tournament.name}"


class DoubleEliminationSettings(BaseModel):
    """
    Configuration for Double Elimination format.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    tournament = models.OneToOneField(
        Tournament,
        on_delete=models.CASCADE,
        related_name="double_elim_settings"
    )
    
    grand_final_reset_enabled = models.BooleanField(default=True)
    third_place_match = models.BooleanField(default=True)
    
    class Meta:
        db_table = "double_elimination_settings"
    
    def __str__(self):
        return f"Double Elim Settings: {self.tournament.name}"


class GroupKnockoutSettings(BaseModel):
    """
    Configuration for Group Stage + Knockout format.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    tournament = models.OneToOneField(
        Tournament,
        on_delete=models.CASCADE,
        related_name="group_knockout_settings"
    )
    
    group_size = models.PositiveIntegerField(default=4, validators=[MinValueValidator(2)])
    qualifiers_per_group = models.PositiveIntegerField(default=2)
    
    points_per_win = models.PositiveIntegerField(default=3)
    points_per_draw = models.PositiveIntegerField(default=1)
    points_per_loss = models.PositiveIntegerField(default=0)
    
    tiebreaker_rule = models.CharField(
        max_length=50,
        choices=[(rule.value, rule.value) for rule in TiebreakRule],
        default=TiebreakRule.GOAL_DIFF.value
    )
    
    auto_generate_knockout = models.BooleanField(default=True)
    
    class Meta:
        db_table = "group_knockout_settings"
    
    def __str__(self):
        return f"Group Knockout Settings: {self.tournament.name}"


# ============================================================================
# 4️⃣ PLAYER MODEL
# ============================================================================

class Player(BaseModel):
    """
    Players registered in the tournament.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    tournament = models.ForeignKey(
        Tournament,
        on_delete=models.CASCADE,
        related_name="players"
    )
    
    name = models.CharField(max_length=255)
    gamer_tag = models.CharField(max_length=255)
    phone = models.CharField(max_length=20, blank=True, null=True)
    
    seed_number = models.PositiveIntegerField(blank=True, null=True)
    
    status = models.CharField(
        max_length=50,
        choices=[(status.value, status.value) for status in PlayerStatus],
        default=PlayerStatus.REGISTERED.value
    )
    
    class Meta:
        db_table = "players"
        unique_together = ("tournament", "gamer_tag")
        ordering = ["seed_number", "created_at"]
    
    def __str__(self):
        return f"{self.gamer_tag} ({self.tournament.name})"


# ============================================================================
# 5️⃣ GROUP MODEL (For Group Stage + Knockout)
# ============================================================================

class Group(BaseModel):
    """
    Groups for group stage tournaments.
    Only used in GROUP_KNOCKOUT format.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    tournament = models.ForeignKey(
        Tournament,
        on_delete=models.CASCADE,
        related_name="groups"
    )
    
    name = models.CharField(max_length=50)  # e.g., "Group A", "Group 1"
    group_number = models.PositiveIntegerField()
    
    class Meta:
        db_table = "groups"
        unique_together = ("tournament", "group_number")
    
    def __str__(self):
        return f"{self.name} - {self.tournament.name}"


class GroupMembership(BaseModel):
    """
    Links players to groups.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    group = models.ForeignKey(
        Group,
        on_delete=models.CASCADE,
        related_name="memberships"
    )
    player = models.ForeignKey(
        Player,
        on_delete=models.CASCADE,
        related_name="group_memberships"
    )
    
    class Meta:
        db_table = "group_memberships"
        unique_together = ("group", "player")
    
    def __str__(self):
        return f"{self.player.gamer_tag} in {self.group.name}"


# ============================================================================
# 6️⃣ UNIFIED MATCH MODEL
# ============================================================================

class Match(BaseModel):
    """
    Unified match model for all tournament formats.
    Works for groups, winners bracket, losers bracket, and finals.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    tournament = models.ForeignKey(
        Tournament,
        on_delete=models.CASCADE,
        related_name="matches"
    )
    
    round_number = models.PositiveIntegerField()
    
    bracket_type = models.CharField(
        max_length=50,
        choices=[(btype.value, btype.value) for btype in BracketType],
        default=BracketType.GROUP.value
    )
    
    # For group stage matches
    group = models.ForeignKey(
        Group,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="matches"
    )
    
    # Players
    player1 = models.ForeignKey(
        Player,
        on_delete=models.CASCADE,
        related_name="matches_as_player1"
    )
    player2 = models.ForeignKey(
        Player,
        on_delete=models.CASCADE,
        related_name="matches_as_player2"
    )
    
    # Scores
    player1_score = models.PositiveIntegerField(blank=True, null=True)
    player2_score = models.PositiveIntegerField(blank=True, null=True)
    
    # Result
    winner = models.ForeignKey(
        Player,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="matches_won"
    )
    
    status = models.CharField(
        max_length=50,
        choices=[(status.value, status.value) for status in MatchStatus],
        default=MatchStatus.PENDING.value
    )
    
    # Console assignment
    console_assigned = models.PositiveIntegerField(blank=True, null=True)
    scheduled_time = models.DateTimeField(blank=True, null=True)
    
    class Meta:
        db_table = "matches"
        ordering = ["round_number", "bracket_type", "created_at"]
    
    def __str__(self):
        return f"{self.player1.gamer_tag} vs {self.player2.gamer_tag} (Round {self.round_number})"


# ============================================================================
# 7️⃣ GROUP STANDINGS MODEL (For Group Stage)
# ============================================================================

class GroupStandings(BaseModel):
    """
    Tracks standings in group stage.
    Only used in GROUP_KNOCKOUT format.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    group = models.ForeignKey(
        Group,
        on_delete=models.CASCADE,
        related_name="standings"
    )
    player = models.ForeignKey(
        Player,
        on_delete=models.CASCADE,
        related_name="group_standings"
    )
    
    matches_played = models.PositiveIntegerField(default=0)
    wins = models.PositiveIntegerField(default=0)
    draws = models.PositiveIntegerField(default=0)
    losses = models.PositiveIntegerField(default=0)
    
    points = models.PositiveIntegerField(default=0)
    score_for = models.PositiveIntegerField(default=0)
    score_against = models.PositiveIntegerField(default=0)
    score_difference = models.IntegerField(default=0)
    
    position = models.PositiveIntegerField(blank=True, null=True)
    qualified = models.BooleanField(default=False)
    
    class Meta:
        db_table = "group_standings"
        unique_together = ("group", "player")
        ordering = ["-points", "-score_difference"]
    
    def __str__(self):
        return f"{self.player.gamer_tag} - {self.group.name}"


# ============================================================================
# 8️⃣ BRACKET POSITION MODEL (For Elimination Formats)
# ============================================================================

class BracketPosition(BaseModel):
    """
    Tracks player positions in elimination brackets.
    Used for Single Elimination and Double Elimination.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    tournament = models.ForeignKey(
        Tournament,
        on_delete=models.CASCADE,
        related_name="bracket_positions"
    )
    
    player = models.ForeignKey(
        Player,
        on_delete=models.CASCADE,
        related_name="bracket_positions"
    )
    
    bracket_type = models.CharField(
        max_length=50,
        choices=[(btype.value, btype.value) for btype in BracketType],
        default=BracketType.WINNERS.value
    )
    
    position = models.PositiveIntegerField()  # Position in bracket tree
    round_eliminated = models.PositiveIntegerField(blank=True, null=True)
    
    class Meta:
        db_table = "bracket_positions"
        unique_together = ("tournament", "player", "bracket_type")
    
    def __str__(self):
        return f"{self.player.gamer_tag} - {self.bracket_type} #{self.position}"

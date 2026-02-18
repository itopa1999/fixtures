"""
Tournament Admin Configuration
Intuitive admin interface for managing tournaments, players, matches, and standings.
"""

from django.contrib import admin
from django.utils.html import format_html
from django.db.models import Q, Count
from .models import (
    Tournament,
    TournamentSettings,
    SingleEliminationSettings,
    DoubleEliminationSettings,
    GroupKnockoutSettings,
    Player,
    Group,
    GroupMembership,
    Match,
    GroupStandings,
    BracketPosition,
)


# ============================================================================
# 📋 INLINE ADMINS (For Related Models)
# ============================================================================

class TournamentSettingsInline(admin.TabularInline):
    """Inline settings for tournament."""
    model = TournamentSettings
    extra = 0
    fields = (
        'seeding_enabled', 'shuffle_players', 'number_of_consoles',
        'match_duration_minutes', 'third_place_match', 'auto_generate_fixtures'
    )


class SingleEliminationSettingsInline(admin.TabularInline):
    """Inline single elimination settings."""
    model = SingleEliminationSettings
    extra = 0
    fields = ('allow_byes', 'auto_balance_bracket')


class DoubleEliminationSettingsInline(admin.TabularInline):
    """Inline double elimination settings."""
    model = DoubleEliminationSettings
    extra = 0
    fields = ('grand_final_reset_enabled', 'third_place_match')


class GroupKnockoutSettingsInline(admin.TabularInline):
    """Inline group knockout settings."""
    model = GroupKnockoutSettings
    extra = 0
    fields = (
        'group_size', 'qualifiers_per_group', 'points_per_win',
        'points_per_draw', 'points_per_loss', 'tiebreaker_rule'
    )


class PlayerInline(admin.TabularInline):
    """Inline players for tournament."""
    model = Player
    extra = 1
    fields = ('gamer_tag', 'name', 'seed_number', 'status', 'phone')
    ordering = ['seed_number']


class GroupMembershipInline(admin.TabularInline):
    """Inline group memberships."""
    model = GroupMembership
    extra = 1
    fields = ('player',)


class MatchInline(admin.TabularInline):
    """Inline matches for groups."""
    model = Match
    extra = 0
    fields = (
        'round_number', 'player1', 'player2', 'player1_score',
        'player2_score', 'winner', 'status', 'console_assigned'
    )
    readonly_fields = ('round_number',)


class GroupStandingsInline(admin.TabularInline):
    """Inline standings for groups."""
    model = GroupStandings
    extra = 0
    fields = (
        'player', 'matches_played', 'wins', 'draws', 'losses',
        'points', 'score_difference', 'position', 'qualified'
    )
    readonly_fields = ('matches_played', 'points', 'score_difference')


# ============================================================================
# 🏆 TOURNAMENT ADMIN (Main Hub)
# ============================================================================

@admin.register(Tournament)
class TournamentAdmin(admin.ModelAdmin):
    """Main tournament management interface."""
    
    list_display = (
        'name_badge', 'game_title', 'format_type_badge',
        'status_badge', 'player_count', 'registration_deadline_short'
    )
    
    list_filter = (
        'status', 'format_type', 'created_at', 'registration_deadline'
    )
    
    search_fields = ('name', 'game_title')
    
    fieldsets = (
        ('🎮 Tournament Info', {
            'fields': ('name', 'game_title', 'format_type', 'status')
        }),
        ('👥 Players', {
            'fields': ('max_players', 'current_player_count')
        }),
        ('📅 Timeline', {
            'fields': ('registration_deadline', 'start_date')
        }),
        ('⏰ Metadata', {
            'fields': ('created_at', 'modified_at', 'created_by', 'modified_by'),
            'classes': ('collapse',)
        }),
    )
    
    readonly_fields = ('created_at', 'modified_at', 'created_by', 'modified_by')
    
    inlines = [
        TournamentSettingsInline,
        SingleEliminationSettingsInline,
        DoubleEliminationSettingsInline,
        GroupKnockoutSettingsInline,
        PlayerInline,
    ]
    
    ordering = ['-created_at']
    
    def name_badge(self, obj):
        """Display tournament name with badge."""
        return format_html(
            '<strong>{}</strong>',
            obj.name
        )
    name_badge.short_description = 'Tournament'
    
    def format_type_badge(self, obj):
        """Display format with color coding."""
        colors = {
            'single_elimination': '#3498db',
            'double_elimination': '#9b59b6',
            'group_knockout': '#e74c3c',
        }
        color = colors.get(obj.format_type, '#95a5a6')
        return format_html(
            '<span style="background-color: {}; color: white; padding: 3px 8px; border-radius: 3px;">{}</span>',
            color,
            obj.get_format_type_display()
        )
    format_type_badge.short_description = 'Format'
    
    def status_badge(self, obj):
        """Display status with color coding."""
        colors = {
            'registration': '#3498db',
            'active': '#2ecc71',
            'completed': '#95a5a6',
            'cancelled': '#e74c3c',
        }
        color = colors.get(obj.status, '#95a5a6')
        return format_html(
            '<span style="background-color: {}; color: white; padding: 3px 8px; border-radius: 3px;">{}</span>',
            color,
            obj.get_status_display()
        )
    status_badge.short_description = 'Status'
    
    def player_count(self, obj):
        """Display current vs max players."""
        return format_html(
            '<strong>{}/{}</strong>',
            obj.current_player_count,
            obj.max_players
        )
    player_count.short_description = 'Players'
    
    def registration_deadline_short(self, obj):
        """Display registration deadline in short format."""
        return obj.registration_deadline.strftime('%b %d, %Y')
    registration_deadline_short.short_description = 'Registration'


# ============================================================================
# 👥 PLAYER ADMIN
# ============================================================================

@admin.register(Player)
class PlayerAdmin(admin.ModelAdmin):
    """Player management interface."""
    
    list_display = (
        'gamer_tag', 'name', 'tournament_link', 'seed_number',
        'status_badge', 'phone'
    )
    
    list_filter = (
        'tournament', 'status', 'seed_number', 'created_at'
    )
    
    search_fields = ('gamer_tag', 'name', 'phone', 'tournament__name')
    
    fieldsets = (
        ('📋 Player Info', {
            'fields': ('tournament', 'gamer_tag', 'name', 'phone')
        }),
        ('🏅 Tournament Details', {
            'fields': ('seed_number', 'status')
        }),
        ('⏰ Metadata', {
            'fields': ('created_at', 'modified_at', 'created_by', 'modified_by'),
            'classes': ('collapse',)
        }),
    )
    
    readonly_fields = ('created_at', 'modified_at', 'created_by', 'modified_by')
    
    ordering = ['tournament', 'seed_number']
    
    def tournament_link(self, obj):
        """Link to tournament."""
        return format_html(
            '<strong><a href="/admin/tour/tournament/{}/change/">{}</a></strong>',
            obj.tournament.id,
            obj.tournament.name
        )
    tournament_link.short_description = 'Tournament'
    
    def status_badge(self, obj):
        """Display player status with badge."""
        colors = {
            'registered': '#3498db',
            'eliminated': '#e74c3c',
            'qualified': '#f39c12',
            'winner': '#2ecc71',
        }
        color = colors.get(obj.status, '#95a5a6')
        return format_html(
            '<span style="background-color: {}; color: white; padding: 3px 8px; border-radius: 3px; font-weight: bold;">{}</span>',
            color,
            obj.get_status_display()
        )
    status_badge.short_description = 'Status'


# ============================================================================
# 🔀 MATCH ADMIN
# ============================================================================

@admin.register(Match)
class MatchAdmin(admin.ModelAdmin):
    """Match management interface."""
    
    list_display = (
        'match_info', 'round_number', 'bracket_type_badge',
        'score_display', 'status_badge', 'console_assigned'
    )
    
    list_filter = (
        'tournament', 'bracket_type', 'status', 'round_number'
    )
    
    search_fields = (
        'player1__gamer_tag', 'player2__gamer_tag',
        'tournament__name'
    )
    
    fieldsets = (
        ('🏆 Match Setup', {
            'fields': ('tournament', 'round_number', 'bracket_type', 'group')
        }),
        ('👥 Players', {
            'fields': ('player1', 'player2')
        }),
        ('📊 Results', {
            'fields': ('player1_score', 'player2_score', 'winner', 'status')
        }),
        ('⚙️ Logistics', {
            'fields': ('console_assigned', 'scheduled_time')
        }),
        ('⏰ Metadata', {
            'fields': ('created_at', 'modified_at', 'created_by', 'modified_by'),
            'classes': ('collapse',)
        }),
    )
    
    readonly_fields = ('created_at', 'modified_at', 'created_by', 'modified_by')
    
    ordering = ['-created_at']
    
    def match_info(self, obj):
        """Display match info."""
        return format_html(
            '<strong>{} vs {}</strong>',
            obj.player1.gamer_tag,
            obj.player2.gamer_tag
        )
    match_info.short_description = 'Match'
    
    def bracket_type_badge(self, obj):
        """Display bracket type."""
        colors = {
            'group': '#3498db',
            'winners': '#2ecc71',
            'losers': '#e74c3c',
            'final': '#f39c12',
        }
        color = colors.get(obj.bracket_type, '#95a5a6')
        return format_html(
            '<span style="background-color: {}; color: white; padding: 3px 8px; border-radius: 3px;">{}</span>',
            color,
            obj.get_bracket_type_display()
        )
    bracket_type_badge.short_description = 'Bracket'
    
    def score_display(self, obj):
        """Display match score."""
        if obj.player1_score is None or obj.player2_score is None:
            return '—'
        return format_html(
            '<strong>{} - {}</strong>',
            obj.player1_score,
            obj.player2_score
        )
    score_display.short_description = 'Score'
    
    def status_badge(self, obj):
        """Display match status."""
        colors = {
            'pending': '#95a5a6',
            'playing': '#f39c12',
            'completed': '#2ecc71',
            'cancelled': '#e74c3c',
        }
        color = colors.get(obj.status, '#95a5a6')
        return format_html(
            '<span style="background-color: {}; color: white; padding: 3px 8px; border-radius: 3px;">{}</span>',
            color,
            obj.get_status_display()
        )
    status_badge.short_description = 'Status'


# ============================================================================
# 🎲 GROUP ADMIN
# ============================================================================

@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    """Group management for group stage tournaments."""
    
    list_display = ('name', 'tournament_link', 'member_count', 'group_number')
    
    list_filter = ('tournament', 'group_number')
    
    search_fields = ('name', 'tournament__name')
    
    fieldsets = (
        ('📍 Group Info', {
            'fields': ('tournament', 'name', 'group_number')
        }),
        ('⏰ Metadata', {
            'fields': ('created_at', 'modified_at', 'created_by', 'modified_by'),
            'classes': ('collapse',)
        }),
    )
    
    readonly_fields = ('created_at', 'modified_at', 'created_by', 'modified_by')
    
    inlines = [GroupMembershipInline, MatchInline, GroupStandingsInline]
    
    ordering = ['tournament', 'group_number']
    
    def tournament_link(self, obj):
        """Link to tournament."""
        return format_html(
            '<a href="/admin/tour/tournament/{}/change/">{}</a>',
            obj.tournament.id,
            obj.tournament.name
        )
    tournament_link.short_description = 'Tournament'
    
    def member_count(self, obj):
        """Count of members in group."""
        count = obj.memberships.count()
        return format_html('<strong>{}</strong> members', count)
    member_count.short_description = 'Members'


# ============================================================================
# 📊 GROUP STANDINGS ADMIN
# ============================================================================

@admin.register(GroupStandings)
class GroupStandingsAdmin(admin.ModelAdmin):
    """Standings management for group stage."""
    
    list_display = (
        'player_name', 'group_name', 'position_badge',
        'record', 'points_badge', 'score_diff', 'qualified_badge'
    )
    
    list_filter = ('group__tournament', 'qualified', 'position')
    
    search_fields = ('player__gamer_tag', 'group__name')
    
    fieldsets = (
        ('👥 Participant', {
            'fields': ('group', 'player')
        }),
        ('📈 Record', {
            'fields': (
                'matches_played', 'wins', 'draws', 'losses',
                'points', 'score_for', 'score_against', 'score_difference'
            )
        }),
        ('🏆 Position', {
            'fields': ('position', 'qualified')
        }),
        ('⏰ Metadata', {
            'fields': ('modified_at', 'modified_by'),
            'classes': ('collapse',)
        }),
    )
    
    readonly_fields = (
        'matches_played', 'wins', 'draws', 'losses',
        'points', 'score_for', 'score_against', 'score_difference',
        'modified_at', 'modified_by'
    )
    
    ordering = ['group', '-points', '-score_difference']
    
    def player_name(self, obj):
        """Player gamer tag."""
        return format_html(
            '<strong>{}</strong>',
            obj.player.gamer_tag
        )
    player_name.short_description = 'Player'
    
    def group_name(self, obj):
        """Group name."""
        return obj.group.name
    group_name.short_description = 'Group'
    
    def position_badge(self, obj):
        """Display position with badge."""
        if obj.position is None:
            return '—'
        colors = ['#f39c12', '#95a5a6', '#cd7f32', '#95a5a6']
        color = colors[obj.position - 1] if obj.position <= 4 else '#95a5a6'
        return format_html(
            '<span style="background-color: {}; color: white; padding: 5px 10px; border-radius: 50%; font-weight: bold; display: inline-block; width: 20px; text-align: center;">{}</span>',
            color,
            obj.position
        )
    position_badge.short_description = 'Pos'
    
    def record(self, obj):
        """Win-Draw-Loss record."""
        return format_html(
            '<strong>{}-{}-{}</strong>',
            obj.wins,
            obj.draws,
            obj.losses
        )
    record.short_description = 'Record'
    
    def points_badge(self, obj):
        """Points with badge."""
        return format_html(
            '<span style="background-color: #3498db; color: white; padding: 3px 8px; border-radius: 3px; font-weight: bold;">{}</span>',
            obj.points
        )
    points_badge.short_description = 'Points'
    
    def score_diff(self, obj):
        """Score difference."""
        color = '#2ecc71' if obj.score_difference >= 0 else '#e74c3c'
        sign = '+' if obj.score_difference >= 0 else ''
        return format_html(
            '<span style="color: {}; font-weight: bold;">{}{}</span>',
            color,
            sign,
            obj.score_difference
        )
    score_diff.short_description = 'Score Diff'
    
    def qualified_badge(self, obj):
        """Qualified status."""
        if obj.qualified:
            return format_html(
                '<span style="background-color: #2ecc71; color: white; padding: 3px 8px; border-radius: 3px; font-weight: bold;">✓ Qualified</span>'
            )
        return format_html(
            '<span style="background-color: #95a5a6; color: white; padding: 3px 8px; border-radius: 3px;">—</span>'
        )
    qualified_badge.short_description = 'Qualified'


# ============================================================================
# 🎯 BRACKET POSITION ADMIN
# ============================================================================

@admin.register(BracketPosition)
class BracketPositionAdmin(admin.ModelAdmin):
    """Bracket position management for elimination tournaments."""
    
    list_display = (
        'player_name', 'tournament_link', 'bracket_type_badge',
        'position', 'round_eliminated_display'
    )
    
    list_filter = ('tournament', 'bracket_type')
    
    search_fields = ('player__gamer_tag', 'tournament__name')
    
    fieldsets = (
        ('🏆 Position Info', {
            'fields': ('tournament', 'player', 'bracket_type', 'position')
        }),
        ('📋 Elimination', {
            'fields': ('round_eliminated',)
        }),
        ('⏰ Metadata', {
            'fields': ('created_at', 'modified_at', 'created_by', 'modified_by'),
            'classes': ('collapse',)
        }),
    )
    
    readonly_fields = ('created_at', 'modified_at', 'created_by', 'modified_by')
    
    ordering = ['tournament', 'bracket_type', 'position']
    
    def player_name(self, obj):
        """Player gamer tag."""
        return format_html(
            '<strong>{}</strong>',
            obj.player.gamer_tag
        )
    player_name.short_description = 'Player'
    
    def tournament_link(self, obj):
        """Link to tournament."""
        return format_html(
            '<a href="/admin/tour/tournament/{}/change/">{}</a>',
            obj.tournament.id,
            obj.tournament.name
        )
    tournament_link.short_description = 'Tournament'
    
    def bracket_type_badge(self, obj):
        """Display bracket type."""
        colors = {
            'winners': '#2ecc71',
            'losers': '#e74c3c',
            'final': '#f39c12',
        }
        color = colors.get(obj.bracket_type, '#95a5a6')
        return format_html(
            '<span style="background-color: {}; color: white; padding: 3px 8px; border-radius: 3px;">{}</span>',
            color,
            obj.get_bracket_type_display()
        )
    bracket_type_badge.short_description = 'Bracket'
    
    def round_eliminated_display(self, obj):
        """Show round eliminated or N/A."""
        if obj.round_eliminated is None:
            return format_html(
                '<span style="color: #2ecc71; font-weight: bold;">Still Active</span>'
            )
        return format_html(
            'Round <strong>{}</strong>',
            obj.round_eliminated
        )
    round_eliminated_display.short_description = 'Eliminated'


# ============================================================================
# ⚙️ SETTINGS ADMINS (Read-only for reference)
# ============================================================================

@admin.register(TournamentSettings)
class TournamentSettingsAdmin(admin.ModelAdmin):
    """Tournament settings management."""
    
    list_display = (
        'tournament_link', 'seeding_enabled', 'number_of_consoles',
        'match_duration_minutes', 'auto_generate_fixtures'
    )
    
    list_filter = ('seeding_enabled', 'shuffle_players', 'auto_generate_fixtures')
    
    search_fields = ('tournament__name',)
    
    fieldsets = (
        ('🎮 Tournament', {
            'fields': ('tournament',)
        }),
        ('⚙️ Seeding & Shuffling', {
            'fields': ('seeding_enabled', 'shuffle_players')
        }),
        ('🖥️ Hardware', {
            'fields': ('number_of_consoles', 'match_duration_minutes')
        }),
        ('🏆 Match Config', {
            'fields': ('third_place_match', 'auto_generate_fixtures', 'lock_settings')
        }),
    )
    
    ordering = ['tournament']
    
    def tournament_link(self, obj):
        """Link to tournament."""
        return format_html(
            '<strong><a href="/admin/tour/tournament/{}/change/">{}</a></strong>',
            obj.tournament.id,
            obj.tournament.name
        )
    tournament_link.short_description = 'Tournament'


@admin.register(SingleEliminationSettings)
class SingleEliminationSettingsAdmin(admin.ModelAdmin):
    """Single elimination settings."""
    
    list_display = (
        'tournament_name', 'allow_byes', 'auto_balance_bracket'
    )
    
    search_fields = ('tournament__name',)
    
    def tournament_name(self, obj):
        """Tournament name."""
        return obj.tournament.name
    tournament_name.short_description = 'Tournament'


@admin.register(DoubleEliminationSettings)
class DoubleEliminationSettingsAdmin(admin.ModelAdmin):
    """Double elimination settings."""
    
    list_display = (
        'tournament_name', 'grand_final_reset_enabled', 'third_place_match'
    )
    
    search_fields = ('tournament__name',)
    
    def tournament_name(self, obj):
        """Tournament name."""
        return obj.tournament.name
    tournament_name.short_description = 'Tournament'


@admin.register(GroupKnockoutSettings)
class GroupKnockoutSettingsAdmin(admin.ModelAdmin):
    """Group knockout settings."""
    
    list_display = (
        'tournament_name', 'group_size', 'qualifiers_per_group',
        'points_per_win', 'tiebreaker_rule'
    )
    
    search_fields = ('tournament__name',)
    
    fieldsets = (
        ('🎮 Tournament', {
            'fields': ('tournament',)
        }),
        ('👥 Groups', {
            'fields': ('group_size', 'qualifiers_per_group')
        }),
        ('📊 Scoring', {
            'fields': ('points_per_win', 'points_per_draw', 'points_per_loss', 'tiebreaker_rule')
        }),
        ('🔧 Generation', {
            'fields': ('auto_generate_knockout',)
        }),
    )
    
    def tournament_name(self, obj):
        """Tournament name."""
        return obj.tournament.name
    tournament_name.short_description = 'Tournament'

from typing import Optional, List

from naff.client.mixins.nattrs import Field, Nattrs
from naff.client.utils.attr_converters import timestamp_converter, optional
from naff.client.utils.serializer import dict_filter_none
from naff.models.discord.emoji import PartialEmoji
from naff.models.discord.enums import ActivityType, ActivityFlags
from naff.models.discord.snowflake import Snowflake_Type
from naff.models.discord.timestamp import Timestamp

__all__ = (
    "ActivityTimestamps",
    "ActivityParty",
    "ActivityAssets",
    "ActivitySecrets",
    "Activity",
)


class ActivityTimestamps(Nattrs):
    start: Optional[Timestamp] = Field(repr=False, default=None, converter=optional(timestamp_converter))
    """The start time of the activity. Shows "elapsed" timer on discord client."""
    end: Optional[Timestamp] = Field(repr=False, default=None, converter=optional(timestamp_converter))
    """The end time of the activity. Shows "remaining" timer on discord client."""


class ActivityParty(Nattrs):
    id: Optional[str] = Field(repr=False, default=None)
    """A unique identifier for this party"""
    size: Optional[List[int]] = Field(repr=False, default=None)
    """Info about the size of the party"""


class ActivityAssets(Nattrs):
    large_image: Optional[str] = Field(repr=False, default=None)
    """The large image for this activity. Uses discord's asset image url format."""
    large_text: Optional[str] = Field(repr=False, default=None)
    """Hover text for the large image"""
    small_image: Optional[str] = Field(repr=False, default=None)
    """The large image for this activity. Uses discord's asset image url format."""
    small_text: Optional[str] = Field(repr=False, default=None)
    """Hover text for the small image"""


class ActivitySecrets(Nattrs):
    join: Optional[str] = Field(repr=False, default=None)
    """The secret for joining a party"""
    spectate: Optional[str] = Field(repr=False, default=None)
    """The secret for spectating a party"""
    match: Optional[str] = Field(repr=False, default=None)
    """The secret for a specific instanced match"""


class Activity(Nattrs):
    """Represents a discord activity object use for rich presence in discord."""

    name: str = Field(repr=True)
    """The activity's name"""
    type: ActivityType = Field(repr=True, default=ActivityType.GAME)
    """The type of activity"""
    url: Optional[str] = Field(repr=True, default=None)
    """Stream url, is validated when type is 1"""
    created_at: Optional[Timestamp] = Field(repr=True, default=None, converter=optional(timestamp_converter))
    """When the activity was added to the user's session"""
    timestamps: Optional[ActivityTimestamps] = Field(
        repr=False, default=None, converter=optional(ActivityTimestamps.from_dict)
    )
    """Start and/or end of the game"""
    application_id: "Snowflake_Type" = Field(repr=False, default=None)
    """Application id for the game"""
    details: Optional[str] = Field(repr=False, default=None)
    """What the player is currently doing"""
    state: Optional[str] = Field(repr=False, default=None)
    """The user's current party status"""
    emoji: Optional[PartialEmoji] = Field(repr=False, default=None, converter=optional(PartialEmoji.from_dict))
    """The emoji used for a custom status"""
    party: Optional[ActivityParty] = Field(repr=False, default=None, converter=optional(ActivityParty.from_dict))
    """Information for the current party of the player"""
    assets: Optional[ActivityAssets] = Field(repr=False, default=None, converter=optional(ActivityAssets.from_dict))
    """Assets to display on the player's profile"""
    secrets: Optional[ActivitySecrets] = Field(repr=False, default=None, converter=optional(ActivitySecrets.from_dict))
    """Secrets for Rich Presence joining and spectating"""
    instance: Optional[bool] = Field(repr=False, default=False)
    """Whether or not the activity is an instanced game session"""
    flags: Optional[ActivityFlags] = Field(repr=False, default=None, converter=optional(ActivityFlags))
    """Activity flags bitwise OR together, describes what the payload includes"""
    buttons: List[str] = Field(repr=False, factory=list)
    """The custom buttons shown in the Rich Presence (max 2)"""

    @classmethod
    def create(cls, name: str, type: ActivityType = ActivityType.GAME, url: Optional[str] = None) -> "Activity":
        """
        Creates an activity object for the bot.

        Args:
            name: The new activity's name
            type: Type of activity to create
            url: Stream link for the activity

        Returns:
            The new activity object

        """
        return cls(name=name, type=type, url=url)  # noqa

    def to_dict(self) -> dict:
        return dict_filter_none({"name": self.name, "type": self.type, "url": self.url})

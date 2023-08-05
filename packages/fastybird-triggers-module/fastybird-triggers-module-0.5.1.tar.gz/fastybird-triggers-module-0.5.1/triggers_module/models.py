#!/usr/bin/python3

#     Copyright 2021. FastyBird s.r.o.
#
#     Licensed under the Apache License, Version 2.0 (the "License");
#     you may not use this file except in compliance with the License.
#     You may obtain a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#     Unless required by applicable law or agreed to in writing, software
#     distributed under the License is distributed on an "AS IS" BASIS,
#     WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#     See the License for the specific language governing permissions and
#     limitations under the License.

"""
Triggers module models
"""

# Library dependencies
import uuid
import datetime
from typing import List, Tuple, Dict
from exchange_plugin.dispatcher import EventDispatcher
from kink import inject
from modules_metadata.triggers_module import TriggerConditionOperator
from pony.orm import Database, PrimaryKey, Required, Optional, Set, Discriminator, Json

# Create triggers module database accessor
from triggers_module.events import ModelEntityCreatedEvent, ModelEntityUpdatedEvent, ModelEntityDeletedEvent

db: Database = Database()


@inject
class TriggerEntity(db.Entity):
    """
    Base trigger entity

    @package        FastyBird:TriggersModule!
    @module         models

    @author         Adam Kadlec <adam.kadlec@fastybird.com>
    """
    _table_: str = "fb_triggers"

    type = Discriminator(str, column="trigger_type")
    _discriminator_: str = "trigger"

    trigger_id: uuid.UUID = PrimaryKey(uuid.UUID, default=uuid.uuid4, column="trigger_id")
    name: str = Required(str, column="trigger_name", max_len=100, nullable=False)
    comment: str or None = Optional(str, column="trigger_comment", nullable=True, default=None)
    enabled: bool = Optional(bool, column="trigger_enabled", nullable=True, default=True)
    params: Json or None = Optional(Json, column="params", nullable=True)
    created_at: datetime.datetime or None = Optional(datetime.datetime, column="created_at", nullable=True)
    updated_at: datetime.datetime or None = Optional(datetime.datetime, column="updated_at", nullable=True)

    actions: List["ActionEntity"] = Set("ActionEntity", reverse="trigger")
    notifications: List["NotificationEntity"] = Set("NotificationEntity", reverse="trigger")
    controls: List["TriggerControlEntity"] = Set("TriggerControlEntity", reverse="trigger")

    _event_dispatcher: EventDispatcher

    # -----------------------------------------------------------------------------

    def __init__(self, event_dispatcher: EventDispatcher, *args, **kwargs) -> None:
        db.Entity.__init__(self, *args, **kwargs)

        self._event_dispatcher = event_dispatcher

    # -----------------------------------------------------------------------------

    def to_dict(
        self,
        only: Tuple = None,  # pylint: disable=unused-argument
        exclude: Tuple = None,  # pylint: disable=unused-argument
        with_collections: bool = False,  # pylint: disable=unused-argument
        with_lazy: bool = False,  # pylint: disable=unused-argument
        related_objects: bool = False,  # pylint: disable=unused-argument
    ) -> Dict[str, str or int or bool or None]:
        """Transform entity to dictionary"""
        return {
            "id": self.trigger_id.__str__(),
            "type": self.type,
            "name": self.name,
            "comment": self.comment,
            "enabled": self.enabled,
            "params": self.params,
        }

    # -----------------------------------------------------------------------------

    def before_insert(self) -> None:
        """Before insert entity hook"""
        self.created_at = datetime.datetime.now()

    # -----------------------------------------------------------------------------

    def after_insert(self) -> None:
        """After insert entity hook"""
        self._event_dispatcher.dispatch(
            ModelEntityCreatedEvent.EVENT_NAME,
            ModelEntityCreatedEvent(self),
        )

    # -----------------------------------------------------------------------------

    def before_update(self) -> None:
        """Before update entity hook"""
        self.updated_at = datetime.datetime.now()

    # -----------------------------------------------------------------------------

    def after_update(self) -> None:
        """After update entity hook"""
        self._event_dispatcher.dispatch(
            ModelEntityUpdatedEvent.EVENT_NAME,
            ModelEntityUpdatedEvent(self),
        )

    # -----------------------------------------------------------------------------

    def after_delete(self) -> None:
        """After delete entity hook"""
        self._event_dispatcher.dispatch(
            ModelEntityDeletedEvent.EVENT_NAME,
            ModelEntityDeletedEvent(self),
        )


class ManualTriggerEntity(TriggerEntity):
    """
    Manual trigger entity

    @package        FastyBird:TriggersModule!
    @module         models

    @author         Adam Kadlec <adam.kadlec@fastybird.com>
    """
    _discriminator_: str = "manual"


class AutomaticTriggerEntity(TriggerEntity):
    """
    Automatic trigger entity

    @package        FastyBird:TriggersModule!
    @module         models

    @author         Adam Kadlec <adam.kadlec@fastybird.com>
    """
    _discriminator_: str = "automatic"

    conditions: List["ConditionEntity"] = Set("ConditionEntity", reverse="trigger")


@inject
class TriggerControlEntity(db.Entity):
    """
    Trigger control entity

    @package        FastyBird:DevicesModule!
    @module         models

    @author         Adam Kadlec <adam.kadlec@fastybird.com>
    """
    _table_: str = "fb_triggers_controls"

    control_id: uuid.UUID = PrimaryKey(uuid.UUID, default=uuid.uuid4, column="control_id")
    name: str = Optional(str, column="control_name", nullable=False)
    created_at: datetime.datetime or None = Optional(datetime.datetime, column="created_at", nullable=True)
    updated_at: datetime.datetime or None = Optional(datetime.datetime, column="updated_at", nullable=True)

    trigger: TriggerEntity = Required("TriggerEntity", reverse="controls", column="trigger_id", nullable=False)

    __event_dispatcher: EventDispatcher

    # -----------------------------------------------------------------------------

    def __init__(self, event_dispatcher: EventDispatcher, *args, **kwargs) -> None:
        db.Entity.__init__(self, *args, **kwargs)

        self.__event_dispatcher = event_dispatcher

    # -----------------------------------------------------------------------------

    def before_insert(self) -> None:
        """Before insert entity hook"""
        self.created_at = datetime.datetime.now()

    # -----------------------------------------------------------------------------

    def after_insert(self) -> None:
        """After insert entity hook"""
        self.__event_dispatcher.dispatch(
            ModelEntityCreatedEvent.EVENT_NAME,
            ModelEntityCreatedEvent(self),
        )

    # -----------------------------------------------------------------------------

    def before_update(self) -> None:
        """Before update entity hook"""
        self.updated_at = datetime.datetime.now()

    # -----------------------------------------------------------------------------

    def after_update(self) -> None:
        """After update entity hook"""
        self.__event_dispatcher.dispatch(
            ModelEntityUpdatedEvent.EVENT_NAME,
            ModelEntityUpdatedEvent(self),
        )

    # -----------------------------------------------------------------------------

    def after_delete(self) -> None:
        """After delete entity hook"""
        self.__event_dispatcher.dispatch(
            ModelEntityDeletedEvent.EVENT_NAME,
            ModelEntityDeletedEvent(self),
        )


@inject
class ActionEntity(db.Entity):
    """
    Base action entity

    @package        FastyBird:TriggersModule!
    @module         models

    @author         Adam Kadlec <adam.kadlec@fastybird.com>
    """
    _table_: str = "fb_actions"

    type = Discriminator(str, column="action_type")

    action_id: uuid.UUID = PrimaryKey(uuid.UUID, default=uuid.uuid4, column="action_id")
    enabled: bool = Required(bool, column="action_enabled", nullable=False, default=True)
    created_at: datetime.datetime or None = Optional(datetime.datetime, column="created_at", nullable=True)
    updated_at: datetime.datetime or None = Optional(datetime.datetime, column="updated_at", nullable=True)

    trigger: TriggerEntity = Required("TriggerEntity", reverse="actions", column="trigger_id", nullable=False)

    _event_dispatcher: EventDispatcher

    # -----------------------------------------------------------------------------

    def __init__(self, event_dispatcher: EventDispatcher, *args, **kwargs) -> None:
        db.Entity.__init__(self, *args, **kwargs)

        self._event_dispatcher = event_dispatcher

    # -----------------------------------------------------------------------------

    def to_dict(
        self,
        only: Tuple = None,  # pylint: disable=unused-argument
        exclude: Tuple = None,  # pylint: disable=unused-argument
        with_collections: bool = False,  # pylint: disable=unused-argument
        with_lazy: bool = False,  # pylint: disable=unused-argument
        related_objects: bool = False,  # pylint: disable=unused-argument
    ) -> Dict[str, str or int or bool or None]:
        """Transform entity to dictionary"""
        return {
            "id": self.action_id.__str__(),
            "type": self.type,
            "enabled": self.enabled,
            "trigger": self.trigger.trigger_id.__str__(),
        }

    # -----------------------------------------------------------------------------

    def before_insert(self) -> None:
        """Before insert entity hook"""
        self.created_at = datetime.datetime.now()

    # -----------------------------------------------------------------------------

    def after_insert(self) -> None:
        """After insert entity hook"""
        self._event_dispatcher.dispatch(
            ModelEntityCreatedEvent.EVENT_NAME,
            ModelEntityCreatedEvent(self),
        )

    # -----------------------------------------------------------------------------

    def before_update(self) -> None:
        """Before update entity hook"""
        self.updated_at = datetime.datetime.now()

    # -----------------------------------------------------------------------------

    def after_update(self) -> None:
        """After update entity hook"""
        self._event_dispatcher.dispatch(
            ModelEntityUpdatedEvent.EVENT_NAME,
            ModelEntityUpdatedEvent(self),
        )

    # -----------------------------------------------------------------------------

    def after_delete(self) -> None:
        """After delete entity hook"""
        self._event_dispatcher.dispatch(
            ModelEntityDeletedEvent.EVENT_NAME,
            ModelEntityDeletedEvent(self),
        )


class PropertyActionEntity(ActionEntity):
    """
    Property action entity

    @package        FastyBird:TriggersModule!
    @module         models

    @author         Adam Kadlec <adam.kadlec@fastybird.com>
    """
    device: uuid.UUID = Required(uuid.UUID, column="action_device", nullable=True)

    value: str = Required(str, column="action_value", max_len=100, nullable=True)

    # -----------------------------------------------------------------------------

    def to_dict(
        self,
        only: Tuple = None,
        exclude: Tuple = None,
        with_collections: bool = False,
        with_lazy: bool = False,
        related_objects: bool = False,
    ) -> Dict[str, str or int or bool or None]:
        """Transform entity to dictionary"""
        return {**{
            "device": self.device.__str__(),
            "value": self.value,
        }, **super().to_dict(only, exclude, with_collections, with_lazy, related_objects)}


class DevicePropertyActionEntity(PropertyActionEntity):
    """
    Device property action entity

    @package        FastyBird:TriggersModule!
    @module         models

    @author         Adam Kadlec <adam.kadlec@fastybird.com>
    """
    _discriminator_: str = "device-property"

    device_property: uuid.UUID = Required(uuid.UUID, column="action_device_property", nullable=True)

    # -----------------------------------------------------------------------------

    def to_dict(
        self,
        only: Tuple = None,
        exclude: Tuple = None,
        with_collections: bool = False,
        with_lazy: bool = False,
        related_objects: bool = False,
    ) -> Dict[str, str or int or bool or None]:
        """Transform entity to dictionary"""
        return {**{
            "property": self.device_property.__str__(),
        }, **super().to_dict(only, exclude, with_collections, with_lazy, related_objects)}


class ChannelPropertyActionEntity(PropertyActionEntity):
    """
    Channel property action entity

    @package        FastyBird:TriggersModule!
    @module         models

    @author         Adam Kadlec <adam.kadlec@fastybird.com>
    """
    _discriminator_: str = "channel-property"

    channel: uuid.UUID = Required(uuid.UUID, column="action_channel", nullable=True)
    channel_property: uuid.UUID = Required(uuid.UUID, column="action_channel_property", nullable=True)

    # -----------------------------------------------------------------------------

    def to_dict(
        self,
        only: Tuple = None,
        exclude: Tuple = None,
        with_collections: bool = False,
        with_lazy: bool = False,
        related_objects: bool = False,
    ) -> Dict[str, str or int or bool or None]:
        """Transform entity to dictionary"""
        return {**{
            "channel": self.channel.__str__(),
            "property": self.channel_property.__str__(),
        }, **super().to_dict(only, exclude, with_collections, with_lazy, related_objects)}


@inject
class NotificationEntity(db.Entity):
    """
    Base notification entity

    @package        FastyBird:TriggersModule!
    @module         models

    @author         Adam Kadlec <adam.kadlec@fastybird.com>
    """
    _table_: str = "fb_notifications"

    type = Discriminator(str, column="notification_type")

    notification_id: uuid.UUID = PrimaryKey(uuid.UUID, default=uuid.uuid4, column="notification_id")
    enabled: bool = Required(bool, column="notification_enabled", nullable=False, default=True)
    created_at: datetime.datetime or None = Optional(datetime.datetime, column="created_at", nullable=True)
    updated_at: datetime.datetime or None = Optional(datetime.datetime, column="updated_at", nullable=True)

    trigger: TriggerEntity = Required("TriggerEntity", reverse="notifications", column="trigger_id", nullable=False)

    _event_dispatcher: EventDispatcher

    # -----------------------------------------------------------------------------

    def __init__(self, event_dispatcher: EventDispatcher, *args, **kwargs) -> None:
        db.Entity.__init__(self, *args, **kwargs)

        self._event_dispatcher = event_dispatcher

    # -----------------------------------------------------------------------------

    def to_dict(
        self,
        only: Tuple = None,  # pylint: disable=unused-argument
        exclude: Tuple = None,  # pylint: disable=unused-argument
        with_collections: bool = False,  # pylint: disable=unused-argument
        with_lazy: bool = False,  # pylint: disable=unused-argument
        related_objects: bool = False,  # pylint: disable=unused-argument
    ) -> Dict[str, str or int or bool or None]:
        """Transform entity to dictionary"""
        return {
            "id": self.notification_id.__str__(),
            "type": self.type,
            "enabled": self.enabled,
            "trigger": self.trigger.trigger_id.__str__(),
        }

    # -----------------------------------------------------------------------------

    def before_insert(self) -> None:
        """Before insert entity hook"""
        self.created_at = datetime.datetime.now()

    # -----------------------------------------------------------------------------

    def after_insert(self) -> None:
        """After insert entity hook"""
        self._event_dispatcher.dispatch(
            ModelEntityCreatedEvent.EVENT_NAME,
            ModelEntityCreatedEvent(self),
        )

    # -----------------------------------------------------------------------------

    def before_update(self) -> None:
        """Before update entity hook"""
        self.updated_at = datetime.datetime.now()

    # -----------------------------------------------------------------------------

    def after_update(self) -> None:
        """After update entity hook"""
        self._event_dispatcher.dispatch(
            ModelEntityUpdatedEvent.EVENT_NAME,
            ModelEntityUpdatedEvent(self),
        )

    # -----------------------------------------------------------------------------

    def after_delete(self) -> None:
        """After delete entity hook"""
        self._event_dispatcher.dispatch(
            ModelEntityDeletedEvent.EVENT_NAME,
            ModelEntityDeletedEvent(self),
        )


class EmailNotificationEntity(NotificationEntity):
    """
    Email notification entity

    @package        FastyBird:TriggersModule!
    @module         models

    @author         Adam Kadlec <adam.kadlec@fastybird.com>
    """
    _discriminator_: str = "email"

    email: str = Required(str, column="notification_email", max_len=150, nullable=True)

    # -----------------------------------------------------------------------------

    def to_dict(
        self,
        only: Tuple = None,
        exclude: Tuple = None,
        with_collections: bool = False,
        with_lazy: bool = False,
        related_objects: bool = False,
    ) -> Dict[str, str or int or bool or None]:
        """Transform entity to dictionary"""
        return {**{
            "email": self.email,
        }, **super().to_dict(only, exclude, with_collections, with_lazy, related_objects)}


class SmsNotificationEntity(NotificationEntity):
    """
    SMS notification entity

    @package        FastyBird:TriggersModule!
    @module         models

    @author         Adam Kadlec <adam.kadlec@fastybird.com>
    """
    _discriminator_: str = "sms"

    phone: str = Required(str, column="notification_phone", max_len=150, nullable=True)

    # -----------------------------------------------------------------------------

    def to_dict(
        self,
        only: Tuple = None,
        exclude: Tuple = None,
        with_collections: bool = False,
        with_lazy: bool = False,
        related_objects: bool = False,
    ) -> Dict[str, str or int or bool or None]:
        """Transform entity to dictionary"""
        return {**{
            "phone": self.phone,
        }, **super().to_dict(only, exclude, with_collections, with_lazy, related_objects)}


@inject
class ConditionEntity(db.Entity):
    """
    Base condition entity

    @package        FastyBird:TriggersModule!
    @module         models

    @author         Adam Kadlec <adam.kadlec@fastybird.com>
    """
    _table_: str = "fb_conditions"

    type = Discriminator(str, column="condition_type")

    condition_id: uuid.UUID = PrimaryKey(uuid.UUID, default=uuid.uuid4, column="condition_id")
    enabled: bool = Required(bool, column="condition_enabled", nullable=False, default=True)
    created_at: datetime.datetime or None = Optional(datetime.datetime, column="created_at", nullable=True)
    updated_at: datetime.datetime or None = Optional(datetime.datetime, column="updated_at", nullable=True)

    trigger: AutomaticTriggerEntity = Required(
        "AutomaticTriggerEntity",
        reverse="conditions",
        column="trigger_id",
        nullable=False,
    )

    _event_dispatcher: EventDispatcher

    # -----------------------------------------------------------------------------

    def __init__(self, event_dispatcher: EventDispatcher, *args, **kwargs) -> None:
        db.Entity.__init__(self, *args, **kwargs)

        self._event_dispatcher = event_dispatcher

    # -----------------------------------------------------------------------------

    def to_dict(
        self,
        only: Tuple = None,  # pylint: disable=unused-argument
        exclude: Tuple = None,  # pylint: disable=unused-argument
        with_collections: bool = False,  # pylint: disable=unused-argument
        with_lazy: bool = False,  # pylint: disable=unused-argument
        related_objects: bool = False,  # pylint: disable=unused-argument
    ) -> Dict[str, str or int or bool or None]:
        """Transform entity to dictionary"""
        return {
            "id": self.condition_id.__str__(),
            "type": self.type,
            "enabled": self.enabled,
            "trigger": self.trigger.trigger_id.__str__(),
        }

    # -----------------------------------------------------------------------------

    def before_insert(self) -> None:
        """Before insert entity hook"""
        self.created_at = datetime.datetime.now()

    # -----------------------------------------------------------------------------

    def after_insert(self) -> None:
        """After insert entity hook"""
        self._event_dispatcher.dispatch(
            ModelEntityCreatedEvent.EVENT_NAME,
            ModelEntityCreatedEvent(self),
        )

    # -----------------------------------------------------------------------------

    def before_update(self) -> None:
        """Before update entity hook"""
        self.updated_at = datetime.datetime.now()

    # -----------------------------------------------------------------------------

    def after_update(self) -> None:
        """After update entity hook"""
        self._event_dispatcher.dispatch(
            ModelEntityUpdatedEvent.EVENT_NAME,
            ModelEntityUpdatedEvent(self),
        )

    # -----------------------------------------------------------------------------

    def after_delete(self) -> None:
        """After delete entity hook"""
        self._event_dispatcher.dispatch(
            ModelEntityDeletedEvent.EVENT_NAME,
            ModelEntityDeletedEvent(self),
        )


class PropertyConditionEntity(ConditionEntity):
    """
    Property condition entity

    @package        FastyBird:TriggersModule!
    @module         models

    @author         Adam Kadlec <adam.kadlec@fastybird.com>
    """
    operator: TriggerConditionOperator = Required(TriggerConditionOperator, column="condition_operator",
                                                  nullable=True)
    operand: str = Required(str, column="condition_operand", max_len=100, nullable=True)

    device: uuid.UUID = Required(uuid.UUID, column="condition_device", nullable=True)

    # -----------------------------------------------------------------------------

    def to_dict(
        self,
        only: Tuple = None,
        exclude: Tuple = None,
        with_collections: bool = False,
        with_lazy: bool = False,
        related_objects: bool = False,
    ) -> Dict[str, str or int or bool or None]:
        """Transform entity to dictionary"""
        return {**{
            "operator": self.operator,
            "operand": self.operand,
            "device": self.device.__str__(),
        }, **super().to_dict(only, exclude, with_collections, with_lazy, related_objects)}


class DevicePropertyConditionEntity(PropertyConditionEntity):
    """
    Device property condition entity

    @package        FastyBird:TriggersModule!
    @module         models

    @author         Adam Kadlec <adam.kadlec@fastybird.com>
    """
    _discriminator_: str = "device-property"

    device_property: uuid.UUID = Required(uuid.UUID, column="condition_device_property", nullable=True)

    # -----------------------------------------------------------------------------

    def to_dict(
        self,
        only: Tuple = None,
        exclude: Tuple = None,
        with_collections: bool = False,
        with_lazy: bool = False,
        related_objects: bool = False,
    ) -> Dict[str, str or int or bool or None]:
        """Transform entity to dictionary"""
        return {**{
            "property": self.device_property.__str__(),
        }, **super().to_dict(only, exclude, with_collections, with_lazy, related_objects)}


class ChannelPropertyConditionEntity(PropertyConditionEntity):
    """
    Channel property condition entity

    @package        FastyBird:TriggersModule!
    @module         models

    @author         Adam Kadlec <adam.kadlec@fastybird.com>
    """
    _discriminator_: str = "channel-property"

    channel: uuid.UUID = Required(uuid.UUID, column="condition_channel", nullable=True)
    channel_property: uuid.UUID = Required(uuid.UUID, column="condition_channel_property", nullable=True)

    # -----------------------------------------------------------------------------

    def to_dict(
        self,
        only: Tuple = None,
        exclude: Tuple = None,
        with_collections: bool = False,
        with_lazy: bool = False,
        related_objects: bool = False,
    ) -> Dict[str, str or int or bool or None]:
        """Transform entity to dictionary"""
        return {**{
            "channel": self.channel.__str__(),
            "property": self.channel_property.__str__(),
        }, **super().to_dict(only, exclude, with_collections, with_lazy, related_objects)}


class TimeConditionEntity(ConditionEntity):
    """
    Time property condition entity

    @package        FastyBird:TriggersModule!
    @module         models

    @author         Adam Kadlec <adam.kadlec@fastybird.com>
    """
    _discriminator_: str = "time"

    time: datetime.timedelta = Required(datetime.timedelta, column="condition_time", nullable=True)
    days: str = Required(str, column="condition_days", max_len=100, nullable=True)

    # -----------------------------------------------------------------------------

    def to_dict(
        self,
        only: Tuple = None,
        exclude: Tuple = None,
        with_collections: bool = False,
        with_lazy: bool = False,
        related_objects: bool = False,
    ) -> Dict[str, str or int or bool or None]:
        """Transform entity to dictionary"""
        return {**{
            "time": self.time,
            "days": self.days,
        }, **super().to_dict(only, exclude, with_collections, with_lazy, related_objects)}


class DateConditionEntity(ConditionEntity):
    """
    Date property condition entity

    @package        FastyBird:TriggersModule!
    @module         models

    @author         Adam Kadlec <adam.kadlec@fastybird.com>
    """
    _discriminator_: str = "date"

    date: datetime.datetime = Required(datetime.datetime, column="condition_date", nullable=True)

    # -----------------------------------------------------------------------------

    def to_dict(
        self,
        only: Tuple = None,
        exclude: Tuple = None,
        with_collections: bool = False,
        with_lazy: bool = False,
        related_objects: bool = False,
    ) -> Dict[str, str or int or bool or None]:
        """Transform entity to dictionary"""
        return {**{
            "date": self.date,
        }, **super().to_dict(only, exclude, with_collections, with_lazy, related_objects)}

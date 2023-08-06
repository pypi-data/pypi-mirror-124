from abc import ABC
from typing import Optional, List

from lgt_data.engine import UserFeedLead
from loguru import logger
from cachetools import cached, TTLCache
from lgt_data.model import UserModel
from lgt_data.mongo_repository import UserBotCredentialsMongoRepository, UserMongoRepository, DedicatedBotRepository, \
    LeadMongoRepository, to_object_id
from pydantic import BaseModel

from ..basejobs import BaseBackgroundJobData, BaseBackgroundJob

"""
User user feed handling
"""

class UpdateUserFeedJobData(BaseBackgroundJobData, BaseModel):
    lead_id: str
    bot_name: Optional[str]
    dedicated_bot_id: Optional[str]

class UpdateUserFeedJob(BaseBackgroundJob, ABC):
    @cached(cache=TTLCache(maxsize=500, ttl=600))
    def get_user_ids(self, workspace) -> List[str]:
        bots = UserBotCredentialsMongoRepository().get_active_bots(workspace)
        return list(set([str(bot.user_id) for bot in bots]))

    @property
    def job_data_type(self) -> type:
        return UpdateUserFeedJobData

    @staticmethod
    def get_users(users_ids: List[str]) -> List[UserModel]:
        return UserMongoRepository().get_users(users_ids=users_ids)

    def exec(self, data: UpdateUserFeedJobData):
        lead = LeadMongoRepository().get(data.lead_id)
        if not lead:
            logger.warning(f"[WARNING] Unable resolve lead by id: {data.lead_id}")
            return

        if data.dedicated_bot_id:
            bot = DedicatedBotRepository().get_by_id(data.dedicated_bot_id)
            if not bot:
                logger.warning(f"[WARNING] Unable resolve bot by id: {data.dedicated_bot_id}")
                return


        user_ids = self.get_user_ids(data.bot_name)
        users = self.get_users(user_ids)

        for user_id in user_ids:
            user = next((user for user in users if str(user.id) == user_id), None)
            if user and data.bot_name in user.excluded_workspaces:
                continue

            if user and user.excluded_channels and user.excluded_channels.get(data.bot_name) and \
                    (lead.message.channel_id in user.excluded_channels.get(data.bot_name)):
                continue

            UserFeedLead(
                user_id=to_object_id(user.id),
                lead_id=lead.id,
                text=lead.message.message,
                created_at=lead.created_at,
                full_message_text=lead.full_message_text
            ).save()

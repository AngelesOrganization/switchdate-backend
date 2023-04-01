from abc import ABC, abstractmethod

from presentation.schemes.group_schema import GroupCreateSchema


class GroupRepository(ABC):

    @abstractmethod
    def get_group_by_id(self, group_id: int):
        pass

    @abstractmethod
    def get_groups(self, skip: int = 0, limit: int = 100):
        pass

    @abstractmethod
    def create_group(self, user: GroupCreateSchema):
        pass

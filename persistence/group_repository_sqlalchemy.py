from uuid import UUID

from sqlalchemy.orm import Session

from database.configuration import SessionLocal
from database.group import Group
from persistence.schemes.group_schema import GroupCreate


class GroupRepositorySqlAlchemy:
    db: Session = SessionLocal()

    def get_group_by_id(self, group_id: UUID) -> Group | None:
        return self.db.query(Group).filter(Group.id == group_id).first()

    def get_groups(self, skip: int = 0, limit: int = 100):
        pass

    def create_group(self, group: GroupCreate) -> Group:
        db_group = Group(
            name=group.name,
            description=group.description
        )
        self.db.add(db_group)
        self.db.commit()
        self.db.refresh(db_group)
        self.db.close()

        return db_group

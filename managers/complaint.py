from db_api import database
from models import complaint, RoleType, State


class ComplaintManager:
    @staticmethod
    async def get_complaints(user):
        q = complaint.select()
        if user['role'] == RoleType.complainer:
            q = q.where(complaint.c.complainer_id == user['id'])

        elif user['role'] == RoleType.approver:
            q = q.where(complaint.c.state == State.pending)

        return await database.fetch_all(q)

    @staticmethod
    async def create_complaint(complaint_data):
        id_ = await database.execute(complaint.insert().values(complaint_data))
        data = await database.execute(complaint.select().where(complaint.c.id == id_))
        return {
            "status": "success",
            "data": data
        }

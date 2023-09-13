import os
import uuid

from constants import TEMP_FILE_FOLDER
from db_api import database
from models import RoleType, State, complaint, transaction
from services import S3Service, SESService
from services.wise import WiseService
from utils.helper import decode_photo

s3 = S3Service()
ses = SESService()


class ComplaintManager:
    @staticmethod
    async def get_complaints(user):
        q = complaint.select()
        if user["role"] == RoleType.complainer:
            q = q.where(complaint.c.complainer_id == user["id"])

        elif user["role"] == RoleType.approver:
            q = q.where(complaint.c.state == State.pending)

        return await database.fetch_all(q)

    @staticmethod
    async def create_complaint(complaint_data: dict, user):
        complaint_data["complainer_id"] = user["id"]
        encoded_photo = complaint_data.pop("encoded_photo")
        extension = complaint_data.pop("extension")
        name = f"{uuid.uuid4()}.{extension}"
        path = os.path.join(TEMP_FILE_FOLDER, name)
        decode_photo(path, encoded_photo)

        complaint_data["photo_url"] = s3.upload(path, name, extension)
        os.remove(path)

        id_ = await database.execute(complaint.insert().values(complaint_data))
        await ComplaintManager.issue_transaction(
            complaint_data["amount"], f"{user['first_name']} {user['last_name']}"
        , user['iban'], id_)

        return await database.fetch_one(complaint.select().where(complaint.c.id == id_))

    @staticmethod
    async def delete_complaint(complaint_id):
        await database.execute(complaint.delete().where(complaint.c.id == complaint_id))

    @staticmethod
    async def approve(id_):
        await database.execute(
            complaint.update()
            .where(complaint.c.id == id_)
            .values(status=State.approved)
        )
        ses.send_mail(
            "Complaint approved",
            ["abisher72@gmail.com"],
            "Congratulations! Your complaint has been approved. Check your bank account for refund.",
        )

    @staticmethod
    async def rejected(id_):
        await database.execute(
            complaint.update()
            .where(complaint.c.id == id_)
            .values(status=State.rejected)
        )

    @staticmethod
    async def issue_transaction(amount, full_name, iban, complaint_id):
        wise = WiseService()

        quote_id = await wise.create_quote(amount)
        recipient_id = await wise.create_recipient_account(full_name, iban)
        transfer_id = await wise.create_transfer(recipient_id, quote_id)

        data = {
            "quote_id": quote_id,
            "transfer_id": transfer_id,
            "target_account_id": str(recipient_id),
            "amount": amount,
            "complaint_id": complaint_id,
        }

        await database.execute(transaction.insert().values(**data))

        # res = await wise.fund_transfer(transfer_id)

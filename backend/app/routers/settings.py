from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.dependencies import get_current_user
from app.database.connection import get_db
from app.models.setting import HotelSetting
from app.models.room_type import RoomType
from app.schemas.setting import HotelProfile, TaxSetting, PaymentSetting, RoomSetting

router = APIRouter(prefix="/api/settings", tags=["Settings"])


def ok(message, data=None):
    return {"success": True, "message": message, "data": data, "errors": None}


async def get_or_create(db):
    x = await db.scalar(select(HotelSetting).where(HotelSetting.is_deleted.is_(False)))
    if not x:
        x = HotelSetting()
        db.add(x)
        await db.commit()
        await db.refresh(x)
    return x


def data(x):
    return {
        "name": x.name,
        "phone": x.phone,
        "email": x.email,
        "address": x.address,
        "gst": float(x.gst),
        "service_tax": float(x.service_tax),
        "cash": x.cash,
        "upi": x.upi,
        "card": x.card,
    }


@router.get("")
async def read(db: AsyncSession = Depends(get_db), _=Depends(get_current_user)):
    return ok("Settings retrieved", data(await get_or_create(db)))


@router.put("")
async def profile(
    req: HotelProfile, db: AsyncSession = Depends(get_db), _=Depends(get_current_user)
):
    x = await get_or_create(db)
    for k, v in req.model_dump().items():
        setattr(x, k, v.strip() if isinstance(v, str) else v)
    await db.commit()
    return ok("Hotel profile updated", data(x))


@router.put("/tax")
async def tax(
    req: TaxSetting, db: AsyncSession = Depends(get_db), _=Depends(get_current_user)
):
    x = await get_or_create(db)
    x.gst = req.gst
    x.service_tax = req.service_tax
    await db.commit()
    return ok("Tax settings updated", data(x))


@router.put("/payment")
async def payment(
    req: PaymentSetting, db: AsyncSession = Depends(get_db), _=Depends(get_current_user)
):
    x = await get_or_create(db)
    x.cash = req.cash
    x.upi = req.upi
    x.card = req.card
    await db.commit()
    return ok("Payment settings updated", data(x))


@router.post("/rooms")
async def room(
    req: RoomSetting, db: AsyncSession = Depends(get_db), _=Depends(get_current_user)
):
    x = await db.scalar(
        select(RoomType).where(
            RoomType.name == req.room_type, RoomType.is_deleted.is_(False)
        )
    )
    if x:
        x.base_price = req.price
        x.capacity = req.capacity
    else:
        x = RoomType(
            name=req.room_type,
            base_price=req.price,
            capacity=req.capacity,
            bed_type="Standard",
            description="Created from settings",
        )
        db.add(x)
    await db.commit()
    return ok("Room type settings saved", {"id": str(x.id)})

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from src.main.auth.auth_controller import get_current_user
from src.main.commons.db_configuration import get_db
from src.main.shifts.models import Shift
from src.main.swaps.schemes import CreateSwap
from src.main.swaps.models import ShiftSwap, ShiftSwapStatus

from src.main.users.models import User

router = APIRouter(
    prefix='/swaps',
    tags=['swaps']
)


@router.get("/{swap_id}")
async def get_swap(shift_swaps_id: str, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    return user.shift_swap


@router.post("")
async def create_swap(request: CreateSwap, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    shift_swap: ShiftSwap = ShiftSwap(
        requester_id=user.id,
        requested_id=request.requested_id,
        requester_shift_id=request.requester_shift_id,
        requested_shift_id=request.requested_shift_id,
        status=ShiftSwapStatus.pendiente
    )
    db.add(shift_swap)
    db.commit()
    db.refresh(shift_swap)

    return shift_swap


@router.put("/accept/{swap_id}")
async def accept_swap(swap_id: str, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    swap = db.query(ShiftSwap).filter(ShiftSwap.id == swap_id).first()

    if not swap:
        return {"detail": "Swap not found"}

    if user.id != swap.requester_id and user.id != swap.requested_id:
        return {"detail": "User not part of this swap"}

    requester_shift = db.query(Shift).filter(Shift.id == swap.requester_shift_id).first()
    requested_shift = db.query(Shift).filter(Shift.id == swap.requested_shift_id).first()

    if not requester_shift or not requested_shift:
        return {"detail": "Shift not found"}

    requester_shift.user_id, requested_shift.user_id = requested_shift.user_id, requester_shift.user_id

    swap.status = ShiftSwapStatus.aceptado

    db.commit()

    return swap


@router.put("/decline/{swap_id}")
async def decline_swap(swap_id: str, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    swap = db.query(ShiftSwap).filter(ShiftSwap.id == swap_id).first()

    if not swap:
        return {"detail": "Swap not found"}

    if user.id != swap.requester_id and user.id != swap.requested_id:
        return {"detail": "User not part of this swap"}

    swap.status = ShiftSwapStatus.rechazado

    db.commit()

    return swap

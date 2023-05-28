from fastapi import APIRouter, Depends, HTTPException
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


@router.put("/status/{swap_id}")
async def status_swap(swap_id: str, status: str, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    swap = db.query(ShiftSwap).filter(ShiftSwap.id == swap_id, ShiftSwap.requested_id == user.id).first()

    if not swap:
        return {"detail": "Swap not found"}

    requester_shift = db.query(Shift).filter(Shift.id == swap.requester_shift_id).first()
    requested_shift = db.query(Shift).filter(Shift.id == swap.requested_shift_id).first()

    if not requester_shift or not requested_shift:
        return {"detail": "Shift not found"}

    if status == "rechazar":
        swap.status = ShiftSwapStatus.rechazado
    elif status == "aceptar":
        requester_shift.user_id, requested_shift.user_id = requested_shift.user_id, requester_shift.user_id
        swap.status = ShiftSwapStatus.aceptado
    else:
        raise HTTPException(status_code=400, detail=f"Status [{status}] not valid.")

    db.commit()

    return swap


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

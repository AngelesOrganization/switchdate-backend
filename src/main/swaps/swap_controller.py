from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from src.main.auth.auth_controller import get_current_user
from src.main.commons.db_configuration import get_db
from src.main.swaps.schemes import CreateSwaps
from src.main.swaps.models import ShiftSwap, ShiftSwapStatus

from src.main.users.models import User

router = APIRouter(
    prefix='/swaps',
    tags=['swaps']
)


@router.get("/{swap_id}")
async def get_swap(shift_swaps_id: str, db: Session = Depends(get_db), user: User = Depends(get_current_user)):

    
    return user.shift_swap


@router.post("/")
async def create_swap(request: CreateSwaps, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
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

@router.get("/")
async def accept_swap():


    return

@router.get("/")
async def decline_swap()


    return




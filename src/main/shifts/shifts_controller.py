from fastapi import APIRouter, Depends
from fastapi import HTTPException
from sqlalchemy import extract, func
from sqlalchemy.orm import Session

from src.main.auth.auth_controller import get_current_user
from src.main.commons.db_configuration import get_db
from src.main.shifts.models import Shift
from src.main.shifts.schemes import CreateShift
from src.main.users.models import User

router = APIRouter(
    prefix='/shifts',
    tags=['shifts']
)


@router.get("")
async def get_shifts(month: int, year: int, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    if month > 12 or month < 1:
        return "Invalid month"

    return db.query(Shift).filter(Shift.user_id == user.id, extract('month', Shift.start_time) == month,
                                  extract('year', Shift.start_time) == year).all()


@router.post("")
async def create_shift(request: CreateShift, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    shift_date = request.start_time.date()

    existing_shift = db.query(Shift).filter(
        Shift.user_id == user.id,
        func.date(Shift.start_time) == shift_date
    ).first()
    if existing_shift:
        raise HTTPException(status_code=400, detail="Ya tienes un turno para este día")

    shift: Shift = Shift(
        user_id=user.id,
        start_time=request.start_time,
        end_time=request.end_time
    )

    db.add(shift)
    db.commit()
    db.refresh(shift)

    return shift


@router.delete("/{shift_id}")
async def delete_shift(shift_id: str, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    shift: Shift | None = db.query(Shift).filter(Shift.id == shift_id, Shift.user_id == user.id).first()
    if shift is None:
        return

    db.delete(shift)
    db.commit()


@router.get("/{user_id}")
def get_shifts(month: int, year: int, user_id: str, user: User = Depends(get_current_user),
               db: Session = Depends(get_db)):
    candidate_user = db.query(User).filter(User.id == user_id).first()

    if candidate_user is None or user is None:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    # Verificar si los usuarios están en el mismo grupo
    common_groups = set(candidate_user.groups) & set(user.groups)
    if not common_groups:
        raise HTTPException(status_code=403, detail="No tienes permiso para acceder a los turnos de este usuario")

    return db.query(Shift).filter(
        Shift.user_id == candidate_user.id,
        extract('month', Shift.start_time) == month,
        extract('year', Shift.start_time) == year).all()


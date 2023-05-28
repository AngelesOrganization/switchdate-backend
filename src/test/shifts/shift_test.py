from datetime import datetime, timedelta

from sqlalchemy import func

from src.main.groups.models import Group, UserGroup
from src.main.shifts.models import Shift


def test_get_shifts(client, db_session, user_token: str, test_user, postgres_container):
    # Crear un grupo y agregarlo a la base de datos
    group = Group(name="testgroup", description="Test Group")
    db_session.add(group)
    db_session.commit()
    db_session.refresh(group)

    # Crear un UserGroup que asocie el usuario y el grupo y agregarlo a la base de datos
    user_group = UserGroup(user_id=test_user.id, group_id=group.id)
    db_session.add(user_group)
    db_session.commit()

    # Crear un turno para testUser para el que se solicitará un cambio
    shift = Shift(user_id=test_user.id, start_time=datetime.now(),
                  end_time=datetime.now() + timedelta(hours=8))
    db_session.add(shift)
    db_session.commit()

    # Hacer la solicitud GET al endpoint
    headers = {"Authorization": f"Bearer {user_token}"}
    response = client.get(f"/shifts/{test_user.id}?month={datetime.now().month}&year={datetime.now().year}",
                          headers=headers)
    assert response.status_code == 200, response.text
    data = response.json()

    # Verificar que el turno es devuelto correctamente
    assert len(data) == 1
    assert data[0]['id'] == str(shift.id)
    assert data[0]['user_id'] == str(test_user.id)
    assert data[0]['start_time'].replace("T", " ") == str(shift.start_time)
    assert data[0]['end_time'].replace("T", " ") == str(shift.end_time)


def test_delete_shift(client, db_session, user_token: str, test_user, postgres_container):
    # Crear un turno para testUser para luego borrarlo
    shift = Shift(user_id=test_user.id, start_time=datetime.now(),
                  end_time=datetime.now() + timedelta(hours=8))
    db_session.add(shift)
    db_session.commit()

    # Hacer la solicitud DELETE al endpoint
    headers = {"Authorization": f"Bearer {user_token}"}
    response = client.delete(f"/shifts/{shift.id}", headers=headers)
    assert response.status_code == 200, response.text

    # Verificar que el turno ha sido eliminado
    deleted_shift = db_session.query(Shift).filter_by(id=shift.id).first()
    assert deleted_shift is None


def test_create_shift(client, db_session, user_token: str, test_user, postgres_container):
    # Crear los datos para el turno
    shift_data = {
        "start_time": datetime.now().isoformat(),
        "end_time": (datetime.now() + timedelta(hours=8)).isoformat()
    }

    # Hacer la solicitud POST al endpoint
    headers = {"Authorization": f"Bearer {user_token}"}
    response = client.post("/shifts", json=shift_data, headers=headers)

    # Comprobar que la respuesta tiene un código de estado 200
    assert response.status_code == 200, response.text

    # Comprobar que el turno se ha creado correctamente
    shift = db_session.query(Shift).filter(
        Shift.user_id == test_user.id,
        func.date(Shift.start_time) == datetime.now().date()
    ).first()
    assert shift is not None

    # Comprobar que los datos del turno corresponden a los datos enviados en la solicitud
    assert shift.start_time.isoformat() == shift_data["start_time"]
    assert shift.end_time.isoformat() == shift_data["end_time"]


def test_get_shifts(client, db_session, user_token: str, test_user, postgres_container):
    # Crear los datos para un turno
    current_month = datetime.now().month
    current_year = datetime.now().year
    shift_data = {
        "start_time": datetime.now().isoformat(),
        "end_time": (datetime.now() + timedelta(hours=8)).isoformat()
    }

    # Crear un turno para el usuario
    shift: Shift = Shift(
        user_id=test_user.id,
        start_time=datetime.fromisoformat(shift_data["start_time"]),
        end_time=datetime.fromisoformat(shift_data["end_time"])
    )
    db_session.add(shift)
    db_session.commit()

    # Hacer la solicitud GET al endpoint
    headers = {"Authorization": f"Bearer {user_token}"}
    response = client.get(f"/shifts?month={current_month}&year={current_year}", headers=headers)

    # Comprobar que la respuesta tiene un código de estado 200
    assert response.status_code == 200, response.text

    # Comprobar que los turnos se han devuelto correctamente
    shifts = response.json()
    assert shifts is not None
    assert len(shifts) > 0

    # Comprobar que los datos del turno corresponden a los datos enviados en la solicitud
    assert shifts[0]["start_time"] == shift_data["start_time"]
    assert shifts[0]["end_time"] == shift_data["end_time"]

from datetime import datetime, timedelta

from src.main.groups.models import UserGroup, UserGroupRole, Group
from src.main.shifts.models import Shift
from src.main.swaps.models import ShiftSwap, ShiftSwapStatus
from src.main.users.models import User


def test_create_user(client, postgres_container, db_session):
    new_user = {
        "username": "testuser",
        "email": "testuser@example.com",
        "first_name": "Test",
        "last_name": "User",
        "password": "testpassword",
        "role": "member"
    }
    response = client.post("/users/", json=new_user)
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["email"] == new_user["email"]
    assert data["username"] == new_user["username"]
    assert "id" in data
    user_id = data["id"]

    user_in_db = db_session.query(User).filter(User.id == user_id).first()
    assert user_in_db is not None
    assert user_in_db.email == new_user["email"]
    assert user_in_db.username == new_user["username"]


def test_get_users_by_group(client, db_session, user_token: str, postgres_container, test_user):
    # Crear un grupo y agregarlo a la base de datos
    group = Group(name="testgroup", description="Test Group")
    db_session.add(group)
    db_session.commit()
    db_session.refresh(group)

    # Crear un UserGroup que asocie el usuario y el grupo y agregarlo a la base de datos
    user_group = UserGroup(user_id=test_user.id, group_id=group.id)
    db_session.add(user_group)
    db_session.commit()

    # Hacer la solicitud GET al endpoint
    headers = {"Authorization": f"Bearer {user_token}"}
    response = client.get(f"/users/{group.id}", headers=headers)
    assert response.status_code == 200, response.text
    data = response.json()

    # Verificar que el usuario está en el grupo
    assert len(data) == 1
    assert data[0]["id"] == str(test_user.id)
    assert data[0]["username"] == test_user.username


def test_get_user_requested_swaps(client, db_session, user_token: str, postgres_container, test_user):
    # Crear un turno para testUser para el que se solicitará un cambio
    requester_shift = Shift(user_id=test_user.id, start_time=datetime.now(),
                            end_time=datetime.now() + timedelta(hours=8))
    db_session.add(requester_shift)
    db_session.commit()

    # Crear un segundo usuario y turno que será solicitado para el cambio
    requested_user = User(username="requested", email="requested@test.com", first_name="Requested",
                          last_name="Test", hashed_password="hashed_password", role="user_role")
    db_session.add(requested_user)
    db_session.commit()
    requested_shift = Shift(user_id=requested_user.id, start_time=datetime.now(),
                            end_time=datetime.now() + timedelta(hours=8))
    db_session.add(requested_shift)
    db_session.commit()

    # Crear un ShiftSwap que vincula ambos turnos y usuarios
    swap = ShiftSwap(requester_id=test_user.id, requested_id=requested_user.id,
                     requester_shift_id=requester_shift.id, requested_shift_id=requested_shift.id,
                     status=ShiftSwapStatus.pendiente)
    db_session.add(swap)
    db_session.commit()

    # Hacer la solicitud GET al endpoint
    headers = {"Authorization": f"Bearer {user_token}"}
    response = client.get("/users/requested-swaps", headers=headers)
    assert response.status_code == 200, response.text
    data = response.json()

    # Verificar que el ShiftSwap fue devuelto correctamente
    assert len(data['swaps']) == 1
    assert data['swaps'][0]['id'] == str(swap.id)
    assert data['swaps'][0]['requester']['id'] == str(test_user.id)
    assert data['swaps'][0]['requested']['id'] == str(requested_user.id)
    assert data['swaps'][0]['requester_shift']['id'] == str(requester_shift.id)
    assert data['swaps'][0]['requested_shift']['id'] == str(requested_shift.id)


def test_get_user_requester_swaps(client, db_session, user_token: str, postgres_container, test_user):
    # Crear un turno para testUser para el que se solicitará un cambio
    requester_shift = Shift(user_id=test_user.id, start_time=datetime.now(),
                            end_time=datetime.now() + timedelta(hours=8))
    db_session.add(requester_shift)
    db_session.commit()

    # Crear un segundo usuario y turno que será solicitado para el cambio
    requested_user = User(username="requested", email="requested@test.com", first_name="Requested",
                          last_name="Test", hashed_password="hashed_password", role="user_role")
    db_session.add(requested_user)
    db_session.commit()
    requested_shift = Shift(user_id=requested_user.id, start_time=datetime.now(),
                            end_time=datetime.now() + timedelta(hours=8))
    db_session.add(requested_shift)
    db_session.commit()

    # Crear un ShiftSwap que vincula ambos turnos y usuarios
    swap = ShiftSwap(requester_id=requested_user.id, requested_id=test_user.id,
                     requester_shift_id=requested_shift.id, requested_shift_id=requester_shift.id,
                     status=ShiftSwapStatus.pendiente)
    db_session.add(swap)
    db_session.commit()

    # Hacer la solicitud GET al endpoint
    headers = {"Authorization": f"Bearer {user_token}"}
    response = client.get("/users/requester-swaps", headers=headers)
    assert response.status_code == 200, response.text
    data = response.json()

    # Verificar que el ShiftSwap fue devuelto correctamente
    assert len(data['swaps']) == 1
    assert data['swaps'][0]['id'] == str(swap.id)
    assert data['swaps'][0]['requester']['id'] == str(requested_user.id)
    assert data['swaps'][0]['requested']['id'] == str(test_user.id)
    assert data['swaps'][0]['requester_shift']['id'] == str(requested_shift.id)
    assert data['swaps'][0]['requested_shift']['id'] == str(requester_shift.id)

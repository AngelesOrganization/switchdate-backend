from src.main.shifts.models import Shift
from src.main.swaps.models import ShiftSwap, ShiftSwapStatus


def test_create_swap(client, db_session, user_token, test_user, postgres_container):
    # Crear un segundo usuario para el test
    test_user2_data = {
        "username": "test_user2",
        "email": "test_user2@test.com",
        "first_name": "Test",
        "last_name": "User2",
        "password": "test_password2",
        "role": "user"
    }
    response = client.post("/users", json=test_user2_data)
    assert response.status_code == 200
    test_user2_id = response.json()["id"]

    # Crear dos turnos
    shift1_data = {
        "start_time": "2023-05-10T08:00:00Z",
        "end_time": "2023-05-10T16:00:00Z"
    }
    shift2_data = {
        "start_time": "2023-05-11T08:00:00Z",
        "end_time": "2023-05-11T16:00:00Z"
    }
    headers = {"Authorization": f"Bearer {user_token}"}
    response = client.post("/shifts", json=shift1_data, headers=headers)
    assert response.status_code == 200
    shift1_id = response.json()["id"]

    response = client.post("/shifts", json=shift2_data, headers=headers)
    assert response.status_code == 200
    shift2_id = response.json()["id"]

    # Crear un swap
    swap_data = {
        "requester_id": str(test_user.id),
        "requested_id": test_user2_id,
        "requester_shift_id": shift1_id,
        "requested_shift_id": shift2_id
    }
    response = client.post("/swaps", json=swap_data, headers=headers)
    assert response.status_code == 200

    # Verificar la creación del swap directamente desde la base de datos
    swap_id = response.json()["id"]
    created_swap = db_session.query(ShiftSwap).filter(ShiftSwap.id == swap_id).first()
    assert created_swap is not None
    assert str(created_swap.id) == swap_id
    assert str(created_swap.requested_id) == test_user2_id
    assert str(created_swap.requester_shift_id) == shift1_id
    assert str(created_swap.requested_shift_id) == shift2_id
    assert created_swap.status == ShiftSwapStatus.pendiente


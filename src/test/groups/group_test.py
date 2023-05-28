from src.main.groups.models import UserGroup, UserGroupRole, Group


def test_create_group(client, db_session, user_token: str, test_user, postgres_container):
    # Crear los datos para un grupo
    group_data = {
        "name": "Test Group",
        "description": "This is a test group"
    }

    # Hacer la solicitud POST al endpoint
    headers = {"Authorization": f"Bearer {user_token}"}
    response = client.post("/groups", json=group_data, headers=headers)

    # Comprobar que la respuesta tiene un código de estado 200
    assert response.status_code == 200, response.text

    # Comprobar que el grupo se ha creado correctamente
    group = response.json()
    assert group is not None
    assert group["name"] == group_data["name"]
    assert group["description"] == group_data["description"]

    # Verificar que el usuario sea el administrador del grupo
    user_group: UserGroup | None = db_session.query(UserGroup).filter(UserGroup.user_id == test_user.id).filter(
        UserGroup.group_id == group["id"]).first()
    assert user_group is not None
    assert user_group.role == UserGroupRole.administrador


def test_delete_group(client, db_session, user_token: str, test_user, postgres_container):
    # Primero, crea un grupo
    group_data = {
        "name": "Test Group",
        "description": "This is a test group"
    }
    headers = {"Authorization": f"Bearer {user_token}"}
    response = client.post("/groups", json=group_data, headers=headers)
    assert response.status_code == 200
    group = response.json()

    # Ahora intenta eliminar el grupo
    response = client.delete(f"/groups/{group['id']}", headers=headers)
    assert response.status_code == 200

    # Verificar que el grupo se ha eliminado
    group: Group | None = db_session.query(Group).filter(Group.id == group['id']).first()
    assert group is None


def test_get_groups(client, db_session, user_token: str, test_user, postgres_container):
    # Crear algunos grupos a los que el usuario pertenezca
    group_data1 = {
        "name": "Test Group 1",
        "description": "This is a test group 1"
    }
    group_data2 = {
        "name": "Test Group 2",
        "description": "This is a test group 2"
    }
    headers = {"Authorization": f"Bearer {user_token}"}
    response1 = client.post("/groups", json=group_data1, headers=headers)
    response2 = client.post("/groups", json=group_data2, headers=headers)
    assert response1.status_code == 200
    assert response2.status_code == 200

    # Luego, intentar recuperar los grupos del usuario
    response = client.get("/groups", headers=headers)
    assert response.status_code == 200

    # Comprobar si los grupos creados se devuelven correctamente
    groups = response.json()
    assert len(groups) == 2
    assert any(group["name"] == "Test Group 1" for group in groups)
    assert any(group["name"] == "Test Group 2" for group in groups)


def test_join_user_to_group(client, db_session, user_token: str, test_user, postgres_container):
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
    test_user2_username = response.json()["username"]

    # Crear un grupo
    group_data = {
        "name": "Test Group",
        "description": "This is a test group"
    }
    headers = {"Authorization": f"Bearer {user_token}"}
    response = client.post("/groups", json=group_data, headers=headers)
    assert response.status_code == 200
    group_id = response.json()["id"]

    # Intentar unirse al grupo
    join_data = {
        "candidate_username": test_user2_username,
        "group_id": group_id
    }
    response = client.post("/groups/join", json=join_data, headers=headers)
    assert response.status_code == 200

    # Verificar si el usuario se unió correctamente al grupo
    response = client.get("/groups", headers={"Authorization": f"Bearer {user_token}"})
    assert response.status_code == 200
    groups = response.json()
    assert any(group["id"] == group_id for group in groups)

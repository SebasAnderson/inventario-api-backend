from decimal import Decimal
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.db.session import get_db
from app.main import app
from app.models import Base, Demographic, Franchise, Product, Publisher


SQLALCHEMY_TEST_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)


@event.listens_for(engine, "connect")
def _set_sqlite_pragma(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()


TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture()
def db_session():
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)


@pytest.fixture()
def client(db_session):
    def _override_get_db():
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[get_db] = _override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()


CATALOG_RESOURCES = [
    ("/api/v1/publishers", "Ivrea", "Panini", "Ovni Press"),
    ("/api/v1/franchises", "Dragon Ball", "Naruto", "Batman"),
    ("/api/v1/demographics", "Shonen", "Seinen", "Shojo"),
]


@pytest.mark.parametrize("base_url,name1,name2,name3", CATALOG_RESOURCES)
def test_catalog_crud_lifecycle(client, base_url, name1, name2, name3):
    # Lista vacía al inicio
    res = client.get(f"{base_url}/")
    assert res.status_code == 200
    assert res.json() == []

    # Crear con espacios alrededor (debe recortar whitespace)
    res = client.post(f"{base_url}/", json={"nombre": f"  {name1}  "})
    assert res.status_code == 201
    created1 = res.json()
    assert created1["nombre"] == name1
    item_id = created1["id"]

    # Crear otros dos registros
    assert client.post(f"{base_url}/", json={"nombre": name2}).status_code == 201
    assert client.post(f"{base_url}/", json={"nombre": name3}).status_code == 201

    # Listar con paginación
    res = client.get(f"{base_url}/?skip=1&limit=2")
    assert res.status_code == 200
    items = res.json()
    assert len(items) == 2
    assert [item["nombre"] for item in items] == [name2, name3]

    # Obtener por ID
    res = client.get(f"{base_url}/{item_id}")
    assert res.status_code == 200
    assert res.json()["nombre"] == name1

    # Actualizar nombre
    updated_name = f"{name1} Editado"
    res = client.put(f"{base_url}/{item_id}", json={"nombre": updated_name})
    assert res.status_code == 200
    assert res.json()["nombre"] == updated_name

    # Actualizar enviando el mismo nombre con distinta capitalización (propio registro)
    res = client.put(f"{base_url}/{item_id}", json={"nombre": updated_name.lower()})
    assert res.status_code == 200
    assert res.json()["nombre"] == updated_name.lower()

    # Eliminar registro
    res = client.delete(f"{base_url}/{item_id}")
    assert res.status_code == 204

    # Verificar que ya no existe
    res = client.get(f"{base_url}/{item_id}")
    assert res.status_code == 404


@pytest.mark.parametrize("base_url,name1,name2,_", CATALOG_RESOURCES)
def test_catalog_validation_and_errors(client, base_url, name1, name2, _):
    # Crear registros base
    r1 = client.post(f"{base_url}/", json={"nombre": name1})
    r2 = client.post(f"{base_url}/", json={"nombre": name2})
    assert r1.status_code == 201
    assert r2.status_code == 201
    id1 = r1.json()["id"]

    # Rechazar duplicado exacto y case-insensitive
    assert client.post(f"{base_url}/", json={"nombre": name1}).status_code == 400
    assert client.post(f"{base_url}/", json={"nombre": name1.lower()}).status_code == 400

    # Rechazar nombre vacío o solo espacios
    assert client.post(f"{base_url}/", json={"nombre": ""}).status_code == 422
    assert client.post(f"{base_url}/", json={"nombre": "   "}).status_code == 422

    # Rechazar conflicto de nombre al actualizar
    assert client.put(f"{base_url}/{id1}", json={"nombre": name2.upper()}).status_code == 400

    # Rechazar paginación inválida
    assert client.get(f"{base_url}/?skip=-1").status_code == 422
    assert client.get(f"{base_url}/?limit=0").status_code == 422

    # 404 en operaciones sobre ID inexistente
    assert client.get(f"{base_url}/9999").status_code == 404
    assert client.put(f"{base_url}/9999", json={"nombre": "Otro"}).status_code == 404
    assert client.delete(f"{base_url}/9999").status_code == 404


def test_cannot_delete_catalog_items_with_associated_products(client, db_session):
    pub = Publisher(nombre="Editorial Ivrea")
    fran = Franchise(nombre="Chainsaw Man")
    demo = Demographic(nombre="Shonen")
    db_session.add_all([pub, fran, demo])
    db_session.commit()
    db_session.refresh(pub)
    db_session.refresh(fran)
    db_session.refresh(demo)

    product = Product(
        titulo_nombre="Chainsaw Man Vol. 1",
        precio_venta=Decimal("8500.00"),
        stock_actual=10,
        tipo_producto="Manga",
        id_franquicia=fran.id,
        id_editorial=pub.id,
        id_demografia=demo.id,
        numero_tomo="1",
    )
    db_session.add(product)
    db_session.commit()

    # Intentar borrar cualquiera de los tres debe fallar con 400
    res_pub = client.delete(f"/api/v1/publishers/{pub.id}")
    res_fran = client.delete(f"/api/v1/franchises/{fran.id}")
    res_demo = client.delete(f"/api/v1/demographics/{demo.id}")

    assert res_pub.status_code == 400
    assert res_fran.status_code == 400
    assert res_demo.status_code == 400

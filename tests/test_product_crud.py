from decimal import Decimal
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.db.session import get_db
from app.main import app
from app.models import Base, Demographic, Franchise, Publisher, StockMovement, User


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


@pytest.fixture()
def catalog_refs(db_session):
    fran = Franchise(nombre="Chainsaw Man")
    pub = Publisher(nombre="Editorial Ivrea")
    demo = Demographic(nombre="Shonen")
    db_session.add_all([fran, pub, demo])
    db_session.commit()
    db_session.refresh(fran)
    db_session.refresh(pub)
    db_session.refresh(demo)
    return {"franchise_id": fran.id, "publisher_id": pub.id, "demographic_id": demo.id}


def _manga_payload(catalog_refs, **overrides):
    data = {
        "titulo_nombre": "  Chainsaw Man Vol. 1  ",
        "descripcion": "Tomo inicial",
        "precio_venta": "8500.00",
        "stock_actual": 15,
        "tipo_producto": "Manga",
        "id_franquicia": catalog_refs["franchise_id"],
        "numero_tomo": "1",
        "id_editorial": catalog_refs["publisher_id"],
        "id_demografia": catalog_refs["demographic_id"],
        "isbn": "978-987-807-001-8",
    }
    data.update(overrides)
    return data


def _figure_payload(catalog_refs, **overrides):
    data = {
        "titulo_nombre": "Figura Denji",
        "precio_venta": "42000.50",
        "stock_actual": 4,
        "tipo_producto": "Figura",
        "id_franquicia": catalog_refs["franchise_id"],
        "marca_fabricante": "Bandai Spirits",
    }
    data.update(overrides)
    return data


def test_product_crud_lifecycle(client, catalog_refs):
    # Lista vacía al inicio
    res = client.get("/api/v1/products/")
    assert res.status_code == 200
    assert res.json() == []

    # Crear Manga, Cómic (sin demografía ni ISBN) y Figura
    res_manga = client.post("/api/v1/products/", json=_manga_payload(catalog_refs))
    assert res_manga.status_code == 201
    manga = res_manga.json()
    assert manga["titulo_nombre"] == "Chainsaw Man Vol. 1"
    assert Decimal(manga["precio_venta"]) == Decimal("8500.00")

    res_comic = client.post(
        "/api/v1/products/",
        json=_manga_payload(
            catalog_refs,
            titulo_nombre="Batman: Año Uno",
            tipo_producto="Cómic",
            numero_tomo="Tomo Único",
            id_demografia=None,
            isbn="   ",
        ),
    )
    assert res_comic.status_code == 201
    assert res_comic.json()["isbn"] is None

    res_fig = client.post("/api/v1/products/", json=_figure_payload(catalog_refs, isbn=""))
    assert res_fig.status_code == 201
    assert res_fig.json()["isbn"] is None
    assert res_fig.json()["marca_fabricante"] == "Bandai Spirits"

    # Paginación
    res_page = client.get("/api/v1/products/?skip=1&limit=2")
    assert res_page.status_code == 200
    items = res_page.json()
    assert len(items) == 2
    assert [p["titulo_nombre"] for p in items] == ["Batman: Año Uno", "Figura Denji"]

    # Obtener por ID
    res_get = client.get(f"/api/v1/products/{manga['id']}")
    assert res_get.status_code == 200
    assert res_get.json()["isbn"] == "978-987-807-001-8"

    # Actualización parcial de precio y descripción
    res_upd = client.put(
        f"/api/v1/products/{manga['id']}",
        json={"precio_venta": "9900.00", "descripcion": "Edición reimpresa"},
    )
    assert res_upd.status_code == 200
    updated = res_upd.json()
    assert Decimal(updated["precio_venta"]) == Decimal("9900.00")
    assert updated["descripcion"] == "Edición reimpresa"
    assert updated["titulo_nombre"] == "Chainsaw Man Vol. 1"

    # Eliminar producto
    res_del = client.delete(f"/api/v1/products/{manga['id']}")
    assert res_del.status_code == 204
    assert client.get(f"/api/v1/products/{manga['id']}").status_code == 404


def test_product_validations_and_constraints(client, catalog_refs):
    # Precio negativo o cero y stock negativo
    assert client.post("/api/v1/products/", json=_manga_payload(catalog_refs, precio_venta="-10.00")).status_code == 422
    assert client.post("/api/v1/products/", json=_manga_payload(catalog_refs, precio_venta="0")).status_code == 422
    assert client.post("/api/v1/products/", json=_manga_payload(catalog_refs, stock_actual=-1)).status_code == 422
    assert client.post("/api/v1/products/", json=_manga_payload(catalog_refs, titulo_nombre="   ")).status_code == 422

    # Campos dinámicos obligatorios según tipo_producto (US-03)
    assert client.post("/api/v1/products/", json=_manga_payload(catalog_refs, id_editorial=None)).status_code == 422
    assert client.post("/api/v1/products/", json=_manga_payload(catalog_refs, numero_tomo="  ")).status_code == 422
    assert client.post("/api/v1/products/", json=_figure_payload(catalog_refs, marca_fabricante=None)).status_code == 422
    assert client.post(
        "/api/v1/products/",
        json=_figure_payload(catalog_refs, tipo_producto="Merchandising", marca_fabricante=""),
    ).status_code == 422

    # Claves foráneas inexistentes
    assert client.post("/api/v1/products/", json=_manga_payload(catalog_refs, id_franquicia=9999)).status_code == 400
    assert client.post("/api/v1/products/", json=_manga_payload(catalog_refs, id_editorial=9999)).status_code == 400
    assert client.post("/api/v1/products/", json=_manga_payload(catalog_refs, id_demografia=9999)).status_code == 400

    # Crear dos productos para probar unicidad de ISBN y validaciones en PUT
    p1 = client.post("/api/v1/products/", json=_manga_payload(catalog_refs, isbn="ISBN-111")).json()
    p2 = client.post("/api/v1/products/", json=_manga_payload(catalog_refs, isbn="ISBN-222", numero_tomo="2")).json()

    # ISBN duplicado en POST y PUT
    assert client.post("/api/v1/products/", json=_manga_payload(catalog_refs, isbn="ISBN-111")).status_code == 400
    assert client.put(f"/api/v1/products/{p2['id']}", json={"isbn": "ISBN-111"}).status_code == 400

    # Actualizar manteniendo su propio ISBN sí debe funcionar
    assert client.put(f"/api/v1/products/{p1['id']}", json={"isbn": "ISBN-111"}).status_code == 200

    # Cambio de tipo incompatible o nulo en campos obligatorios en PUT
    assert client.put(f"/api/v1/products/{p1['id']}", json={"tipo_producto": "Figura"}).status_code == 400
    assert client.put(
        f"/api/v1/products/{p1['id']}",
        json={"tipo_producto": "Figura", "marca_fabricante": "Good Smile"},
    ).status_code == 200
    assert client.put(f"/api/v1/products/{p1['id']}", json={"precio_venta": None}).status_code == 422
    assert client.put(f"/api/v1/products/{p2['id']}", json={"id_editorial": 9999}).status_code == 400

    # 404 en recursos inexistentes y 422 en paginación inválida
    assert client.get("/api/v1/products/9999").status_code == 404
    assert client.put("/api/v1/products/9999", json={"precio_venta": "100.00"}).status_code == 404
    assert client.delete("/api/v1/products/9999").status_code == 404
    assert client.get("/api/v1/products/?skip=-1").status_code == 422


def test_cannot_delete_product_with_stock_movements(client, db_session, catalog_refs):
    res = client.post("/api/v1/products/", json=_manga_payload(catalog_refs))
    assert res.status_code == 201
    product_id = res.json()["id"]

    user = User(email="staff@comicstore.com", password_hash="hashed", rol="Empleado", activo=True)
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)

    movement = StockMovement(
        id_producto=product_id,
        id_usuario=user.id,
        tipo_movimiento="Ingreso",
        cantidad=10,
    )
    db_session.add(movement)
    db_session.commit()

    del_res = client.delete(f"/api/v1/products/{product_id}")
    assert del_res.status_code == 400

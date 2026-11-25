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
    # Emula LOWER() Unicode de PostgreSQL en pruebas con SQLite en memoria
    dbapi_connection.create_function("lower", 1, lambda s: s.lower() if s is not None else None)


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
def seeded_catalog(db_session):
    f_csm = Franchise(nombre="Chainsaw Man")
    f_db = Franchise(nombre="Dragon Ball")
    f_bat = Franchise(nombre="Batman")

    p_ivrea = Publisher(nombre="Editorial Ivrea")
    p_panini = Publisher(nombre="Panini Cómics")
    p_ovni = Publisher(nombre="Ovni Press")

    d_shonen = Demographic(nombre="Shonen")
    d_seinen = Demographic(nombre="Seinen")

    db_session.add_all([f_csm, f_db, f_bat, p_ivrea, p_panini, p_ovni, d_shonen, d_seinen])
    db_session.commit()
    for obj in (f_csm, f_db, f_bat, p_ivrea, p_panini, p_ovni, d_shonen, d_seinen):
        db_session.refresh(obj)

    products = [
        Product(
            titulo_nombre="Chainsaw Man Vol. 1",
            descripcion="Inicio de la saga de Denji",
            precio_venta=Decimal("8500.00"),
            stock_actual=12,
            tipo_producto="Manga",
            id_franquicia=f_csm.id,
            id_editorial=p_ivrea.id,
            id_demografia=d_shonen.id,
            numero_tomo="1",
            isbn="978-987-807-001-1",
        ),
        Product(
            titulo_nombre="Chainsaw Man Vol. 2",
            descripcion="Segundo tomo agotado",
            precio_venta=Decimal("8500.00"),
            stock_actual=0,
            tipo_producto="Manga",
            id_franquicia=f_csm.id,
            id_editorial=p_ivrea.id,
            id_demografia=d_shonen.id,
            numero_tomo="2",
            isbn="978-987-807-002-8",
        ),
        Product(
            titulo_nombre="Chainsaw Man Vol. 10",
            descripcion="Cierre de la primera parte",
            precio_venta=Decimal("9200.00"),
            stock_actual=5,
            tipo_producto="Manga",
            id_franquicia=f_csm.id,
            id_editorial=p_ivrea.id,
            id_demografia=d_shonen.id,
            numero_tomo="10",
            isbn="978-987-807-010-3",
        ),
        Product(
            titulo_nombre="Dragon Ball Color Vol. 1",
            descripcion="Edición a todo color",
            precio_venta=Decimal("12000.00"),
            stock_actual=7,
            tipo_producto="Manga",
            id_franquicia=f_db.id,
            id_editorial=p_panini.id,
            id_demografia=d_shonen.id,
            numero_tomo="1",
            isbn="978-987-808-001-0",
        ),
        Product(
            titulo_nombre="Batman: Año Uno",
            descripcion="Edición especial Frank Miller",
            precio_venta=Decimal("14500.00"),
            stock_actual=3,
            tipo_producto="Cómic",
            id_franquicia=f_bat.id,
            id_editorial=p_ovni.id,
            id_demografia=d_seinen.id,
            numero_tomo="Tomo Único",
            isbn="978-987-724-401-2",
        ),
        Product(
            titulo_nombre="Figura Denji 100% PVC",
            descripcion="Coleccionable articulado",
            precio_venta=Decimal("45000.00"),
            stock_actual=2,
            tipo_producto="Figura",
            id_franquicia=f_csm.id,
            marca_fabricante="Bandai Spirits",
        ),
    ]
    db_session.add_all(products)
    db_session.commit()
    return {
        "franchises": {"csm": f_csm.id, "db": f_db.id, "bat": f_bat.id},
        "publishers": {"ivrea": p_ivrea.id, "panini": p_panini.id, "ovni": p_ovni.id},
        "demographics": {"shonen": d_shonen.id, "seinen": d_seinen.id},
    }


def test_search_by_title_volume_and_publisher(client, seeded_catalog):
    # Buscar por título parcial (case-insensitive)
    res = client.get("/api/v1/products/search?titulo=chainsaw")
    assert res.status_code == 200
    data = res.json()
    assert data["total"] == 3
    assert all("Chainsaw Man" in item["titulo_nombre"] for item in data["items"])

    # Filtrar por número de tomo exacto '1' (no debe mezclar tomo '10')
    res = client.get("/api/v1/products/search?numero_tomo=1")
    assert res.status_code == 200
    titles = [item["titulo_nombre"] for item in res.json()["items"]]
    assert titles == ["Chainsaw Man Vol. 1", "Dragon Ball Color Vol. 1"]

    # Filtrar por número de tomo 'tomo único' (insensible a mayúsculas)
    res = client.get("/api/v1/products/search?numero_tomo=tomo%20único")
    assert res.status_code == 200
    assert [i["titulo_nombre"] for i in res.json()["items"]] == ["Batman: Año Uno"]

    # Combinar editorial + número de tomo
    ivrea_id = seeded_catalog["publishers"]["ivrea"]
    res = client.get(f"/api/v1/products/search?id_editorial={ivrea_id}&numero_tomo=1")
    assert res.status_code == 200
    assert [i["titulo_nombre"] for i in res.json()["items"]] == ["Chainsaw Man Vol. 1"]

    # Los mismos filtros funcionan también en GET /api/v1/products/
    res_list = client.get(f"/api/v1/products/?id_editorial={ivrea_id}&numero_tomo=1")
    assert res_list.status_code == 200
    assert [i["titulo_nombre"] for i in res_list.json()] == ["Chainsaw Man Vol. 1"]


def test_combined_filters_search_and_sorting(client, seeded_catalog):
    csm_id = seeded_catalog["franchises"]["csm"]
    shonen_id = seeded_catalog["demographics"]["shonen"]

    # Franquicia + demografía + en_stock=true excluye Vol. 2 (stock=0)
    res = client.get(
        f"/api/v1/products/search?id_franquicia={csm_id}&id_demografia={shonen_id}&en_stock=true"
    )
    assert res.status_code == 200
    assert [i["titulo_nombre"] for i in res.json()["items"]] == [
        "Chainsaw Man Vol. 1",
        "Chainsaw Man Vol. 10",
    ]

    # Solo sin stock
    res_out = client.get("/api/v1/products/search?en_stock=false")
    assert res_out.status_code == 200
    assert [i["titulo_nombre"] for i in res_out.json()["items"]] == ["Chainsaw Man Vol. 2"]

    # Búsqueda general por ISBN o carácter '%' escapado
    res_isbn = client.get("/api/v1/products/search?search=978-987-724")
    assert res_isbn.status_code == 200
    assert [i["titulo_nombre"] for i in res_isbn.json()["items"]] == ["Batman: Año Uno"]

    res_pct = client.get("/api/v1/products/search?search=100%25")
    assert res_pct.status_code == 200
    assert [i["titulo_nombre"] for i in res_pct.json()["items"]] == ["Figura Denji 100% PVC"]

    # Filtro por tipo y rango de precios ordenado descendente por precio
    res_price = client.get(
        "/api/v1/products/search?precio_min=9000&precio_max=15000&sort_by=precio_venta&sort_order=desc"
    )
    assert res_price.status_code == 200
    assert [i["titulo_nombre"] for i in res_price.json()["items"]] == [
        "Batman: Año Uno",
        "Dragon Ball Color Vol. 1",
        "Chainsaw Man Vol. 10",
    ]

    # Rango de precio inválido -> 400
    assert client.get("/api/v1/products/search?precio_min=20000&precio_max=10000").status_code == 400


def test_search_pagination_metadata_and_validation(client, seeded_catalog):
    # Página 1 de 3 (6 productos, 2 por página)
    p1 = client.get("/api/v1/products/search?page=1&limit=2&sort_by=id&sort_order=asc").json()
    assert p1["total"] == 6
    assert p1["page"] == 1
    assert p1["limit"] == 2
    assert p1["total_pages"] == 3
    assert p1["has_next"] is True
    assert p1["has_prev"] is False
    assert len(p1["items"]) == 2

    # Página 2
    p2 = client.get("/api/v1/products/search?page=2&limit=2").json()
    assert p2["has_next"] is True
    assert p2["has_prev"] is True
    assert len(p2["items"]) == 2

    # Página 3 (última)
    p3 = client.get("/api/v1/products/search?page=3&limit=2").json()
    assert p3["has_next"] is False
    assert p3["has_prev"] is True
    assert len(p3["items"]) == 2

    # Página vacía fuera de rango
    p4 = client.get("/api/v1/products/search?page=4&limit=2").json()
    assert p4["total"] == 6
    assert p4["total_pages"] == 3
    assert p4["has_next"] is False
    assert p4["has_prev"] is True
    assert p4["items"] == []

    # Sin resultados
    empty = client.get("/api/v1/products/search?titulo=Inexistente123").json()
    assert empty == {
        "total": 0,
        "page": 1,
        "limit": 20,
        "total_pages": 0,
        "has_next": False,
        "has_prev": False,
        "items": [],
    }

    # Parámetros inválidos de paginación -> 422
    assert client.get("/api/v1/products/search?page=0").status_code == 422
    assert client.get("/api/v1/products/search?limit=101").status_code == 422

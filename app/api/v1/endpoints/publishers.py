from typing import List
from fastapi import APIRouter, status, Path, Response
from app.schemas.publisher import PublisherCreate, PublisherUpdate, PublisherResponse

router = APIRouter()

MOCK_PUBLISHERS = [
    PublisherResponse(id=1, nombre="Editorial Ivrea"),
    PublisherResponse(id=2, nombre="Panini Cómics"),
    PublisherResponse(id=3, nombre="Ovni Press"),
]


@router.get(
    "/",
    response_model=List[PublisherResponse],
    summary="Listar editoriales",
    description="Retorna el catálogo completo de editoriales asociadas a mangas y cómics."
)
def list_publishers():
    return MOCK_PUBLISHERS


@router.post(
    "/",
    response_model=PublisherResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Crear editorial",
    description="Registra una nueva editorial en el sistema."
)
def create_publisher(publisher_in: PublisherCreate):
    return PublisherResponse(id=4, nombre=publisher_in.nombre)


@router.get(
    "/{publisher_id}",
    response_model=PublisherResponse,
    summary="Obtener editorial por ID",
    description="Consulta los detalles de una editorial específica."
)
def get_publisher(publisher_id: int = Path(..., ge=1)):
    return PublisherResponse(id=publisher_id, nombre="Editorial Ivrea")


@router.put(
    "/{publisher_id}",
    response_model=PublisherResponse,
    summary="Actualizar editorial",
    description="Actualiza el nombre de una editorial existente."
)
def update_publisher(publisher_in: PublisherUpdate, publisher_id: int = Path(..., ge=1)):
    return PublisherResponse(id=publisher_id, nombre=publisher_in.nombre or "Editorial Actualizada")


@router.delete(
    "/{publisher_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Eliminar editorial",
    description="Elimina una editorial del sistema."
)
def delete_publisher(publisher_id: int = Path(..., ge=1)):
    return Response(status_code=status.HTTP_204_NO_CONTENT)

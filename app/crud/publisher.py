from app.crud.base import CatalogCRUD
from app.models.publisher import Publisher
from app.schemas.publisher import PublisherCreate, PublisherUpdate

publisher = CatalogCRUD[Publisher, PublisherCreate, PublisherUpdate](Publisher)

from app.crud.base import CatalogCRUD
from app.models.demographic import Demographic
from app.schemas.demographic import DemographicCreate, DemographicUpdate

demographic = CatalogCRUD[Demographic, DemographicCreate, DemographicUpdate](Demographic)

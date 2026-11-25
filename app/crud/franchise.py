from app.crud.base import CatalogCRUD
from app.models.franchise import Franchise
from app.schemas.franchise import FranchiseCreate, FranchiseUpdate

franchise = CatalogCRUD[Franchise, FranchiseCreate, FranchiseUpdate](Franchise)

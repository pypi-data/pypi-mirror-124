from fireorm.Queries import Query
from interface import Interface

from fireorm_repository.types.types import T


class InterfaceBaseRepository(Interface):
    def execute_query(
            self,
            query: Query,
    ) -> list[T]:
        pass

    def get_by_id(
            self,
            item_id: str
    ) -> Query:
        pass

    def get_by_field(
            self,
            field: str,
            operator: str,
            value: str | int | bool | list,
            query: Query = None
    ) -> Query:
        pass

    def update(self, item: T) -> T:
        pass

from fireorm.Queries import Query
from interface import implements

from fireorm_repository.repositories.interface import (
    InterfaceBaseRepository,
)
from fireorm_repository.types.types import T


class BaseRepository(implements(InterfaceBaseRepository)):
    model: T

    def execute_query(
            self,
            query: Query | T,
    ) -> list[T]:
        """
        Выполнение запроса
        """
        if isinstance(query, Query):
            items: T = query.firebase_query.get()
            return [
                self.model(id=item.id, **item._data)
                for item in items
            ]
        else:
            item: T = query
            return self.model(id=item.id, **item._data)

    def get_by_id(
            self,
            item_id: str
    ) -> Query:
        """
        Получение по id
        """
        return self.model.collection.get(item_id)

    def get_by_field(
            self,
            field: str,
            operator: str,
            value: str | int | bool | list,
            query: Query = None
    ) -> Query:
        """
        Получение по полю
        """
        if query:
            query.where(field, operator, value)
        else:
            query = self.model.collection.where(field, operator, value)
        return query

    def update(self, item: T) -> T:
        """
        Обновление
        """
        return item.update()

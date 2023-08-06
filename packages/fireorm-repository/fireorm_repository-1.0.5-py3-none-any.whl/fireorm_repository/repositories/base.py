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
            query: Query,
    ) -> list[T]:
        """
        Выполнение запроса
        """
        items: T = query.firebase_query.get()
        return [
            self.model(id=item.id, **item._data)
            for item in items
        ]

    def execute_query_raw(
            self,
            query: Query,
    ) -> list[T]:
        """
        Выполнение запроса без преобразования к объектам
        """
        items: T = query.firebase_query.get()
        return [
            {id: item.id, **item._data}
            for item in items
        ]

    def get_by_id(
            self,
            item_id: str
    ) -> T:
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

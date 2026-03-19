class NotFoundException[T](Exception):
    def __init__(self, entity_class: type[T], id: int | str, *args: object) -> None:
        super().__init__(*args)
        self.__class_name = entity_class.__name__
        self.__id = id

    def __str__(self) -> str:
        return f"{self.__class_name} with id {self.__id} does not exist"

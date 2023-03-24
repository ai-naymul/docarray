from typing import MutableSequence, TypeVar

from docarray.array.stacked.list_advance_indexing import ListAdvancedIndexing
from docarray.utils._typing import change_cls_name

T_item = TypeVar('T_item', bound=type)


class MagicList(ListAdvancedIndexing[T_item], MutableSequence[T_item]):

    _internal_type: T_item

    def __class_getitem__(cls, item):
        class _TypedList(cls):
            _internal_type = item

        return change_cls_name(
            _TypedList,
            f'{cls.__name__}[{item.__name__}]',
        )

    def __getattr__(self, item):
        return MagicList([getattr(data, item) for data in self])

    def __call__(self, *args, **kwargs):
        return MagicList([func(*args, **kwargs) for func in self])

    def __repr__(self):
        return self._data.__repr__()

    def insert(self, index: int, value: T_item) -> None:
        self._data.insert(index, value)
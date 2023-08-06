import dataclasses
from enum import Enum
from functools import partial
from inspect import isclass, iscoroutinefunction
from typing import Any, Callable, Dict, List, Tuple, Type, Union

from sqlalchemy import Table, and_, delete, inspect, not_, or_, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import RelationshipProperty, contains_eager, selectinload
from sqlalchemy.orm.util import AliasedClass, with_polymorphic
from sqlalchemy.sql import ColumnElement, Join
from sqlalchemy.sql.expression import desc, func
from sqlalchemy.sql.operators import ColumnOperators as ColOps
from strawberry.arguments import is_unset

from strawberry_mage.backends.sqlalchemy.models import _SQLAlchemyModel
from strawberry_mage.core.strawberry_types import (
    DeleteResult,
    OrderingDirection,
    PrimaryKeyField,
    QueryMany,
)
from strawberry_mage.core.type_creator import strip_typename
from strawberry_mage.core.types import IEntityModel, IsDataclass

SelectablesType = Dict[str, Union[Join, Type[_SQLAlchemyModel]]]


def _build_pk_query(
    model: Union[Type[IEntityModel], Type[_SQLAlchemyModel]],
    selectable: Union[Table, Type[_SQLAlchemyModel]],
    data: Any,
):
    pk = model.get_primary_key()
    attribute_getter = data.get if isinstance(data, dict) else partial(getattr, data)
    column_getter = (
        partial(getattr, selectable)
        if (isclass(selectable) and issubclass(selectable, IEntityModel)) or isinstance(selectable, AliasedClass)
        else partial(getattr, selectable.c)
    )
    conditions = [column_getter(key) == attribute_getter(key) for key in pk]
    return and_(*conditions)


def _build_multiple_pk_query(model: Type[Union[_SQLAlchemyModel, IEntityModel]], selectable, data: List[Any]):
    if not data:
        return
    return or_(
        _build_pk_query(
            model,
            selectable,
            {k: getattr(entry.primary_key_, k) for k in model.get_primary_key()},
        )
        for entry in data
    )


def _get_model_pk_values(model: Type[Union[_SQLAlchemyModel, IEntityModel]], data: IsDataclass):
    return tuple(getattr(data, key) for key in model.get_primary_key())


def _get_dict_pk_values(model: Type[Union[_SQLAlchemyModel, IEntityModel]], data: Dict[str, Any]):
    return tuple(data.get(key) for key in model.get_primary_key())


def _create_pk_class(data: Dict[str, Any]):
    return type("StubInput", (), {"primary_key_": type("StubPk", (), data)})()


async def _set_instance_attrs(
    model: Type[Union[_SQLAlchemyModel, IEntityModel]],
    instance: object,
    input_object: IsDataclass,
    session: AsyncSession,
):
    for prop in input_object.__dataclass_fields__:
        value = getattr(input_object, prop)
        if is_unset(value) or prop == "primary_key_":
            continue
        prop_type = strip_typename(model.get_attribute_type(prop))
        if isinstance(prop_type, str):
            related_model = model.get_schema_manager().get_model_for_name(prop_type)
            if related_model is None:
                raise Exception(f"Unable to resolve related type for {prop_type} on {model}")
            if isinstance(value, list):
                expr = select(related_model).where(_build_multiple_pk_query(related_model, related_model, value))
                setattr(instance, prop, (await session.execute(expr)).scalars().all())
            elif isinstance(value, Enum):
                setattr(instance, prop, value.name)
            else:
                setattr(
                    instance,
                    prop,
                    await session.get(related_model, dataclasses.asdict(value.primary_key_)),
                )
        else:
            setattr(instance, prop, value)


async def _apply_nested(
    model: Union[Type[IEntityModel], Type[_SQLAlchemyModel]],
    path: str,
    input_: Any,
    op: Callable,
    attribute: str,
    selectables: SelectablesType,
    eager_options: Any = None,
):
    nested_path = f"{path}.{attribute}"
    select_from = selectables[path]
    attr_getter = (
        partial(getattr, select_from)
        if (isinstance(select_from, AliasedClass) or isinstance(select_from, _SQLAlchemyModel))
        else partial(getattr, select_from.c)
    )
    prop = attr_getter(attribute)
    if nested_path not in selectables:
        related_type_name = strip_typename(model.get_attribute_type(attribute))
        related_model_raw = model.get_schema_manager().get_model_for_name(related_type_name)
        related_model = with_polymorphic(related_model_raw, "*", aliased=True)
        selectables[nested_path] = related_model
        ex = prop.expression
        join_expression = (
            ex.left == getattr(related_model, ex.right.key)
            if inspect(select_from).local_table == ex.left.table
            else ex.right == getattr(related_model, ex.left.key)
        )
        selectables["__selection__"] = selectables["__selection__"].join(related_model, join_expression, isouter=True)
    eager_options = (
        contains_eager(prop.of_type(selectables[nested_path]))
        if eager_options is None
        else eager_options.contains_eager(prop.of_type(selectables[nested_path]))
    )
    if iscoroutinefunction(op):
        return await op(selectables[nested_path], nested_path, input_, selectables, eager_options)
    return op(selectables[nested_path], nested_path, input_, selectables, eager_options)


async def create_(
    session: AsyncSession,
    model: Type[Union[_SQLAlchemyModel, IEntityModel]],
    data: List[Any],
    selection: Dict[str, Dict],
):
    # TODO: create related models as well maybe?
    models = []
    for create_type in data:
        instance = model()
        await _set_instance_attrs(model, instance, create_type, session)
        models.append(instance)
    session.add_all(models)
    await session.flush(models)
    primary_keys = [{key: getattr(instance, key) for key in model.get_primary_key()} for instance in models]
    await session.commit()

    data = [_create_pk_class(instance) for instance in primary_keys]
    polymorphic_model = with_polymorphic(model, "*", aliased=True)
    model_query = select(polymorphic_model)
    selectables: SelectablesType = {"": polymorphic_model, "__selection__": model_query}
    pk_filter = _build_multiple_pk_query(model, polymorphic_model, data)

    eager_options = await create_selection_joins(model, "", selection, selectables)
    ordering = await create_ordering(model, "", add_default_ordering(model, []), selectables)

    expression = selectables["__selection__"].filter(pk_filter).order_by(*ordering)
    if eager_options != (None,):
        expression = expression.options(*eager_options)
    return (await session.execute(expression)).unique().scalars().all()


async def update_(
    session: AsyncSession,
    model: Type[Union[_SQLAlchemyModel, IEntityModel]],
    data: List[Any],
    selection: Dict[str, Dict],
):
    pk_filter = _build_multiple_pk_query(model, model, data)
    instances = (
        (
            await session.execute(
                select(model)
                .options(*[selectinload(a.key) for a in inspect(model).attrs if isinstance(a, RelationshipProperty)])
                .where(pk_filter)
            )
        )
        .scalars()
        .all()
    )
    entities = {_get_model_pk_values(model, en): en for en in instances}
    if len(entities) != len(data):
        return [None]
    for entry in data:
        model_instance = entities[_get_model_pk_values(model, entry.primary_key_)]
        await _set_instance_attrs(model, model_instance, entry, session)
    session.add_all(entities.values())
    await session.commit()

    polymorphic_model = with_polymorphic(model, "*", aliased=True)
    model_query = select(polymorphic_model)
    selectables: SelectablesType = {"": polymorphic_model, "__selection__": model_query}
    pk_filter = _build_multiple_pk_query(model, polymorphic_model, data)

    eager_options = await create_selection_joins(model, "", selection, selectables)
    ordering = await create_ordering(model, "", add_default_ordering(model, []), selectables)

    expression = selectables["__selection__"].filter(pk_filter).order_by(*ordering)
    if eager_options != (None,):
        expression = expression.options(*eager_options)
    return (await session.execute(expression)).unique().scalars().all()


async def delete_(
    session: AsyncSession,
    model: Union[Type[IEntityModel], Type[_SQLAlchemyModel]],
    data: List[Any],
):
    pk_q = _build_multiple_pk_query(model, model, data)
    statement = delete(model).where(pk_q)
    r = await session.execute(statement)
    await session.commit()
    return DeleteResult(affected_rows=r.rowcount)


async def retrieve_(
    session: AsyncSession,
    model: Union[Type[IEntityModel], Type[_SQLAlchemyModel]],
    data: PrimaryKeyField,
    selection: Dict[str, Dict],
):
    polymorphic_model = with_polymorphic(model, "*", aliased=True)
    model_query = select(polymorphic_model)
    selectables: SelectablesType = {"": polymorphic_model, "__selection__": model_query}
    pk_filter = _build_pk_query(model, polymorphic_model, data.primary_key_)

    eager_options = await create_selection_joins(model, "", selection, selectables)

    expression = selectables["__selection__"].filter(pk_filter)
    if eager_options != (None,):
        expression = expression.options(*eager_options)
    return (await session.execute(expression)).unique().scalar()


def add_default_ordering(model: Type[Union[_SQLAlchemyModel, IEntityModel]], ordering: List[Dict]):
    return ordering + [{k: OrderingDirection.DESC for k in model.get_primary_key()}]


def cleanup_ordering(ordering: List[Dict]):
    result_ordering = []
    for ordering_entry in ordering:
        for field, value in ordering_entry.items():
            if isinstance(value, list):
                result_ordering.append({field: cleanup_ordering(value)})
            elif not is_unset(value):
                result_ordering.append({field: value})
    return result_ordering


async def create_selection_joins(
    model: Union[Type[IEntityModel], Type[_SQLAlchemyModel]],
    path: str,
    selection: Dict[Union[str, Type], Dict],
    selectables: SelectablesType,
    eager_options: Any = None,
) -> Tuple:
    eager_options_created = []
    for attr, sub_selection in selection.items():
        if isclass(attr) and issubclass(attr, _SQLAlchemyModel):
            sub_path = f"{path}-{attr.__name__}"
            if not hasattr(model, attr.__name__):
                continue
            selectables[sub_path] = getattr(model, attr.__name__)
            eager_options_created.extend(
                await create_selection_joins(
                    getattr(model, attr.__name__),
                    sub_path,
                    sub_selection,
                    selectables,
                    eager_options,
                )
            )
        else:
            eager_options_created.extend(
                await _apply_nested(
                    model,
                    path,
                    sub_selection,
                    create_selection_joins,
                    attr,
                    selectables,
                    eager_options,
                )
            )
    return tuple(eager_options_created) if eager_options_created else (eager_options,)


async def create_ordering(
    model: Union[Type[IEntityModel], Type[_SQLAlchemyModel]],
    path: str,
    ordering: List[Dict],
    selectables: SelectablesType,
    *_,
) -> List[ColumnElement]:
    result_ordering = []
    for entry in ordering:
        for attribute, value in entry.items():
            if is_unset(value):
                continue
            if isinstance(value, OrderingDirection):
                select_from = selectables[path]
                col = (
                    getattr(select_from, attribute)
                    if (isinstance(select_from, AliasedClass) or isinstance(select_from, _SQLAlchemyModel))
                    else getattr(select_from.c, attribute)
                )
                result_ordering.append(desc(col) if value == OrderingDirection.DESC else col)
            else:
                result_ordering.extend(
                    await _apply_nested(model, path, [value], create_ordering, attribute, selectables)
                )
    return result_ordering


FILTER_OPS = {
    "exact": lambda c, v: ColOps.__eq__(c, v),
    "iexact": lambda c, v: ColOps.__eq__(func.lower(c), func.lower(v)),
    "contains": lambda c, v: ColOps.contains(c, v),
    "icontains": lambda c, v: ColOps.contains(func.lower(c), func.lower(v)),
    "like": lambda c, v: ColOps.like(c, v),
    "ilike": lambda c, v: ColOps.ilike(c, v),
    "gt": lambda c, v: ColOps.__gt__(c, v),
    "gte": lambda c, v: ColOps.__ge__(c, v),
    "lt": lambda c, v: ColOps.__lt__(c, v),
    "lte": lambda c, v: ColOps.__le__(c, v),
    "in_": lambda c, v: ColOps.in_(c, v),
}


def create_filter_op(column: Any, op_name: str, value: Any, negate: bool) -> ColOps:
    op = FILTER_OPS[op_name](column, value)
    if negate:
        op = not_(op)
    return op


def get_attr(selectables, path, attribute):
    select_from = selectables[path]
    return (
        getattr(select_from, attribute)
        if (isinstance(select_from, AliasedClass) or isinstance(select_from, _SQLAlchemyModel))
        else getattr(select_from.c, attribute)
    )


async def create_object_filters(
    model: Union[Type[IEntityModel], Type[_SQLAlchemyModel]],
    path: str,
    filters: List[Dict],
    selectables: SelectablesType,
    *_,
) -> List[ColOps]:
    result_filters = []
    for filter_ in filters:
        for attribute, value in filter_.items():
            if is_unset(value):
                continue
            if attribute == "AND_":
                nested_filters = await create_object_filters(model, path, value, selectables)
                result_filters.append(and_(*nested_filters))
            elif attribute == "OR_":
                nested_filters = await create_object_filters(model, path, value, selectables)
                result_filters.append(or_(*nested_filters))
            elif isinstance(value, dict) and "AND_" in value:
                # Nested filter
                result_filters.extend(
                    await _apply_nested(
                        model,
                        path,
                        [value],
                        create_object_filters,
                        attribute,
                        selectables,
                    )
                )
                attr = get_attr(selectables, path, attribute)
                result_filters.append(ColOps.__ne__(attr, None))
            else:
                negate = value.pop("NOT_", False)
                for operation, filter_value in value.items():
                    if is_unset(filter_value):
                        continue
                    else:
                        attr = get_attr(selectables, path, attribute)
                        result_filters.append(create_filter_op(attr, operation, filter_value, negate))
    return result_filters


async def list_(
    session: AsyncSession,
    model: Type[Union[_SQLAlchemyModel, IEntityModel]],
    data: QueryMany,
    selection: Dict[str, Dict],
):
    polymorphic_model = with_polymorphic(model, "*", aliased=True)
    model_query = select(polymorphic_model)
    selectables: SelectablesType = {"": polymorphic_model, "__selection__": model_query}

    eager_options = await create_selection_joins(model, "", selection, selectables)

    expression = selectables["__selection__"]

    if eager_options != (None,):
        expression = expression.options(*eager_options)

    filters, ordering = None, None
    if not is_unset(data):
        if not is_unset(data.filters) and data.filters:
            raw_filter = [dataclasses.asdict(f) for f in data.filters]
            filters = await create_object_filters(model, "", raw_filter, selectables)

        if not is_unset(data.ordering) and data.ordering:
            raw_ordering = [dataclasses.asdict(o) for o in data.ordering]
            ordering = add_default_ordering(model, raw_ordering)
            ordering = cleanup_ordering(ordering)
            ordering = await create_ordering(model, "", ordering, selectables)

        # Expression needs to be created again, selectables may have been modified in filters / ordering builder
        expression = selectables["__selection__"]

        if eager_options != (None,):
            expression = expression.options(*eager_options)

        if filters:
            expression = expression.filter(*filters)

        if ordering:
            expression = expression.order_by(*ordering)

        if not is_unset(data.page_size) and data.page_size:
            expression = expression.limit(data.page_size)
            if not is_unset(data.page_number) and data.page_number:
                expression = expression.offset((data.page_number - 1) * data.page_size)

    return (await session.execute(expression)).unique().scalars().all()

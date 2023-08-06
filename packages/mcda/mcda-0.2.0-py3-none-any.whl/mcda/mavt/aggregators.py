from typing import List, cast

from ..core.aliases import (
    NumericPerformanceTable,
    NumericValue,
    PerformanceTable,
)
from ..core.performance_table import (
    apply_criteria_weights,
    normalize,
    sum_table,
)
from ..core.scales import Scale


def weighted_sum_after_normalization(
    performance_table: NumericPerformanceTable,
    criteria_weights: List[NumericValue],
) -> List[NumericValue]:
    """Compute alternatives values as weighted sum of normalized alternatives'
    performances.

    :param performance_table:
    :param criteria_weights:
    :return: alternatives values
    """
    weighted_table = cast(
        PerformanceTable,
        apply_criteria_weights(performance_table, criteria_weights),
    )
    res = sum_table(weighted_table, axis=1)
    res = cast(List[NumericValue], res)
    return res


def weighted_sum(
    performance_table: PerformanceTable,
    criteria_scales: List[Scale],
    criteria_weights: List[NumericValue],
) -> List[NumericValue]:
    """Compute alternatives values as weighted sum of alternatives'
    performances.

    :param performance_table:
    :param criteria_scales:
    :param criteria_weights:
    :return: alternatives values
    """
    normalized_table = normalize(performance_table, criteria_scales)
    weighted_table = cast(
        PerformanceTable,
        apply_criteria_weights(normalized_table, criteria_weights),
    )
    res = sum_table(weighted_table, axis=1)
    res = cast(List[NumericValue], res)
    return res

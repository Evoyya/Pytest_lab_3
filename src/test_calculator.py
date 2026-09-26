import pytest
from calculator import calculate_commission

class TestCalculateCommissionPositive:
    """Позитивные тесты: корректный расчёт комиссии."""

    @pytest.mark.parametrize(
        "amount, expected",
        [
            # Тариф 1: 100–1000 → 50 руб.
            (100, 50.0),      # нижняя граница
            (500, 50.0),      # внутри диапазона
            (1000, 50.0),     # верхняя граница
            # Тариф 2: 1001–20000 → 100 руб.
            (1001, 100.0),    # нижняя граница
            (10000, 100.0),   # внутри диапазона
            (20000, 100.0),   # верхняя граница
            # Тариф 3: 20001–40000 → 200 руб. + 1%
            (20001, 400.01),  # нижняя граница
            (30000, 500.0),   # внутри диапазона
            (40000, 600.0),   # верхняя граница
            # Тариф 4: 40001–50000 → 500 руб.
            (40001, 500.0),   # нижняя граница
            (45000, 500.0),   # внутри диапазона
            (50000, 500.0),   # верхняя граница
        ],
        ids=[
            "min_100", "mid_500", "max_1000",
            "min_1001", "mid_10000", "max_20000",
            "min_20001", "mid_30000", "max_40000",
            "min_40001", "mid_45000", "max_50000",
        ],
    )
    def test_commission_calculation(self, amount, expected):
        """Проверяет корректный расчёт комиссии для всех диапазонов."""
        assert calculate_commission(amount) == expected


class TestCalculateCommissionBoundary:
    """Тесты граничных значений."""

    @pytest.mark.parametrize(
        "amount, expected",
        [
            (99, 50.0),        # ниже минимума — должно упасть
            (101, 50.0),       # чуть выше минимума
            (999, 50.0),       # перед границей 1000
            (1001, 100.0),     # сразу после 1000
            (19999, 100.0),    # перед границей 20000
            (20001, 400.01),   # сразу после 20000
            (39999, 599.99),   # перед границей 40000
            (40001, 500.0),    # сразу после 40000 (новое правило)
            (49999, 500.0),    # перед максимумом
        ],
    )
    def test_boundary_values(self, amount, expected):
        """Проверяет поведение на границах тарифных диапазонов."""
        if  not (100 <= amount <= 50_000):
            with pytest.raises(ValueError):
                calculate_commission(amount)
        else:
            assert calculate_commission(amount) == expected

class TestCalculateCommissionNegative:
    """Негативные тесты: обработка невалидных данных."""

    @pytest.mark.parametrize(
        "invalid_amount",
        [99, 50001, -1, 0, 100_000],
        ids=["below_min", "above_max", "negative", "zero", "too_big"],
    )
    def test_invalid_amount_raises_value_error(self, invalid_amount):
        """Сумма вне диапазона [100; 50 000] -> ValueError."""
        with pytest.raises(ValueError):
            calculate_commission(invalid_amount)

    @pytest.mark.parametrize(
        "invalid_type",
        ["abc", "100", None, [], {}, True],
        ids=["string", "numeric_string", "none", "list", "dict", "bool"],
    )
    def test_invalid_type_raises_type_error(self, invalid_type):
        """Нечисловые значения -> TypeError."""
        with pytest.raises(TypeError):
            calculate_commission(invalid_type)

class TestCalculateCommissionNewFeature:
    """Тесты новой функциональности: фиксированная комиссия 500 руб. свыше 40 000."""

    @pytest.mark.parametrize(
        "amount, expected",
        [
            (40000, 600.0),   # ещё работает старое правило
            (40001, 500.0),   # начало нового правила
            (42000, 500.0),
            (45000, 500.0),
            (49999, 500.0),
            (50000, 500.0),   # верхняя граница нового правила
        ],
    )
    def test_fixed_commission_above_40000(self, amount, expected):
        """Для сумм свыше 40 000 руб. комиссия фиксированная — 500 руб."""
        assert calculate_commission(amount) == expected

    def test_commission_does_not_exceed_500_in_new_range(self):
        """Комиссия в новом диапазоне не должна превышать 500 руб."""
        for amount in range(40001, 50001, 500):
            assert calculate_commission(amount) == 500.0

    def test_commission_at_40001_less_than_at_40000(self):
        """На границе 40 000 → 40 001 комиссия снижается (600 → 500)."""
        assert calculate_commission(40000) > calculate_commission(40001)
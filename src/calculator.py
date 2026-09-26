from typing import Union

# Константы границ диапазона
MIN_AMOUNT: int = 100
MAX_AMOUNT: int = 50_000

# Константы тарифных порогов
THRESHOLD_1: int = 1_000
THRESHOLD_2: int = 20_000
THRESHOLD_3: int = 40_000

# Константы фиксированных комиссий
COMMISSION_1: float = 50.0
COMMISSION_2: float = 100.0
COMMISSION_3: float = 500.0
BASE_COMMISSION: float = 200.0
PERCENT_RATE: float = 0.01


def _validate_amount(amount: Union[int, float]) -> None:
    """
    Проверяет корректность входной суммы.

    Args:
        amount: Сумма перевода.

    Raises:
        TypeError: Если передан не числовой тип.
        ValueError: Если сумма вне диапазона [100; 50 000].
    """
    if isinstance(amount, bool) or not isinstance(amount, (int, float)):
        raise TypeError(
            f"Сумма должна быть числом, получено: {type(amount).__name__}"
        )

    if not MIN_AMOUNT < amount < MAX_AMOUNT:
        raise ValueError(
            f"Сумма перевода должна быть от {MIN_AMOUNT} до {MAX_AMOUNT} руб."
        )


def calculate_commission(amount: Union[int, float]) -> float:
    """
    Рассчитывает комиссию для денежного перевода.

    Args:
        amount: Сумма перевода (от 100 до 50 000 руб.).

    Returns:
        float: Размер комиссии в рублях.

    Raises:
        TypeError: Если передан не числовой тип.
        ValueError: Если сумма не входит в допустимый диапазон.
    """
    _validate_amount(amount)

    if amount <= THRESHOLD_1:
        return COMMISSION_1
    elif amount <= THRESHOLD_2:
        return COMMISSION_2
    elif amount <= THRESHOLD_3:
        return BASE_COMMISSION + round(amount * PERCENT_RATE, 2)
    else:
        return COMMISSION_3
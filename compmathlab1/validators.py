from logger import Logger


def validate_n(n: str, logger: Logger) -> int:
    if not n.isdigit():
        logger.critical("N must be an integer.")
        exit(1)

    if not 1 <= int(n) <= 20:
        logger.critical("N must be in range [1, 20]")
        exit(1)

    return int(n)


def validate_float(f: str, logger: Logger) -> float:
    try:
        return float(f)
    except ValueError:
        logger.critical(f"{f} is not a float")
        exit(1)

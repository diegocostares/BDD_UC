import datetime
import string


def generate_siglas(start: str or None = None) -> list:
    if start is not None and len(start) > 5:
        raise ValueError("Siglas can't be longer than 5 characters")
    letters = string.ascii_uppercase
    numbers = [str(i) for i in range(1, 10)]

    if start is None:
        return list(letters)
    elif len(start) in [1, 2]:
        return [start + letter for letter in letters]
    elif len(start) in [3, 4, 5]:
        return [start + number for number in numbers]


def current_semester() -> str:
    current_month = datetime.datetime.now().month
    current_year = datetime.datetime.now().year
    semester = 1 if current_month <= 6 else 2
    return f"{current_year}-{semester}"


if __name__ == "__main__":
    print(generate_siglas())
    print(generate_siglas("A"))
    print(generate_siglas("B"))
    print(generate_siglas("ABC2"))
    print(current_semester())

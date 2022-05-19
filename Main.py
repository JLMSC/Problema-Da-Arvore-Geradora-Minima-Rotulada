from random import randint

from Reader import Reader


def main(k_value: int = randint(0, 10)):
    """
    Função principal.

    Args
        k_value (int): A quantidade máxima de rótulos distintos.
    """
    Reader("Data/Input.txt", k_value=k_value)


if __name__ == "__main__":
    main(13)

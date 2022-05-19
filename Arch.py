from dataclasses import dataclass


@dataclass
class Arch:
    """Representação de um Arco, com custo não negativo e rótulo.

    Args:
        source (int): Vértice de origem.
        destiny (int): Vértice de destino.
        cost (float): Custo do Arco entre a origem e o destino.
        label (int): Rótulo do Arco entre a origem e o destino.

    Returns:
        str: A representação textual do Arco.
    """

    source: int
    destiny: int
    cost: float
    label: int

    def __str__(self) -> str:
        """Retorna a representação textual do Arco."""
        return (
            f"Arco=["
            + f"Origem={self.source}, "
            + f"Destino={self.destiny}, "
            + f"Custo={self.cost}, "
            + f"Rótulo={self.label}];\n"
        )

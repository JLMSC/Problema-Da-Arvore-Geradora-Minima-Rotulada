from dataclasses import dataclass, field

from Arch import Arch
from Model import Model


@dataclass
class Reader:
    """
    Realiza a leitura de um arquivo.

    Args:
        input_file (str): Diretório do arquivo de entrada.
        k_value (int): A quantidade máxima de rótulos distintos.
        arch_data (list[Arch]): Lista com todos os Arcos.
        vertex_count (int): A quantidade de vértices.
        edges_count (int): A quantidade de arcos.
        label_count (int): A quantidade de rótulos.
    """

    input_file: str
    k_value: int
    arch_data: list[Arch] = field(init=False)
    vertex_count: int = 0
    edges_count: int = 0
    label_count: int = 0

    def read(self):
        """Faz a leitura de um arquivo."""
        try:

            # Lista com todos os arcos.
            self.arch_data = []

            with open(self.input_file, "r", encoding="utf-8") as file:
                for line_index, line in enumerate(file):
                    # Remove espaços no início e no final da linha.
                    # Transforma os elementos em uma lista.
                    line = line.strip()
                    line = line.split(" ")
                    # A primeira linha contem a quantidade máxima de rótulos distintos ("K").
                    if not line_index:
                        line = list(map(int, line))
                        self.vertex_count = line[0]
                        self.edges_count = line[1]
                        self.label_count = line[2]
                    # As demais linhas contem as informações dos Arcos.
                    else:
                        # Transforma a informação em "Arch" e adiciona-os na lista.
                        # Obs: Os arcos adicionados são não-orientados.
                        self.arch_data.append(
                            Arch(
                                source=int(line[0]),
                                destiny=int(line[1]),
                                cost=float(line[2]),
                                label=int(line[3]),
                            )
                        )
                        self.arch_data.append(
                            Arch(
                                source=int(line[1]),
                                destiny=int(line[0]),
                                cost=float(line[2]),
                                label=int(line[3]),
                            )
                        )

                # Fecha o arquivo após a leitura.
                file.close()

            # Passa a informação pro "Model".
            Model(
                arch_data=self.arch_data,
                vertex_count=self.vertex_count,
                edges_count=self.edges_count,
                label_count=self.label_count,
                k=self.k_value,
            )

        except FileNotFoundError:
            raise FileNotFoundError

    def __post_init__(self):
        """Inicializa os demais atributos."""
        self.read()

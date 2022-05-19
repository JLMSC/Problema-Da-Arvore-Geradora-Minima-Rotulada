from dataclasses import dataclass


@dataclass
class Writer:
    """
    Realiza a escrita em um arquivo.

    Args:
        output_file (str): Diretório do arquivo de saída.
        k_value (int): A quantidade máxima de rótulos distintos.
        archs (dict): Os arcos utilizados no modelo.
        labels (dict): Os rótulos utilizados no modelo.
        subtour (dict): Os 'subtours' utilizados no modelo.
        math_model (str): O modelo matemático do modelo.
        optimal_solution (float): A solução ótima do modelo.
    """

    output_file: str
    k_value: int
    archs: dict
    labels: dict
    subtour: dict
    math_model: str
    optimal_solution: float

    def write(self):
        """Faz a escrita em um arquivo."""
        try:
            with open(self.output_file, "w", encoding="utf-8") as file:
                # Variáveis dos arcos e os seus valores.
                archs_vars = ""
                for arch in self.archs.values():
                    archs_vars += f"{str(arch)} = {arch.solution_value()}\n"

                # Variáveis dos rótulos e os seus valores.
                labels_vars = ""
                for label in self.labels.values():
                    labels_vars += f"{str(label)} = {label.solution_value()}\n"

                # Variáveis dos 'subtours' e seus valores.
                subtour_vars = ""
                for sbt in self.subtour.values():
                    subtour_vars += f"{str(sbt)} = {sbt.solution_value()}\n"

                file.write(
                    f"{'#' * 25} SAÍDA {'#' * 25}"
                    + "\n\n"
                    + f"{'#' * 25} SOLUÇÃO ÓTIMA {'#' * 25}"
                    + "\n"
                    + str(self.optimal_solution)
                    + "\n\n"
                    + f"{'#' * 25} VARIÁVEIS DOS ARCOS E SEUS VALORES {'#' * 25}"
                    + "\n"
                    + archs_vars
                    + "\n"
                    + f"{'#' * 25} VARIÁVEIS DOS RÓTULOS E SEUS VALORES {'#' * 25}"
                    + "\n"
                    + labels_vars
                    + "\n"
                    + f"{'#' * 25} VARIÁVEIS DOS 'SUBTOURS' {'#' * 25}"
                    + "\n"
                    + subtour_vars
                    + "\n"
                    # (Opcional)
                    # + f"{'#' * 25} MODELO MATEMÁTICO {'#' * 25}"
                    # + "\n"
                    # + self.math_model
                    # + "\n"
                )
                # Fecha o arquivo.
                file.close()
        except FileNotFoundError:
            raise FileNotFoundError

    def __post_init__(self):
        """Inicializa os demais atributos."""
        self.write()

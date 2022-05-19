from dataclasses import dataclass, field

from ortools.linear_solver import pywraplp

from Arch import Arch
from Writer import Writer


@dataclass
class Model:
    """Representação de um Modelo, utilizando o OR-Tools.

    Args:
        arch_data (list[Arch]): A representação de todos os arcos.
        archs (dict): Dicionário com as variáveis do modelo (arcos).
        labels (dict): Dicionário com as variáveis do modelo (rótulos).
        subtours (dict): Dicionário com as variáveis do modelo ('subtours').
        vertex_count (int): A quantidade de vértices do grafo.
        edges_count (int): A quantidade de arcos do grafo.
        label_count (int): A quantidade de rótulos do grafo.
        k (int): A quantidade máxima de rótulos distintos.
        solver (pywraplp.Solver): O 'Solver' do modelo ("SCIP").
        objective (Solver.Objective): A função objetivo do modelo.
        data (dict): A representação dos dados, em um dicionário.
    """

    arch_data: list[Arch]
    archs: dict = field(init=False, default_factory=dict)
    labels: dict = field(init=False, default_factory=dict)
    subtours: dict = field(init=False, default_factory=dict)
    vertex_count: int
    edges_count: int
    label_count: int
    k: int
    solver = pywraplp.Solver(
        "Labeled-Constrained Minimum Spanning Tree",
        pywraplp.Solver.SCIP_MIXED_INTEGER_PROGRAMMING,
    )
    objective = solver.Objective()
    data: dict = field(init=False, default_factory=dict)

    def create_data_model(self):
        """Cria os dados do modelo."""
        # Contém todos os arcos do grafo.
        self.data["Archs"] = [[arch.source, arch.destiny] for arch in self.arch_data]
        # Contém todos os rótulos dos arcos.
        self.data["Labels"] = [arch.label for arch in self.arch_data]
        # Contém todos os custos dos arcos.
        self.data["Cost"] = [arch.cost for arch in self.arch_data]
        # Contém o 'subtour' do grafo.
        self.data["Subtour"] = [i for i in range(1, self.vertex_count + 1)]

    def define_arch_variables(self):
        """Define as variáveis dos arcos no modelo."""
        for i, j in self.data["Archs"]:
            self.archs[(i, j)] = self.solver.IntVar(0, 1, "A[%i, %i]" % (i, j))

    def define_arch_constraints(self):
        """Define as restrições dos arcos no modelo.
        O qual indica que o número de arcos da árvore geradora deve ser '|V| - 1'."""
        self.solver.Add(sum(self.archs.values()) == self.vertex_count - 1)

    def define_label_variables(self):
        """Define as variáveis dos rótulos no modelo."""
        for label in self.data["Labels"]:
            self.labels[label] = self.solver.IntVar(0, 1, "Y[%i]" % (label))

    def define_label_constraints(self):
        """Define as restrições dos rótulos no modelo.
        O qual indica a utilização de um rótulo para um arco qualquer que, também,
        foi utilizado."""
        archs_from_label = []
        for label in self.labels.keys():
            for arch in self.arch_data:
                if arch.label == label:
                    archs_from_label.append(self.archs[(arch.source, arch.destiny)])
            self.solver.Add(
                self.solver.Sum(archs_from_label)
                <= ((self.vertex_count - 1) * self.labels[label])
            )
            archs_from_label.clear()

    def define_k_labels_constraints(self):
        """Define as restrições dos rótulos no modelo.
        O qual indica que a quantidade de rótulos distintos deve ser menor
        ou igual a 'k'."""
        self.solver.Add(self.solver.Sum(self.labels.values()) <= self.k)

    def define_subtour_variables(self):
        """Define as variáveis de 'subtour' no modelo."""
        # Define o 'subtour' do vértice de partida com o valor padrão de 0 (zero).
        source = self.data["Subtour"][0]
        self.subtours[source] = self.solver.IntVar(0, 0, "U[%i]" % (source))

        # Define o 'subtour' dos demais vértices, sendo eles >= 0.
        for subtour in self.data["Subtour"][1::]:
            self.subtours[subtour] = self.solver.IntVar(
                0, self.solver.Infinity(), "U[%i]" % (subtour)
            )

    def define_subtour_constraints(self):
        """Define a restrição do 'subtour'.
        O qual restringe a árvore geradora de ter ciclos."""
        for ij, arch in self.archs.items():
            i, j = ij
            self.solver.Add(
                self.subtours[i] - self.subtours[j] + self.vertex_count * arch
                <= self.vertex_count - 1
            )

    def define_arch_path_constraints(self):
        """Define a restrição dos arcos.
        O qual indica que pelo menos 1 (um) arco irá sair
        do ponto de partida e vice-versa."""
        archs_from_source = []
        for j in range(2, self.vertex_count + 1):
            if (1, j) in self.archs.keys():
                archs_from_source.append(self.archs[(1, j)])
        self.solver.Add(self.solver.Sum(archs_from_source) >= 1)

        archs_to_destiny = []
        for j in range(2, self.vertex_count + 1):
            for i in range(1, self.vertex_count + 1):
                if (i, j) in self.archs.keys():
                    archs_to_destiny.append(self.archs[(i, j)])
            self.solver.Add(self.solver.Sum(archs_to_destiny) == 1)
            archs_to_destiny.clear()

    def define_objective_function(self):
        """Define a função objetivo do modelo,
        o qual é representada por 'Cij * Aij', onde 'Cij' é o custo do
        arco e, 'Aij' indica se tal arco foi utilizado."""
        for arch, cost in zip(self.archs.values(), self.data["Cost"]):
            self.objective.SetCoefficient(arch, cost)
        self.objective.SetMinimization()

    def solve_model(self):
        """Resolve o modelo."""
        status = self.solver.Solve()
        if status == self.solver.OPTIMAL:
            Writer(
                "Data/Output.txt",
                k_value=self.k,
                archs=self.archs,
                labels=self.labels,
                subtour=self.subtours,
                math_model=self.solver.ExportModelAsLpFormat(False),
                optimal_solution=self.objective.Value(),
            )
            print(self.objective.Value())

    def __post_init__(self):
        """Inicializa os demais atributos."""
        self.create_data_model()

        # Define as variáveis e as restrições.
        self.define_arch_variables()
        self.define_arch_constraints()

        # Define as variáveis e as restrições.
        self.define_label_variables()
        self.define_label_constraints()
        self.define_k_labels_constraints()

        # Define as variáveis e as restrições.
        self.define_subtour_variables()
        self.define_subtour_constraints()

        # Define a restrição de caminho dos arcos.
        self.define_arch_path_constraints()

        # Define a função objetivo do modelo.
        self.define_objective_function()

        # Resolve o modelo e mostra a solução.
        self.solve_model()

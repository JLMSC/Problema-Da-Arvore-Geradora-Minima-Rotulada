# **Problema da Árvore Geradora Mínima Rotulada** (***PAGMR***)

O problema, em questão, também conhecido como 
"***Label-Constrained Minimum Spanning Tree*** (***LCMST***)", 
é definido em um **grafo não-direcionado**, *G = (V, E, L)* 
com conjunto de **vértices** *V*, conjunto de **arestas** *E*,
e conjunto de **rótulos** *L*.

Cada **aresta** $e = \\{ i, j \\} \in E$ é associada a um 
**custo não-negativo** $c_e$ e a um **rótulo** $l_e \in L$, por fim
temos $K$, um número inteiro positivo, representando 
**a quantidade máxima de rótulos distintos**.

Dado as informações necessárias do problema, o mesmo foi modelado,
com a utilização da ferramenta [**Or-Tools**](https://developers.google.com/optimization),
as **restrições necessárias** para, através da aplicação do
[**SIMPLEX**](https://pt.wikipedia.org/wiki/Algoritmo_simplex) /
[**Branch and bound**](https://en.wikipedia.org/wiki/Branch_and_bound),
obter-se uma solução ótima dado uma determinada entrada e, também,
um determinado $K$.

As implementação feita, baseia-se nas 
**restrições de *Miller–Tucker–Zemlin*** (***MTZ***), 
as quais são definidas a seguir:

**Minimização (Função Objetivo)**

&ensp; $(1) \sum_{(i, j) \in A} c_{ij}a_{ij}$ 

**Sujeito à (Restrições)**

&ensp; $(2) u_1 = 0$

&ensp; $(3) \sum_{k \in L} y_k \leq K$

&ensp; $(4) \sum_{(i,j) \in A} a_{ij} = |V| - 1$

&ensp; $(5) \sum_{i \in V | (i,j) \in A} a_{ij} = 1, \forall j \in V \ \{1\}$

&ensp; $(6) u_i - u_j + |V|a_{ij} \leq |V| - 1, \forall (i,j) \in A$

&ensp; $(7) \sum_{(i,j) \in A | l_{ij} = k} a_{ij} \leq (|V| - 1).y_k, \forall k \in L$

&ensp; $(8) a_{ij} \in \{0, 1\}, \forall (i,j) \in A$

&ensp; $(9) y_k \in \{0, 1\}, \forall k \in L$ 

&ensp; $(10) u_i \geq 0, \forall i \in V$ 

> **Observação**: 
> Por padrão, neste modelo, o vértice **tomado como
> ponto de partida** será o vértice 1 (um).

**Explicação do modelo**:

(**1**). Minimiza o custo da solução, ou seja, da Árvore Geradora.

(**2**). Define, no vértice 1 (um), ou seja, o ponto de partida, 
para o '*subtour*', o valor 0 (zero).

(**3**). Limita a quantidade de rótulos distintos utilizados na
solução para ser menor ou igual a $K$.

(**4**). Garante que, as arestas utilizadas na solução, tenha
exatamente $|V| - 1$ arestas.

(**5**). Garante que, pelo menos 1 (um), vértice, saindo de $i$,
chegue no vértice $j$, ou seja, que haja pelo menos 1 (um) aresta
$a_{ij}$.

(**6**). Aplica o "*subtour*" na solução encontrada, limitando a
existência de ciclos na mesma.

(**7**). Garante que haja pelo menos 1 (um) rótulo, se pelos menos 
1 (um), de tal rótulo, foi utilizada na solução.

(**8**). Admite somente valores binários para $a_{ij}$.

(**9**). Admite somente valores binários para $y_k$.

(**10**). Admite somente valores maiores ou iguais a zero para $u_i$.

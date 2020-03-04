# Pré-requisitos

Não há dependência de módulos Python de terceiros.

# Descrição

## lattice/partition.py

Classe que representa uma partição. Duas representações são utilizadas: blocos e máscaras. Como exemplo, supor um conjunto A = (a, b, c) e uma partição p = ((a, c), (b))

### Blocos

Cada partição é um conjunto que contém os índices dos itens. Nesse caso, a partição p é armazenada como ((0, 2), (1))

### Máscaras

Cada partição é um vetor de inteiros em que a i-ésima posição representa a partição ao qual o i-ésimo item pertence. No caso de p, a máscara utilizada é (0, 1, 0). Tal representação é a de menor ordem lexicográfica, conforme definido no [livro do Knuth](http://www.cs.utsa.edu/~wagner/knuth/fasc3b.pdf). 

## Módulo robdd/*

Dentro desse módulo, o arquivo mais interessante é o robdd.py, que contém o método `get_random_solution`, que é utilizado para sortear o início de caminho em cada iteração do algoritmo U-Curve.

## ucurve/path_start.py

Contém os métodos `get_initial_robdd`, `remove_interval_inf` e `remove_interval_sup`, utilizados para eliminar intervalos do reticulado Booleano durante a execução do U-Curve.

## util/partition_to_boolean.py

Contém o algoritmo que mapeia os nós de um reticulado das partições de n itens em um reticulado Booleano de 2**(n-1) itens.

## run_ucurve.py

Implementação do algoritmo U-Curve (não está feito ainda).
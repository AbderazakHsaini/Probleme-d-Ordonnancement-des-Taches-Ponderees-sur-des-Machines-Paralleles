include "globals.mzn";
include "data.dzn";

int: m;                          % Nombre de machines
int: n;                          % Nombre d'opérations
set of int: Machines = 1..m;     % Ensemble des machines
set of int: Operations = 1..n;   % Ensemble des opérations

array[Operations] of int: t;     % Temps de traitement pour chaque opération
array[Operations] of int: w;     % Poids de chaque opération

% Variables de décision
array[Operations, Machines] of var bool: x;   % x[i, y] = 1 si l'opération i est affectée à la machine y, 0 sinon
array[Operations, Operations, Machines] of var bool: a;  % a[i, j, y] = 1 si i et j sont affectées à la même machine y, 0 sinon

array[Operations] of var int: F;              % Temps de fin de chaque opération
var int: C;                                   % Makespan (temps de fin maximal de toutes les opérations)

% Fonction objectif : minimiser la somme pondérée des temps de fin et du makespan
var int: objective = sum(j in Operations)(w[j] * F[j]) + C;
solve minimize objective;

% Contraintes
constraint forall(i in Operations) (
    sum(y in Machines) (x[i, y]) = 1               % (4) Chaque opération est affectée à exactement une machine
);

constraint forall(i in Operations, j in Operations where i < j, y in Machines) (
    a[i, j, y] - x[i, y] - x[j, y] >= -1           % (1)
    /\ -a[i, j, y] + x[i, y] >= 0                  % (2)
    /\ -a[i, j, y] + x[j, y] >= 0                  % (3)
);

constraint forall(j in Operations) (
    F[j] = sum(i in 1..j-1, y in Machines) (t[i] * a[i, j, y]) + t[j]    % (5) Calcul du temps de fin de chaque opération
);

constraint forall(j in Operations) (
    C >= F[j]                                      % (6) Makespan est supérieur ou égal au temps de fin de chaque opération
);

constraint forall(i in Operations) (
    F[i] >= 0                                      % (7) Temps de fin de chaque opération est non négatif
);

% Contraintes d'intégrité pour les variables binaires
constraint forall(i in Operations, j in Operations where i < j, y in Machines) (
    a[i, j, y] in 0..1                             % (8) a[i, j, y] est binaire
);

constraint forall(i in Operations, y in Machines) (
    x[i, y] in 0..1                                % (9) x[i, y] est binaire
);

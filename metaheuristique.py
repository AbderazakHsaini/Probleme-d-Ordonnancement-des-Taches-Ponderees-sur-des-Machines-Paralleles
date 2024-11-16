import heapq
import random
import copy
from collections import deque

# Paramètres du problème
n = 5  # Nombre d'opérations
m = 3  # Nombre de machines
processing_times = [3, 2, 7, 5, 4]  # Temps de traitement de chaque opération
weights = [1, 3, 2, 4, 1]  # Poids de chaque opération

# Paramètres de la recherche tabou
tabu_tenure = 5              # Durée de la liste tabou
max_iter = 100               # Nombre d'itérations maximum
no_improvement_limit = 20    # Limite de non-amélioration
num_neighbors = min(10, n)   # Nombre de voisins explorés

# 1. Solution Initiale avec l'Heuristique List Scheduling Pondéré
def initial_solution():
    tasks = sorted([(i, processing_times[i], weights[i], weights[i] / processing_times[i]) for i in range(n)],
                   key=lambda x: x[3], reverse=True)
    machine_times = [0] * m
    assignment = [[] for _ in range(m)]
    completion_times = [0] * n
    
    for task in tasks:
        i, processing_time, weight, priority = task
        min_machine = min(range(m), key=lambda x: machine_times[x])
        start_time = machine_times[min_machine]
        end_time = start_time + processing_time
        machine_times[min_machine] = end_time
        assignment[min_machine].append(i)
        completion_times[i] = end_time

    makespan = max(machine_times)
    weighted_completion = sum(weights[i] * completion_times[i] for i in range(n))
    return assignment, makespan, weighted_completion

# Calcul de l'objectif : Makespan et Somme Pondérée des Temps de Fin
def calculate_objective(assignment):
    machine_times = [0] * m
    completion_times = [0] * n
    
    for y in range(m):
        for i in assignment[y]:
            completion_times[i] = machine_times[y] + processing_times[i]
            machine_times[y] += processing_times[i]

    makespan = max(machine_times)
    weighted_completion = sum(weights[i] * completion_times[i] for i in range(n))
    return makespan, weighted_completion

# Génération des voisins
def generate_neighbors(assignment):
    neighbors = []
    for y1 in range(m):
        for y2 in range(m):
            if y1 != y2 and assignment[y1]:  # Transférer une tâche de y1 à y2
                for i in range(len(assignment[y1])):
                    new_assignment = copy.deepcopy(assignment)
                    task = new_assignment[y1].pop(i)
                    new_assignment[y2].append(task)
                    neighbors.append(new_assignment)
    return neighbors

# 2. Métaheuristique de Recherche Tabou
def tabu_search():
    current_assignment, current_makespan, current_weighted_completion = initial_solution()
    best_assignment = current_assignment
    best_makespan = current_makespan
    best_weighted_completion = current_weighted_completion
    
    tabu_list = deque(maxlen=tabu_tenure)  # Liste Tabou avec taille limitée
    iter_no_improve = 0

    for iteration in range(max_iter):
        if iter_no_improve >= no_improvement_limit:
            break  # Arrêt si pas d'amélioration

        # Génération et Filtrage des Voisins
        neighbors = generate_neighbors(current_assignment)
        neighbors = [neighbor for neighbor in neighbors if neighbor not in tabu_list]

        best_neighbor = None
        best_neighbor_makespan = float('inf')
        best_neighbor_weighted_completion = float('inf')

        # 3. Critère d'Aspiration et Sélection du Meilleur Voisin
        for neighbor in neighbors:
            makespan, weighted_completion = calculate_objective(neighbor)
            if (weighted_completion < best_neighbor_weighted_completion or
               (weighted_completion == best_neighbor_weighted_completion and makespan < best_neighbor_makespan)):
                best_neighbor = neighbor
                best_neighbor_makespan = makespan
                best_neighbor_weighted_completion = weighted_completion

        if best_neighbor is None:
            break  # Aucun voisin valide trouvé

        # Mise à jour de la solution actuelle
        current_assignment = best_neighbor
        current_makespan = best_neighbor_makespan
        current_weighted_completion = best_neighbor_weighted_completion

        # 4. Mise à jour de la Liste Tabou
        tabu_list.append(best_neighbor)

        # 5. Mise à jour des Meilleures Solutions
        if (current_weighted_completion < best_weighted_completion or
           (current_weighted_completion == best_weighted_completion and current_makespan < best_makespan)):
            best_assignment = current_assignment
            best_makespan = current_makespan
            best_weighted_completion = current_weighted_completion
            iter_no_improve = 0  # Réinitialisation en cas d'amélioration
        else:
            iter_no_improve += 1  # Incrémentation en cas de non-amélioration

    return best_assignment, best_makespan, best_weighted_completion

# Exécution de la Recherche Tabou
best_assignment, best_makespan, best_weighted_completion = tabu_search()
print("Meilleur assignement des opérations:", best_assignment)
print("Makespan optimal trouvé:", best_makespan)
print("Somme pondérée des temps de fin optimale:", best_weighted_completion)

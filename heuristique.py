import heapq

# Données d'entrée du problème
n = 5  # Nombre d'opérations (tâches)
m = 3  # Nombre de machines
processing_times = [3, 2, 7, 5, 4]  # Temps de traitement de chaque opération
weights = [1, 3, 2, 4, 1]  # Poids de chaque opération

# Calcul du ratio poids/temps de traitement pour trier les opérations par ordre de priorité
tasks = sorted([(i, processing_times[i], weights[i], weights[i] / processing_times[i]) for i in range(n)],
               key=lambda x: x[3], reverse=True)

# Liste pour enregistrer les temps de fin des machines (initialement toutes à 0)
machine_times = [0] * m  # Temps de fin de chaque machine

# Variables pour stocker le temps de fin de chaque opération et la valeur du makespan
completion_times = [0] * n  # Temps de fin de chaque opération
total_weighted_completion_time = 0  # Somme pondérée des temps de fin

# Appliquer l'algorithme de List Scheduling Pondéré
for task in tasks:
    i, processing_time, weight, priority = task
    
    # Trouver la machine avec le temps de fin minimal
    min_machine = min(range(m), key=lambda x: machine_times[x])
    
    # Affecter l'opération à cette machine
    start_time = machine_times[min_machine]
    end_time = start_time + processing_time
    machine_times[min_machine] = end_time
    
    # Mettre à jour le temps de fin de l'opération et la somme pondérée des temps de fin
    completion_times[i] = end_time
    total_weighted_completion_time += weight * end_time

# Calcul du makespan (temps de fin maximal des machines)
makespan = max(machine_times)

# Affichage des résultats
print("Temps de fin de chaque opération :", completion_times)
print("Somme pondérée des temps de fin :", total_weighted_completion_time)
print("Makespan :", makespan)

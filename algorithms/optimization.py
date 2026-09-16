import math
import random

from optimization.problem import SmartGridOptimizationProblem
from optimization.result import Configuration, OptimizationResult


def configuration_score(
    problem: SmartGridOptimizationProblem, configuration: Configuration
) -> float:
    """
    Combina cobertura, redundancia y exposición en un puntaje a maximizar.

    Tips:
    - Use problem.score_components(configuration); ya retorna cobertura,
      redundancia y exposición en ese orden.
    """
    coverage, redundancy, exposure = problem.score_components(configuration)
    return coverage - redundancy - exposure


def hill_climbing(
    problem: SmartGridOptimizationProblem,
    initial_configuration: Configuration,
    max_iterations: int = 500,
) -> OptimizationResult:
    """
    Ejecuta ascenso de colina con mejora estricta.

    Debe examinar todos los vecinos, seleccionar el de mayor puntaje y
    conservar el orden entregado por el problema para desempatar. La búsqueda
    termina cuando no existe una mejora estricta o se alcanza el límite.

    Tips:
    - problem.neighbors(current) retorna vecinos válidos en el orden que debe
      usarse para desempatar.
    - Cada llamada a configuration_score(...) cuenta como una evaluación.
    - Inicialice los historiales con la configuración inicial y agregue solo las
      mejoras aceptadas antes de retornar el OptimizationResult.
    """
    
    current = initial_configuration
    current_score = configuration_score(problem, current)

    history = [current]
    score_history = [current_score]

    evaluaciones = 1
    i = 0
    improved = True

    while i < max_iterations and improved:
        neighbors = problem.neighbors(current)

        best_neighbor = neighbors[0]
        best_score = configuration_score(problem, best_neighbor)
        evaluaciones += 1

        for neighbor in neighbors[1:]:
            score = configuration_score(problem, neighbor)
            evaluaciones += 1

            if score > best_score:
                best_neighbor = neighbor
                best_score = score

        i += 1

        improved = best_score > current_score

        if improved:
            current = best_neighbor
            current_score = best_score

            history.append(current)
            score_history.append(current_score)

    return OptimizationResult(
        best_configuration=current,
        best_score=current_score,
        evaluations=evaluaciones,
        iterations=i,
        history=history,
        score_history=score_history,
    )
    
    """
    Codigo inicial:
    
    current = initial_configuration
    current_score = configuration_score
    
    evaluaciones = 1
    i = 0 
    improved = True
    
    while i < max_iterations:
        neighbors = problem(current)
        best_neighbor = neighbors(0)
        best_score = configuration_score(problem, best_neighbor)
        evaluacions += 1
        
        
        for neighbor in neighbors:
            score = configuration_score(problem, neighbor)
            evaluciones += 1
            
            if score > best_score:
                best_neighbor = neighbor
                best_score = score
            
        i += 1
        
        current = best_neighbor
        current_score = best_score
        
    return OptimizationResult(best_configuration=current, best_score=current_score, evaluaciones=evaluaciones,iterations=i)
    
    
    Cambios realizados con IA:

    Se corrigió la llamada a configuration_score para que reciba el problema y la configuración actual.
   
    Se corrigió la obtención de los vecinos usando problem.neighbors(current), ya que neighbors es el resultado de una función.

    Se agregó history y score_history para guardar la configuración inicial y las mejoras aceptadas.

    Se agregó la condición improved al ciclo while para que la búsqueda termine cuando el mejor vecino no tenga un puntaje estrictamente mayor al actual.

    Se agregó el retorno de history y score_history al OptimizationResult.

    """
    

def cooling_schedule(initial_temperature: float, cooling_rate: float, iteration: int) -> float:
    """
    Retorna el programa geométrico T(t) = T0 * alpha**t.

    Esta función se invoca desde simulated_annealing en cada iteración.
    """
    # TODO: Add your code here
    return initial_temperature * ( cooling_rate **  iteration)


def simulated_annealing(
    problem: SmartGridOptimizationProblem,
    initial_configuration: Configuration,
    initial_temperature: float = 20.0,
    cooling_rate: float = 0.97,
    max_iterations: int = 500,
    rng: random.Random | None = None,
) -> OptimizationResult:
    """
    Ejecuta recocido simulado para un problema de maximización.

    Debe proponer un vecino aleatorio por iteración, aceptar siempre las
    mejoras y aplicar exp(delta / temperature) en los demás casos. El estado
    actual y el mejor estado encontrado deben conservarse por separado.

    Tips:
    - Seleccione el candidato con rng.choice(problem.neighbors(current)) y use
      exclusivamente rng para conservar la reproducibilidad.
    - Obtenga la temperatura con cooling_schedule(...) y calcule la aceptación
      con delta = puntaje_candidato - puntaje_actual y math.exp(...).
    - Mantenga separados el estado actual y el mejor encontrado; registre el
      estado actual después de cada intento, incluso si se rechaza.
    - Detenga la ejecución cuando la temperatura alcance minimum_temperature.
    """
    rng = rng or random.Random()
    minimum_temperature = 1e-9

    current = initial_configuration
    current_score = configuration_score(problem, current)

    best= current
    best_score =current_score

    evaluations =1 
    history=[current]
    score_history =  [current_score]

    iteration = 0
    while iteration < max_iterations:
        temperature = cooling_schedule( initial_temperature , cooling_rate, iteration )
        if temperature <= minimum_temperature:
            break

        candidate = rng.choice( problem.neighbors(current)  )
        candidate_score= configuration_score( problem, candidate ) 
        evaluations += 1

        delta = candidate_score-current_score
        accept =delta > 0 or rng.random() < math.exp( delta / temperature )

        if accept:
            current, current_score = candidate, candidate_score
            if current_score > best_score:
                best, best_score =current, current_score

        history.append( current ) 
        score_history.append( current_score)
        iteration +=1

    return OptimizationResult(best_configuration=best, best_score=best_score, evaluations=evaluations,   iterations=iteration,
        history=history,  score_history=score_history,  metadata={},  )
    
    
    """
    
    Version olriginal de Codigo
    IA utilizada: Claude
    
    def simulated_annealing(
    problem: SmartGridOptimizationProblem,
    initial_configuration: Configuration,
    initial_temperature: float = 20.0,
    cooling_rate: float = 0.97,
    max_iterations: int = 500,
    rng: random.Random | None = None,
) -> OptimizationResult:

    rng = random.Random()
    current = initial_configuration
    current_score = configuration_score(current)
    best = current
    best_score = current_score
    evaluations = 0
    history = []
    score_history = []
    iteration = 0

    while iteration < max_iterations:

        temperature =initial_temperature *cooling_rate ** iteration
        neighbors = problem.neighbors(current)
        candidate = rng.choice(neighbors)
        candidate_score = configuration_score(problem, current)
        delta = current_score - candidate_score

        if delta > 0:
            current = candidate
            current_score = candidate_score
        else:
            probability = math.exp(delta * temperature)

        if current_score < best_score:
            best = current
            best_score =current_score

        history.append(candidate)
        score_history.append(candidate_score)

        iteration +=1

    return OptimizationResult(  best_configuration=current,  best_score=current_score,  evaluations=evaluations  iterations=iteration,  history=history,  score_history=score_history )
    
    
    entre lops errores q ayudo a encontrar la ia se pueden identificar :
    
    Inicializacion de rng ya q se creaba un generador nuevo en lugar de utilizar el recibido
    configuration_score: faltaba enviar el problema como argumento
    Calculo de delta estaba invertido. debe ser candidato menos actual
    Probabilidad de aceptacioon: e multiplicaba por la temperatura en lugar de dividir 
    se guardaba el candidato aunque hubiera sido rechazado
    No se contabilizaba correctamente la evaluacion de la configuración inicial
    Temperatura minima: faltaba detener el algoritmo cuando la temperatura llegaba al limite dado
    Sintaxis: faltaba una coma en el Optimizationresult  entro algunos otros mas 
        
    
    
    
    """


def one_point_crossover(
    parent1: Configuration, parent2: Configuration, rng: random.Random
) -> tuple[Configuration, Configuration]:
    """
    Realiza un cruce de un punto y retorna dos descendientes.

    La reparación de la cantidad de módulos se realiza posteriormente.

    Tips:
    - Seleccione con rng un corte interior, entre las posiciones 1 y len-1.
    - Cada descendiente combina el prefijo de un padre con el sufijo del otro.
    - Retorne tuplas y no repare aquí los descendientes.
    """
    if len(parent1) != len(parent2):
        raise ValueError("Los padres deben tener la misma longitud")
    if len(parent1) < 2:
        return parent1, parent2
    
    cut = rng.randrange(1, len(parent1))

    hijo1 = parent1[:cut] + parent2[cut:]
    hijo2 = parent2[:cut] + parent1[cut:]
    return hijo1, hijo2

    """
Se utilizó IA para revisar el rango del punto de corte y confirmar que este debía quedar entre la posición 1 y la última posición válida, evitando cortar antes del primer elemento o después del último.

Cambio realizado:
Se verificó el uso de rng.randrange(1, len(parent1)) para generar un corte interno y se mantuvo la combinación de ambas partes de los padres.

Verificación:
Se probaron ejemplos manuales de dos padres y se comprobó que los hijos conservaran la misma longitud.
    """


def swap_mutation(
    individual: Configuration, mutation_probability: float, rng: random.Random
) -> Configuration:
    """
    Aplica mutación por intercambio con la probabilidad indicada.

    Cuando ocurre una mutación, intercambia un bit activo y uno inactivo para
    conservar la cantidad de módulos instalados.

    Tips:
    - Use rng.random() para decidir si se aplica la mutación.
    - Identifique por separado los índices activos e inactivos y seleccione uno
      de cada grupo con rng.choice(...).
    - Si alguno de los dos grupos está vacío, no hay un intercambio posible.
    - Retorne una tupla nueva; no modifique el individuo recibido.
    """
    if rng.random() >= mutation_probability:
        return individual

    active_indices = [
        i for i, bit in enumerate(individual) if bit == 1
        ]
    inactive_indices = [
        i for i, bit in enumerate(individual) if bit == 0
        ]

    if not active_indices or not inactive_indices:
        return individual

    active_index = rng.choice(active_indices)
    inactive_index = rng.choice(inactive_indices)
    mutated_individual = list(individual)
    mutated_individual[active_index], mutated_individual[inactive_index] = (
        mutated_individual[inactive_index],
        mutated_individual[active_index],
    )

    return tuple(mutated_individual)

    """
Se consultó la lógica de la probabilidad de mutación y la forma de conservar la misma cantidad de bits activos después de mutar.

Cambio realizado:
Se confirmó que primero debía seleccionarse un índice con valor 1 y otro con valor 0, para después intercambiarlos. También se revisó la condición:

if rng.random() >= mutation_probability:
    return individual

para asegurar que el individuo solo se modifica cuando ocurre la mutación.

Verificación:
Se comprobó con configuraciones sencillas que después del intercambio se mantiene la misma cantidad de 1.
    """


def genetic_algorithm(
    problem: SmartGridOptimizationProblem,
    population_size: int = 40,
    generations: int = 100,
    mutation_probability: float = 0.05,
    elite_size: int = 2,
    rng: random.Random | None = None,
) -> OptimizationResult:
    """
    Ejecuta un algoritmo genético generacional.

    Debe integrar la población inicial, la selección por torneo, el cruce, la
    reparación, la mutación y el elitismo entregados por el proyecto. Retorna
    el mejor individuo encontrado durante toda la ejecución.

    Tips:
    - Use problem.initial_population(...), problem.tournament_select(...) y
      problem.repair_configuration(...) para las operaciones ya entregadas.
    - Aplique one_point_crossover(...) antes de reparar y swap_mutation(...)
      después de la reparación.
    - Conserve los mejores individuos por elitismo y registre en los historiales
      el mejor global de cada generación.
    """

    rng = rng or random.Random()

    if population_size < 2:
        raise ValueError("La población debe tener al menos dos individuos")

    if generations < 0:
        raise ValueError("El número de generaciones no puede ser negativo")

    if not 0.0 <= mutation_probability <= 1.0:
        raise ValueError("La probabilidad de mutación debe estar entre 0 y 1")

    if not 0 <= elite_size <= population_size:
        raise ValueError("elite_size debe estar entre 0 y population_size")

    poblacion = problem.initial_population(population_size, rng)
    puntajes = []

    for individuo in poblacion:
        puntaje = configuration_score(problem, individuo)
        puntajes.append(puntaje)

    evaluaciones = population_size
    indice_mejor = max(
        range(population_size),
        key=lambda i: puntajes[i]
    )

    mejor_configuracion = poblacion[indice_mejor]
    mejor_puntaje = puntajes[indice_mejor]
    historial = [mejor_configuracion]
    historial_puntajes = [mejor_puntaje]

    for generacion in range(generations):
        indices_ordenados = sorted(
            range(population_size),
            key=lambda i: puntajes[i],
            reverse=True
        )
        nueva_poblacion = []

        for i in indices_ordenados[:elite_size]:
            nueva_poblacion.append(poblacion[i])

        while len(nueva_poblacion) < population_size:
            padre1 = problem.tournament_select(
                poblacion,
                puntajes,
                rng
            )
            padre2 = problem.tournament_select(
                poblacion,
                puntajes,
                rng
            )
            hijo1, hijo2 = one_point_crossover(
                padre1,
                padre2,
                rng
            )
            hijo1 = problem.repair_configuration(
                hijo1,
                rng
            )
            hijo1 = swap_mutation(
                hijo1,
                mutation_probability,
                rng
            )
            nueva_poblacion.append(hijo1)
            if len(nueva_poblacion) < population_size:

                hijo2 = problem.repair_configuration(
                    hijo2,
                    rng
                )

                hijo2 = swap_mutation(
                    hijo2,
                    mutation_probability,
                    rng
                )

                nueva_poblacion.append(hijo2)
        poblacion = nueva_poblacion
        puntajes = []

        for individuo in poblacion:
            puntaje = configuration_score(
                problem,
                individuo
            )
            puntajes.append(puntaje)
        evaluaciones += population_size
        indice_mejor_generacion = max(
            range(population_size),
            key=lambda i: puntajes[i]
        )
        mejor_puntaje_generacion = puntajes[
            indice_mejor_generacion
        ]
        if mejor_puntaje_generacion > mejor_puntaje:
            mejor_puntaje = mejor_puntaje_generacion
            mejor_configuracion = poblacion[
                indice_mejor_generacion
            ]
        historial.append(mejor_configuracion)
        historial_puntajes.append(mejor_puntaje)

    return OptimizationResult(
        best_configuration=mejor_configuracion,
        best_score=mejor_puntaje,
        evaluations=evaluaciones,
        iterations=generations,
        history=historial,
        score_history=historial_puntajes,
    )
    
    
    """
    Codigo inicial:
    
    for generacion in range(generations):

    indices_ordenados = sorted(
        range(population_size),
        key=lambda i: puntajes[i],
        reverse=True
    )

    nueva_poblacion = []

    for i in indices_ordenados[:elite_size]:
        nueva_poblacion.append(poblacion[i])

    while len(nueva_poblacion) < population_size:

        padre1 = problem.tournament_select(
            poblacion, puntajes, rng
        )

        padre2 = problem.tournament_select(
            poblacion, puntajes, rng
        )

        hijo1, hijo2 = one_point_crossover(
            padre1, padre2, rng
        )

        hijo1 = problem.repair_configuration(hijo1, rng)
        hijo2 = problem.repair_configuration(hijo2, rng)
        hijo1 = swap_mutation(
            hijo1, mutation_probability, rng
        )
        hijo2 = swap_mutation(
            hijo2, mutation_probability, rng
        )
        nueva_poblacion.append(hijo1)
        if len(nueva_poblacion) < population_size:
            nueva_poblacion.append(hijo2)
    poblacion = nueva_poblacion
    puntajes = []
    for individuo in poblacion:
        puntaje = configuration_score(problem, individuo)
        puntajes.append(puntaje)
    indice_mejor_generacion = max(
        range(population_size),
        key=lambda i: puntajes[i]
    )
    mejor_puntaje_generacion = puntajes[
        indice_mejor_generacion
    ]
    if mejor_puntaje_generacion > mejor_puntaje:
        mejor_puntaje = mejor_puntaje_generacion
        mejor_configuracion = poblacion[
            indice_mejor_generacion
        ]
        historial.append(mejor_configuracion)
    historial_puntajes.append(mejor_puntaje)

return OptimizationResult(best_configuration=mejor_configuracion,best_score=mejor_puntaje,evaluations=evaluaciones,iterations=generations,history=historial,score_history=historial_puntajes,
)

Se corrigió la posición de historial.append(...), ya que inicialmente solo se estaba agregando una configuración cuando aparecía una mejora.
Se ajustó la indentación del return OptimizationResult(...) para que quedara fuera del ciclo de generaciones.
Se revisó que el segundo hijo solo se agregara cuando todavía hubiera espacio disponible en la nueva población.
Se verificó que el mejor individuo guardado fuera el mejor encontrado durante toda la ejecución y no únicamente el de la última generación.

Verificación:
Se revisó que historial y historial_puntajes registraran un valor por generación y que el tamaño de la población se mantuviera constante.
    """
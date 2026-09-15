import math

from world.game_state import GameState


def base_evaluation_function(state: GameState) -> float:
    """
    Retorna la evaluación base entregada para desarrollar el punto 4.

    Esta función no forma parte del código que debe modificar el estudiante y
    permite probar Minimax antes de desarrollar la heurística del punto 5.
    """
    if state.is_win():
        return 1000.0
    if state.is_lose():
        return -1000.0
    return float(state.get_score())


def evaluation_function(state: GameState) -> float:
    """
    Evalúa un estado desde la perspectiva del defensor MAX.

    Debe conservar las utilidades terminales de la evaluación base y diseñar
    una valoración no trivial para estados de corte. Minimax y alfa-beta usan
    esta misma función al comparar sus decisiones en el punto 5.

    Tips:
    - Los estados terminales ya se resuelven antes del bloque TODO; diseñe allí
      únicamente la valoración de estados no terminales.
    - Consulte state.defender_position, state.intruder_position,
      state.pending_terminals, state.get_score() y state.get_legal_actions(0).
    - state.layout.distance(start, goal) calcula y almacena en caché la distancia
      real por el mapa respetando los muros.
    - Maneje conjuntos vacíos y distancias infinitas, y mantenga todo estado no
      terminal estrictamente entre -1000 y +1000.
    """
    if state.is_win() or state.is_lose():
        return base_evaluation_function(state)

    valor = state.get_score()

    if state.pending_terminals:

        distancias = []

        for terminal in state.pending_terminals:
            distancia =state.layout.distance( state.defender_position,terminal,  )

            if not math.isinf(distancia):
                distancias.append(float(distancia))

        if distancias:
            suma_distancias= sum(distancias)
            distancia_minima =min(distancias)
            valor -=12.0 * suma_distancias
            valor -= 8.0*distancia_minima

        else:
            valor -=100.0
        valor -= 20.0 * len ( state.pending_terminals)

    distancia_intruso =state.layout.distance( state.defender_position , state.intruder_position,  )

    if math.isinf(distancia_intruso):
        valor += 25.0
    else:
        valor +=6.0*distancia_intruso

        if distancia_intruso == 1:
            valor -=80.0
        elif distancia_intruso ==2:
            valor -= 35.0
        elif distancia_intruso== 3:
            valor -=15.0

    acciones =state.get_legal_actions(0)
    valor += 3.0 * len(acciones )
    valor =999.0 * (valor /(1.0 + abs(valor)))

    return float(valor)
    
    """
    
    Primera version del Codigo
    
    def evaluation_function(state: GameState) -> float:
    if state.is_win() or state.is_lose():
        return base_evaluation_function(state)

    puntuacion = state.get_score()


    puntuacion -=0.1 *state.turns
    distancia_intruso =state.layout.distance(  state.defender_position,    state.intruder_position )

    if distancia_intruso != math.inf:
        if distancia_intruso ==1:
            puntuacion -= 20
        elif distancia_intruso== 2:
            puntuacion -= 10
        else:
            puntuacion+=5

    # Distancia a las terminales
    if state.pending_terminals:
        distancia_minima = math.inf

        for terminal in state.pending_terminals:
            distancia = state.layout.distance( state.defender_position, terminal)

            if distancia !=math.inf and distancia>distancia_minima:
                distancia_minima =distancia

        if distancia_minima != math.inf:
            puntuacion -= 5 * distancia_minima
    movilidad= len(state.get_legal_actions(0))}
    puntuacion -= 2* movilidad

    return puntuacion
    
    
    IA utilizada: Chat GPT
    La ia ayudo a comoprender porque el algoritmo quedara estancado y no se moviera mas 
    Penalizacion al intruso ya q usaba una penalizacion insuficiente cuando el intruso estaba cerca haciendo que el defensor tomara riesgos
    El peso era muy bajo 5.0 por lo q avanzar hacia las terminales tenia poca importancia
    e restaba la movilidad (-2.0 * movilidad) en lugar de sumarla, haciendo que tener mas opciones de movimiento empeorara la evaluacion
    y utilizaba -500 para una distancia de 0, aunque ese caso ya estaba controlado por is_lose().
    La combinacion de pesos no diferenciaba suficientemente algunas posiciones, lo que podía provocar que el agente repitiera movimientos
        
    """
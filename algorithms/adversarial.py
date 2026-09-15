from abc import ABC, abstractmethod
from typing import Self

from algorithms.evaluation import evaluation_function
from world.game_state import GameState


class MultiAgentSearchAgent(ABC):
    """Clase base para los agentes de búsqueda adversaria."""

    def __init__(self, depth: int | str = 2) -> None:
        self.depth = int(depth)
        if self.depth < 1:
            raise ValueError("La profundidad debe ser al menos 1 ply")
        self.nodes_evaluated = 0

    @abstractmethod
    def get_action(self, state: GameState) -> str | None:
        raise NotImplementedError


class MinimaxAgent(MultiAgentSearchAgent):
    """Agente Minimax para el defensor MAX frente al intruso MIN."""

    def get_action(self, state: GameState) -> str | None:
        """
        Retorna la acción del defensor con mayor valor Minimax.

        El defensor es MAX (agente 0), el intruso es MIN (agente 1) y cada
        acción consume un ply. Debe respetar el orden de las acciones legales,
        usar evaluation_function en terminales y cortes, y contar cada estado
        procesado una vez en self.nodes_evaluated, incluida la raíz.

        Tips:
        - Use state.get_legal_actions(agent_index) y
          state.generate_successor(agent_index, action) para expandir el árbol.
        - Compruebe state.is_win(), state.is_lose() y el corte de profundidad;
          evalúe esos estados con evaluation_function(state).
        - El siguiente agente es (agent_index + 1) % state.get_num_agents().
          depth=1 incluye una acción de MAX y depth=2 una de MAX y una de MIN.
        - Reinicie las métricas y cuente una vez cada estado procesado, incluida
          la raíz. Retorne la acción de MAX y conserve la primera en los empates.
        """
        
       
        self.nodes_evaluated =0
        self.nodes_evaluated+= 1 

        actions = state.get_legal_actions(0)
        if not actions:
            return None

        best_action = None
        best_value = float("-inf")
        for action in actions:
            successor = state.generate_successor(0, action)
            value = self._value(successor, 1, self.depth - 1)
            if value > best_value:      
                best_value = value
                best_action = action
        return best_action

    def _value ( self,state: GameState, agent_index: int, depth_remaining: int) ->  float:
        self.nodes_evaluated += 1

        if state.is_win():
            return 1000.0
        if state.is_lose():
            return -1000.0
        if depth_remaining ==0:
            return evaluation_function(state)

        actions= state.get_legal_actions(agent_index)
        next_agent =( agent_index + 1) %  state.get_num_agents()

        if agent_index == 0:  
            best_value= float("-inf")
            for action in actions:
                successor = state.generate_successor( agent_index, action )
                best_value= max(best_value, self._value( successor,next_agent,depth_remaining - 1))
            return best_value
          
        else:  
            best_value=float("inf")
            for action in actions:
                successor = state.generate_successor(agent_index,action)
                best_value= min(best_value, self._value(successor , next_agent,  depth_remaining-1))
            return best_value 
        
""" 

        Primera version de Codigo 

        self.nodes_evaluated = 0
        
        acciones = state.get_legal_actions(0)
        if not acciones
          return None
        
        mejor_accion = None
        mejor_valor = float("-inf")
          
        for accion in acciones:
                siguiente_estado = state.generate_successor(0, accion)
                valor = self._value(siguiente_estado,1,self.deptp)

                if valor >= mejor_valor:
                    mejor_valor = valor
                    mejor_accion = accion
            
        return mejor_accion

    def value( self,state: GameState, agent_index: int depth_remaining: int  ) -> float:

        self.nodes_evaluated += 1
        if state.is_win():
            return 1000.0
        if state.is_lose():
            return -1000.0
        if depth_remaining <= 1:
            return evaluation_function(state)
     
        acciones = state.get_legal_actions(agent_index)
        siguiente_agente = (agent_index + 2) %state.get_num_agents()

        if agent_index == 0:
            mejor_valor = float("-inf")
            for accion in acciones:

                siguiente_estado = state.generate_successor(agent_index,accion )
                valor = self._value( siguiente_estado, siguiente_agente,  depth_remaining - 1)

                if valor > mejor_valor:
                    mejor_valor = valor
            return mejor_valor

        else:
            peor_valor = float(inf)

            for accion in acciones:
                siguiente_estado = state.generate_successor(agent_index,accion )
                valor = self._value( siguiente_estado,agent_index, depth_remaining - 1)

                if valor < peor_valor
                    peor_valor = valor
            return peor_valor
        
        
        IA utilizada: Chat GPT
        Reflexion:  Se uso a la IA para poder preguntarle si el codigo estaba bien planteado y si funcionaba sin errores, al
        poder ver la version que dio como respuesta se pudo evidenciar que habian errores de logica y tambien de sintaxis
        
        1. en depth_remaining - 1 se resta la profundidad en cada turno de un agente, haciendo que la 
        búsqueda termine antes de lo esperado
        2.en next_agent =(agent_index +2) se suma 2 en vez de 1 por lo q se puede saltar un agente
        3. elf._value(successor, agent_index, )se vuelve a llamar al mismo agente, haciendo 
        q el mismo fantasma juegue varias veces seguidas
        4. if value >= best_value se usa >= en vez de > por lo q en caso de empate se cambia la accion 
        5. best_value = float("-inf") / float("inf") si actions esta vacío se devuelve 
        infinito sin haber evaluado ninguna accion dando un resultado incorrecto
        6. otros errores como los : que olvide poner o un par de comillas
        
        
        """
           
    
          

class AlphaBetaAgent(MultiAgentSearchAgent):
    """Agente Minimax que evita explorar ramas mediante poda alfa-beta."""

    def get_action(self, state: GameState) -> str | None:
        """
        Retorna la acción de Minimax aplicando poda alfa-beta.

        Debe usar la misma profundidad, orden de acciones y función de
        evaluación que Minimax.

        Tips:
        - Conserve la misma estructura y casos base de MinimaxAgent.
        - Inicie alpha en -infinito y beta en +infinito, y páselos en las
          llamadas recursivas.
        - En MAX actualice alpha y corte si valor >= beta; en MIN actualice beta
          y corte si valor <= alpha.
        """
        # TODO: Add your code here
        raise NotImplementedError("Punto 5: implemente AlphaBetaAgent.get_action")
    

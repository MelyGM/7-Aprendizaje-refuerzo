"""
El problema del blackjack simplificado como un problema de aprendizaje por refuerzo

"""

from RL import MDPsim, SARSA, Q_learning, PoliticaGreedy
from random import random, randint

class BlackJack(MDPsim):
    """
    Clase que representa un MDP para el problema del jugador.
    
    El jugador tiene un capital inicial y el objetivo es llegar a un capital
    objetivo o quedarse sin dinero.
    
    """
    def __init__(self, gama):
        self.estados = []
        self.gama = gama

        self.estados = [
            (suma, carta, as_usable)
            for suma in range(12, 22)
            for carta in range(1,11)
            for as_usable in [True, False]
        ]

        self.suma_crupier =0
        self.as_crupier =False

    def reparte_carta(self):
        """
        Genera una carta aleatoria para el juego.
        Las cartas del 1 al 9 conservan su valor, en cambio las cartas:
            10, J, Q y K tienen un valor de 10.
        El As se representa con el número 1, pero puede valer 11 si no hace que el jugador se pase de 21.
        """
        carta = randint(1, 13)

        if carta > 10:
            return 10
        else:
            return carta
        
    def estado_inicial(self):
        """
        Genera el estado inicial de una partida.
        Reaprte dos cartas al jugador y dos cartas al crupier, una de las cuales es visible para el jugador.
        """
        #jugador 1
        carta1 = self.reparte_carta()
        carta2 = self.reparte_carta()
        suma_jugador = carta1 + carta2

        as_usable = False
        if 1 in [carta1, carta2]:
            if suma_jugador + 10 <= 21:
                suma_jugador += 10
                as_usable = True


        #crupier
        carta_crupier1 = self.reparte_carta()
        carta_crupier2 = self.reparte_carta()
        self.suma_crupier = carta_crupier1 + carta_crupier2

        carta_visible = carta_crupier1

        self.as_crupier = False
        if 1 in [carta_crupier1, carta_crupier2]:
            if self.suma_crupier + 10 <= 21:
                self.suma_crupier += 10
                self.as_crupier = True

        #blackjack natural
        if suma_jugador == 21:
            return (21, carta_visible, as_usable)
        
        #si j1 tiene menos de 12
        while suma_jugador < 12:
            nueva=self.reparte_carta()
            suma_jugador += nueva
            if nueva == 1 and suma_jugador + 10 <= 21:
                suma_jugador += 10
                as_usable = True  
            if suma_jugador > 21 and as_usable:
                suma_jugador -= 10
                as_usable = False
        if suma_jugador > 21:
            return ("Terminal", -1)
        return (suma_jugador, carta_visible, as_usable)      
    
    def acciones_legales(self, s):
        """
        Devuelve las acciones que puede realizar el jugador en un estado.
        Si el estado es teminal, no hay acciones disponibles.
        En otro caso el jugador puede plantarse (0) o pedir otra carta (1).
        """
        if self.es_terminal(s):
            return []
        else:
            return [0, 1]
      
    def recompensa(self, s, a, s_):
        """
        Devuelve la recompensa obtenida después de pasar del estado s al estado s_ usando la acción a.
        Si el nuevo estado es teminal, se devuelve la recompensa guardada. Si el juego continua la recompensa
        es 0.
        """
        if self.es_terminal(s_):
            return s_[1]
        return 0
    
    def transicion(self, s, a):
        """
        Calcula el siguiente estado después de ejecutar una acción. 
            Si el jugador pide carta, se actualiza la suma del jugador y se verifica si se ha pasado de 21 o si tiene un as usable.
            Si el jugador se planta, el crupier toma cartas hsta llegar al menos a 17. Después se comparan las sumas
            para decidir si el jugador gana, empata o pierde.
        """
        suma_jugador = s[0]
        carta_visible = s[1]
        as_usable = s[2]

        if a == 1:
            carta = self.reparte_carta()
            suma_jugador += carta

            if carta == 1 and suma_jugador + 10 <= 21:
                suma_jugador += 10
                as_usable = True    
            if suma_jugador > 21 and as_usable:
                suma_jugador -= 10
                as_usable = False
            if suma_jugador > 21:
                return ("Terminal", -1)
            if suma_jugador < 12:
                suma_jugador = 12
            return (suma_jugador, carta_visible, as_usable)
        
        if a == 0:
            while self.suma_crupier < 17:
                carta = self.reparte_carta()
                self.suma_crupier += carta

                if carta == 1 and self.suma_crupier + 10 <= 21:
                    self.suma_crupier = self.suma_crupier + 10
                    self.as_crupier = True

                if self.suma_crupier > 21 and self.as_crupier:
                    self.suma_crupier -= 10
                    self.as_crupier = False

            if self.suma_crupier > 21:
                return ("Terminal", 1)
            if suma_jugador > self.suma_crupier:
                return ("Terminal", 1)
            if suma_jugador == self.suma_crupier:
                return ("Terminal", 0)
            return ("Terminal", -1)
        raise ValueError("Acción no válida")
        

    def es_terminal(self, s):
        """
        Verifica si un estado representa el final de la partida.
        Estado termianl.
            ("Terminal", recompensa)
            
            donde recompensa es 1 si el jugador gana, 0 si empata y -1 si pierde. 
            Si el jugador obtiene un blackjack natural, la recompensa es 1.5.
        """
        return type(s) == tuple  and len(s) == 2 and s[0] == "Terminal"


if __name__ == "__main__":

    blackjack = BlackJack(gama=1)
   
    Q_sarsa = SARSA( blackjack, alfa=0.1, epsilon=0.1, n_ep=50000, n_iter=100)
    Q_learning = Q_learning( blackjack, alfa=0.1, epsilon=0.1, n_ep=50000, n_iter=100)

    # Encuentra las políticas óptimas para cada algoritmo
    pi_s = PoliticaGreedy(Q_sarsa)
    pi_q = PoliticaGreedy(Q_learning)

    # Imprime las políticas óptimas para cada estado no terminal
    print("Estado".center(20) + '|' +  "SARSA".center(10) + '|' + "Q-learning".center(10))
    print("-"*20 + '|' + "-"*10 + '|' + "-"*10)
    for s in blackjack.estados:
        if not blackjack.es_terminal(s):
            print(str(s).center(20) + '|' 
                  + str(pi_s(s)).center(10) + '|' 
                  + str(pi_q(s)).center(10))
    print("-"*20 + '|' + "-"*10 + '|' + "-"*10)


"""
****************************************************************************************
Responde las siguientes preguntas:

1. ¿Cuáles son los estados, acciones, recompensas y transiciones en el problema del 
    blackjack?  

    Los estados se representan como tuplas (suma_jugador, carta_visible, as_usable), 
    las acciones son [0,1], 0 (plantarse) y 1 (pedir carta). Las transiciones ocurren cuando el
    jugador realiza una acción y el juego cambia de estado dependiendo de las cartas obtenidas 
    o del turno del crupier. Las recompensas se obtienen al terminar la partida, donde si el jugador gana 
    recibe una recompensa de 1, si empata recibe 0, si pierde recibe -1 y si se obtine un blackjack natural 
    recibe una recompensa de 1.5


2. ¿Cómo se pueden representar los estados del blackjack de manera eficiente para el 
    aprendizaje por refuerzo?

    Usando una tupla con solo la información necesaria para tomar decisiones (suma del jugador, carta visible del crupier, as usable) 
    Esto reduce la cantidad de estados posibles y facilita el aprendizaje por refuerzo. Al trabajar con menos información, el entrenamiento
    requiere menos memoria y las decisiones pueden calcularse de manera más eficiente.

3. ¿Qué pasa si se modifica el valor de epsilón de la política epsilon-greedy?

    Si epsilón es alto, el agente explora más pruebas y acciones aleatorias con mayor frecuencia, lo que 
    puede ayudar a descubrir mejores estrategias aunque el aprendizaje sea más inestable. En cambio si el epsilón 
    es bajo el agente explora menos y aprovecha más lo que ya aprendió, tomando decisiones más consistentes, pero con 
    el riesgo de quedarse en una estrategia no óptima.

4. ¿Cómo afecta el valor de alfa en la convergencia de los algoritmos SARSA y Q-learning?

    Si alfa es alto, los algoritmos SARSA y Q-learning aprenden más rápido porque le dan más importancia a la información 
    nueva, aunque esto puede hacer que las decisiones sean más inestables. Por otro lado, si alfa es bajo, el aprendizaje es más lento 
    pero la convergencia suele ser más estable, ya que el agente conserva más de la experiencia pasada.

5. ¿Cuál de los dos algoritmos, SARSA o Q-learning, consideras que es más adecuado para 
   el problema del blackjack y por qué?

   Q-learning es más adecuado para el blackjack porque busca aprender directamente la mejor acción posible en cada estado, lo que suele
   generar políticas más óptimas y  maximizar las recompensas, ya que asume que en el futuro siempre tomará la mejor acción disponible.
   En cambio SARSA aprende usando la acción que el agente sí tomó, incluyendo las acciones aleatorias de exploración, por lo que sus decisiones
   suelen ser un poco más cautelosas y menos óptimas.

6. ¿Se puede explicar con cierta lógica del juego la política óptima encontrada por cada 
   algoritmo? ¿Qué acciones se toman en cada estado y por qué?

   Sip. El estado donde el jugador tiene una suma baja como 12 normalmete la mejor opción es pedir otra carta, ya que el riesgo de perder todavía es
   pequeño. En cambio, cuando la suma es alta como 19 la mejor decisión suele ser plantarse para evitar pasarse de 21. También influye la carta del crupier,
   si el crupier tiene una carta baja, muchas veces conviene plantarse y esperar que el crupier pierda al pasarse de 21. 

****************************************************************************************
"""

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
        carta = randint(1, 13)

        if carta > 10:
            return 10
        else:
            return carta
        
    def estado_inicial(self):
        #jugador 1
        carta1 = self.reparte_carta()
        carta2 = self.reparte_carta()
        suma_jugador = carta1 + carta2

        as_usable = False
        if 1 in [carta1, carta2]:
            if suma + 10 <= 21:
                suma += 10
                as_usable = True


        #crupier
        carta_crupier1 = self.reparte_carta()
        carta_crupier2 = self.reparte_carta()
        self.suma_crupier = carta_crupier1 + carta_crupier2

        carta_visbile = carta_crupier1

        self.as_crupier = False
        if 1 in [carta_crupier1, carta_crupier2]:
            if self.suma_crupier + 10 <= 21:
                self.suma_crupier += 10
                self.as_crupier = True

        #blackjack natural
        if suma_jugador == 21:
            return ("Blackjack",1.5)
        
        #si j1 tiene menos de 12
        while suma_jugador < 12:
            nueva=self.reparte_carta()
            suma_jugador += nueva
        return (suma_jugador, carta_visbile, as_usable)
    
    def acciones_legales(self, s):
        if self.es_terminal(s):
            return []
        else:
            return [0, 1]
      
    def recompensa(self, s, a, s_):
        # TODO: implementar la recompensa del blackjack
        raise NotImplementedError("Implementa la recompensa del blackjack")
    
    def transicion(self, s, a):
        # TODO: implementar la transición del blackjack
        raise NotImplementedError("Implementa la transición del blackjack") 
    
    def es_terminal(self, s):
        return type(s) == tuple  and len(s) == 2 and s[0] == "Blackjack"


if __name__ == "__main__":

    blackjack = BlackJack(gama=1) # TODO: agregar los parámetros necesarios para el blackjack   
    s = blackjack.estado_inicial()
    print("Estado inicial:", s)
    print("Acciones legales:", blackjack.acciones_legales(s))
    print ("terminaaaaaal? ", blackjack.es_terminal(s)) 
    """
    # definir los parámetros de SARSA y Q-learning, luego crear las instancias 
    # de cada algoritmo
    Q_sarsa = SARSA( blackjack, alfa=..., epsilon=..., n_ep=..., n_iter=...)
    Q_learning = Q_learning( blackjack, alfa=..., epsilon=..., n_ep=..., n_iter=...)

    # Encuentra las políticas óptimas para cada algoritmo
    pi_s = PoliticaGreedy(Q_sarsa)
    pi_q = PoliticaGreedy(Q_learning)

    # Imprime las políticas óptimas para cada estado no terminal
    print("Estado".center(10) + '|' +  "SARSA".center(10) + '|' + "Q-learning".center(10))
    print("-"*10 + '|' + "-"*10 + '|' + "-"*10)
    for s in blackjack.estados:
        if not blackjack.es_terminal(s):
            print(str(s).center(10) + '|' 
                  + str(pi_s(s)).center(10) + '|' 
                  + str(pi_q(s)).center(10))
    print("-"*10 + '|' + "-"*10 + '|' + "-"*10)
"""

"""
****************************************************************************************
Responde las siguientes preguntas:

1. ¿Cuáles son los estados, acciones, recompensas y transiciones en el problema del 
    blackjack?  

2. ¿Cómo se pueden representar los estados del blackjack de manera eficiente para el 
    aprendizaje por refuerzo?

3. ¿Qué pasa si se modifica el valor de epsilón de la política epsilon-greedy?

4. ¿Cómo afecta el valor de alfa en la convergencia de los algoritmos SARSA y Q-learning?

5. ¿Cuál de los dos algoritmos, SARSA o Q-learning, consideras que es más adecuado para 
   el problema del blackjack y por qué?

6. ¿Se puede explicar con cierta lógica del juego la política óptima encontrada por cada 
   algoritmo? ¿Qué acciones se toman en cada estado y por qué?
****************************************************************************************
"""

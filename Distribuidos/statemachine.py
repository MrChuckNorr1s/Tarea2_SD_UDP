class FiniteStateMachine:
    def __init__(self, initial_state, states):
        self.state = initial_state
        self.states = states

    def transition(self, action):
        if self.state in self.states and action in self.states[self.state]:
            self.state = self.states[self.state][action]
            return self.state
        else:
            raise Exception(f"No se puede realizar la transición desde {self.state} con la acción {action}")

# Definición de estados y transiciones
states = {
    'Procesando': {'next': 'Preparación'},
    'Preparación': {'next': 'Enviado'},
    'Enviado': {'next': 'Entregado'},
    'Entregado': {'next': 'Finalizado'},
}

# Ejemplo de uso
fsm = FiniteStateMachine('Procesando', states)
print(fsm.transition('next'))  # Cambia a 'Preparación'


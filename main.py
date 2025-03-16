import numpy as np
import skfuzzy as fuzz
import matplotlib.pyplot as plt
from skfuzzy import control as ctrl

#Variaveis de Entrada (Antecedent)
comer = ctrl.Antecedent(np.arange(0, 11, 1), 'comer')
atividade = ctrl.Antecedent(np.arange(0, 11, 1), 'atividade')

#Variaveis de saída (Consequent)
peso = ctrl.Consequent(np.arange(0, 11, 1), 'peso')
peso_trap = ctrl.Consequent(np.arange(0, 11, 1), 'peso')

# automf -> Atribuição de categorias automaticamente
comer.automf(names=['pouco','razoavel','bastante'],)
atividade.automf(names=['baixa','media','alta'])

# atribuicao sem o automf
peso['leve'] = fuzz.gaussmf(peso.universe, 2, 1.5)
peso['medio'] = fuzz.gaussmf(peso.universe, 5, 1.5) 
peso['pesado'] = fuzz.gaussmf(peso.universe, 8, 1.5) 

peso_trap['leve'] = fuzz.trapmf(peso_trap.universe, [0, 2, 3, 4])
peso_trap['medio'] = fuzz.trapmf(peso_trap.universe, [4, 5, 6, 7])
peso_trap['pesado'] = fuzz.trapmf(peso_trap.universe, [7, 8, 9, 10])

#Visualizando as variáveis
comer.view()
atividade.view()
peso.view()
peso_trap.view()

#Criando as regras
regra_1 = ctrl.Rule(comer['bastante'] & atividade['baixa'], peso['pesado'])
regra_2 = ctrl.Rule(comer['pouco'], peso['leve'])
regra_3 = ctrl.Rule(comer['razoavel'] & atividade["media"], peso['medio'])
regra_4 = ctrl.Rule(comer['bastante'] & atividade["alta"], peso['medio'])
regra_5 = ctrl.Rule(comer['bastante'] & atividade["media"], peso['pesado'])

regra_6 = ctrl.Rule(comer['bastante'] & atividade['baixa'], peso_trap['pesado'])
regra_7 = ctrl.Rule(comer['pouco'], peso_trap['leve'])
regra_8 = ctrl.Rule(comer['razoavel'] & atividade["media"], peso_trap['medio'])
regra_9 = ctrl.Rule(comer['bastante'] & atividade["alta"], peso_trap['medio'])
regra_10 = ctrl.Rule(comer['bastante'] & atividade["media"], peso_trap['pesado'])

controlador = ctrl.ControlSystem([regra_1, regra_2, regra_3,regra_4, regra_5, regra_6, regra_7, regra_8, regra_9, regra_10])


#Simulando
Calculopeso = ctrl.ControlSystemSimulation(controlador)

notacomer = int(input('comer: '))
notaatividade = int(input('atividade: '))
Calculopeso.input['comer'] = notacomer
Calculopeso.input['atividade'] = notaatividade
Calculopeso.compute()

valorpeso = Calculopeso.output['peso']

print("\ncomer %d \nAtividade %d \npeso de %5.2f" %(
notacomer,
notaatividade,
valorpeso))


comer.view(sim=Calculopeso)
atividade.view(sim=Calculopeso)
peso.view(sim=Calculopeso)
peso_trap.view(sim=Calculopeso)

plt.show()
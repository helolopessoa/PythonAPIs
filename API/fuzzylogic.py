# 1. Entram os valores das axes emocionais
# 2. Se calculam as intensidades utilizando max_value(abs())
# 3. Se intensidade é média em mais de um axe, parte para a lógica fuzzy, se não, retorna a emoção mediana
# 4. A Lógica Fuzzy recebe como entrada TODOS os axes
# 5. Calcula a resposta para as regras primary
# 6. Calcula a resposta para as regras do secundary 1
# 7. Calcula a resposta para as regras do secundary 2
# 8. Calcula a resposta para as regras do tertiary
# 9. Compara todas estas com max_value(abs())
# 10. Retorna a de maior valor

import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl

global result;
result = "Neutral";

# Creating fuzzy sets for Pluthick's basic axes
angerxfear = ctrl.Antecedent(np.arange(-100,100,1),'angerxfear')
disgustxtrust = ctrl.Antecedent(np.arange(-100,100,1),'disgustxtrust')
sadnessxjoy = ctrl.Antecedent(np.arange(-100,100,1),'sadnessxjoy')
anticipationxsurprise = ctrl.Antecedent(np.arange(-100,100,1),'anticipationxsurprise')

# Creating membership functions)

axes = [angerxfear,disgustxtrust,sadnessxjoy,anticipationxsurprise]
str_axes = ['angerxfear','disgustxtrust','sadnessxjoy','anticipationxsurprise']
axes_emotions = [['annoyance','anger','rage','apprehension','fear','terror'],
                  ['boredom','disgust','loathing','acceptance','trust','admiration'],
                  ['pensiveness','sadness','grief','serenity','joy','ecstasy'],
                  ['interest','anticipation','vigilance','distraction','surprise','amazement']]
basic_coordinates = [[-50,0,0],[-100,-50,0],[-100,-100,-50], [0,0,50], [0,50,100], [50,100,100]]

#Plutchik's axes membership functions
for i in range(len(axes)):
    for j in range(len(axes_emotions[0])):
        axes[i][axes_emotions[i][j]] = fuzz.trimf(axes[i].universe,basic_coordinates[j])


#Creating fuzzy response sets for dyads
primary = ctrl.Consequent(np.arange(-100,100,1),'primary')
secundary1 = ctrl.Consequent(np.arange(-50,50,1),'secundary1')
secundary2 = ctrl.Consequent(np.arange(-50,50,1),'secundary2')
tertiary = ctrl.Consequent(np.arange(-100,100,1),'tertiary')

dyads = [primary,tertiary]
s_dyads = [secundary1,secundary2]


dyads_emotions = [['anticipation','optmistic','joy','in love','trust','submissive','fear','awe','surprise',
                   'disapproval','sad','remorse','disgust','contempt','angry','aggressive','anticipation2'],
                 ['sadness','sentimentality','trust','dominance','anger','outrage','surprise','delight','joy',
                  'morbidness','disgust','shame','fear','anxiety','anticipation','pessimism','sadness2']]

s_dyads_emotions = [['disgust','unbelief','surprise','curiosity','trust','hope','anticipation','cynism','disgust2'],
                            ['anger','envy','sadness','despair','fear','guilt','joy','pride','anger2']]



coordinates = [[87.5,100,100],[75,87.5,100],[62.5,75,87.5],[50,62.5,75],[37.5,50,62.5],[25,37.5,50],[12.5,25,37.5],
               [0,12.5,25],[-12.5,0,12.5],[-25,-12.5,0],[-37.5,-25,-12.5],[-50,-37.5,-25],[-62.5,-50,-37.5],
               [-75,-62.5,-50],[-87.5,-75,-62.5],[-100,-87.5,-75],[-100,-100,-87.5]]
               
s_coordinates = [[37.5,50,50],[25,37.5,50],[12.5,25,37.5],[0,12.5,25],[-12.5,0,12.5],
                         [-25,-12.5,0],[-37.5,-25,-12.5],[-50,-37.5,-25],[-50,-50,-37.5]]


#Dyads membership functions
for i in range(len(dyads)):
    for j in range(len(dyads_emotions[0])):
        dyads[i][dyads_emotions[i][j]] = fuzz.trimf(dyads[i].universe,coordinates[j])

for i in range(len(s_dyads)):
    for j in range(len(s_dyads_emotions[0])):
        s_dyads[i][s_dyads_emotions[i][j]] = fuzz.trimf(s_dyads[i].universe,s_coordinates[j])

# Fuzzy Inference
                            
# primary dyads
p_rule1 = ctrl.Rule(anticipationxsurprise['anticipation'] & sadnessxjoy['joy'], primary['optmistic'])
p_rule2 = ctrl.Rule(sadnessxjoy['joy'] & disgustxtrust['trust'], primary['in love'])
p_rule3 = ctrl.Rule(disgustxtrust['trust'] & angerxfear['fear'], primary['submissive'])
p_rule4 = ctrl.Rule(angerxfear['fear'] & anticipationxsurprise['surprise'], primary['awe'])
p_rule5 = ctrl.Rule(anticipationxsurprise['surprise'] & sadnessxjoy['sadness'], primary['disapproval'])
p_rule6 = ctrl.Rule(sadnessxjoy['sadness'] & disgustxtrust['disgust'], primary['remorse'])
p_rule7 = ctrl.Rule(disgustxtrust['disgust'] & angerxfear['anger'], primary['contempt'])
p_rule8 = ctrl.Rule(angerxfear['anger'] & anticipationxsurprise['anticipation'], primary['aggressive'])

# secundary 1 dyads
s1_rule1 = ctrl.Rule(anticipationxsurprise['anticipation'] & disgustxtrust['trust'], secundary1['hope'])
s1_rule2 = ctrl.Rule(disgustxtrust['disgust'] & anticipationxsurprise['anticipation'], secundary1['cynism'])
s1_rule3 = ctrl.Rule(disgustxtrust['trust'] & anticipationxsurprise['surprise'], secundary1['curiosity'])
s1_rule4 = ctrl.Rule(anticipationxsurprise['surprise'] & disgustxtrust['disgust'], secundary1['unbelief'])

# secundary 2 dyads
s2_rule1 = ctrl.Rule(sadnessxjoy['sadness'] & angerxfear['anger'], secundary2['envy'])
s2_rule2 = ctrl.Rule(angerxfear['fear'] & sadnessxjoy['sadness'], secundary2['despair'])
s2_rule3 = ctrl.Rule(sadnessxjoy['joy'] & angerxfear['fear'], secundary2['guilt'])
s2_rule4 = ctrl.Rule(angerxfear['anger'] & sadnessxjoy['joy'], secundary2['pride'])

# tertiary dyads
t_rule1 = ctrl.Rule(anticipationxsurprise['anticipation'] & angerxfear['fear'], tertiary['anxiety'])
t_rule2 = ctrl.Rule(sadnessxjoy['joy'] & anticipationxsurprise['surprise'], tertiary['delight'])
t_rule3 = ctrl.Rule(disgustxtrust['trust'] & sadnessxjoy['sadness'], tertiary['sentimentality'])
t_rule4 = ctrl.Rule(angerxfear['fear'] & disgustxtrust['disgust'], tertiary['shame'])
t_rule5 = ctrl.Rule(anticipationxsurprise['surprise'] & angerxfear['anger'], tertiary['outrage'])
t_rule6 = ctrl.Rule(sadnessxjoy['sadness'] & anticipationxsurprise['anticipation'], tertiary['pessimism'])
t_rule7 = ctrl.Rule(disgustxtrust['disgust'] & sadnessxjoy['joy'], tertiary['morbidness'])
t_rule8 = ctrl.Rule(angerxfear['anger'] & disgustxtrust['trust'], tertiary['dominance'])


# Fuzzy Sistems and Simulations
primary_ctrl = ctrl.ControlSystem([p_rule1,p_rule2,p_rule3,p_rule4,p_rule5,p_rule6,p_rule7,p_rule8])
secundary1_ctrl = ctrl.ControlSystem([s1_rule1,s1_rule2,s1_rule3,s1_rule4])
secundary2_ctrl = ctrl.ControlSystem([s2_rule1,s2_rule2,s2_rule3,s2_rule4])
tertiary_ctrl = ctrl.ControlSystem([t_rule1,t_rule2,t_rule3,t_rule4,t_rule5,t_rule6,t_rule7,t_rule8])

primary_simulator = ctrl.ControlSystemSimulation(primary_ctrl)
secundary1_simulator = ctrl.ControlSystemSimulation(secundary1_ctrl)
secundary2_simulator = ctrl.ControlSystemSimulation(secundary2_ctrl)
tertiary_simulator = ctrl.ControlSystemSimulation(tertiary_ctrl)

def postEmotion(emotion):
    global result; 
    result = calculateResultEmotion(emotion)

def getEmotion():
    return result

def calculateResultEmotion(emotion):
    for i in range(len(emotion)):
        emotion[i] = emotion[i]*100 # adjust emotion axes values as percentages for membership functions
    
    response_emotion = []
    membership_values = []
    max_values = []
    response_emotion.clear()
    membership_values.clear()
    max_values.clear()
    for i in range(len(axes)):
        membership_values.append([])
        for j in range(len(axes_emotions[0])):
            membership_values[i].append(fuzz.interp_membership(axes[i].universe, axes[i][axes_emotions[i][j]].mf, emotion[i])) 

    # for i in range(len(membership_values)):
    #     response_emotion.append(membership_values[i].index(max(membership_values[i])))

    # Checks which membership is dominant, if it's medium intensity, and if there's more than one
    cont_medium = 0
    for i in range(len(membership_values)):
        response_emotion.append(membership_values[i].index(max(membership_values[i])))
        max_values.append(max(membership_values[i]))
        if(response_emotion[i] == 1 or response_emotion[i] == 4):
            cont_medium += 1
    if(cont_medium <= 1):
       result = setResponseEmotion(response_emotion, max_values)
       return result
    else:
        result = calculateDyads(emotion)
        return result
        #VAI PRA LÓGICA FUZZY

def calculateDyads(emotion):
    for i in range(len(emotion)):
        primary_simulator.input[str_axes[i]] = emotion[i]
        tertiary_simulator.input[str_axes[i]] = emotion[i]
        if(i==0 or i==2):
            secundary2_simulator.input[str_axes[i]] = emotion[i]
        elif(i==1 or i==3):
            secundary1_simulator.input[str_axes[i]] = emotion[i]


    
    primary_simulator.compute()
    secundary1_simulator.compute()
    secundary2_simulator.compute()
    tertiary_simulator.compute()


    outputs = [primary_simulator.output['primary'],tertiary_simulator.output['tertiary']]
    s_outputs = [secundary1_simulator.output['secundary1'],secundary2_simulator.output['secundary2']]

    response_emotion = []
    membership_values = []
    response_emotion.clear()
    membership_values.clear()

    mvalues_size = 0
    for i in range(len(dyads)):
        membership_values.append([])
        mvalues_size += 1
        for j in range(len(dyads_emotions[0])):
            membership_values[i].append(fuzz.interp_membership(dyads[i].universe, dyads[i][dyads_emotions[i][j]].mf, outputs[i])) 


    for i in range(len(s_dyads)):
        membership_values.append([])
        for j in range(len(s_dyads_emotions[0])):
            membership_values[i + mvalues_size].append(fuzz.interp_membership(s_dyads[i].universe, 
                                                                            s_dyads[i][s_dyads_emotions[i][j]].mf, s_outputs[i]))

    max_memberships = []
    max_memberships.clear()
    for i in range(len(membership_values)):
        max_memberships.append(max(membership_values[i]))
        response_emotion.append(membership_values[i].index(max_memberships[i]))

    result = setDyadsResponseEmotion(response_emotion, max_memberships)
    return result
    # final_emotion = max(max_responses)
    # index_emotion = max_responses.index(final_emotion)
    #FALTA CHECAR SE É SECUNDARIO OU PRIMARIO/TERCIARIO

# max_memberships = valor máximo do membership de cada plutchik axe
# response_emotion = índice da emoção correspondente aos valores em max_memberships

def setResponseEmotion(response_emotion, max_memberships):
    final_index = 0
    max_index = []
    max_index.clear()
    max_ = max(max_memberships)

    for i in range(len(max_memberships)):
            if max_memberships[i] == max_:
                max_index.append(i);  #index dos máximos


    if(len(max_index) == 1):
        result = str(axes_emotions[max_index[0]][response_emotion[max_index[0]]])
        return result.capitalize()
    else:
        for i in range(len(max_index)):
            if response_emotion[max_index[i]] == 4 or response_emotion[max_index[i]] == 1:
                result = str(axes_emotions[max_index[i]][response_emotion[max_index[i]]])
                return result.capitalize()
            elif response_emotion[max_index[i]] == 2 or response_emotion[max_index[i]] == 5:
                result = str(axes_emotions[max_index[i]][response_emotion[max_index[i]]])
                return result.capitalize()
            else:
                final_index = max_index[i]


    result = str(axes_emotions[final_index][response_emotion[final_index]])
    return result.capitalize()

def setDyadsResponseEmotion(response_emotion, max_memberships):
    final_index = 0
    max_index = []
    max_index.clear()
    max_ = max(max_memberships)

    for i in range(len(max_memberships)):
            if max_memberships[i] == max_:
                max_index.append(i)

    if(len(max_index) == 1):
        if max_index[0] == 0 or max_index[0] == 1:
            result = str(dyads_emotions[max_index[0]][response_emotion[max_index[0]]])
            return result.capitalize()
        else:
            result = str(s_dyads_emotions[max_index[0]][response_emotion[max_index[0]]])
            return result.capitalize()
    else: #ordem de frequencia das dyads
        for i in range(len(max_index)):
            if max_index[i] == 0: #primary
                result = str(dyads_emotions[max_index[i]][response_emotion[max_index[i]]])
                return result.capitalize()
            elif max_index[i] == 2 or max_index[i] == 3: #secundary
                result = str(s_dyads_emotions[max_index[i]][response_emotion[max_index[i]]])
                return result.capitalize()
            else: #tertiary
                result = str(dyads_emotions[max_index[i]][response_emotion[max_index[i]]])
                return result.capitalize()

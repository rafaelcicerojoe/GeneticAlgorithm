import random;
from functools import cmp_to_key

# Genetic algorithm
# Coded by:
# Cícero-Joe Rafael Lima de Oliveira
# Eduardo José Torres Rocha
# Universidade Federal do Maranhão - Brazil
# Artificial Intelligence -  2020.1


def newCromossome():
  cromossome = [];
  while(True):
    cromossome.append(random.randint(0, 5))
    cromossome.append(random.randint(0, 7))
    cromossome.append(random.randint(0, 7))
    cromossome.append(random.randint(0, 7))
    
    if(getFitnessG(cromossome) + 15 <= 15):
      break;
    
    cromossome = []
  return cromossome
  
def newPopulation():
  population = []
  for x in range(6):
    population.append(newCromossome())
  return population

def getFitnessF(c):
  return abs(c[0]**3+c[1]**2+c[2]+5*c[3]-185)

def getFitnessG(c):
  return abs(c[0]+c[1]+c[2]+c[3]-15)

def getFitnessPopulation(population):
  result = 0
  for c in population:
    result += getFitnessF(c)+getFitnessG(c)
  return result

def getFitProbability(cromossome, population):
  fitness = getFitnessF(cromossome)+getFitnessG(cromossome)
  return fitness/getFitnessPopulation(population)

def getRandGene(probabilities):
  rand = random.random()
  i = 0
  for c in probabilities:
    if rand <= c:
      return i
    i += 1

def crossover(population):
  populationFitness = []
  for c in population:
    populationFitness.append([c, getFitnessF(c) + getFitnessG(c)])
  populationFitness.sort(key = cmp_to_key(cmpCromossomesFitness))

  bestCromossomes = populationFitness[0:3]
  worstCromossomes = populationFitness[3:6]

  probBestCromossomes = []
  for c in bestCromossomes:
    probBestCromossomes.append(getFitProbability(c[0], list(map(lambda x: x[0], bestCromossomes))))

  for index, p in enumerate(probBestCromossomes):
    if(index == 0): continue
    probBestCromossomes[index] += probBestCromossomes[index-1]

  worstCromossomes = populationFitness[3:6]
  probWorstCromossomes = []
  for c in worstCromossomes:
    probWorstCromossomes.append(getFitProbability(c[0], list(map(lambda x: x[0], worstCromossomes))))

  for index, p in enumerate(probWorstCromossomes):
    if(index == 0): continue
    probWorstCromossomes[index] += probWorstCromossomes[index-1]
  
  father1 = getRandGene(probBestCromossomes)
  father2 = getRandGene(probWorstCromossomes)

  father1 = bestCromossomes[father1][0]
  father2 = worstCromossomes[father2][0]

  randGene = random.randint(0, 3)
  aux = father1[randGene]
  father1[randGene] = father2[randGene]
  father2[randGene] = aux

  randGene = random.randint(0, 3)
  aux = father1[randGene]
  father1[randGene] = father2[randGene]
  father2[randGene] = aux

  if(random.random() < 0.5):
    mutate(father1)
  else:
    mutate(father2)

  return [
    father1,
    father2,
    newCromossome(),
    newCromossome(),
    newCromossome(),
    newCromossome(),
  ]

def mutate(c):
  randProb = random.random()
  if(randProb > 0.10): return

  probabilities = [0.25, 0.5, 0.75, 1]
  geneIndex = getRandGene(probabilities)

  c[geneIndex] = random.randint(0, 7)

def cmpCromossomesFitness(a, b):
    if a[1] < b[1]:
        return -1
    elif a[1] > b[1]:
        return 1
    else:
        return 0

def getBestFitness(population):
  populationFitness = []
  for index, c in enumerate(population):
    populationFitness.append([c, getFitnessF(c) + getFitnessG(c)])
  populationFitness.sort(key = cmp_to_key(cmpCromossomesFitness))
  return populationFitness[0]

population = newPopulation()
bestCase = None
i = 0
while(True):
  population = crossover(population)
  currestBestFitness = getBestFitness(population)
  if(bestCase == None or bestCase[1] > currestBestFitness[1]):
    bestCase = currestBestFitness
    if(bestCase[1] == 0):
      break;
    
  i += 1
  
j = 0
cromossome = newCromossome();
while(True):
  if((getFitnessF(cromossome) + getFitnessG(cromossome)) == 0):
    break;
  cromossome = newCromossome()
  j += 1

print('Genetic algorithm = ' + str(i) + ' iterations')
print('Looking for a solution randomly = ' + str(j) + ' iterations')
print('Solution = ' + str(bestCase[0]))

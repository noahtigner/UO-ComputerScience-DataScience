import random, csv
import numpy as np
import json
#======================Additional Functions and classes========================
class AB_Rule():

	def __init__(self, ID, cohesiveState, action):
		self._ID = str(ID)
		self._cs = cohesiveState
		self._action = action
		self._weight = 0
		
	def getAction(self):
		return self._action

	def getID(self):
		return self._ID

	def incrWeight(self):
		if(self._weight < 1):
			self._weight += .01

	def dercWeight(self):
		if(self._weight > -1):
			self._weight -= .01

	def upVote(self):
		self._weight = 1
		
	def downVote(self):
		self._weight = -1
		
	def __str__(self):
		return "Rule ID: "+self._ID+"     CS: "+self._cs+"          "+"Action: "+self._action

def insert_rules(cohesiveState, hub, acu, rules, activeSet, ruleBase, stats):
	ruleBase[hub][acu][cohesiveState] = []
	for rule in rules:
		if(rule._weight>0):
			activeSet[hub][acu][cohesiveState] = rule.getAction()
			ruleBase[hub][acu][cohesiveState].append(rule)
			stats["# active rules"] += 1
		else:
			ruleBase[hub][acu][cohesiveState].append(rule)

def evaluate_CS(hub, acu, cohesiveState, A, ID, stats, nec_cs):  
	rated_cs = ()
	rules = []
	fitness = 0
	cs_value = sum(map(int, cohesiveState.split(",")))

	#get user input on the cohesive state
	cs_rating = cs_value%4+1
	stats["Total UI"]+=1
	stats["#CS"]+=1
	
	if(cs_rating == 1):
		stats["#CS Nec"]+=1
		rated_cs = (cohesiveState, 1)
		nec_cs.add(cohesiveState)
		#generate the rules
		for action in A:
			rules.append(AB_Rule(ID, cohesiveState, action))
			ID+=1
		#select a rule for the OPD
		idx = random.choice(list(range(len(rules))))
		rules[idx].upVote()
		stats["Total UI"]+=1
		fitness = 1
	elif(cs_rating == 2):
		stats["#CS Ext"]+=1
		rated_cs = (cohesiveState, 2)
		fitness = -1
	elif(cs_rating == 3):
		stats["#CS Red"]+=1
		rated_cs = (cohesiveState, 3)
		fitness = -1
	elif(cs_rating == 4):
		stats["#CS Err"]+=1
		rated_cs = (cohesiveState, 4)
		fitness = -1

	return rated_cs, rules, ID, fitness, nec_cs

def continueAlgorithm(maxCS, record, nec_cs, k):
	flag = None
	if(len(record) < maxCS):
		#response = input("Do you wish to continue? (y/n): ")
		if(len(nec_cs) < (maxCS*0.25) and k<=100000):
			flag = True
		else:
			flag = False
	else:
		flag = False
		#print("All possible cohesive states for this device have been reviewed. Press <enter> to exit.")
		#input()
	return flag
#==============================================================================

def get_genome(state_matrix):
	cs = []
	
	#STEP-01: Build a cohesive state by randomly selecting states from the given matrix
	for i in range(0, len(state_matrix)):
		idx = np.random.randint(0, len(state_matrix[i]))
		cs.append((state_matrix[i][idx], idx))
	return cs

def random_selection(population, parent1):
	pop = population.copy() #create a copy so we don't change the actual population
	#print(pop)
	pop.remove(parent1)
	
	#select parent 2
	parent2 = random.choice(pop)
	pop.remove(parent2)
	
	#select parent 3
	parent3 = random.choice(pop)
	pop.remove(parent3)
	
	return parent2, parent3

def crossover_mutation(stateMatrix, parent1, parent2, parent3, child, weightingFactor, deviceindex):
	#get indexed rep of parents
	p1 = [x[1] for x in parent1] #[d1s, d2s,...]
	p2 = [x[1] for x in parent2]
	p3 = [x[1] for x in parent3]

	#mutate the gene by using a weighted difference
	#print("Parent gene index: p1: ", p1[deviceindex], "p2: ", p2[deviceindex], "p3: ", p3[deviceindex])
	mutatedStateIndex = round(p3[deviceindex] + weightingFactor * (p1[deviceindex] - p2[deviceindex]))
	if(mutatedStateIndex > len(stateMatrix[deviceindex])-1):
		mutatedStateIndex = len(stateMatrix[deviceindex])-1
	elif(mutatedStateIndex < 0):
		mutatedStateIndex = 0
	#print("Mutated index: ", mutatedStateIndex)
	mutatedGene = (stateMatrix[deviceindex][mutatedStateIndex], mutatedStateIndex)
	
	return mutatedGene

def differential_evolution(D, populationSize = 3, mutationRate = 0.6, weightingFactor = 0.7):
	ActiveRuleSet = {}
	RuleBase = {}
	stats = {"PGA": "A-Posteriori",
			 "Total UI": 0,
			 "Total CS": 0,
			 "#CS": 0,
			 "#CS Nec": 0,
			 "#CS Ext": 0,
			 "#CS Red": 0,
			 "#CS Err": 0,
			 "# rules": 0,
			 "# active rules": 0,
			}
	ID=0

	#L = D['Laws']
	for hub in D['Hubs']:
		for acu in D['Hubs'][hub]['ACUs']:
			if(D['Hubs'][hub]['ACUs'][acu]['Actions'] != 'NA'):
				#add the hub to the rule base if its new
				try:
					RuleBase[hub]
					ActiveRuleSet[hub]
				except:
					RuleBase[hub] = {}
					ActiveRuleSet[hub] = {}

				#add the ACU to the rule base
				RuleBase[hub][acu] = {}
				ActiveRuleSet[hub][acu] = {}

				#get the states, links, actions, and constraints
				S = D['Hubs'][hub]['ACUs'][acu]["Defined States"]
				A = D['Hubs'][hub]['ACUs'][acu]["Actions"]
				I = D['Hubs'][hub]['ACUs'][acu]["Semantic Links"]
				#C = D['Hubs'][hub]['ACUs'][acu]["Constraints"]
				nec_cs = set()
				#create a the matrix: SxI
				stateMatrix = [S]
				if(I != "NA"):
					for link in I:
						link = link.split(":")
						stateMatrix.append(D['Hubs'][link[0]]['ACUs'][link[1]]["Defined States"])
				
				print("="*25, "Device: ", acu, "="*25)
				#STEP-1: Generate initial population and evaluate them
				#print("="*25, "GENERATING INITIAL POPULATION", "="*25)
				population = []
				popFit = []
				maxCS = np.prod([len(x) for x in stateMatrix]) #maximum number of individuals determined by |S|x|I|
				stats["Total CS"] = maxCS
				record = {}
				assert(populationSize<=maxCS)
				
				while(len(record)<=maxCS and len(population)<=populationSize):
					while(True):
						cs = get_genome(stateMatrix)
						cohesiveState = ",".join([x[0] for x in cs])
						if(cohesiveState not in record):
							cohesiveState, rules, ID, fitness, nec_cs = evaluate_CS(hub, acu, cohesiveState, A, ID, stats, nec_cs)
							population.append(cs)
							popFit.append(fitness)
							record[cohesiveState[0]] = fitness
							insert_rules(cohesiveState[0], hub, acu, rules, ActiveRuleSet, RuleBase, stats)
							break
				#print("="*25, "END OF INITIAL POPULATION GENERATION", "="*25)
				
				
				#STEP-3: DE main loop
				k=0
				stopCondition = continueAlgorithm(maxCS, record, nec_cs, k)
				while(stopCondition):
					#print("="*25, "BEGINNING EVOLUTION STAGE", "="*25)
					#Start new population
					nextGeneration = []
					nextGenerationFitness = []
					for i in range(len(population)):
						
						#STEP-3A: Select parents from the current population
						parent1 = population[i]
						parent2, parent3 = random_selection(population, parent1)
						#print("===Random selection results===")
						#print("Parent 1: ", parent1)
						#print("Parent 2: ", parent2)
						#print("Parent 3: ", parent3)
						#print("-"*30)

						#STEP-3B: Perform crossover and mutation at the same time to generate a child
						child = np.zeros(len(parent1)).tolist()
						crossoverPoint = random.randint(0, len(parent1)-1)
						#print("Crossover point: ", crossoverPoint)
						for j in range(0, len(parent1)): #for each gene in parent1
							if(j == crossoverPoint or j > crossoverPoint and np.random.random() < mutationRate):
								#print("Mutating child gene at index: ", str(i))
								child[j] = crossover_mutation(stateMatrix, parent1, parent2, parent3, child, weightingFactor, j)
								#print("Mutated gene: ", child[i])
							else:
								#print("Passing on Parent 1 gene: ", parent1[i], " at index: ", str(i))
								child[j] = parent1[j]
						#print("Child: ", child)
						#print(k)

						#STEP-3D: Evaluate children and add them to the new population
						cohesiveState = ",".join([x[0] for x in child])
						#print("Has this child been seen before? ", cohesiveState in record)
						#print("Record: ", record)
						#print(len(population), len(popFit), i)
						pFit = popFit[i]
						if(cohesiveState not in record):
							cohesiveState, rules, ID, cFit, nec_cs = evaluate_CS(hub, acu, cohesiveState, A, ID, stats, nec_cs)
							insert_rules(cohesiveState, hub, acu, rules, ActiveRuleSet, RuleBase, stats)
							record[cohesiveState[0]] = cFit
							
							if(cFit > pFit):
								nextGeneration.append(child)
								nextGenerationFitness.append(cFit)
							elif(cFit == pFit and cFit > 0):
								nextGeneration.append(child)
								nextGenerationFitness.append(cFit)
								nextGeneration.append(parent1)
								nextGenerationFitness.append(pFit)
							elif(np.random.random() < .5):
								nextGeneration.append(parent1)
								nextGenerationFitness.append(pFit)
							else:
								nextGeneration.append(child)
								nextGenerationFitness.append(cFit)
							#if the user has seen all cs possible or wants to quit then stop
							stopCondition = continueAlgorithm(maxCS, record, nec_cs, k)
							if(not stopCondition):
								break
								k=0
							else:
								k+=1
						else:
							nextGeneration.append(parent1)
							nextGenerationFitness.append(pFit)
						#input()
							stopCondition = continueAlgorithm(maxCS, record, nec_cs, k)
							if(not stopCondition):
								break
								k=0
							else:
								k+=1
					#STEP-3F: Setup for next generation
					population = nextGeneration
					popFit = nextGenerationFitness
					
	#print("="*25, "END OF POLICY GENERATION", "="*25)
	return ActiveRuleSet, RuleBase, stats


#==============================Testing=========================================
if(__name__=="__main__"):
	infile = open("data/Experimental-Network.ndf", 'r')
	net = json.load(infile)
	infile.close()
	
	
	results = {"Simulations" : {}}
	
	
	
	#run the simulation
	for hub in net["Hubs"]:
		D = {"Hubs": {}}
		D["Hubs"][hub] = net["Hubs"][hub]
		OPD, Rulebase, stats = differential_evolution(D)
		sim_size = hub.split('-')[1]
		if(int(sim_size) < 100):
			sim_size = sim_size[0]+'-'+sim_size[1]
		else:
			sim_size = sim_size[0]+sim_size[1]+'-'+sim_size[2]
		results["Simulations"][sim_size] = stats
	
	#Write the rulults to file
	outfile = open('data/DE-Results.csv', 'w')
	writer = csv.writer(outfile)
	header = ["Simulation Size", "Total User Interactions", "Total Number of Cohesive States", "Number of Rated Cohesive States", "Number of States Rated: Necessary", "Number of States Rated: Extreneuous", "Number of States Rated: Redundant", "Number of States Rated: Error"]
	writer.writerow(header)
	for sim_size in results["Simulations"]:
		stats = results["Simulations"][sim_size]
		row = [sim_size, stats["Total UI"], stats["Total CS"], stats["#CS"], stats["#CS Nec"], stats["#CS Ext"], stats["#CS Red"], stats["#CS Err"]]
		writer.writerow(row)
	outfile.close()
#==============================================================================
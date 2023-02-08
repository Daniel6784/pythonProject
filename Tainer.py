import numpy as np
from main import *
from Agent import Agent
import time
import random
class Trainer:
    def __init__(self,generations, population):
        self.generation_num = generations
        self.population_size = population


    def makeFirstPop(self):
        population = []
        for i in range(self.population_size):
            coefs = np.random.rand(4)

            norm = np.linalg.norm(coefs)
            norm_coefs = coefs/norm

            agent = Agent(norm_coefs)
            player = Player(agent)
            population.append(player)
        self.population = population
        return population

    def fitnessFunction(self,player):
        avg_score = 0
        for i in range(1):
            avg_score += player.Play()
        return avg_score

    def nextPop(self):
         pop_with_scores = []
         weights = []
         for ind in self.population:
             fitness = self.fitnessFunction(ind)
             pop_with_scores.append([fitness,ind])
             weights.append(fitness)
         pop_with_scores.sort(key= lambda x: x[0],reverse=True)
         best = pop_with_scores[0][1]
         best_score = pop_with_scores[0][0]

         parents_a = random.choices(pop_with_scores, k=self.population_size-1)
         parents_b = random.choices(pop_with_scores,  k=self.population_size-1)
         new_children = []
         for parent_a, parent_b in zip(parents_a,parents_b):
            coefs = []
            for i in range(4):
                parent_a_cont = parent_a[1].agent.coef[i]*parent_a[0]
                parent_b_cont = parent_b[1].agent.coef[i]*parent_b[0]
                total_cont = (parent_a_cont+parent_b_cont)/(parent_a[0]+parent_b[0])
                coefs.append(total_cont)
            if random.uniform(0,1) < .1:
                 mutation = random.randint(0,3)
                 print(f"mutation index {mutation}")
                 coefs[mutation] += random.uniform(-.2,.2)
            norm = np.linalg.norm(coefs)
            norm_coefs = coefs / norm
            child_agent = Agent(norm_coefs)
            child_player = Player(child_agent)
            new_children.append(child_player)
         print(f"Average Score: {sum(weights)/50}")
         print(f"Best SCore : {best_score} with coef {best.agent.coef}")

         new_children.append(best)
         self.population = new_children




def main(name):
    print(f'Hi, {name}')  # Press ⌘F8 to toggle the breakpoint
    pygame.init()
    #agent = Agent([0.91686656, 0.16331045, 0.23661111, 0.27694872])
    agent = Agent([0.69826004, 0.14299241, 0.68546697, 0.14873171])
    #agent = Agent([0.76858026, 0.18908734, 0.34404906, 0.50513425])
    player = Player(agent)
    player.display()
    """
    trainer = Trainer(1,100)
    population = trainer.makeFirstPop()
    start_time = time.time()
    scores = []
    for i in range(10):

        trainer.nextPop()
        print("Completed One Generation")

    print(f" total time elapsed {time.time()- start_time}")

    print(trainer.population)
    for player in trainer.population:
        print(f"score: {trainer.fitnessFunction(player)}")
        print(player.agent.coef)
    """

if __name__ == '__main__':
    main('PyCharm')






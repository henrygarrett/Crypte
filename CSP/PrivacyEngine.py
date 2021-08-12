import os
import pandas as pd
class PrivacyEngine():
    def __init__(self, epsilon_budget):
        self.epsilon_budget = epsilon_budget
        self.save_epsilon_budget()

    def __str__(self):
        return "Privacy Budget: " + str(self.epsilon_budget)

    def is_program_allowed(self, program_epsilon):
        if self.epsilon_budget - program_epsilon < 0:
            return False
        else:
            self.add_to_ledger(program_epsilon)
            self.epsilon_budget -= program_epsilon
            return True

    def add_to_ledger(self, program_epsilon):
        length = pd.read_csv('.' + os.sep + 'budget.txt').shape[0]
        df = pd.DataFrame({'change': -program_epsilon, 'total': self.epsilon_budget - program_epsilon}, index=[length + 1])
        df.to_csv('.' + os.sep + 'budget.txt', mode='a',index=False, header=not '.' + os.sep + 'budget.txt')

    def save_epsilon_budget(self):
        df = pd.DataFrame({'change': self.epsilon_budget, 'total': self.epsilon_budget}, index=[0])
        df.to_csv('.' + os.sep + 'budget.txt',index=False)




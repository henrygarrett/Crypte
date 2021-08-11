import os

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
            return True
    def add_to_ledger(self, program_epsilon):
        pass

    def save_epsilon_budget(self):
        with open('.' + os.sep + 'budget.txt', 'w') as budget_file:
            budget_file.write(str(self.epsilon_budget))

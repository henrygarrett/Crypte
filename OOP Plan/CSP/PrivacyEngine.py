
# Very basic structure but can provide a starting point later for a more complicated privacy engine if needed...
import pathlib
PATH = str(pathlib.Path.cwd().parents[0])
class PrivacyEngine():
    def __init__(self, epsilon_budget):
        self.epsilon_budget = epsilon_budget
        self.save_epsilon_budget()

    def is_program_allowed(self, program_epsilon):
        if self.epsilon_budget - program_epsilon < 0:
            return False

        return True
    def save_epsilon_budget(self):
        with open(PATH + '\\CSP\\budget.txt', 'w') as budget_file:
            budget_file.write(str(self.epsilon_budget))

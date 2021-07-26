
# Very basic structure but can provide a starting point later for a more complicated privacy engine if needed...

class PrivacyEngine():
    def __init__(self, epsilon_budget):
        self.epsilon_budget = epsilon_budget


    def is_program_allowed(self, program_epsilon):
        if self.epsilon_budget - program_epsilon < 0:
            return False

        return True

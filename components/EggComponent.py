     
class EggComponent:
    def __init__(self):
        self.eggs = []
        self.hatching_time = 5 / (1/20)  # Time steps required for an egg to hatch

    def lay_egg(self):
        # Add a new egg with a countdown timer
        self.eggs.append({
            "timer": self.hatching_time
        })

    def process_time(self):
        # Process time decrement here, separate from hatching logic
        for egg in self.eggs:
            egg["timer"] -= 1

    def hatch_eggs(self):
        # Hatch eggs that are ready and return their count
        hatching_eggs = [egg for egg in self.eggs if egg["timer"] <= 0]
        self.eggs = [egg for egg in self.eggs if egg["timer"] > 0]
        return len(hatching_eggs)  # Return number of hatched eggs for external processing

        
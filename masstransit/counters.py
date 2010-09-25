class StatisticsUpdate(object):
    def __init__(self, stats):
        self.stats = stats

class Counter(object):
    
    def __init__(self):
        self.stats = {}
    
    def increment(self, stat):
        if not stat in self.stats:
            self.stats[stat] = 0
        
        self.stats[stat] += 1

    def get_raw_stats(self):
        return self.stats

counter = Counter()
increment = counter.increment
raw_stats = counter.get_raw_stats
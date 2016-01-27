class Todo:
    DIVIDER = "\t"

    def __init__(self, **kwargs):
        self.date = kwargs['date']
        self.start_time = kwargs['start_time']
        self.end_time = kwargs['end_time']
        self.content = kwargs['content']
        self.priority = kwargs['priority']

    def to_string(self):
        return self.date + self.DIVIDER + \
               self.start_time + self.DIVIDER + \
               self.end_time + self.DIVIDER + \
               self.content + self.DIVIDER + \
               self.priority

    def to_list(self):
        return [self.date, self.start_time, self.end_time, self.content, self.priority]


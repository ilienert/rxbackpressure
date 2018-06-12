from rx.concurrency import immediate_scheduler


class DequeuableBuffer:
    def __init__(self):
        self.first_idx = 0
        self.queue = []

    @property
    def last_idx(self):
        return self.first_idx + len(self.queue)

    def __len__(self):
        return len(self.queue)

    def has_element_at(self, idx):
        return idx <= self.last_idx

    def append(self, value):
        self.queue.append(value)

    def get(self, idx):
        if idx < self.first_idx:
            raise NameError('index %s is smaller than first index %s' % (idx, self.first_idx))
        elif idx - self.first_idx >= len(self.queue):
            raise NameError(
                'index %s is bigger or equal than length of queue %s' % (idx - self.first_idx, len(self.queue)))
        return self.queue[idx - self.first_idx]

    def dequeue(self, idx):
        if self.first_idx <= idx and len(self.queue) > 0:
            while self.first_idx <= idx and len(self.queue) > 0:
                self.first_idx += 1
                self.queue.pop(0)
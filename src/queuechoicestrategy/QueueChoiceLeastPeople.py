from operator import methodcaller

class QueueChoiceLeastPeople(QueueChoiceStrategy):

    # Returns shortest/smalles queue from queues, the comparison is made on the
    # basis of the size() function of the queues
    def choose_queue(self, queues: List):
        return min(queues, key = methodcaller('size'))

from src.queuejockeystrategy.QueueJockeyLeastPeople import QueueJockeyStrategy

# Idealmente dovrebbe ritornare la stessa coda nella quale si trova il Customer
# senza passare alla strategy il customer non posso peró fare questo controllo
# quindi o aggiungiamo a tutte le strategy dell jockying il ref al customer oppure
# controlliamo a mano che il valore di ritorno non sia None


class QueueJockeyNoJockeying(QueueJockeyStrategy):

    def switch_queue(self, cash_desks):
        return None

from src.Customer import Customer
import random

from src.cashdesk.CashDesk import CashDesk
from src.queue.SupermarketQueue import SupermarketQueue
from src.states.cashdeskstates.CashDeskStandardStates import CashDeskStandardNewCustomerState


class CashDeskStandard(CashDesk):

    def __init__(self, agent_id, model, supermarket_queue: SupermarketQueue, working: bool):
        super().__init__(agent_id, model, supermarket_queue)
        self.state_change(CashDeskStandardNewCustomerState(self))
        self.__working = working
        self.a_transaction = 0.6984
        self.b_transaction = 2.1219
        self.a_break = 0.2251
        self.b_break = 3.5167

    @property
    def working(self):
        return self.__working

    @working.setter
    def working(self, value: bool):
        self.__working = value

    def move_customer_beside_cashdesk(self):
        self.model.cash_desk_standard_zone.move_customer_beside_cashdesk(self.customer, self)

    def advance(self, customer: Customer):
        self.model.cash_desk_standard_zone.advance(customer)

    # Il calcolo del breaktime nel caso di cassa Standard non dipende da
    # basket size. Nel paper non dice come lo calcola.
    # Andando a vedere nel codice netlogo lo calcola con una distribuzione gamma
    # con i parametri usati in questa funzione. Non dice da dove prende questi parametri.
    # Viene lasciato Customer nella firma del metodo per non far sbagliare l'override di questo metodo.
    # https://github.com/tant2002/NetLogo-Supermarket-Queue-Model/blob/master/SupermarketQueueModel_version_3_2.nlogo
    # riga 689
    # Documentazione funzione: https://github.com/AFMac/rngs, il parametro che qui chiama lambda dovrebbe corrispondere a
    # quello che python e wikipedia chiamano Beta

    def break_time(self, c: Customer):
        alpha = 3.074209
        beta = 1 / 4.830613
        return random.gammavariate(alpha, beta)

    def get_image(self):
        if self.working:
            return "images/nSquare.png"
        else:
            return "images/nSquareGrey.png"

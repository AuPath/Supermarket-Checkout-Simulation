import logging

from src.states.State import State


class CustomerQueuedState(State):

    def action(self):
        logging.info("Customer " + str(self.context.unique_id) + " is in a QUEUE")

        if self.context.get_cash_desk(self.context.target_queue) in self.context.model.cash_desk_standard_zone\
                .cash_desks:
            chosen_queue = self.context.jockey()

            # Il controllo del None serve nel caso non vogliamo jockeying
            if chosen_queue is not None and chosen_queue != self.context.target_queue:

                logging.info("Customer " + str(self.context.unique_id) +
                             " is JOCKEYING from cashdesk " + str(self.context.get_cash_desk(self.context.target_queue).unique_id) +
                             " to cashdesk " + str(self.context.get_cash_desk(chosen_queue).unique_id))

                queue_before_customer = self.context.target_queue.content()
                i = queue_before_customer.index(self.context)
                queue_before_customer = queue_before_customer[i + 1:]

                self.context.leave_queue()

                self.context.target_queue = chosen_queue
                self.context.target_queue.enqueue(self.context)
                self.context.move_to_queue()

                if len(queue_before_customer):
                    for customer in queue_before_customer:
                        self.context.get_cash_desk(self.context.target_queue).advance(customer)

    def get_image(self):
        return "images/qCircle.png"


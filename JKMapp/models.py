#from django.db import models

from django.db import models

class TicketInformation(models.Model):
    iteration = models.IntegerField()
    ticket_count = models.IntegerField()
    date = models.DateField()
    time = models.TimeField()

    def __str__(self):
        return f"Iteration: {self.iteration}, Ticket Count: {self.ticket_count}, Date: {self.date}, Time: {self.time}"
    
    

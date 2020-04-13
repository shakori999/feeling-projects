from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

CONDITIONS = (
    (1, "Joy"),
    (2, "Passionate"),
    (3, "Happy"),
    (4, "Optimistic"),
    (5, "Content"),
    (6, " Bored"),
    (7, "Pessimistic"),
    (8, "Frustrated"),
    (9, "Overwhelmed"),
    (10, "Disappointed"),
    (11, "Worried"),
    (12, "Angry"),
    (13, "Jealous"),
    (14, "Insecure"),
    (15, "Guilty"),
    (16, "Fear"),
    (17, "Grief"),
    (18, "Despair"),
)
# Create your models here.
class Thought(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="thoughts")
    recorded_at = models.DateTimeField(default=timezone.now, editable=False)
    condition = models.IntegerField(choices=CONDITIONS)
    note = models.TextField(blank=True, default="")

    def __str__(self):
        return "{}: {}".format(
            self.recorded_at.strftime("%Y-%m-%d %H:%M:%S"), self.get_condition_display()
        )

from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from autoslug import AutoSlugField
import uuid
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.


class Group(models.Model):
    created_at = models.DateTimeField(default=timezone.now)
    created_by = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="%(class)s_created"
    )
    name = models.CharField(max_length=255)
    slug = AutoSlugField(populate_from="name", default="", unique=True)
    description = models.TextField(default="")

    class Meta:
        abstract = True

    def __str__(self):
        return self.slug


class Family(Group):
    members = models.ManyToManyField(User, related_name="families")

    class Meta:
        verbose_name_plural = "families"


class Company(Group):
    members = models.ManyToManyField(User, related_name="companies")

    class Meta:
        verbose_name_plural = "companies"


INVITE_STATUS = (
    (0, "Pending"),
    (1, "Accepted"),
    (2, "Rejected"),
)


class Invite(models.Model):
    from_user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="%(class)s_created"
    )
    to_user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="%(class)s_receved"
    )
    accepted = models.IntegerField(default=0, choices=INVITE_STATUS)
    uuid = models.CharField(max_length=32, default="", blank=True)

    class Meta:
        abstract = True

    def __str__(self):
        return f"{self.to_user} invtied by {self.from_user}"

    def save(self, *args, **kwargs):
        if not self.pk:
            self.uuid = uuid.uuid4().hex
        super().save(*args, **kwargs)


class CompanyInvite(Invite):
    company = models.ForeignKey(
        Company, related_name="invites", on_delete=models.CASCADE
    )

    def __str__(self):
        return f"{self.to_user} invited to {self.company} by {self.from_user}"


class FamilyInvite(Invite):
    family = models.ForeignKey(Family, related_name="invites", on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.to_user} invited to {self.family} by {self.from_user}"


@receiver(post_save, sender=CompanyInvite)
def join_company(sender, instance, created, **kwargs):
    if not created:
        if instance.accepted == 1:
            instance.company.members.add(instance.to_user)


@receiver(post_save, sender=FamilyInvite)
def join_family(sender, instance, created, **kwargs):
    if not created:
        if instance.accepted == 1:
            instance.family.members.add(instance.to_user)

from django.db import models
from django_tenants.models import TenantMixin, DomainMixin

class Client(TenantMixin):
    name = models.CharField(max_length=100)
    paid_until =  models.DateField(blank=True,null = True)
    on_trial = models.BooleanField(default = True)
    created_on = models.DateField(auto_now_add=True)
    schema_name=models.CharField(max_length=50)
    trial_period = models.PositiveSmallIntegerField(default = 15,help_text="Number of days for trial")
    active = models.BooleanField(default = True)

    # default true, schema will be automatically created and synced when it is saved
    auto_create_schema = True

class Domain(DomainMixin):
    pass
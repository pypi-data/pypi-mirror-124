from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Client,Domain


def convert_name_into_schema(brand):
    """
    Takes a brand name and converts all the white space into 
    underscore as the schema name is invalid for '-' or '<white space>'.
    and returns the result in lower case
    """
    n = brand.replace(" ","_")
    m = n.replace("-","_")
    return m.lower()


def convert_name_into_domain(brand):
    """
    Takes a brand name and converts all the white space into
    hyphons(-) as the domain name is invalid for '_' or '<white space>'.
    and returns the result in lower case
    """
    n = brand.replace("_","-")
    m = n.replace(" ","-")

    return m.lower()


@receiver(post_save,sender=Client)
def create_tenant(sender,instance,created,**kwargs):
    if created:
        sch_name = convert_name_into_schema(instance.name)
        instance.schema_name=sch_name
        instance.save()
        # create new domain url for new tenant
        dom=Domain()
        dom_url=DomainUrl(instance.schema_name)
        dom.domain=dom_url.final_url
        dom.tenant=instance
        dom.is_primary=True
        dom.save()


class DomainUrl:

    def __init__(self,schema_name):
        self.name=schema_name

    @property
    def get_schema_name(self):
        return convert_name_into_domain(self.name)
        
    @property
    def final_url(self):
        local='localhost'
        return '{}.{}'.format(self.get_schema_name,local)
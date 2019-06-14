from django.test import TestCase

# Create your tests here.


from .models import *


for i in range(10):
    Step.objects.create(step_name="test{}".format(i), belong_module_id=1)


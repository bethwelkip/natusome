from django.test import TestCase
from .models import Customer, Content

# Tests appear below this.
'''
Models tests
'''
class CustomerModel(TestCase):

    def setUp(self):
        self.customer = Customer(name="whatsapp:+12345679842", phone = "whatsapp:+12345679842")
    
    def test_instance(self):
        self.customer.save()
        self.assertTrue(isinstance(self.customer, Customer))

    def test_get_content(self):
        cont = self.customer.get_content(5)
        self.assertTrue(cont==sorted(cont)[::-1])) # confirm that content exists and sorted in descending order


    def tearDown(self):
        Customer.objects.all().delete()
        self.assertTrue(len(Customer.objects.all())==0)

class ContentModel(TestCase):
    pass



'''
Views Tests
'''
class CustomerModel(TestCase):
    pass



'''
Urls tests
'''
class CustomerModel(TestCase):
    pass

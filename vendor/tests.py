from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from .models import Vendors,PurchaseOrder
from .serializers import vendorSerializer,purchaseorderSerializer
from faker import Faker
from django.contrib.auth.models import User
# Create your tests here.


class SigninAPITestCase(TestCase):
    def test_login(self):
        User.objects.create_user(username="vivekkumar",password="vivek")
        crediantials = {
            "username": "vivekkumar",
            "password": "vivek",
        }
        response = APIClient().post('/api/login/',data=crediantials,format='json')
        if response.data['access_token']:
            token = response.data['access_token']
            self.assertTrue(token)
        self.assertEqual(response.status_code,status.HTTP_200_OK)

       
class VendorAPITestCase(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()
        self.fake = Faker()
        User.objects.create_user(username="vivekkumar",password="vivek")
        crediantials = {
            "username": "vivekkumar",
            "password": "vivek",
        }
        response = self.client.post('/api/login/',data=crediantials,format='json')
        if response.data['success']:
            token = response.data['access_token']
            headers = {
                "Authorization": f'Bearer {token}'
            }
        self.headers = headers
    
    def test_create_vendor(self):
        fake_name = self.fake.company()
        fake_contact_details = self.fake.email()
        fake_address = self.fake.address()
        fake_vendor_code = self.fake.uuid4()[:8].upper()
        
        data = {
            'name': fake_name,
            'contact_details':fake_contact_details,
            'address' : fake_address,
            'vendor_code': fake_vendor_code
        }
        response = self.client.post('/api/vendors/',data=data,format='json',headers=self.headers)
        
        self.assertEqual(response.status_code,status.HTTP_201_CREATED)
        self.assertTrue(Vendors.objects.get(vendor_code=fake_vendor_code))
        
    
    def test_vendor_list(self):
        response = self.client.get('/api/vendors/',headers=self.headers)
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        
    def test_get_vendor(self):
        vendor = Vendors.objects.all()
        if vendor:
            vendor = vendor[0]
            response = self.client.get(f'/api/vendors/{vendor.id}',headers=self.headers)
            self.assertEqual(response.status_code,status.HTTP_200_OK)
    
    def test_vendor_performance(self):
        vendor = Vendors.objects.all()
        if vendor:
            vendor = vendor[0]
            response = self.client.get(f'/api/vendors/{vendor.id}/performance/',headers=self.headers)
            self.assertEqual(response.status_code,status.HTTP_200_OK)
    
    def test_edit_vendor(self):
        vendor = Vendors.objects.all()
        if vendor:
            vendor = vendor[0]
            fake_name = self.fake.company()
            data = {
                'name':fake_name
            }
            response = self.client.put(f'/api/vendors/{vendor.id}',data=data,format='json',headers=self.headers)
            self.assertEqual(response.status_code,status.HTTP_200_OK)
            updatedvendor = Vendors.objects.get(id=vendor.id)
            self.assertEqual(updatedvendor.name,fake_name)
        
    def test_delete_vendor(self):
        vendor = Vendors.objects.all()
        if vendor:
            vendor = vendor[0] 
            response = self.client.delete(f'/api/vendors/{vendor.id}/',headers=self.headers)
            self.assertEqual(response.status_code,status.HTTP_200_OK)
            self.assertFalse(Vendors.objects.filter(id=vendor.id).exists())
            
            


class PurchaseOrderAPITestCase(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()
        self.fake = Faker()
        fake_name = self.fake.company()
        fake_contact_details = self.fake.email()
        fake_address = self.fake.address()
        fake_vendor_code = self.fake.uuid4()[:8].upper()
        self.vendor = Vendors.objects.create(
            name=fake_name,
            contact_details=fake_contact_details,
            address = fake_address,
            vendor_code = fake_vendor_code
        )
        User.objects.create_user(username="vivekkumar",password="vivek")
        crediantials = {
            "username": "vivekkumar",
            "password": "vivek",
        }
        response = self.client.post('/api/login/',data=crediantials,format='json')
        if response.data['success']:
            token = response.data['access_token']
            headers = {
                "Authorization": f'Bearer {token}'
            }
        self.headers = headers
    
    def test_create_po(self):
        # po_number = self.fake.uuid4()[:8].upper()
        # vendor = self.vendor.id
        # po_number = self.fake.uuid4()[:8].upper()
        order_date = self.fake.date_time_this_year()
        # delivery_date = self.fake.date_time_between(start_date=order_date)
        # items = {'item1': self.fake.random_number(digits=2), 'item2': self.fake.random_number(digits=2), 'item3': self.fake.random_number(digits=2)}
        # quantity = self.fake.random_number(digits=2)
        # status = self.fake.random_element(['pending', 'completed', 'canceled'])
        # quality_rating = self.fake.pyfloat(left_digits=2, right_digits=2, positive=True)
        issue_date = self.fake.date_time_between(start_date=order_date)
        # acknowledgment_date = self.fake.date_time_between(start_date=issue_date)
        data = {
            "po_number": self.fake.uuid4()[:8].upper(),
            "vendor": self.vendor.id,
            "order_date": order_date,
            "expected_delivery_date": self.fake.date_time_between(start_date=order_date),
            "delivery_date": self.fake.date_time_between(start_date=order_date),
            "items": {'item1': self.fake.random_number(digits=2), 'item2': self.fake.random_number(digits=2), 'item3': self.fake.random_number(digits=2)},
            "quantity": self.fake.random_number(digits=2),
            "status": self.fake.random_element(['pending', 'completed', 'canceled']),
            "quality_rating": self.fake.pyfloat(left_digits=2, right_digits=2, positive=True),
            "issue_date": issue_date,
            "acknowledgment_date": self.fake.date_time_between(start_date=issue_date),
        }
        response = self.client.post('/api/purchase_orders/',data=data,format='json',headers=self.headers)
        self.assertEqual(response.status_code,status.HTTP_201_CREATED)
        self.assertTrue(PurchaseOrder.objects.filter(po_number = data['po_number']).exists())
    
    def test_pos_list(self):
        response = self.client.get('/api/purchase_orders/',headers=self.headers)
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        
    def test_po(self):
        pos = PurchaseOrder.objects.all()
        if pos:
            po = pos[0]
            response = self.client.get(f'/api/purchase_orders/{po.id}/',headers=self.headers)
            self.assertEqual(response.status_code,status.HTTP_200_OK)
    
    
    def test_update_po(self):
        pos = PurchaseOrder.objects.all()
        if pos:
            po = pos[0]
            data = {
                "status":"completed",
                "acknowledment_date": self.fake.date_time_between(start_date=po.issue_date)
            }
            response = self.client.put(f'/api/purchase_orders/{po.id}/',data=data,format='json',headers=self.headers)
            updatepo = PurchaseOrder.objects.get(id=po.id)
            self.assertEqual(response.status_code,status.HTTP_200_OK)
            self.assertEqual(updatepo.status,data['status'])
            self.assertEqual(updatepo.acknowledgment_date,data['acknowledgment_date'])
    
    def test_update_ack_date(self):
        pos = PurchaseOrder.objects.all()
        if pos:
            po = pos[0]
            response = self.client.post(f'/api/purchase_orders/{po.id}/acknowledge/',headers = self.headers)
            self.assertEqual(response.status_code,status.HTTP_200_OK)
    
    def test_delete_po(self):
        pos = PurchaseOrder.objects.all()
        if pos:
            po = pos[0]
            response = self.client.delete(f'/api/purchase_orders/{po.id}/',headers=self.headers)
            self.assertEqual(response.status_code,status.HTTP_200_OK)
            self.assertFalse(PurchaseOrder.objects.filter(id = po.id))
            
            
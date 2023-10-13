from faker import Faker
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

faker = Faker()
class TestsSetUp(APITestCase):
    def setUp(self):
        from src.user.models import UserAccount as User
        self.login_url = reverse('jwt-create')
        self.user = User.objects.create_superuser(
            username =faker.name(),
            first_name = 'Developer',
            last_name = 'Developer',
            password = 'Developer',
            email = faker.email() 
        )
        
        response = self.client.post(
            self.login_url,
            {
                'username': self.user.username,
                'password':'Developer'
            },
            format = 'json',
        )
        
        self.assertEqual(status.HTTP_200_OK,response.status_code)
        
        self.token = response.data['access']
        
        self.client.credentials(HTTP_AUTHORIZATION='Bearer '+ self.token)
        return super().setUp()
    
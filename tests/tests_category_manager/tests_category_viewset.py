from django.urls import reverse
from rest_framework import status
from tests.test_setup import TestsSetUp
from tests.factories.category_manager.category_factory import CategoryFactory
from core.const import BASE_URL
class CategoryTestCase(TestsSetUp):
    def test_find_category(self):
        
        category = CategoryFactory().build_category()
        response = self.client.get(
            reverse('category_retrieve',args=[category.id]),
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        self.assertEqual(response.data['id'], str(category.id))
        self.assertEqual(response.data['name'], category.name)
        self.assertEqual(response.data['desc'], category.desc)
    
    def test_error_find_category(self):
        CategoryFactory().build_category()
        response = self.client.get(
            reverse('category_retrieve',args=['364763764736476']),
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    
    def test_new_category(self):
        category = CategoryFactory().build_category_JSON()
        response = self.client.post(
            reverse('category_create_list'),
            category,
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['name'], category['name'])
        self.assertEqual(response.data['desc'], category['desc'])
    
    def test_no_pass_validation(self):
        category = CategoryFactory().build_category_JSON()
        category['name'] = ''
        response = self.client.post(
            reverse('category_create_list'),
            category,
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['name'][0], 'This field may not be blank.')
        
    def test_no_pass_unique_name_validation(self):
        CategoryFactory().build_category()
        category = CategoryFactory().build_category_JSON()
        response = self.client.post(
            reverse('category_create_list'),
            category,
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['name'][0], 'Category with this name already exists.')
    
    def test_update_category(self):
        category = CategoryFactory().build_category()
        response = self.client.put(
            reverse('category_update',args=[category.id]),{
                "name":"category2",
                "desc":"desc2"    
            },
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], "category2")
        self.assertEqual(response.data['desc'], "desc2")
        
    def test_delete_category(self):
        category = CategoryFactory().build_category()
        response = self.client.delete(
            reverse('category_destroy',args=[category.id]),
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
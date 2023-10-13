from src.category.models import Category

class CategoryFactory:
    def build_category_JSON(self):
        return{
            'name':"category",
            'desc':'category',
        }
    def build_category(self):
        return Category.objects.create(**self.build_category_JSON())
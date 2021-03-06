from django import forms

from authapp.forms import ShopUserEditForm
from authapp.models import ShopUser
from mainapp.models import ProductCategory, Product


class ShopUserAdminEditForm(ShopUserEditForm):
    class Meta:
        model = ShopUser
        fields = '__all__'


class ProductCategoryEditForm(forms.ModelForm):
    discount = forms.IntegerField(label='скидка', min_value=0, max_value=90, initial=0, required=False)

    class Meta:
        model = ProductCategory
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if hasattr(field.widget, 'input_type') and field.widget.input_type == 'checkbox':
                field.widget.attrs['class'] = 'form-check-input'
            else:
                field.widget.attrs['class'] = 'form-control'
            field.help_text = ''


class ProductCreateForm(forms.ModelForm):
    class Meta:
        model = Product
        exclude = ['is_active', ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if hasattr(field.widget, 'input_type') and field.widget.input_type == 'checkbox':
                field.widget.attrs['class'] = 'form-check-input'
            else:
                field.widget.attrs['class'] = 'form-control'
            field.help_text = ''


class ProductEditForm(ProductCreateForm):
    class Meta(ProductCreateForm.Meta):
        exclude = ['', ]

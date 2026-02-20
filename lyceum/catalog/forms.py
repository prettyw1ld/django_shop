import django

import catalog.models


class TagForm(django.forms.ModelForm):
    class Meta:
        model = catalog.models.Tag
        fields = ["name"]

    def clean_name(self):
        name = self.cleaned_data["name"]
        clean_name = catalog.utils.normalization_function(name)
        if catalog.models.Tag.objects.filter(
            normalized_name=clean_name
        ).exists():
            raise django.core.validators.ValidationError(
                "Тег с таким названием уже существует"
            )

        return name


class CategoryForm(django.forms.ModelForm):
    class Meta:
        model = catalog.models.Category
        fields = ["name"]

    def clean_name(self):
        name = self.cleaned_data["name"]
        clean_name = catalog.utils.normalization_function(name)
        if catalog.models.Category.objects.filter(
            normalized_name=clean_name
        ).exists():
            raise django.core.validators.ValidationError(
                "Категория с таким названием уже существует"
            )

        return name

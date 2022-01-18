from django import forms
from .models import Group_tbl


class GroupForm(forms.ModelForm):
    class Meta:
        model = Group_tbl
        fields = ('Name', 'About', 'Media')

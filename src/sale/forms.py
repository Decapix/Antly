from django import forms


class UpdateQuantityForm(forms.Form):
    item_id = forms.UUIDField(widget=forms.HiddenInput())
    new_quantity = forms.IntegerField(min_value=1, required=True)
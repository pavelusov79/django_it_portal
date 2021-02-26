from django import forms


class ContactForm(forms.Form):
    name = forms.CharField(label="Ваше имя", max_length=50, required=True)
    email = forms.EmailField(label="Ваш почтовый адрес", max_length=50, required=True)
    message = forms.CharField(label="Текст обращения", required=True)

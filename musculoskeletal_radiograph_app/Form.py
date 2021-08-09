from django import forms


class CreatePatientForm(forms.Form):
    first_name=forms.CharField(label="First Name",max_length=255,widget=forms.TextInput(attrs={"class":"form-control", "placeholder":"First name"}))
    sur_name=forms.CharField(label="Last Name",max_length=255,widget=forms.TextInput(attrs={"class":"form-control", "placeholder":"Last name"}))
    phone_number=forms.IntegerField(label="Phone Number",widget=forms.NumberInput(attrs={"class":"form-control", "placeholder":"Phone number"}))
    email_address=forms.EmailField(label="Email Address",max_length=100,widget=forms.EmailInput(attrs={"class":"form-control", "autocomplete":"off", "placeholder":"Email address"}))
    image_url=forms.FileField(label="Profile Image",max_length=500,widget=forms.FileInput(attrs={"class":"form-control"}))


class CreateRadiograph(forms.Form):
    image_url=forms.FileField(label="Profile Image",max_length=500,widget=forms.FileInput(attrs={"class":"form-control"}))
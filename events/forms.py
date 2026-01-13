from django import forms
from .models import Event, Category, Participant


class CategoryForm(forms.ModelForm):
    class meta:  # meta class tells django form settings
        model = Category  # Which model this form is for
        fields = "__all__"  # use all fields from category model


class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = "__all__"

    # Custom validation for event name
    def clean_name(self):  # Runs automatically when form,is_valid()
        name = self.cleaned_data.get("name")  # get entered name
        if len(name) < 3:
            raise forms.ValidationError(
                "Event name must be at least 3 characters"
            )  # stop invalid submission
        return name


class ParticipantForm(forms.ModelForm):
    class Meta:
        model = Participant
        fields = "__all__"

    # custom validation for email field
    def clean_email(self):
        email = self.cleaned_data.get("email")  # Get email from form
        if Participant.objects.filter(email=email).exists():
            raise forms.ValidationError(
                "This email is already registered"
            )  # prevent duplicate email
        return email  # return valid email

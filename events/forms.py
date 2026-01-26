from django import forms
from events.models import Event, Category, Participant


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


"""Mixing to apply"""


class StyleFormMixin:
    default_classes = "border border-gray-300 w-full p-3 rounded-lg shadow-sm focus:border-rose-500 focus:outline-none"

    
    """Using mixins widget"""

    def __init__(self, *arg, **kwarg):
        super().__init__(*arg, **kwarg)
        self.apply_styled_widgets()


    def apply_styled_widgets(self):
        for field_name, field in self.fields.items():
            if isinstance(field.widget, forms.TextInput):
                field.widget.attrs.update(
                    {
                        "class": self.default_classes,
                        "placeholder": f"Enter{field.label.lower()}",
                    }
                )
            elif isinstance(field.widget, forms.Textarea):
                field.widget.attrs.update(
                    {
                        "class": self.default_classes,
                        "placeholder": f"Enter{field.label.lower()}",
                        "rows": 5,
                    }
                )
            elif isinstance(field.widget, forms.SelectDateWidget):
                print("inside date")
                field.widget.attrs.update(
                    {
                        "class": "border border-gray-300 p-3 rounded-lg shadow-sm focus:border-rose-500 focus:outline-none"
                    }
                )
            elif isinstance(field.widget, forms.CheckboxSelectMultiple):
                print("inside checkbox")
                field.widget.attrs.update({"class": "space-y-2"})

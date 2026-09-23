from django import forms

from .models import Booking


class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = [
            "name",
            "phone",
            "email",
            "occasion",
            "guests",
            "preferred_date",
            "preferred_time",
            "message",
        ]
        widgets = {
            "name": forms.TextInput(attrs={"placeholder": "Your name"}),
            "phone": forms.TextInput(attrs={"placeholder": "10-digit mobile number"}),
            "email": forms.EmailInput(attrs={"placeholder": "you@example.com (optional)"}),
            "guests": forms.NumberInput(attrs={"min": 1, "max": 200}),
            "preferred_date": forms.DateInput(attrs={"type": "date"}),
            "preferred_time": forms.TextInput(attrs={"placeholder": "8:30 pm"}),
            "message": forms.Textarea(
                attrs={
                    "rows": 4,
                    "placeholder": "Anything we should know? Birthday cake, no-spice plates, parking help.",
                }
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            css = "fp-input"
            if isinstance(field.widget, forms.Textarea):
                css += " fp-input--area"
            existing = field.widget.attrs.get("class", "")
            field.widget.attrs["class"] = f"{existing} {css}".strip()
        self.fields["email"].required = False
        self.fields["preferred_date"].required = False

    def clean_phone(self):
        phone = "".join(ch for ch in self.cleaned_data["phone"] if ch.isdigit())
        if len(phone) < 10:
            raise forms.ValidationError("Enter a phone number we can call you back on.")
        return phone

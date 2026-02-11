from django import forms
from .models import Comment, Post



class TicketForm(forms.Form):
    SUBJECT_CHOICES = (
    ('پیشنهاد', 'پیشنهاد'),
    ('انتقاد', 'انتقاد'),
    ('گزارش مشکل', 'گزارش مشکل'),
    )
    message = forms.CharField(widget=forms.Textarea, required=True)
    name = forms.CharField(max_length=250, required=True)
    email = forms.EmailField()
    phone = forms.CharField(max_length=11, required=True, label="شماره تماس")
    subject = forms.ChoiceField(choices=SUBJECT_CHOICES)

    def clean_phone(self):
        """
        customising phone number validation
        """

        phone = self.cleaned_data['phone']
        if phone:
            if len(phone) != 11or not phone.isnumeric():
                raise forms.ValidationError('شماره نامعتبر است')
            else:
                return phone
        return None


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('name', 'body')

        '''ایجاد استثنا مثلا بگی همه فیلد ها باشن به جز مثلا user مثل مثال پایین'''
        #exclude = ('user',)

    def clean_name(self):

        name = self.cleaned_data['name']
        if name:
            if len(name)<3:
                raise forms.ValidationError('نام کوتاه است!')
            else:
                return name
        return None

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'description', 'author',)


class PostSearch(forms.Form):
    query = forms.CharField()


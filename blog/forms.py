from django import forms
from .models import Comment, Post, User, Profile


class TicketForm(forms.Form):
    SUBJECT_CHOICES = (
        ('انتقاد', 'انتقاد'),
        ('پیشنهاد', 'پیشنهاد'),
        ('گزارش', 'گزارش')
    )
    name = forms.CharField(max_length=250, required=True)
    email = forms.EmailField()
    phone = forms.CharField(max_length=11, required=True)
    subject = forms.ChoiceField(choices=SUBJECT_CHOICES)
    message = forms.CharField(widget=forms.Textarea, max_length=1000, required=True)

    def clean_phone(self):
        phone = self.cleaned_data['phone']
        if phone:
            if not phone.isnumeric():
                raise forms.ValidationError("مقداری که وارد کردید عدد نیست !")
            else:
                if len(str(phone)) == 11:
                    return phone
                else:
                    raise forms.ValidationError("شماره تلفن باید 11 رقم باشد !")


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['name', 'text']

    def clean_name(self):
        name = self.cleaned_data['name']
        if name:
            if len(name) < 3:
                raise forms.ValidationError('نام کوتاه است !')
            else:
                return name

    def clean_text(self):
        text = self.cleaned_data['text']
        if text:
            if len(text) > 5000:
                raise forms.ValidationError('کامنت شما بیشتر از 5000 کاراکتر است !')
            else:
                return text


class SearchForm(forms.Form):
    query = forms.CharField()


class PostForm(forms.ModelForm):
    image1 = forms.ImageField(label='تصویر اول')
    image2 = forms.ImageField(label='تصویر دوم')

    class Meta:
        model = Post
        fields = ["title", "description", "reading_time", "category"]


# class LoginForm(forms.Form):
#     username = forms.CharField(max_length=250, required=True)
#     password = forms.CharField(max_length=250, required=True, widget=forms.PasswordInput)

class UserRegisterForm(forms.ModelForm):
    password = forms.CharField(max_length=20, widget=forms.PasswordInput, label='رمز عبور')
    password2 = forms.CharField(max_length=20, widget=forms.PasswordInput, label='تکرار رمز عبور')

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']

    def clean_password2(self):
        cd = self.cleaned_data
        password = cd.get('password')
        password2 = cd.get('password2')
        if password and password2 and password != password2:
            raise forms.ValidationError('پسورد ها مطابقت ندارد!')
        return password2


class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']


class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['date_of_birth', 'job', 'bio', 'photo']
from django import forms
from .models import Comment

class EmailPostForm1(forms.Form):
    name = forms.CharField(max_length=25)
    email = forms.EmailField()  #можно убрать это и отправлять с адреса по умолчанию
    to = forms.EmailField()
    comments = forms.CharField(required=False, widget=forms.Textarea)


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('name', 'email', 'body')

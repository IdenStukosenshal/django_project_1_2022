from django import forms
from .models import Comment, Post

class EmailPostForm1(forms.Form):
    name = forms.CharField(max_length=25)
    email = forms.EmailField()  #можно убрать это и отправлять с адреса по умолчанию
    to = forms.EmailField()
    comments = forms.CharField(required=False, widget=forms.Textarea)


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('name', 'email', 'body')


class SearchForm(forms.Form):
    query = forms.CharField()









class CreatePostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'author', 'body', 'publish', 'status', 'tags')

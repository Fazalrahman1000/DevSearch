from django.forms import ModelForm
from .models import Projects, Reviews
from django import forms

class ProjectForm(ModelForm):
    class Meta:
        model = Projects
        fields = ['title','description', 'featured_image','demo_link','source_link','tags']
        widgets = {
            'tags':forms.CheckboxSelectMultiple(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({'class':'input'})
        # self.fields['title'].widget.attrs.update({'class':'input','placeholder':'Enter Project Title'})
        # self.fields['description'].widget.attrs.update({'class':'input','placeholder':'describe your project'})

class ReviewForm(ModelForm):
    class Meta:
        model = Reviews
        fields = ['value', 'body']


        labels = {
            'value':'Place your Votes',
            'body':'Add comment with you vote'
        }



    def __init__(self, *args, **kwargs):
        super(ReviewForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({'class':'input'})
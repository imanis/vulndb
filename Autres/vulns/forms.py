from django import forms
from vulnDB.projects.models import ProjectNature
from vulnDB.vulns.models import Vuln, VulnCategory, VulnType, VulnAction_priority, VulnAction_complexity, VulnExploitation_impact, VulnExploitation_complexity
from ckeditor.widgets import CKEditorWidget
from ckeditor.fields import RichTextFormField

#from crispy_forms.helper import FormHelper


class VulnForm(forms.ModelForm):

    # Hide Field
    status = forms.CharField(widget=forms.HiddenInput())

    vulnerability = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}),max_length=255)
    description = forms.CharField(widget=CKEditorWidget(config_name='vuln_description'))
    affected_item_tags = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}),
        max_length=255,
        required=True,
        help_text='Use spaces to separate the affected items tags')

    category =  forms.ModelChoiceField(queryset=VulnCategory.objects.all(), empty_label="(choose from the list)")
    nature = forms.ModelChoiceField(queryset=ProjectNature.objects.all(), empty_label="(choose from the list)")
    type = forms.ModelChoiceField(queryset=VulnType.objects.all(), empty_label="(choose from the list)")


    #description = forms.CharField(widget=forms.Textarea(attrs={'class':'form-control'}),max_length=4000)
    recommendation = forms.CharField(widget=CKEditorWidget(config_name='vuln_recommendation'))


    exploitation_impact = forms.ModelChoiceField(queryset=VulnExploitation_impact.objects.all(), empty_label="(choose from the list)")
    exploitation_complexity =  forms.ModelChoiceField(queryset=VulnExploitation_complexity.objects.all(), empty_label="(choose from the list)")
    action_complexity =  forms.ModelChoiceField(queryset=VulnAction_complexity.objects.all(), empty_label="(choose from the list)")

   # severity =  forms.CharField()
   # action_priority =  forms.CharField()


    class Meta:
        model = Vuln
        fields = [ 'vulnerability', 'category', 'nature', 'type','description', 'affected_item_tags' , 'recommendation',
                  'exploitation_impact', 'exploitation_complexity', 'action_complexity']#, 'severity', 'action_priority']


    def __init__(self, *args, **kwargs):
        super(VulnForm, self).__init__(*args, **kwargs)
        self.fields['description'].widget.attrs.update({'class' : 'ckeditor'})

        #self.fields['ref'].widget.attrs.update({'class' : 'form-control'})
        self.fields['vulnerability'].widget.attrs.update({'class' : 'form-control'})
      #  self.fields['severity'].widget.attrs.update({'class' : 'form-control'})
        self.fields['type'].widget.attrs.update({'class' : 'form-control'})
        self.fields['nature'].widget.attrs.update({'class' : 'form-control'})

        self.fields['category'].widget.attrs.update({'class' : ' form-control'})
        #self.fields['affected_item_tags'].widget.attrs.update({'class' : 'form-control'})

        self.fields['exploitation_impact'].widget.attrs.update({'class' : 'form-control'})
        self.fields['exploitation_complexity'].widget.attrs.update({'class' : 'form-control'})
        self.fields['action_complexity'].widget.attrs.update({'class' : 'form-control'})
       # self.fields['action_priority'].widget.attrs.update({'class' : 'form-control'})




class VulnCategoryForm(forms.ModelForm):

    category = forms.CharField(
        max_length=255,
        required=True,
        help_text='Add a new category')

    class Meta:
        model = VulnCategory
        fields = ['category']

    def __init__(self, *args, **kwargs):
        super(VulnCategoryForm, self).__init__(*args, **kwargs)
        self.fields['category'].widget.attrs.update({'class' : 'form-control'})

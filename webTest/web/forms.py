from django import forms

class NewPerson(forms.Form):
    name = forms.CharField(max_length=20)
    department = forms.CharField(max_length=50)
    title = forms.CharField(max_length=50)
    remark = forms.CharField(max_length=200)
    #status = forms.ChoiceField(widget=forms.Select(),choices=Status,initial=Status[0])

class NewMission(forms.Form):
    name = forms.CharField(max_length=50)
    remark = forms.CharField(max_length=200)

class NewSubmission(forms.Form):
    mission_id = forms.IntegerField(max_value=9)
    content = forms.CharField(max_length=200)
    remark = forms.CharField(max_length=200)


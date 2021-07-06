from django import forms
from django.forms import fields
from django.utils.translation import npgettext_lazy, pgettext_lazy

from .models import User

TYPE = [("All","All"),("Aircraft","Aircraft"),("Entity","Entity"),("Individual","Individual"),("Vessel","Vessel")]

PROGRAM = [("All","All"),('561-Related', '561-Related'), ('BALKANS', 'BALKANS'), ('BELARUS', 'BELARUS'), ('BURMA-EO14014', 'BURMA-EO14014'), ('BURUNDI', 'BURUNDI'), ('CAATSA - IRAN', 'CAATSA - IRAN'), ('CAATSA - RUSSIA', 'CAATSA - RUSSIA'), ('CAR', 'CAR'), ('CMIC-EO13959', 'CMIC-EO13959'), ('CUBA', 'CUBA'), ('CYBER2', 'CYBER2'), ('DARFUR', 'DARFUR'), ('DPRK', 'DPRK'), ('DPRK2', 'DPRK2'), ('DPRK3', 'DPRK3'), ('DPRK4', 'DPRK4'), ('DPRK-NKSPEA', 'DPRK-NKSPEA'), ('DRCONGO', 'DRCONGO'), ('ELECTION-EO13848', 'ELECTION-EO13848'), ('FSE-IR', 'FSE-IR'), ('FSE-SY', 'FSE-SY'), ('FTO', 'FTO'), ('GLOMAG', 'GLOMAG'), ('HIFPAA', 'HIFPAA'), ('HK-EO13936', 'HK-EO13936'), ('HRIT-IR', 'HRIT-IR'), ('HRIT-SY', 'HRIT-SY'), ('IFCA', 'IFCA'), ('IFSR', 'IFSR'), ('IRAN', 'IRAN'), ('IRAN-CON-ARMS', 'IRAN-CON-ARMS'), ('IRAN-EO13846', 'IRAN-EO13846'), ('IRAN-EO13871', 'IRAN-EO13871'), ('IRAN-EO13876', 'IRAN-EO13876'), ('IRAN-EO13902', 'IRAN-EO13902'), ('IRAN-HR', 'IRAN-HR'), ('IRAN-TRA', 'IRAN-TRA'), ('IRAQ2', 'IRAQ2'), ('IRAQ3', 'IRAQ3'), ('IRGC', 'IRGC'), ('ISA', 'ISA'), ('LEBANON', 'LEBANON'), ('LIBYA2', 'LIBYA2'), ('LIBYA3', 'LIBYA3'), ('MAGNIT', 'MAGNIT'), ('MALI-EO13882', 'MALI-EO13882'), ('NICARAGUA', 'NICARAGUA'), ('NICARAGUA-NHRAA', 'NICARAGUA-NHRAA'), ('NPWMD', 'NPWMD'), ('NS-PLC', 'NS-PLC'), ('PEESA', 'PEESA'), ('RUSSIA-EO14024', 'RUSSIA-EO14024'), ('SDGT', 'SDGT'), ('SDNT', 'SDNT'), ('SDNTK', 'SDNTK'), ('SOMALIA', 'SOMALIA'), ('SOUTH SUDAN', 'SOUTH SUDAN'), ('SYRIA', 'SYRIA'), ('SYRIA-CAESAR', 'SYRIA-CAESAR'), ('SYRIA-EO13894', 'SYRIA-EO13894'), ('TCO', 'TCO'), ('UKRAINE-EO13660', 'UKRAINE-EO13660'), ('UKRAINE-EO13661', 'UKRAINE-EO13661'), ('UKRAINE-EO13662', 'UKRAINE-EO13662'), ('UKRAINE-EO13685', 'UKRAINE-EO13685'), ('VENEZUELA', 'VENEZUELA'), ('VENEZUELA-EO13850', 'VENEZUELA-EO13850'), ('VENEZUELA-EO13884', 'VENEZUELA-EO13884'), ('YEMEN', 'YEMEN'), ('ZIMBABWE', 'ZIMBABWE')]

COUNTRY = [("All","All"),('Afghanistan', 'Afghanistan'), ('Albania', 'Albania'), ('Algeria', 'Algeria'), ('Angola', 'Angola'), ('Argentina', 'Argentina'), ('Armenia', 'Armenia'), ('Aruba', 'Aruba'), ('Australia', 'Australia'), ('Austria', 'Austria'), ('Azerbaijan', 'Azerbaijan'), ('Bahamas, The', 'Bahamas, The'), ('Bahrain', 'Bahrain'), ('Bangladesh', 'Bangladesh'), ('Barbados', 'Barbados'), ('Belarus', 'Belarus'), ('Belgium', 'Belgium'), ('Belize', 'Belize'), ('Benin', 'Benin'), ('Bolivia', 'Bolivia'), ('Bosnia and Herzegovina', 'Bosnia and Herzegovina'), ('Brazil', 'Brazil'), ('Brunei', 'Brunei'), ('Bulgaria', 'Bulgaria'), ('Burkina Faso', 'Burkina Faso'), ('Burma', 'Burma'), ('Burundi', 'Burundi'), ('Cambodia', 'Cambodia'), ('Canada', 'Canada'), ('Cayman Islands', 'Cayman Islands'), ('Dominican Republic', 'Dominican Republic'), ('Ecuador', 'Ecuador'), ('Egypt', 'Egypt'), ('El Salvador', 'El Salvador'), ('Equatorial Guinea', 'Equatorial Guinea'), ('Eritrea', 'Eritrea'), ('Ethiopia', 'Ethiopia'), ('Finland', 'Finland'), ('France', 'France'), ('Georgia', 'Georgia'), ('Germany', 'Germany'), ('Ghana', 'Ghana'), ('Gibraltar', 'Gibraltar'), ('Greece', 'Greece'), ('Guatemala', 'Guatemala'), ('Guernsey', 'Guernsey'), ('Guyana', 'Guyana'), ('Haiti', 'Haiti'), ('Honduras', 'Honduras'), ('Hong Kong', 'Hong Kong'), ('India', 'India'), ('Indonesia', 'Indonesia'), ('Iran', 'Iran'), ('Iraq', 'Iraq'), ('Ireland', 'Ireland'), ('Israel', 'Israel'), ('Italy', 'Italy'), ('Jamaica', 'Jamaica'), ('Japan', 'Japan'), ('Jersey', 'Jersey'), ('Jordan', 'Jordan'), ('Kazakhstan', 'Kazakhstan'), ('Kenya', 'Kenya'), ('Korea, North', 'Korea, North'), ('Korea, South', 'Korea, South'), ('Kosovo', 'Kosovo'), ('Kuwait', 'Kuwait'), ('Kyrgyzstan', 'Kyrgyzstan'), ('Laos', 'Laos'), ('Latvia', 'Latvia'), ('Lebanon', 'Lebanon'), ('Liberia', 'Liberia'), ('Libya', 'Libya'), ('Liechtenstein', 'Liechtenstein'), ('Luxembourg', 'Luxembourg'), ('Macau', 'Macau'), ('Malaysia', 'Malaysia'), ('Maldives', 'Maldives'), ('Mali', 'Mali'), ('Malta', 'Malta'), ('Marshall Islands', 'Marshall Islands'), ('Mauritania', 'Mauritania'), ('Mexico', 'Mexico'), ('Moldova', 'Moldova'), ('Mongolia', 'Mongolia'), ('Montenegro', 'Montenegro'), ('Morocco', 'Morocco'), ('Mozambique', 'Mozambique'), ('Namibia', 'Namibia'), ('Netherlands', 'Netherlands'), ('Netherlands Antilles', 'Netherlands Antilles'), ('New Zealand', 'New Zealand'), ('Nicaragua', 'Nicaragua'), ('Niger', 'Niger'), ('Nigeria', 'Nigeria'), ('Norway', 'Norway'), ('Oman', 'Oman'), ('Pakistan', 'Pakistan'), ('Palau', 'Palau'), ('Palestinian', 'Palestinian'), ('Panama', 'Panama'), ('Paraguay', 'Paraguay'), ('Peru', 'Peru'), ('Philippines', 'Philippines'), ('Poland', 'Poland'), ('Qatar', 'Qatar'), ('Region: Crimea', 'Region: Crimea'), ('Region: Gaza', 'Region: Gaza'), ('Region: Kafia Kingi', 'Region: Kafia Kingi'), ('Region: Northern Mali', 'Region: Northern Mali'), ('Romania', 'Romania'), ('Russia', 'Russia'), ('Rwanda', 'Rwanda'), ('Saint Kitts and Nevis', 'Saint Kitts and Nevis'), ('Saint Vincent and the Grenadines', 'Saint Vincent and the Grenadines'), ('Samoa', 'Samoa'), ('Saudi Arabia', 'Saudi Arabia'), ('Senegal', 'Senegal'), ('Serbia', 'Serbia'), ('Seychelles', 'Seychelles'), ('Sierra Leone', 'Sierra Leone'), ('Singapore', 'Singapore'), ('Slovakia', 'Slovakia'), ('Slovenia', 'Slovenia'), ('Somalia', 'Somalia'), ('South Africa', 'South Africa'), ('South Sudan', 'South Sudan'), ('Spain', 'Spain'), ('Sri Lanka', 'Sri Lanka'), ('Sudan', 'Sudan'), ('Sweden', 'Sweden'), ('Switzerland', 'Switzerland'), ('Syria', 'Syria'), ('Taiwan', 'Taiwan'), ('Tajikistan', 'Tajikistan'), ('Tanzania', 'Tanzania'), ('Thailand', 'Thailand'), ('The Gambia', 'The Gambia'), ('Trinidad and Tobago', 'Trinidad and Tobago'), ('Tunisia', 'Tunisia'), ('Turkey', 'Turkey'), ('Turkmenistan', 'Turkmenistan'), ('Uganda', 'Uganda'), ('Ukraine', 'Ukraine'), ('undetermined', 'undetermined'), ('United Arab Emirates', 'United Arab Emirates'), ('United Kingdom', 'United Kingdom'), ('United States', 'United States'), ('Uruguay', 'Uruguay'), ('Uzbekistan', 'Uzbekistan'), ('Vanuatu', 'Vanuatu'), ('Venezuela', 'Venezuela'), ('Vietnam', 'Vietnam'), ('Virgin Islands', 'Virgin Islands'), ('British', 'British'), ('West Bank', 'West Bank'), ('Yemen', 'Yemen'), ('Zimbabwe', 'Zimbabwe')]

LISTITEMS = [('All','All'),('Non-SDN','Non-SDN'),('SDN','SDN')]


class UserProfileform(forms.ModelForm):
    class Meta:
        model = User
        exclude = ['created_at', 'updated_at', 'last_login']
    def __init__(self, *args, **kwargs):
        super(UserProfileform, self).__init__(*args, **kwargs)

class Loginform(forms.Form):
    email = forms.CharField(label='Email/Phone')
    password = forms.CharField(label='Password')

    class Meta:
        model = User
        exclude = ['created_at', 'updated_at', 'last_login']
    def __init__(self, *args, **kwargs):
        super(Loginform, self).__init__(*args, **kwargs)


class Dataform(forms.Form):
    country = forms.ChoiceField(
        label=pgettext_lazy('Order field', 'Country'), choices = COUNTRY )
    program = forms.ChoiceField(
        label=pgettext_lazy('Order field', 'Program'), choices = PROGRAM )
    listitem = forms.ChoiceField(
        label=pgettext_lazy('Order field', 'List'), choices = LISTITEMS )
    typeofmetrics = forms.ChoiceField(
        label=pgettext_lazy('Order field', 'Type'), choices = TYPE )
    minimum_name_score = forms.DecimalField(label = pgettext_lazy('label', 'Minimum Name Score'))
    name = forms.CharField(label='Name')
    ids = forms.CharField(label='ID #')
    address = forms.CharField(label='Address')
    city = forms.CharField(label='City')
    state = forms.CharField(label='State/Province:*')

    def __init__(self, *args, **kwargs):
        super(Dataform, self).__init__(*args, **kwargs)
        self.fields['country'].label = "Country"
        self.fields['program'].label = "Program"
        self.fields['listitem'].label = "List"
        self.fields['typeofmetrics'].label = "Type"
        self.fields['country'].widget.attrs.update({"class": "browser-default"})
        self.fields['program'].widget.attrs.update({"class": "browser-default"})
        self.fields['listitem'].widget.attrs.update({"class": "browser-default"})
        self.fields['typeofmetrics'].widget.attrs.update({"class": "browser-default"})
        self.fields['minimum_name_score'].label = "Minimum Name Score"
        self.fields['name'].label = "Name"
        self.fields['ids'].label = "ID #"
        self.fields['address'].label = "Address"
        self.fields['city'].label = "City"
        self.fields['state'].label = "State"

        self.fields['country'].required = False
        self.fields['program'].required = False
        self.fields['listitem'].required = False
        self.fields['typeofmetrics'].required = False
        self.fields['minimum_name_score'].required = False
        self.fields['name'].required = False
        self.fields['ids'].required = False
        self.fields['address'].required = False
        self.fields['city'].required = False
        self.fields['state'].required = False
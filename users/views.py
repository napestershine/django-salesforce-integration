import json
import requests
from django.shortcuts import render, redirect
from django.conf import settings

from .models import User, Account, Contact


def index(request):
    if request.user.is_authenticated:
        return redirect(
            "https://login.salesforce.com/services/oauth2/authorize?client_id=" + settings.SALESFORCE_CLIENT_ID + "&redirect_uri=https://127.0.0.1:8000/test&response_type=code"
        )
    else:
        return redirect('login')


def get_redirect_url(request):
    # try:
    payload = {
        'grant_type': 'authorization_code',
        'client_id': settings.SALESFORCE_CLIENT_ID,
        'client_secret': settings.SALESFORCE_CLIENT_SECRET,
        'code': request.GET.get('code'),
        'redirect_uri': 'https://127.0.0.1/details'
    }

    # Post payload to Salesforce Oauth server and get user
    # token in response.
    r = requests.post(
        "https://login.salesforce.com/services/oauth2/token",
        headers={
            "Content-Type": "application/x-www-form-urlencoded"
        },
        data=payload
    )

    # Decode the JSON response from Salesforce Oauth server
    decoded = json.loads(r.content)
    request.session['access_token'] = decoded['access_token']

    return redirect('detail')


def detail(request):
    if not request.session.get('access_token'):
        return redirect('login')

    users = get_data(request, 'User',
                     'Id+,+AboutMe+,+Email+,+Username+,+Address+,+CompanyName+,+Department,+FirstName+,+LastName')

    for userData in users['records']:
        try:
            password = '123'
            first_name = userData['FirstName']
            username = userData['Username']
            email = userData['Email']
            last_name = userData['LastName']
            about = userData['AboutMe']
            company = userData['CompanyName']
            department = userData['Department']
            address = userData['Address']['street']
            user = User.objects.create(
                email=email,
                password=password,
                first_name=first_name,
                last_name=last_name,
                username=username,
                about=about,
                company=company,
                department=department,
                address=address
            )
            user.save()
        except ValueError as e:
            print(e)

    accounts = get_data(request, 'Account', 'Id+,+Name+,+AccountNumber+,+Description+,+Industry+,+BillingAddress')
    for accountData in accounts['records']:
        try:
            account_address = ''
            if accountData['BillingAddress']:
                account_address = accountData['BillingAddress']['street']
            description = accountData['Description']
            name = accountData['Name']
            industry = accountData['Industry']
            account_number = accountData['AccountNumber']
            account = Account.objects.create(
                address=account_address,
                description=description,
                name=name,
                industry=industry,
                account_number=account_number
            )
            account.save()
        except ValueError as e:
            print(e)

    contacts = get_data(request, 'Contact',
                        'Id+,+Name+,+AccountId+,+Email+,+Birthdate+,+MailingAddress+,+Description+,+Department')

    for contactData in contacts['records']:
        try:
            address = ''
            name = contactData['Name']
            email = contactData['Email']
            department = contactData['Department']
            account_id = contactData['AccountId']
            description = contactData['Description']
            birth_date = contactData['Birthdate']
            if contactData['MailingAddress']:
                address = contactData['MailingAddress']['street']
            contact = Contact.objects.create(
                name=name,
                email=email,
                department=department,
                account_id=account_id,
                description=description,
                birthDate=birth_date,
                address=address
            )
            contact.save()
        except ValueError as e:
            print(e)

    return redirect('show')


def show(request):
    if not request.user.is_authenticated:
        return redirect('login')

    return render(request, 'users/details.html', {
        'users': User.objects.all(),
        'accounts': Account.objects.all(),
        'contacts': Contact.objects.all()
    })


def get_data(request, table, query):
    response = requests.get(
        settings.SALESFORCE_URL + '/services/data/v53.0/query?q=SELECT+' + query + '+FROM+' + table,
        params=None,
        data=None,
        headers={
            'Authorization': 'Bearer ' + request.session.get('access_token')
        }
    )

    return json.loads(response.content)

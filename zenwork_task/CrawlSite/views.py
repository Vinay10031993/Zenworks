import os
import datetime
from uuid import uuid4
import json, requests

from django.http import response
from django.http.response import JsonResponse
from django.shortcuts import redirect, render
from django.http import Http404, HttpResponseForbidden, JsonResponse
from django.template.response import TemplateResponse
from . import forms
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate
from django.db.models import Q
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import NoSuchElementException 

from .models import User, UserToken

url = "https://sanctionssearch.ofac.treas.gov/"
def scrape(request, data):
    options = Options()
    options.headless = True
    options.add_experimental_option("detach", True)
    options.add_argument("--window-size=1920,1080")

    driver = webdriver.Chrome(options=options)

    driver.get(url)
    if data["name"]:
        driver.find_element_by_id('ctl00_MainContent_txtLastName').send_keys(data["name"])
    if data["ids"]:
        driver.find_element_by_id('ctl00_MainContent_txtID').send_keys(data["ids"])
    if data["minimum_name_score"]:
        driver.find_element_by_id('ctl00_MainContent_Slider1_Boundcontrol').send_keys(data["minimum_name_score"])
    if data["address"]:
        driver.find_element_by_id('ctl00_MainContent_txtAddress').send_keys(data["address"])
    if data["city"]:
        driver.find_element_by_id('ctl00_MainContent_txtCity').send_keys(data["city"])
    if data["state"]:
        driver.find_element_by_id('ctl00_MainContent_txtState').send_keys(data["state"])
    if data["typeofmetrics"] != 'All':
        ddltype = Select(driver.find_element_by_id("ctl00_MainContent_ddlType"))
        ddltype.select_by_visible_text(data["typeofmetrics"])
    if data["program"] != "All":
        ddlprograms = Select(driver.find_element_by_id("ctl00_MainContent_lstPrograms"))
        ddlprograms.deselect_by_visible_text("All")
        ddlprograms.select_by_visible_text(data["program"])
    if data["country"] != "All":
        ddlcountry = Select(driver.find_element_by_id("ctl00_MainContent_ddlCountry"))
        ddlcountry.select_by_visible_text(data["country"])
    if data["listitem"] != "All":
        ddllist = Select(driver.find_element_by_id("ctl00_MainContent_ddlList"))
        ddllist.select_by_visible_text(data["listitem"])

    driver.find_element_by_id("ctl00_MainContent_btnSearch").click()
    json_data = []
    for row in driver.find_elements_by_css_selector("tr.alternatingRowColor"):
        dict_data = {}
        dict_data["Name"]= row.find_elements_by_tag_name("td")[0].text
        dict_data["Address"] = row.find_elements_by_tag_name("td")[1].text
        dict_data["Ptype"] = row.find_elements_by_tag_name("td")[2].text
        dict_data["Programs"] = row.find_elements_by_tag_name("td")[3].text
        dict_data["List"] = row.find_elements_by_tag_name("td")[4].text
        dict_data["Score"] = row.find_elements_by_tag_name("td")[5].text
        json_data.append(dict_data)
    try:
        response = driver.find_element_by_id("ctl00_MainContent_lblMessage").text
    except NoSuchElementException:
        response = False
    if json_data:
        yield json_data
    else:
        json_data = response
        yield json_data

    # element = WebDriverWait(driver, 20).until(lambda x: x.find_element_by_id("gvSearchResults"))

@csrf_exempt
def get_records(requests):
    form = forms.Dataform(requests.POST or None)
    ctx = {'form':form}
    if form.is_valid():
        data = {}
        data["name"]= form.cleaned_data.get("name")
        data["country"]= form.cleaned_data.get("country")
        data["ids"]=  form.cleaned_data.get("ids")
        data["city"]= form.cleaned_data.get("city")
        data["address"]= form.cleaned_data.get("address")
        data["state"]=  form.cleaned_data.get("state")
        data["program"]=  form.cleaned_data.get("program")
        data["listitem"]=  form.cleaned_data.get("listitem")
        data["typeofmetrics"]=  form.cleaned_data.get("typeofmetrics")
        data["minimum_name_score"]= form.cleaned_data.get("minimum_name_score")
        json_data = list(scrape(requests,data))
        if not isinstance(json_data[0], str):
            ctx["json_data"] = json.dumps(json_data)
        else:
            ctx["json_data"] = json_data
        return TemplateResponse(requests,"crawlsite/get_info.html", ctx)
    
    return TemplateResponse(requests,'crawlsite/get_info.html', ctx)

@csrf_exempt
def signupview(requests):
    userform = forms.UserProfileform(requests.POST or None)
    if userform.is_valid():
        userform.save()
        return redirect('crawlsites:loginview')
    ctx = {"form": userform}
    return TemplateResponse(requests,"crawlsite/signupform.html", ctx)


@csrf_exempt
def loginview(requests):
    form = forms.Loginform(requests.POST or None)
    if form.is_valid():
        user = User.objects.filter(Q(email = requests.POST.get('email')) | Q(phone=requests.POST.get('email')))
        if user.exists():
            if user.first().password == requests.POST.get('password'):
                rand_token = str(uuid4())
                tok,istrue = UserToken.objects.get_or_create(user = user.first(),access_token = rand_token)
                return {"Access Token": rand_token, "user": user.first().username}
                messages.success(requests,"Login Successful")
                return redirect('crawlsites:login')
            else:
                messages.error(requests,"Credentials doesnt match.")
                return redirect('crawlsites:loginview')

    ctx={"form": form}
    return TemplateResponse(requests,"crawlsite/login.html", ctx)

@csrf_exempt
def signup(requests):
    userform = forms.UserProfileform(requests.POST or None)
    if userform.is_valid():
        try: 
            userform.save()
            return respondWithItem(200,"Signed Up Successfully")
        except Exception as e:
            return respondWithError(403, e)
    else:
        return respondWithError(403, "Something went wrong")

@csrf_exempt
def login(requests):
    user = User.objects.filter(Q(email = requests.POST.get('email')) | Q(phone=requests.POST.get('email')))
    if user.exists():
        if user.first().password == requests.POST.get('password'):
            rand_token = str(uuid4())
            tok,istrue = UserToken.objects.get_or_create(user = user.first(),access_token = rand_token)

            return respondWithItem(200, {"Access Token": rand_token, "user": user.first().username},access_token=rand_token)

    else:
        return respondWithError(403, "Wrong Credentials. Please recheck you Email/Phone and password")


@csrf_exempt
def profile(requests):
    is_true, user = validate_token(requests.META['HTTP_ACCESSTOKEN'])
    if is_true:
        data = {
            "Username": user.user.username,
            "Email":user.user.email,
            "Phone":user.user.phone,
            "Address":user.user.addresses
            }
        return respondWithItem(200, data,access_token=user.access_token)
    else:
        return respondWithError(403, "Access Token is either expired or not valid")
        


def validate_token(token):
    user = UserToken.objects.filter(access_token = token, expires_at__gte = datetime.datetime.now())
    if user.exists():
        return True, user.first()
    else:
        return False, False

def respondWithItem(statusCode, data, access_token=None, is_auth= True):
    response = {}
    response['data'] = data
    response['notification'] = {}    
    response['notification']['hint'] = "Response Sent"
    response['notification']['message'] = "Success"
    response['notification']['code'] = "200"
    response['notification']['type'] = "Success"
    response['notification']['is_auth'] = is_auth    
    
    response = JsonResponse(response, content_type='application/json', status=statusCode)
    response['accessToken'] = access_token
    return response


def respondWithError(statusCode, message, access_token=None, is_auth= True):
    response = {}
    response['data'] = {}
    
    response['notification'] = {}
    response['notification']['hint'] = "Error"
    response['notification']['message'] = message
    response['notification']['code'] = statusCode
    response['notification']['type'] = "Failed"
    response['notification']['is_auth'] = is_auth    
    
    response = JsonResponse(response, content_type='application/json', status=statusCode)
    response['accessToken'] = access_token
    return response
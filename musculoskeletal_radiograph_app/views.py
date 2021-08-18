from django.contrib import admin, messages
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.db.models import Q
import os
import environ
from django.core.paginator import Paginator

from azure.cognitiveservices.vision.customvision.prediction import CustomVisionPredictionClient
from msrest.authentication import ApiKeyCredentials

from musculoskeletal_radiograph_app.Form import CreatePatientForm, CreateRadiograph
from musculoskeletal_radiograph_app.models import Patient, Radiograph


# Create your views here.
def HomePage(request):
    return render(request, "Home/welcome.html")


def GetAllPatient(request):
    if request.method != "POST":
        patient_obj = Patient.objects.all().order_by('-id')
        p = Paginator(patient_obj, 10)

        page = request.GET.get('page')
        patients = p.get_page(page)
        nums = "a" * patients.paginator.num_pages

        return render(request, "home/getall_patient.html", { "patients" : patients, 'nums' : nums })
    else:
        search = request.POST['search']

        if search:
            patient_obj = Patient.objects.filter(Q(id__iexact = search) | Q(sur_name__iexact = search))

            if patient_obj:
                return render(request, "home/getall_patient.html",  { "patients" : patient_obj })
            
            else:
                messages.error(request, "No result found")
                return render(request, "home/getall_patient.html") 
        else:
           return render(request, "home/getall_patient.html") 

            


def CreatePatient(request):
    if request.method != "POST":
        form = CreatePatientForm()
        return render(request, "home/create_patient.html", { "form":form } )
    else:
        form = CreatePatientForm(request.POST,request.FILES)
        if form.is_valid():
            first_name = form.cleaned_data["first_name"]
            sur_name = form.cleaned_data["sur_name"]
            phone_number = form.cleaned_data["phone_number"]
            email_address = form.cleaned_data["email_address"]

            if len(request.FILES) != 0:
                image_url = request.FILES['image_url']
            else:
                image_url =  None

            try:
                patient = Patient.objects.create(
                    first_name = first_name,
                    sur_name = sur_name,
                    phone_number = phone_number,
                    email_address = email_address,
                    image_url = image_url
                )

                messages.success(request, "Successfully Register a New Patient")
                return HttpResponseRedirect(reverse("get_patient", kwargs = { "patient_id": patient.id }))

            except:
                messages.error(request,"Error Occur When Trying to Register New Patient")
                return HttpResponseRedirect(reverse("register_patient"))
        else:
            form = CreatePatientForm()(request.POST, request.FILES)
            return render(request, "home/create_patient.html", { "form": form })


def GetPatient(request, patient_id):
    if request.method!="POST":
        form = CreateRadiograph()
        patient_obj = Patient.objects.get(id = patient_id)
        radiograph = Paginator(Radiograph.objects.filter(patient_id = patient_obj).order_by('-id'), 6)
        page = request.GET.get('page')
        radiographs = radiograph.get_page(page)
        nums = "a" * radiographs.paginator.num_pages

        return render(request, "home/get_patient.html", { "form" : form, "patient" : patient_obj, "radiographs" : radiographs, 'nums' : nums } )
    else:
        form = CreateRadiograph(request.POST,request.FILES)
        if form.is_valid():
            try:
                if len(request.FILES) != 0:
                    image_url = request.FILES['image_url']
                else:
                    image_url =  None
                
                patient_obj = Patient.objects.get(id = patient_id)

                # Get Configuration Settings
                env = environ.Env()
                environ.Env.read_env()

                prediction_endpoint = env('PredictionEndpoint')
                prediction_key = env('PredictionKey')
                project_id = env('ProjectID')
                model_name = env('ModelName')

                # Authenticate a client for the training API
                credentials = ApiKeyCredentials(in_headers = { "Prediction-key": prediction_key })
                prediction_client = CustomVisionPredictionClient(endpoint = prediction_endpoint, credentials = credentials)

                results = prediction_client.classify_image(project_id, model_name, image_url)

                # Loop over each label prediction and print any with probability > 50%
                for prediction in results.predictions:
                    if prediction.probability > 0.5:
                        predictions = prediction.tag_name
                        accuracy = prediction.probability

                radiograph = Radiograph.objects.create(
                    patient_id = patient_obj,
                    image_url = image_url,
                    prediction = predictions,
                    accuracy = accuracy
                )

                messages.success(request,"Musculoskeletal Radiograph Predicted Successfully")
                return HttpResponseRedirect(reverse("get_radiograph", kwargs = { "patient_id" : patient_id, "radiograph_id" : radiograph.id }))
            except:
                messages.error(request,"Failed to Predict Musculoskeletal Radiograph")
                return HttpResponseRedirect(reverse("get_patient", kwargs = { "patient_id" : patient_id }))
        else:
            form = CreateRadiograph(request.POST, request.FILES)
            return render(request, "home/get_patient.html", { "form": form })


def GetRadiograph(request, patient_id, radiograph_id):
    if request.method != "POST":
        patient_obj = Patient.objects.get(id = patient_id)
        radiograph = Radiograph.objects.get(patient_id = patient_obj, id = radiograph_id)
        return render(request, "home/get_radiograph.html", { "patient" : patient_obj, "radiograph" : radiograph } )
import logging
from django.shortcuts import render,HttpResponseRedirect,HttpResponse,reverse
from .models import Salary_Structure
from .forms import SalaryStructureForm
from django.contrib import messages


def salary_structure(request):
    context = Salary_Structure.objects.all()
    return render(request,'work/salary_struct_table.html',{'context':context})

def add(request):
    if request.method=="POST":
        form = SalaryStructureForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse("salary_percentages:salary_structure"))
        else:
            return HttpResponse('You have entered an incorrect data')
    else :
        form = SalaryStructureForm()
        return render(request,'work/salary_struct_form.html',{'form':form})

def upload_csv(request):

    #try:
    data = {}
    if request.method == "GET":
        return render(request, 'work/upload_csv.html', data)
    print(request.FILES)
    csv_file = request.FILES["csv_file"]

    if not csv_file.name.endswith('.csv'):
        messages.error('Sorry!! This file is not csv type')
        return HttpResponseRedirect(reverse("salary_percentages:upload_csv"))

    if csv_file.multiple_chunks():
        messages.error("Uploaded file is too big(%.2f MB) " % (csv_file.size / (1000 * 1000)))
        return HttpResponseRedirect(reverse("salary_percentages:upload_csv"))

    file_data = csv_file.read().decode('utf-8')
    lines = file_data.split("\n")

    for line in lines:

        fields = line.split(",")
        if fields[0] == '':
            break
        data_dict = {}
        print(fields, "fields")
        print(len(fields), "fields")
        print("dfhsjsk")
        data_dict["financial_year"] = fields[0]
        data_dict["hra_percentage"] = fields[1]
        data_dict["dearness_percentage"] = fields[2]
        data_dict["pf_percentage"] = fields[2]
        data_dict["medical_allowance"] = fields[3]
        data_dict["conveyance_allowance"] = fields[4]
        data_dict["washing_allowance"] = fields[5]
        data_dict["other_allowance_percentage"] = fields[6]
        data_dict["max_bonus_percentage"] = fields[7]
        salary_percentages = Salary_Structure(**data_dict)
        if Salary_Structure.objects.filter(financial_year=fields[0]).exists():
            Salary_Structure.objects.filter(financial_year=fields[0]).update(**data_dict)
        else:
            salary_percentages.save()

    # except Exception as e:
    #     logging.getLogger("error_logger").error("Unable to upload file. " + repr(e))
    #
    return HttpResponseRedirect(reverse("salary_percentages:salary_structure"))


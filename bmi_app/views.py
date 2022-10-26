from django.shortcuts import render
from django.http import HttpResponse

from decimal import Decimal, ROUND_HALF_UP, ROUND_HALF_EVEN

from .forms import BMIForm

# bmiと適正体重を計算
def calculation(weight, height):

    height /= 100

    bmi = weight / (height ** 2)
    appropriate_weight = (height ** 2) * 22

    return bmi, appropriate_weight

# 肥満度を言語化
def criterion(bmi):
    degree_of_obesity = ""

    if bmi < 18.5:
        degree_of_obesity = "低体重"
    elif 18.5 <= bmi < 25:
        degree_of_obesity = "普通体重"
    elif 25 <= bmi < 30:
        degree_of_obesity = "肥満（1度）"
    elif 30 <= bmi < 35:
        degree_of_obesity = "肥満（2度）"
    elif 35 <= bmi < 40:
        degree_of_obesity = "肥満（3度）"
    else:
        degree_of_obesity = "肥満（4度）"

    return degree_of_obesity

# 画面に表示
def index(request):

    ctxt = {}

    if request.method == "GET":

        ctxt = {
            'tab_title' : 'あなたのBMIを計算します。',
            'form': BMIForm,
        }

    elif request.method == "POST":
        form = BMIForm(request.POST or None)
        
        if form.is_valid():

            # .cleaned_dataでフォームに入っている情報を取得
            weight = int(form.cleaned_data['weight']) 
            height = int(form.cleaned_data['height'])

            bmi, appropriate_weight = calculation(weight, height)

            # Decimalライブラリを使って四捨五入
            ctxt['bmi'] = Decimal(bmi).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
            ctxt['appropriate_weight'] = Decimal(appropriate_weight).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
            ctxt['form'] = form

            ctxt['criterion'] = criterion(bmi)
            ctxt['appropriate_weight_comparison'] = Decimal(weight - appropriate_weight).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
    
    else:
        return HttpResponse("不正なメソッドです。", status=5)

    return render(request, 'bmi_app/index.html', ctxt)

# bmiについてのページを表示
def about_bmi(request):

    ctxt = {
        'tab_title': 'BMIについて'
    }

    return render(request, 'bmi_app/about_bmi.html', ctxt)

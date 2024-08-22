from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.views import View
from django.urls import reverse
import freecurrencyapi

# Create your views here.
client = freecurrencyapi.Client('fca_live_cMbpMtpIAOEQJxWJpx2xKALmtjgfHjdlxHDZEqcL')

context = {'currencys' : ['EUR', 'USD', 'JPY', 'BGN', 'CZK', 'DKK', 'GBP', 'HUF', 'PLN', 'RON', 'SEK', 'CHF', 'ISK',
                        'NOK', 'HRK', 'RUB', 'TRY', 'AUD', 'BRL', 'CAD', 'CNY', 'HKD', 'IDR', 'ILS', 'INR', 'KRW',
                        'MXN', 'MYR','NZD', 'PHP', 'SGD', 'THB', 'ZAR']}
def calculator(request):

    if request.method == 'POST':
        calselect = request.POST.get('calselect')

        if calselect == 'percent' :
            fund = request.POST.get('fund')
            risk = request.POST.get('risk')
            leverage = request.POST.get('leverage')
            stoploss = request.POST.get('stoploss')

            if fund is None or risk is None or leverage is None or stoploss is None :
                # Handle the error or assign a default value
                error_msg = "fill"
                print(fund,risk,leverage,stoploss)
                return render(request, 'calc/cal.html', {'error_msg': error_msg})
            try:
                # Convert the inputs to float for calculations
                fund = float(fund)
                risk = float(risk)
                leverage = float(leverage)
                stoploss = float(stoploss)

                riskper = risk / 100
                stoplossper = stoploss / 100

                if leverage == 0:
                    position = 0  # Handle division by zero

                position = (fund) * (riskper) / (leverage) / (stoplossper)
            except ValueError:
                # Handle invalid numeric values
                error_msg = "Invalid input. Please enter numeric values."
                return render(request, 'calc/cal.html', {'error_msg': error_msg})

            context.update({'positionsize' : position,})


            return render(request,'calc/cal.html',context)
        else:
            pair1 = request.POST.get('accC')
            pair2 = request.POST.get('pair2')
            result = client.latest(pair1)
            context.update({'position':result,})

            return render(request,'calc/cal.html',context)
    return render(request,'calc/cal.html')
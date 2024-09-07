from django.shortcuts import render
import freecurrencyapi

# Create your views here.
client = freecurrencyapi.Client('fca_live_cMbpMtpIAOEQJxWJpx2xKALmtjgfHjdlxHDZEqcL')

context = {'currencys': ['EUR', 'USD', 'JPY', 'BGN', 'CZK', 'DKK', 'GBP', 'HUF', 'PLN', 'RON', 'SEK', 'CHF', 'ISK',
                         'NOK', 'HRK', 'RUB', 'TRY', 'AUD', 'BRL', 'CAD', 'CNY', 'HKD', 'IDR', 'ILS', 'INR', 'KRW',
                         'MXN', 'MYR', 'NZD', 'PHP', 'SGD', 'THB', 'ZAR']}


def home(request):
    return render(request, 'calc/cal-home.html')

def per(request):
    if request.method == 'POST':
        fund = request.POST.get('fund')
        risk = request.POST.get('risk')
        leverage = request.POST.get('leverage')
        stoploss = request.POST.get('stoploss')

        if fund is None or risk is None or leverage is None or stoploss is None:
            # Handle the error or assign a default value
            print('nul er')
            error_msg = "Please fill all the inputs"
            context.update({'error_msg': error_msg})
            return render(request, 'calc/cal-per.html', context)
        try:
            # Convert the inputs to float for calculations
            fund = float(fund)
            risk = float(risk)
            leverage = float(leverage)
            stoploss = float(stoploss)

            riskper = risk / 100
            stoplossper = stoploss / 100


        except ValueError:
            # Handle invalid numeric values
            print('num er')
            error_msg = "Invalid input. Please enter numeric values."
            context.update({'error_msg': error_msg})
            return render(request, 'calc/cal-per.html', context)



        position = fund * riskper / leverage / stoplossper

        context.update({'positionsize': position})
        return render(request, 'calc/cal-per.html', context)
    else:
        return render(request, 'calc/cal-per.html')

def lots(request):
    if request.method == 'POST':
        acc_c = request.POST.get('accC').upper()
        pair1 = request.POST.get('pair1').upper()
        pair2 = request.POST.get('pair2').upper()
        fund = request.POST.get('fund')
        risk = request.POST.get('risk')
        stop = request.POST.get('stop')
        rou = 2

        if fund is None or risk is None or pair1 is None or pair2 is None or acc_c is None:
            # Handle the error or assign a default value
            error_msg = "Please fill  the inputs"
            context.update({'error_msg': error_msg})
            return render(request, 'calc/cal-lots.html', context)

        if pair1 == 'XAU' or pair1 == 'XAG' and pair2 == 'JPY':
            if pair1 =='XAU':
                lot = 100
            else:
                lot = 1000

            lotpip = 1

        elif pair1 == 'XAU' or pair1 == 'XAG':
            if pair1 =='XAU':
                lot = 100
            else:
                lot = 1000
            lotpip = 10

        elif pair2 == 'JPY':
            lot = 100000
            lotpip = 1000
            rou = 4

        else:
            lot = 100000
            lotpip = 10


        try:
            fund = float(fund)
            risk = float(risk)
            stop = float(stop)
            risk = risk / 100
            at_risk = fund * risk

        except ValueError:
            # Handle invalid numeric values
            error_msg = "Invalid input. Please enter numeric values."
            context.update({'error_msg': error_msg})
            return render(request, 'calc/cal-lots.html', context)

        semiposition = at_risk / stop / lotpip

        req = client.latest(pair2)
        rate = req["data"][acc_c]

        result = semiposition * rate
        if acc_c == "JPY":
            position = result / 100
            position = round(position,rou)
            units = position * lot
            units = round(units, rou)
            at_risk = int(at_risk)
            context.update({'positionsizee': position,
                            'at_risk': at_risk,
                            'units':units})

            return render(request, 'calc/cal-lots.html', context)

        else:
            position = result
            position = round(position, rou)
            units = position * lot
            units = round(units, rou)
            at_risk = int(at_risk)
            context.update({'positionsizee': position,
                            'at_risk': at_risk,
                            'units':units})
            return render(request, 'calc/cal-lots.html', context)
    else:
        return render(request, 'calc/cal-lots.html')

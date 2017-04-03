from flask import Flask, render_template, request
import easypost

app = Flask(__name__)

#render the html pages
@app.route("/index")
def index():
	return render_template("index.html")

@app.route("/parcel")
def parcel():
	return render_template("parcel.html")

#get user input for addresses, parcel size, shipment info, etc. 
@app.route("/addressExtractor", methods=['POST'])
def addressExtractor():
	to_street1 = request.form.get('to_street1')
	to_street2 = request.form.get('to_street2')		
	to_city = request.form.get('to_city')
	to_state = request.form.get('to_state')
	to_zip = request.form.get('to_zip')
	to_country = request.form.get('to_country')
	from_street1 = request.form.get('from_street1')
	from_street2 = request.form.get('from_street2')
	from_city = request.form.get('from_city')
	from_state = request.form.get('from_state')
	from_zip = request.form.get('from_zip')
	from_country = request.form.get('from_country')
	return {'to_street1': to_street1, 'to_street2': to_street2, 'to_city': to_city, 'to_state': to_state, 'to_country': to_country, 'to_zip': to_zip,
		'from_street1': from_street1, 'from_street2': from_street2, 'from_city': from_city, 'from_state': from_state, 'from_country': from_country, 'from_zip': from_zip}

@app.route("/parcelSizeExtractor", methods=['POST'])
def parcelSizeExtractor():
	length = request.form.get('length')
	width = request.form.get('width')
	height = request.form.get('height')
	weight = request.form.get('weight')
	return {'length': lenghth, 'width': width, 'height': height, 'weight': weight}

@app.route("/cusInfoExtractor", methods=['POST'])
def cusInfoExtractor():
	description = request.form.get('description')
	quantity = request.form.get('quantity')
	value = request.form.get('value')
	cusweight = request.form.get('cusweight')
	return {'description': description, 'quantity': quantity, 'value': value, 'cusweight' = weight}

@app.route("/addInfoExtractor", methods=['POST'])
def addInfoExtractor():
	handling = request.form.get('handling')
	insurance = request.form.get('insurance')
	return {'handling': handling, 'insurance': insurance}

# the signature is gathered for validation and consent purpose. 
# Can implement the functionalitylater
@app.route("/signingExtractor", methods=['POST'])
def signingExtractor():
	signature = request.form.get('signature')
	date = request.form.get('date')
	return {'signature': signature, 'date': date}


#################
## EasyPost API##
#################
easypost.api_key = 'qjpxxs99I7GvnzkVGqRTVA'  # Weiwei's test API key
addresses = addressExtractor()
parcelSize = parcelSizeExtractor()
cusInfo = cusInfoExtractor()
addInfo = addInfoExtractor()
signing = signingExtractor()

# create and verify addresses
to_address = easypost.Address.create(
    street1 = addresses['to_street1'],
    street2 = addresses['to_street2'],
    city = addresses['to_city'],
    state = addresses['to_state'],
    zip = addresses['to_zip'],
    country = addresses['to_country'],
)

from_address = easypost.Address.create(
	street1 = addresses['from_street1'],
    street2 = addresses['from_street2'],
    city = addresses['from_city'],
    state = addresses['from_state'],
    zip = addresses['from_zip'],
    country = addresses['from_country'],
)

# create parcel
try:
    parcel = easypost.Parcel.create(
    	length = parcelSize['length'],
    	width = parcelSize['width'],
    	height = parcelSize['height'],
    	weight = parcelSize['weight']
    )
except easypost.Error as e:
    print(str(e))
    if e.param is not None:
        print('Specifically an invalid param: %r' % e.param)

# create customs_info method
customs_item = easypost.CustomsItem.create(
    description = cusInfo['description'],
    quantity = cusInfo['quantity'],
    value = cusInfo['value'],
    cusweight = cusInfo['cusweight']
)

customs_info = easypost.CustomsInfo.create(
    customs_signer = signing['signature'],
    contents_explanation = "",
    eel_pfc='NOEEI 30.37(a)',
    customs_items = [customs_item]
)

# create shipment
shipment = easypost.Shipment.create(
    to_address = to_address,
    from_address = from_address,
    parcel = parcel,
    options = {'handling_instructions': addInfo['handling']},
    customs_info = customs_info
)

# buy postage label
shipment.buy(rate = shipment.rates[0])

print(shipment.tracking_code)
print(shipment.postage_label.label_url)

# create insurance
shipment.insure(amount=addInfo['insurance'])
print(shipment.insurance)


if __name__ == "__main__":
    app.run()
from flask import Flask, render_template, request, flash

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Required for using flash messages

def get_float_field(form, field_name):
    """Helper function to convert form input to float."""
    value = form.get(field_name, '').strip()
    try:
        return float(value) if value else None
    except ValueError:
        return None

@app.route('/', methods=['GET', 'POST'])
def calculate_cost():
    if request.method == 'POST':
        # List of required fields
        fields = [
            'jawarRetail', 'jawarWholeSale', 'dalRetail', 'dalWholeSale', 'saltRetail', 
            'saltWholeSale', 'weightLoss', 'gas', 'ownerLabour', 'electricity', 'transport', 
            'rent', 'maintenance', 'labour', 'extra', 'profitType', 'profit', 
            'packagingCost', 'distributor', 'wholeSeller', 'retailer'
        ]

        # Validate all inputs
        form_data = {}
        for field in fields:
            if field == 'profitType':  # Special case for non-numeric field
                value = request.form.get(field, '').strip()
                if not value:
                    flash("Please fill in all required fields.", "danger")
                    return render_template('index.html', form_data=request.form)
                form_data[field] = value
            else:  # Numeric fields
                value = get_float_field(request.form, field)
                if value is None:
                    flash("Please fill in all required fields.", "danger")
                    return render_template('index.html', form_data=request.form)
                form_data[field] = value

        # Perform calculations
        total_cost = (
            form_data['jawarWholeSale'] + form_data['dalWholeSale'] + form_data['saltWholeSale'] +
            form_data['weightLoss'] + form_data['gas'] + form_data['ownerLabour'] +
            form_data['electricity'] + form_data['transport'] + form_data['rent'] +
            form_data['maintenance'] + form_data['labour'] + form_data['extra'] +
            form_data['packagingCost']
        )

        if form_data['profitType'] == 'fixed':
            profit_amount = form_data['profit']
        elif form_data['profitType'] == 'percentage':
            profit_amount = total_cost * (form_data['profit'] / 100)
        else:
            profit_amount = 0

        mrp = total_cost + profit_amount
        distributor_price = mrp * (1 + form_data['distributor'] / 100)
        wholesaler_price = mrp * (1 + form_data['wholeSeller'] / 100)
        retailer_price = mrp * (1 + form_data['retailer'] / 100)

        # Pass results and form data to the template
        return render_template(
            'index.html', 
            distributor_price=distributor_price,
            wholesaler_price=wholesaler_price,
            retailer_price=retailer_price,
            mrp=mrp,
            form_data=request.form
        )

    # Initial page load
    return render_template(
        'index.html',
        distributor_price=0,
        wholesaler_price=0,
        retailer_price=0,
        mrp=0,
        form_data={}
    )

if __name__ == '__main__':
    app.run(debug=True)


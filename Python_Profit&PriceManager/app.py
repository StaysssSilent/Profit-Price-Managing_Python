from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def calculate_cost():
    if request.method == 'POST':
        # Retrieve form data
        jawar_retail = float(request.form.get('jawarRetail', 0))
        jawar_wholesale = float(request.form.get('jawarWholeSale', 0))
        dal_retail = float(request.form.get('dalRetail', 0))
        dal_wholesale = float(request.form.get('dalWholeSale', 0))
        salt_retail = float(request.form.get('saltRetail', 0))
        salt_wholesale = float(request.form.get('saltWholeSale', 0))
        weight_loss = float(request.form.get('weightLoss', 0))
        gas = float(request.form.get('gas', 0))
        owner_labour = float(request.form.get('ownerLabour', 0))
        electricity = float(request.form.get('electricity', 0))
        transport = float(request.form.get('transport', 0))
        rent = float(request.form.get('rent', 0))
        maintenance = float(request.form.get('maintenance', 0))
        labour = float(request.form.get('labour', 0))
        extra = float(request.form.get('extra', 0))
        profit_type = request.form.get('profitType')
        profit = float(request.form.get('profit', 0))
        packaging_cost = float(request.form.get('packagingCost', 0))
        distributor = float(request.form.get('distributor', 0))
        whole_seller = float(request.form.get('wholeSeller', 0))
        retailer = float(request.form.get('retailer', 0))

        # Perform calculations
        total_cost = jawar_wholesale + dal_wholesale + salt_wholesale + weight_loss + gas + owner_labour + electricity + transport + rent + maintenance + labour + extra + packaging_cost
        
        if profit_type == 'fixed':
            profit_amount = profit
        elif profit_type == 'percentage':
            profit_amount = total_cost * (profit / 100)
        else:
            profit_amount = 0

        mrp = total_cost + profit_amount
        distributor_price = mrp * (1 + distributor / 100)
        wholesaler_price = mrp * (1 + whole_seller / 100)
        retailer_price = mrp * (1 + retailer / 100)

        # Pass results to the template
        return render_template('index.html', 
                               distributor_price=distributor_price,
                               wholesaler_price=wholesaler_price,
                               retailer_price=retailer_price,
                               mrp=mrp)
    else:
        # Initial page load
        return render_template('index.html', 
                               distributor_price=0,
                               wholesaler_price=0,
                               retailer_price=0,
                               mrp=0)

if __name__ == '__main__':
    app.run(debug=True)

from flask import Flask, render_template, request
from waitress import serve

app = Flask(__name__)

def calculate_prices(data):
    try:
        # Get data from form and convert to float, with default values if missing
        jawar_retail = float(data.get('jawarRetail', 0))
        jawar_wholesale = float(data.get('jawarWholeSale', 0))
        dal_retail = float(data.get('dalRetail', 0))
        dal_wholesale = float(data.get('dalWholeSale', 0))
        salt_retail = float(data.get('saltRetail', 0))
        salt_wholesale = float(data.get('saltWholeSale', 0))
        weight_loss = float(data.get('weightLoss', 0))
        gas = float(data.get('gas', 0))
        owner_labour = float(data.get('ownerLabour', 0))
        electricity = float(data.get('electricity', 0))
        transport = float(data.get('transport', 0))
        rent = float(data.get('rent', 0))
        maintenance = float(data.get('maintenance', 0))
        labour = float(data.get('labour', 0))
        extra = float(data.get('extra', 0))
        packaging_cost = float(data.get('packagingCost', 0))
        
        # Default profit type and profit
        profit_type = data.get('profitType', 'select')
        profit = float(data.get('profit', 0))
        
        # Percentages
        distributor_percent = float(data.get('distributor', 0))
        wholesaler_percent = float(data.get('wholeSeller', 0))
        retailer_percent = float(data.get('retailer', 0))

        # Check if profit_type is valid
        if profit_type not in ["fixed", "percentage"]:
            raise ValueError("Invalid profit type selected")

        # Calculate total cost
        total_cost = (jawar_wholesale + dal_wholesale + salt_wholesale + weight_loss +
                      gas + owner_labour + electricity + transport + rent + maintenance +
                      labour + extra + packaging_cost)
        
        # Apply profit based on type
        if profit_type == "fixed":
            total_cost += profit
        elif profit_type == "percentage":
            total_cost += (total_cost * profit / 100)
        
        # Calculate price distribution
        distributor_price = total_cost * (1 + distributor_percent / 100)
        wholesaler_price = total_cost * (1 + wholesaler_percent / 100)
        retailer_price = total_cost * (1 + retailer_percent / 100)
        
        # MRP Calculation (Maximum of distributor, wholesaler, retailer prices)
        mrp = max(distributor_price, wholesaler_price, retailer_price)
        
        return distributor_price, wholesaler_price, retailer_price, mrp
    
    except ValueError as e:
        # Handle invalid input data (e.g., non-numeric input)
        return str(e), None, None, None

@app.route("/", methods=["GET", "POST"])
def index():
    distributor_price = wholesaler_price = retailer_price = mrp = None
    error_message = None
    
    if request.method == "POST":
        data = request.form
        distributor_price, wholesaler_price, retailer_price, mrp = calculate_prices(data)
        
        # If there's an error, capture the error message
        if isinstance(distributor_price, str):  # This indicates an error message
            error_message = distributor_price
            distributor_price = wholesaler_price = retailer_price = mrp = None

    return render_template(
        'index.html', 
        distributor_price=distributor_price, 
        wholesaler_price=wholesaler_price, 
        retailer_price=retailer_price, 
        mrp=mrp,
        error_message=error_message
    )

if __name__ == "__main__":
    # Use waitress to serve the app
    serve(app, host='0.0.0.0', port=8000)

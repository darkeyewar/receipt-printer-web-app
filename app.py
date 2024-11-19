from flask import Flask, render_template, request, jsonify
from datetime import datetime
import os
import inflect

app = Flask(__name__)

# Configure static and template paths explicitly
app.static_folder = 'static'
app.template_folder = 'templates'

# Folder to save receipts
RECEIPTS_FOLDER = 'receipts'
if not os.path.exists(RECEIPTS_FOLDER):
    os.makedirs(RECEIPTS_FOLDER)

# Helper to convert numbers to words
inflector = inflect.engine()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/create-receipt', methods=['POST'])
def create_receipt():
    try:
        data = request.json
        customer_name = data['customerName']
        items = data['items']
        
        receipt_number = int(datetime.now().timestamp() * 1000)
        date_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        total = sum(item['quantity'] * item['price'] for item in items)
        total_in_words = inflector.number_to_words(total, andword='') + " only"

        # Save text version
        receipt_content = f"""
Ali Lace Shop
Shop Number 69, Shah Alam Market
Mob: 0306-1632806
Receipt No: {receipt_number}
Date: {date_time}
Customer Name: {customer_name}

S.No    Particulars    Quantity    Price    Amount
"""
        for idx, item in enumerate(items, start=1):
            receipt_content += f"{idx}\t{item['name']}\t{item['quantity']}\t{item['price']}\t{item['quantity'] * item['price']}\n"

        receipt_content += f"""
Total: {total}
Amount in Words: {total_in_words}
Thank you for shopping with us!
"""

        # Save text receipt
        receipt_path = os.path.join(RECEIPTS_FOLDER, f"receipt_{receipt_number}.txt")
        with open(receipt_path, 'w') as file:
            file.write(receipt_content)

        # Render HTML template
        html_content = render_template('receipt_template.html',
                                     receipt_number=receipt_number,
                                     date_time=date_time,
                                     customer_name=customer_name,
                                     items=items,
                                     total=total,
                                     total_in_words=total_in_words)

        return jsonify({
            'message': 'Receipt generated successfully',
            'html_content': html_content
        })

    except Exception as e:
        return jsonify({
            'error': str(e)
        }), 500

@app.errorhandler(404)
def not_found_error(error):
    return jsonify({'error': 'Not Found'}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Internal Server Error'}), 500

if __name__ == '__main__':
    # Ensure the application can be accessed from your network
    app.run(host='0.0.0.0', port=5000, debug=True)
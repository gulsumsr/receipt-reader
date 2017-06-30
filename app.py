import os
import numpy as np
from PIL import Image
from flask import Flask, render_template, jsonify, request
from preprocess import preprocess_image
from read_receipt_image import read_receipt
import io
import matplotlib
matplotlib.use('agg')
import matplotlib.pyplot as plt


# curl -F "file=@/home/brian/Pictures/lena.jpg" http://0.0.0.0:5000/
# curl -F "file=@../data/receipt.jpg" http://0.0.0.0:5000/

def im_to_json(im):
    """Here's where the magic happens"""
    items = ['sierra nevada stout', 'lagunitas ipa', 'founders centennial']
    prices = [5.50, 6.50, 7.50]
    subtotal = sum(prices)
    tax = subtotal * 0.07
    total = subtotal + tax
    bill_dict = {
        'items': [{'name': item, 'price': price, 'quantity': 1} 
                  for item, price in zip(items, prices)],
        'subtotal': subtotal,
        'tax': tax,
        'total': total
    }

    # preprocessed_im = preprocess_image(im)


    # # with open(fn, 'rb') as f:
    # #     im_data = f.read()
    # buf = io.BytesIO()
    # plt.imsave(buf, preprocessed_im)
    # im_data = buf.getvalue()

    # bill_dict = read_receipt(im_data)

    return jsonify(bill_dict)


app = Flask(__name__)

@app.route("/", methods=["POST", "GET"])
def home():
    if 'file' in request.files:
        im = np.asarray(Image.open(request.files['file']), dtype=np.uint8)
        return im_to_json(im)
    else:
        # return im_to_json(None)
        return 'Request should have an image file attached'


if __name__ == '__main__':
    app.run(debug=True)

from flask import Blueprint, jsonify, request, render_template
from ..Web3.tonapi import TonAPI

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/JettonView/<address>', methods=['GET'])
def get_details_info_jetton(address):
    data = TonAPI().get_gecko_jetton_info(address)
    return render_template('jetton.html', data=data[0])

@auth_bp.route('/getPage/', methods=['GET'])
def get_page_jetton():
    result = TonAPI().get_pool()

    return render_template('home.html', data=result)

@auth_bp.route('/getPage/sort=<sort>', methods=['GET'])
def get_page_and_sort_jetton(sort):
    result = TonAPI().get_pool(sort=sort)

    return render_template('home.html', data=result)
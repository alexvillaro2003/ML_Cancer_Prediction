import streamlit as st
import pickle
import numpy as np
import pdfplumber
import re

def load_model():

    with open('../models/DecisionTree_RandomizedSearchCV/model_DTCRSCV.pkl', 'rb') as file:
        model = pickle.load(file)
    return model



def calculo_bmi(altura, peso):

    bmi = peso / (altura ** 2)
    return bmi

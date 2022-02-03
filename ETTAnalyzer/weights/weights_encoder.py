import argparse
import numpy as np 
from matplotlib import pyplot as plt 

''' 
2 February 2022 
Abraham Tishelman-Charny 

Simplified version of WRS encoding script to derive FENIX encoded weights. 

Original code by William Richard Smith (2019) here: https://gitlab.cern.ch/cms-ecal-dpg/ecall1algooptimization/-/blob/942db3e6cac733e9684a42e7d2b314572ed14129/PileupMC/weights_encoder.py

This script simulate the loss of precision in decimal weights given by the encoding. 
'''

#Encoded weights back to decimals to look at differences
def encoded_to_decimal(enc_weights_not_corrected):
    back_weights = [0]*5
    for count, encw in enumerate(enc_weights_not_corrected):
        if encw > 63:
            encw = -(128 -encw)
        back_weights[count] = encw/64
    
    return back_weights

def decimal_to_encoded(weights):
    enc_weights_not_corrected = [0]*5
    for count, w in enumerate(weights):
        if w >0:
            encodedw = w*64
            encodedw = int(round(encodedw))
            enc_weights_not_corrected[count] = encodedw
        else:
            encodedw = w*64
            encodedw = abs(encodedw)
            encodedw = int(round(encodedw))
            encodedw = 128 - encodedw
            enc_weights_not_corrected[count] = encodedw
            
    return enc_weights_not_corrected

if (__name__ == '__main__'): 
	# DecimalWeights = [0.265625, -0.71875, 0.0, -0.546875, 1.0] # min_delta = 2.5 
	# EncodedWeights = decimal_to_encoded(DecimalWeights)
	# print("Encoded weights:",EncodedWeights)
	# print("Sum:",np.sum(EncodedWeights)) # [17 82 128 93 64]

	encoded_vals = []
	decimal_vals = []

	for i in range(-400, 400):
		weight = [int(i)]
		decimal = encoded_to_decimal(weight)
		print("Encoded, Decimal: %s, %s"%(weight[0], decimal[0])) 
		encoded_vals.append(weight[0])
		decimal_vals.append(decimal[0])

	fig, ax = plt.subplots()
	plt.plot(encoded_vals, decimal_vals)
	plt.savefig("weights.png")
	plt.close()

	print("DONE")


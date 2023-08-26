from collections import defaultdict
from splitwise import Splitwise


arr = [['idiot1', 0], ['idiot2', 0], ['idiot3', 0]]
balance_dict = {}

def calculate(amt, paidFirst, *ppl):
    noOfppl = len(ppl) + 1  # Add 1 for the person who paid (paidFirst)
    payMe = round(amt / noOfppl, 2)
    if paidFirst not in balance_dict:
        arr[paidFirst] = 0
    balance_dict[paidFirst] = amt - payMe
    for person in ppl:
        if person not in balance_dict:
            balance_dict[person] = 0
        balance_dict[person] -= payMe
    return balance_dict
	

def calculate1(amt, paidFirst, *ppl):
    noOfppl = len(ppl) + 1  # Add 1 for the person who paid (paidFirst)
    payMe = round(amt / noOfppl, 2)
    
    for idiot in arr:  # Assuming arr is defined outside the function
        if idiot[0] in ppl:
            idiot[1] -= payMe
        if idiot[0] == paidFirst:
            idiot[1] += amt - payMe
    
    return arr  # Assuming arr is defined outside the function


from collections import defaultdict



arr = [['idiot1', 0], ['idiot2', 0], ['idiot3', 0]]
balance_dict = {}

# def calculate(amt, paidFirst, *ppl):
#     noOfppl = len(ppl) + 1  # Add 1 for the person who paid (paidFirst)
#     payMe = round(amt / noOfppl, 2)
#     if paidFirst not in balance_dict:
#         arr[paidFirst] = 0
#     balance_dict[paidFirst] = amt - payMe
#     for person in ppl:
#         if person not in balance_dict:
#             balance_dict[person] = 0
#         balance_dict[person] -= payMe
#     return balance_dict

def payMe(amt, you, me):
    for ppl in arr: 
        if ppl[0] == you:
            ppl[1] -= amt
        if ppl[0] == me:
            ppl[1] += amt
    return amt
        
	

def calculate1(amt, paidFirst, *ppl):
    noOfppl = len(ppl) + 1  # Add 1 for the person who paid (paidFirst)
    payMe = round(amt / noOfppl, 2)
    
    for idiot in arr:  # Assuming arr is defined outside the function
        if idiot[0] in ppl:
            idiot[1] -= payMe
        if idiot[0] == paidFirst:
            idiot[1] += amt - payMe
    return arr  # Assuming arr is defined outside the function


def settleUp():
    biggestDebt = min(arr, key = lambda x: x[1])
    print(biggestDebt)
    for ppl in arr:
        if ppl[0] == biggestDebt[0]:
            continue
        if ppl[1] < 0:
            print(ppl[0] + " pays " + biggestDebt[0] + " $" + str(abs(ppl[1])))
        elif ppl[1] > 0:
            print(biggestDebt[0] + " pays " + ppl[0] + " $" + str(ppl[1]))
    return arr





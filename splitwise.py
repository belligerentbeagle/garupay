arr = [['i1', 0], ['i2', 0], ['i3', 0]]
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

    for i in arr:  # Assuming arr is defined outside the function
        if i[0] in ppl:
            i[1] -= payMe
        if i[0] == paidFirst:
            i[1] += amt - payMe
    return arr  # Assuming arr is defined outside the function


def settleUp(arr):
    biggestDebt = min(arr, key=lambda x: x[1])
    pos = max(arr, key=lambda x: x[1])
    print(biggestDebt)
    output = []
    for ppl in arr:
        if ppl[0] == biggestDebt[0] or ppl[0] == pos[0]:
            continue

        if ppl[1] < 0:
            print(ppl[0] + " gets from " + biggestDebt[0] + " $" + str(abs(ppl[1])))
            # output.append([biggestDebt[0], ppl[0], abs(ppl[1])])
            output.append([ppl[0], pos[0], abs(ppl[1])])
        elif ppl[1] > 0:
            print(biggestDebt[0] + " gets from " + ppl[0] + " $" + str(ppl[1]))
            # output.append([ppl[0], biggestDebt[0], abs(ppl[1])])
            output.append([biggestDebt[0], ppl[0], abs(ppl[1])])
    return output

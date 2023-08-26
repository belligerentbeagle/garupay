from collections import defaultdict
import heapq
from decimal import Decimal, ROUND_HALF_UP

table = defaultdict(Decimal)

def calculate(amt, paidFirst, *ppl):
    noOfppl = len(ppl) + 1  # Add 1 for the person who paid (paidFirst)
    payMe = Decimal(amt) / Decimal(noOfppl)
    table[paidFirst] += Decimal(amt)
    for person in ppl:
        table[person] -= payMe

def settleUp():
    transactions = []
    for person, balance in table.items():
        heapq.heappush(transactions, (abs(balance), person))

    while len(transactions) > 1:
        min_debt, debtor = heapq.heappop(transactions)
        max_credit, creditor = heapq.heappop(transactions)

        settling_amount = min(min_debt, max_credit)
        print(f"{debtor} owes {settling_amount:.2f} to {creditor}")

        remaining_debt = min_debt - settling_amount
        remaining_credit = max_credit - settling_amount

        if remaining_debt > 0:
            heapq.heappush(transactions, (remaining_debt, debtor))
        if remaining_credit > 0:
            heapq.heappush(transactions, (remaining_credit, creditor))

# Example usage
calculate(5, "idiot1", "idiot2", "idiot3")
settleUp()

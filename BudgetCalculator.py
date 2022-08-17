class Category:
    def __init__(self, category):
        self.category = category
        self.ledger = []
        self.__balance = 0

    def get_balance(self):
        return self.__balance

    def deposit(self, amount, description=''):
        self.__balance += amount
        self.ledger.append({
            'amount': amount,
            'description': description
        })

    def withdraw(self, amount, description=''):
        if self.__balance >= amount:
            self.ledger.append({
                'amount': amount*(-1),
                'description': description
            })
            self.__balance -= amount
            return True
        else:
            return False

    def transfer(self, amount, dest):
        if self.withdraw(amount, "Transfer to {}".format(dest.category)):
            dest.deposit(amount, "Transfer from {}".format(self.category))
            return True
        else:
            return False

    def check_funds(self, amount):
        if self.__balance >= amount:
            return True
        return False

    def __repr__(self):
        header = self.category.center(30, "*") + "\n"
        ledger = ""
        for item in self.ledger:
            # format description and amount
            line_description = "{:<23}".format(item["description"])
            line_amount = "{:>7.2f}".format(item["amount"])
            # Truncate ledger description and amount to 23 and 7 characters respectively
            ledger += "{}{}\n".format(line_description[:23], line_amount[:7])
        total = "Total: {:.2f}".format(self.__balance)
        return header + ledger + total


def create_spend_chart(my_list=[]):
    spent_amounts = []
    # Get total spent in each category
    for category in my_list:
        spent = 0
        for item in category.ledger:
            if item["amount"] < 0:
                spent += abs(item["amount"])
        spent_amounts.append(round(spent, 2))

    # Calculate percentage rounded down to the nearest 10
    total = round(sum(spent_amounts), 2)
    spent_percentage = list(map(lambda amount: int(
        (((amount / total) * 10) // 1) * 10), spent_amounts))

    # Create the bar chart substrings
    header = "Percentage spent by category\n"

    chart = ""
    for value in reversed(range(0, 101, 10)):
        chart += str(value).rjust(3) + '|'
        for percent in spent_percentage:
            if percent >= value:
                chart += " o "
            else:
                chart += "   "
        chart += " \n"

    footer = "    " + "-" * ((3 * len(my_list)) + 1) + "\n"
    descriptions = list(map(lambda category: category.category, my_list))
    max_length = max(map(lambda description: len(description), descriptions))
    descriptions = list(
        map(lambda description: description.ljust(max_length), descriptions))
    for x in zip(*descriptions):
        footer += "    " + "".join(map(lambda s: s.center(3), x)) + " \n"

    return (header + chart + footer).rstrip("\n")


c = Category('Casa')
t = Category('t')
c.deposit(200, 'MYdescription')
c.deposit(300, 'another')
c.withdraw(100, 'cacat')
t.deposit(200)
c.transfer(100, t)


print(c.ledger)
print(c.get_balance())

print('---')
print(t.ledger)
print(t.get_balance())
print(c)

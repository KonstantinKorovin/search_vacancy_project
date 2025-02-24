from abc import ABC, abstractmethod


class Order:

    def __init__(self):
        self.items = []
        self.quantities = []
        self.prices = []
        self.status = "open"

    def add_item(self, name, quantity, price):
        self.items.append(name)
        self.quantities.append(quantity)
        self.prices.append(price)

    def total_price(self):
        return sum(quantities * prices for quantities, prices in zip(self.quantities, self.prices))


class Authorizer(ABC):

    @abstractmethod
    def is_authorized(self):
        pass


class AuthorizerSms(Authorizer):

    def __init__(self):
        self.authorized = False

    def verify_code(self, code):
        print(f'Авторизация SMS кода {code}')
        self.authorized = True

    def is_authorized(self):
        return self.authorized


class AuthorizerRobot(Authorizer):

    def __init__(self):
        self.authorized = False

    def not_a_robot(self):
        self.authorized = True

    def is_authorized(self):
        return self.authorized

class Pay(ABC):

    @abstractmethod
    def pay(self, order):
        pass


class PaySms(Pay):

    @abstractmethod
    def pay(self, order):
        pass


class Debit(PaySms):

    def __init__(self, security_code, authorizer: Authorizer):
        self.security_code = security_code
        self.authorizer = authorizer

    def pay(self, order):
        if not self.authorizer.is_authorized():
            raise Exception('Не авторизован')
        print("Обработка дебетового типа платежа")
        print(f"Проверка кода безопасности: {self.security_code}")
        order.status = 'paid'


class Credit(Pay):

    def __init__(self, security_code):
        self.security_code = security_code

    def pay(self, order):
        print("Обработка кредитного типа платежа")
        print(f"Проверка кода безопасности: {self.security_code}")
        order.status = 'paid'


class PayPal(PaySms):

    def __init__(self, user_email, authorizer: Authorizer):
        self.user_email = user_email
        self.authorizer = authorizer

    def pay(self, order):
        if not self.authorizer.is_authorized():
            raise Exception('Не авторизован')
        print("Обработка платежа типа PayPal")
        print(f"Отправка чека на почту: {self.user_email}")
        order.status = 'paid'

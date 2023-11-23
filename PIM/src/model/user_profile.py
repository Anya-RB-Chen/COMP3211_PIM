
class UserProfile:
    # __count = 0

    def __init__(self, name, password, email="", description=""):
        # self.id = UserProfile.__count
        # UserProfile.__count += 1

        self.__name = name
        self.__password = password
        self.__email = email
        self.__description = description

    def check_password(self, password):
        return self.__password == password

    def set_password(self, new_password):
        self.__password = new_password

    def get_password(self):
        return self.__password

    def get_name(self):
        return self.__name

    def __str__(self):
        return f"Name: {self.__name}\nEmail: {self.__email}\nDescription: {self.__description}"

    def __eq__(self, other):
        return isinstance(other, UserProfile) and self.get_name() == other.get_name()

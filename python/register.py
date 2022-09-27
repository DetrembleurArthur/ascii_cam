

def get_contact(name):
    with open("contacts.txt", "rt") as file:
        for contact in file:
            contact = contact.replace("\n", "")
            contact = contact.split(':')
            if contact[0] == name:
                print("GET " + str(contact))
                return contact


if __name__ == "__main__":
    name = input("contact name: ")
    address = input("contact address")

    with open("contacts.txt", "a") as file:
        file.write(f"{name}:{address}:{port}\n")

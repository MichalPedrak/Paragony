# Struktura danych dla paragonu:
class DataPoint:
    def __init__(self, name, x):
        self.article = name
        self.price = x

    def display_info(self):
        print(f"Article: {self.article}")
        print(f"Price: ({self.price})")

class Recipe:
    def __init__(self, name, date1):
        self.name = name
        self.date = date1
        self.data_points = []

    def add_data_point(self, name, x):
        new_data_point = DataPoint(name, x)
        self.data_points.append(new_data_point)

    def display_info(self):
        print(f"Recipe name: {self.name}")
        print(f"Recipe date: {self.date}")
        for data_point in self.data_points:
            data_point.display_info()

#Dodawanie nowego paragonu:
def add_data():
    print("Podaj nazwe paragonu:\n")
    name = input()
    print("Podaj date paragonu(DD/MM/RR):\n")
    date = input()
    new_recipe = Recipe(name, date)
    print("Podaj nazwe produktu oraz jego cene (q-zakoncz):\n")
    while (True):
        n1 = input()

        if n1 == "q":
            break

        x = float(input())
        new_recipe.add_data_point(n1, x)
    return new_recipe

#Podział kosztu artykułu na ilość osób
def div(price, people):
    return price/people

#Zapisywanie paragonu do pliku txt:
def write_recipe(rec):
    file_name = rec.name + ".txt"
    f = open(file_name, "w")
    f.write("Nazwa paragonu: " + rec.name)
    f.write("\nData paragonu: " + rec.date)
    f.write("\nArtykul:        Cena:")
    for i in range(0, len(rec.data_points)):
        f.write("\n")
        f.write("   " + rec.data_points[i].article + "          " + str(rec.data_points[i].price))
    f.close()

########################################################################################

recipe = add_data()
#print(recipe.data_points[1].article + " " + str(recipe.data_points[1].price))

write_recipe(recipe)
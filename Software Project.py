# classes
class ClothingItem:
    def __init__(self, name, price, size, colour, brand):
        self.name = name
        self.price = price
        self.size = size
        self.colour = colour
        self.brand = brand

    def get_info(self):
        return f"{self.brand} {self.name} (Size: {self.size}, Color: {self.colour}) - ${self.price:.2f}"


class Shirt(ClothingItem):
    def __init__(self, price, size, colour, brand, sleeve_length, fit_type):
        super().__init__("Shirt", price, size, colour, brand)
        self.sleeve_length = sleeve_length
        self.fit_type = fit_type

    def get_info(self):
        return f"{super().get_info()} | Sleeve: {self.sleeve_length}, Fit: {self.fit_type}"


class Pant(ClothingItem):
    def __init__(self, price, size, colour, brand, waist_size, inseam_length, fit_type):
        super().__init__("Pant", price, size, colour, brand)
        self.waist_size = waist_size
        self.inseam_length = inseam_length
        self.fit_type = fit_type

    def get_info(self):
        return f"{super().get_info()} | Waist: {self.waist_size}, Inseam: {self.inseam_length}, Fit: {self.fit_type}"


class Jacket(ClothingItem):
    def __init__(self, price, size, colour, brand, material, insulation_type):
        super().__init__("Jacket", price, size, colour, brand)
        self.material = material
        self.insulation_type = insulation_type

    def get_info(self):
        return f"{super().get_info()} | Material: {self.material}, Insulation: {self.insulation_type}"


class Shoe(ClothingItem):
    def __init__(self, price, size, colour, brand, material, style_type):
        super().__init__("Shoe", price, size, colour, brand)
        self.material = material
        self.style_type = style_type

    def get_info(self):
        return f"{super().get_info()} | Material: {self.material}, Style: {self.style_type}"


# invetory loads
def load_inventory(filename):
    shirt_inventory = []
    pant_inventory = []
    jacket_inventory = []
    shoe_inventory = []

    with open(filename, 'r') as file:
        for line in file:
            parts = line.strip().split(',')
            if not parts or len(parts) < 6:
                continue

            item_type = parts[0].strip().title()
            try:
                if item_type == "Shirt":
                    price, size, colour, brand, sleeve, fit = parts[1:]
                    shirt_inventory.append(Shirt(float(price), size, colour, brand, sleeve, fit))

                elif item_type == "Pant":
                    price, size, colour, brand, waist, inseam, fit = parts[1:]
                    pant_inventory.append(Pant(float(price), size, colour, brand, waist, inseam, fit))

                elif item_type == "Jacket":
                    price, size, colour, brand, material, insulation = parts[1:]
                    jacket_inventory.append(Jacket(float(price), size, colour, brand, material, insulation))

                elif item_type == "Shoe":
                    price, size, colour, brand, material, style = parts[1:]
                    shoe_inventory.append(Shoe(float(price), size, colour, brand, material, style))
            except ValueError:
                print(f"Error processing line: {line.strip()}")

    return shirt_inventory, pant_inventory, jacket_inventory, shoe_inventory


# matching tings
def matches_general(item, brand, size, colour, budget):
    return (
        item.brand.lower() == brand.lower() and
        str(item.size).lower() == str(size).lower() and
        item.colour.lower() == colour.lower() and
        item.price <= budget
    )


def suggest_similar(items, brand, size, colour, budget):
    scored = []
    for item in items:
        score = 0
        if item.brand.lower() == brand.lower(): score += 1
        if str(item.size).lower() == str(size).lower(): score += 1
        if item.colour.lower() == colour.lower(): score += 1
        if item.price <= budget: score += 1
        scored.append((score, item))

    scored.sort(reverse=True, key=lambda x: x[0])
    return [item for score, item in scored if score > 0][:3]


# Main program
def main():
    print("Welcome to the Clothing Store!\n")

    shirts, pants, jackets, shoes = load_inventory("clothes.txt")
    cart = []

    while True:
        item_type = input("\nWhat would you like to shop for? (Shirt, Pant, Jacket, Shoe, View Cart, Purchase Cart): ").strip().title()
        if item_type == "Purchase Cart":
            break
        elif item_type == "View Cart":
            print("\n Your Cart:")
            if not cart:
                print("Your cart is empty.")
            else:
                total = 0
                for item in cart:
                    print(f"- {item.get_info()}")
                    total += item.price
                print(f"Total: ${total:.2f}")
            continue
        elif item_type not in ["Shirt", "Pant", "Jacket", "Shoe"]:
            print("Invalid option.")
            continue

        brand = input("Brand: ").strip()
        size = input("Size: ").strip()
        colour = input("Colour: ").strip()
        try:
            budget = float(input("Budget ($): "))
        except ValueError:
            print("Invalid budget.")
            continue

        matches = []
        inventory = []

        if item_type == "Shirt":
            sleeve = input("Sleeve length (Short/Long): ").strip().title()
            fit = input("Fit type (Slim/Regular/Oversized): ").strip().title()
            inventory = shirts
            for shirt in shirts:
                if (matches_general(shirt, brand, size, colour, budget) and
                    shirt.sleeve_length.lower() == sleeve.lower() and
                    shirt.fit_type.lower() == fit.lower()):
                    matches.append(shirt)

        elif item_type == "Pant":
            waist = input("Waist size: ").strip()
            inseam = input("Inseam length: ").strip()
            fit = input("Fit type (Slim/Regular): ").strip().title()
            inventory = pants
            for pant in pants:
                if (matches_general(pant, brand, size, colour, budget) and
                    pant.waist_size == waist and
                    pant.inseam_length == inseam and
                    pant.fit_type.lower() == fit.lower()):
                    matches.append(pant)

        elif item_type == "Jacket":
            material = input("Material: ").strip()
            insulation = input("Insulation: ").strip()
            inventory = jackets
            for jacket in jackets:
                if (matches_general(jacket, brand, size, colour, budget) and
                    jacket.material.lower() == material.lower() and
                    jacket.insulation_type.lower() == insulation.lower()):
                    matches.append(jacket)

        elif item_type == "Shoe":
            material = input("Material: ").strip()
            style = input("Style: ").strip()
            inventory = shoes
            for shoe in shoes:
                if (matches_general(shoe, brand, size, colour, budget) and
                    shoe.material.lower() == material.lower() and
                    shoe.style_type.lower() == style.lower()):
                    matches.append(shoe)

        # Show results
        if matches:
            print("\n Exact Matches Found:")
            for i, item in enumerate(matches, start=1):
                print(f"{i}. {item.get_info()}")

            choice = input("Add one of these to your cart? (Enter number or N): ").strip()
            if choice.isdigit():
                index = int(choice) - 1
                if 0 <= index < len(matches):
                    cart.append(matches[index])
                    print("Added to cart.")
        else:
            print("\n No exact matches. Here are some close matches:")
            suggestions = suggest_similar(inventory, brand, size, colour, budget)
            if suggestions:
                for i, item in enumerate(suggestions, start=1):
                    print(f"{i}. {item.get_info()}")
                choice = input("Add one of these to your cart? (Enter number or N): ").strip()
                if choice.isdigit():
                    index = int(choice) - 1
                    if 0 <= index < len(suggestions):
                        cart.append(suggestions[index])
                        print("Added to cart.")
            else:
                print("No similar items available.")

    # Final cart display
    print("\n️ Final Cart Summary:")
    if not cart:
        print("Your cart is empty.")
    else:
        total = 0
        for item in cart:
            print(f"- {item.get_info()}")
            total += item.price
        print(f" Total Price: ${total:.2f}")


# Run the Program
if __name__ == "__main__":
    main()


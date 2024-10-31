from PIL import Image
import numpy as np
import pandas as pd

"""
    image: Obraz w trybie skali szarości (Pillow Image)
    threshold: Wartość progowa (0-255), która decyduje, czy piksel jest czarny (0) czy biały(255)
"""
def apply_threshold(image, threshold):

    binary_image = Image.new('L', image.size)
    pixels = binary_image.load()

    for i in range(image.size[0]):
        for j in range(image.size[1]):
            pixel_value = image.getpixel((i, j))
            pixels[i, j] = 255 if pixel_value > threshold else 0

    return binary_image

# funkcja do zmiany jasności obrazu
# factor: Współczynnik jasności (wartość > 0, gdzie 1 oznacza brak zmiany)
# factor > 1 - obraz jaśniejszy, factor < 1 - obraz ciemniejszy
def adjust_brightness(image, factor):

    if factor <= 0:
        raise ValueError("Współczynnik jasności musi być większy od 0.")

    enhanced_image = Image.new('L', image.size)
    pixels = enhanced_image.load()

    for i in range(image.size[0]):
        for j in range(image.size[1]):
            pixel_value = image.getpixel((i, j))
            new_value = min(int(pixel_value * factor), 255)
            pixels[i, j] = new_value

    return enhanced_image

def handle_edges(i, j, width, height):
    if i < 0 or i >= width or j < 0 or j >= height:
        return 0
    return None

def erode(image, radius=1):
    width, height = image.size
    result = Image.new('L', image.size)
    pixels = result.load()
    input_pixels = image.load()

    for i in range(width):
        for j in range(height):
            max_value = 0
            for x in range(-radius, radius + 1):
                for y in range(-radius, radius + 1):
                    # Sprawdzamy krawędzie
                    if (edge_value := handle_edges(i + x, j + y, width, height)) is not None:
                        continue  # Zignoruj ten piksel, jeśli jest poza granicami
                    max_value = max(max_value, input_pixels[i + x, j + y])
            pixels[i, j] = max_value

    return result

def dilate(image, radius=1):
    width, height = image.size
    result = Image.new('L', image.size)
    pixels = result.load()
    input_pixels = image.load()

    for i in range(width):
        for j in range(height):
            min_value = 255
            for x in range(-radius, radius + 1):
                for y in range(-radius, radius + 1):
                    if (edge_value := handle_edges(i + x, j + y, width, height)) is not None:
                        continue
                    min_value = min(min_value, input_pixels[i + x, j + y])
            pixels[i, j] = min_value

    return result
#otwarcie morfologiczne
def open_image(image, radius=1):
    eroded = erode(image, radius)
    opened = dilate(eroded, radius)
    return opened
#domknięcie morfologiczne
def close_image(image, radius=1):
    dilated = dilate(image, radius)
    closed = erode(dilated, radius)
    return closed
#splot z podaną maską
def convolve(image, mask):
    width, height = image.size
    mask_size = len(mask)
    offset = mask_size // 2
    result = Image.new('L', image.size)
    pixels = result.load()
    input_pixels = image.load()

    for i in range(width):
        for j in range(height):
            value = 0
            for x in range(mask_size):
                for y in range(mask_size):
                    if (edge_value := handle_edges(i + x - offset, j + y - offset, width, height)) is not None:
                        continue
                    value += input_pixels[i + x - offset, j + y - offset] * mask[x][y]
            pixels[i, j] = min(max(int(value), 0), 255)

    return result
#Splot z maską o danym promieniu
def convolve_with_radius(image, mask, radius):
    mask_size = 2 * radius + 1
    return convolve(image, mask)

def load_mask_fixed_radius_csv(file_path, expected_radius=1):

    mask = pd.read_csv(file_path, header=None, dtype=np.float64).to_numpy()
    mask_size = mask.shape[0]
    actual_radius = (mask_size - 1) // 2

    if actual_radius == expected_radius:
        return mask
    else:
        print(f"Maska z pliku '{file_path}' ma promień {actual_radius}, a oczekiwany to {expected_radius}.")
        return None


def load_mask_variable_radius_csv(file_path):
    mask = pd.read_csv(file_path, header=None, dtype=np.float64).to_numpy()  # Wczytaj maskę jako numpy array
    mask_size = mask.shape[0]
    radius = (mask_size - 1) // 2

    return mask, radius

#     gauss_mask_path = 'gauss.csv'
#     gauss_mask, radius = load_mask_variable_radius_csv(gauss_mask_path)
#     convolved_image_gauss = convolve_with_radius(image, gauss_mask, radius)
#     convolved_image_gauss.save('gauss.bmp')
#     print(f"Zapisano obraz po zastosowaniu splotu z maską gaussa.")
def main():
    image_file_path = ('obraz.bmp')
    image = Image.open(image_file_path).convert('L')  # Wczytaj w skali szarości
    threshold_value = 128
    binary_image = apply_threshold(image, threshold_value)
    binary_image.save('zbinaryzowany_obraz.bmp')

    while True:
        print("\nWybierz operację:")
        print("1. Dylatacja i erozja")
        print("2. Otwarcie i domknięcie morfologiczne")
        print("3. Splot z maską o promieniu 1")
        print("4. Splot z maską o promieniu r")
        print("5. Wyjście")

        choice = input("Wybierz numer operacji: ")

        match choice:
            case '1':
                radius = int(input("Podaj promień sąsiedztwa (domyślnie 1): ") or 1)
                dilated_image = dilate(binary_image, radius)
                eroded_image = erode(binary_image, radius)
                dilated_image.save('dylatacja.bmp')
                eroded_image.save('erozja.bmp')
                print("Zapisano obrazy po dylatacji i erozji.")

            case '2':
                radius = int(input("Podaj promień sąsiedztwa (domyślnie 1): ") or 1)
                opened_image = open_image(binary_image, radius)
                closed_image = close_image(binary_image, radius)
                opened_image.save('otwarcie.bmp')
                closed_image.save('domkniecie.bmp')
                print("Zapisano obrazy po otwarciu i domknięciu morfologicznym.")

            case '3':
                mask_file_path = 'maska_staly_promien.csv'
                mask = load_mask_fixed_radius_csv(mask_file_path, expected_radius=1)
                if mask is not None:
                    convolved_image = convolve(binary_image, mask)
                    convolved_image.save('splot_staly_promien.bmp')
                    print("Zapisano obraz po zastosowaniu splotu z maską o stałym promieniu.")

            case '4':
                mask_file_path = 'maska_zmienny_promien.csv'
                mask, radius = load_mask_variable_radius_csv(mask_file_path)
                convolved_image = convolve_with_radius(binary_image, mask, radius)
                convolved_image.save('splot_zmienny_promien.bmp')
                print(f"Zapisano obraz po zastosowaniu splotu z maską o promieniu {radius}.")

            case '5':
                print("Koniec programu.")
                break

            case _:
                print("Nieprawidłowy wybór. Spróbuj ponownie.")


if __name__ == "__main__":
    main()
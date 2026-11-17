import mahotas

def load_image(path):
    image = mahotas.imread(path)
    return image
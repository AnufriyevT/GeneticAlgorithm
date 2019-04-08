from PIL import Image, ImageDraw
import random

image = Image.open("cow100.jpg")
width = image.size[0]
height = image.size[1]
pix = image.load()
colors = image.getcolors(width * height)
colors = [a[1] for a in colors]
population = 80 #amount of individuals
generations = 10000 #amount of generations
freq_mutation = 1000 

# Taking values of every pixel from target picture
original = []
for i in range(height):
    posy = []
    for j in range(width):
        posx = [pix[i,j][0], pix[i,j][1], pix[i,j][2]]
        posy.append(posx)
    original.append(posy)

# Creating population
def make_population(number):
    pop = []
    while number >= 0:
        number -= 1
        i_population = []
        for i in range(0, height):
            popy = []
            for j in range(0, width):
                r = random.randint(0, len(colors) - 1)
                popx = [colors[r][0], colors[r][1], colors[r][2]]
                popy.append(popx)
            i_population.append(popy)
        pop.append([i_population, 0])
        print("Generating population number: " + str(population - number - 1))
    return pop


#Fitness-Function
def getFitnessScore(pop, orig):
    score = 0
    for i in range(len(pop)):
        for j in range(len(pop[i])):
            score += abs(pop[i][j][0] - orig[i][j][0]) + abs(pop[i][j][1] - orig[i][j][1]) + abs(
                pop[i][j][2] - orig[i][j][2])
    return score

#Crossover with mutation
def makeChild(father, mother):
    child = []
    for i in range(len(father)):
        childy = []
        for j in range(len(mother)):
            childx = []
            mutation = random.randint(0, freq_mutation)
            if mutation == 0:
                r = random.randint(0, len(colors) - 1)
                childx = [colors[r][0], colors[r][1], colors[r][2]]
            else:
                r = random.randint(0, 1)
                if r == 0:
                    childx  = father[i][j]
                else:
                    childx  = mother[i][j]
            childy.append(childx)
        child.append(childy)
    return [child, 0]


gen = 0

populations = make_population(population)

while gen < generations:

    for i in range(len(populations)):
        score = getFitnessScore(populations[i][0], original)
        populations[i][1] = score
    populations.sort(key=lambda a: a[1])
    pos = len(populations) // 2
    while pos < len(populations):
        father = random.randint(0, population // 2)
        mother = random.randint(0, population // 2)
        populations[pos] = makeChild(populations[father][0], populations[mother][0])
        populations[pos][1] = 0
        pos += 1

    if gen % 100 == 0:
        draw = ImageDraw.Draw(image)
        for i in range(0, height):
            for j in range(0, width):
                red = populations[0][0][i][j][0]
                green = populations[0][0][i][j][1]
                blue = populations[0][0][i][j][2]
                draw.point((i, j), (red, green, blue))
        ans = "picture" + str(gen) + ".jpg"
        print("Generation: " + str(gen))
        image.save(ans, "JPEG")
    gen = gen + 1

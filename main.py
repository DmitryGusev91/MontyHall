import random
def mpProblem(outfile, print):
    l1 = ["goat", "car", "goat"]
    random.shuffle(l1)
    if print:
        outfile.write("\npartitions: " + l1[0]
                      + " " + l1[1] + " " + l1[2])
    l2 = [0, 1, 2]
    ci = l1.index("car")
    if print:
        outfile.write("\nthe car is behind partition number: "
                      + str(ci))
    fc = random.randint(0, 2)
    if print:
        outfile.write("\nfirst choice: " + str(l1[fc])
                      +  "   index: " + str(fc))
    l3 = []
    for i in range(len(l1)):
        if i != ci:
            l3.append(i)
    s = ""
    for x in l3:
      s = s + " " + str(x)
      if x != fc:
          k = x
    if print:
        outfile.write("\nindices of goats partition: " + s)
    if print:
        outfile.write("\nindex of exposed goat partition: "
                      + str(k))
    for i in range(len(l2)):
        if l2[i] != fc and l2[i] != k:
            sc = i
            break
    if print:
        outfile.write("\nsecond choice: " + str(l1[sc])
                      + "  index of second choice: " + str(sc)+"\n\n")
    return ci, fc, sc, k

def main(n, print):
    outfile = open("mhResults.txt", 'w')
    wins = 0
    losses = 0
    for i in range(n):
        if print:
            outfile.write(("\ngame number: " + str(i + 1)))
        ci, fc, sc, k = mpProblem(outfile, print)
        if ci == sc:
            wins += 1
        elif fc == ci:
            losses += 1

    outfile.write("\n\nnumber of games: "
          + "{0:,d}".format(i+1)
          + "\nnumber of wins   because of choice change: "
          + "{0:,d}".format(wins)
          + "\nnumber of losses because of choice change: "
          + "{0:,d}".format(losses))

    outfile.close()


main(10, True)

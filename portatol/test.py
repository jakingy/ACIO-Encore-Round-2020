from os import listdir, system
from os.path import isfile, join

ADD_APPROXIMATE_ANSWER = True

system("g++ sol-full.cpp -o sol -O2")
if ADD_APPROXIMATE_ANSWER:
    system("g++ sol-new.cpp -o sol-new -O2")
    system("g++ sol-sub1.cpp -o sol-sub1 -O2")
    system("g++ sol-floats.cpp -o sol-floats -O2")
    system("g++ sol-doubles.cpp -o sol-doubles -O2")
    system("g++ sol-approx.cpp -o sol-approx -O2")

files = [f for f in listdir("cases/input") if isfile(join("cases/input", f))]
for f in files:
    if f.endswith('.in'):
        of = f.split('.')[0] + '.out'
        print("Generating", of)
        system("sol < %s > %s" % (join("cases/input", f), join("cases/output", of)))
        if ADD_APPROXIMATE_ANSWER:
            system("sol-new < %s >> %s" % (join("cases/input", f), join("cases/output", of)))
            system("sol-sub1 < %s >> %s" % (join("cases/input", f), join("cases/output", of)))
            system("sol-floats < %s >> %s" % (join("cases/input", f), join("cases/output", of)))
            system("sol-doubles < %s >> %s" % (join("cases/input", f), join("cases/output", of)))
            system("sol-approx < %s >> %s" % (join("cases/input", f), join("cases/output", of)))
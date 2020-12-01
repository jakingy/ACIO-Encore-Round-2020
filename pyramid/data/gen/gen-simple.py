import random
#random.seed(19877529)

MAXH = 17
MAXQ = 100000

case_file = open("case.in","w")
H = 7#random.randint(1,MAXH)
case_file.write("%d\n" % H)
N = 2**H-1
for i in range(N-1):
    ai = random.random()
    bi = random.random()
    ai, bi = sorted([ai,bi])
    case_file.write("%f %f\n" % (ai,bi))
Q = random.randint(1,MAXQ)
case_file.write("%d\n" % Q)
for i in range(Q):
    X = random.randint(1, N)
    R = random.random()
    case_file.write("%d %f\n" % (X,R))
case_file.close()

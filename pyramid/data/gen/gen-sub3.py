import random
random.seed(19877529)

MAXH = 17
MAXQ = 100000

def rep_random(lo, hi, n):
    ret = 1
    for i in range(n):
        ret *= random.random() * (hi-lo) + lo
    return ret

def sorted_bis(H):
    return reversed(sorted([random.random() for i in range(2**H-2)]))

def random_queries(H, Q):
    N = 2**H-1
    qs = []
    for i in range(Q):
        X = random.randint(1, N)
        R = random.random()
        qs.append((X,R))
    return qs

def stratified_queries(H, Q):
    qs = []
    for i in range(Q):
        d = random.randint(0, H-1)
        X = random.randrange(2**d, 2**(d+1))
        R = random.random()
        qs.append((X,R))
    return qs

Q = 100000
H_SMALL = list(range(4, 7))
H_MED = list(range(9, 13))
H_LARGE = list(range(15, 18))

def write_case(fname, H, Q, bis, qs):
    print("Generating", fname)
    with open(fname + '.in', "w") as case_file:
        case_file.write("%d\n" % H)
        for bi in bis:
            case_file.write("%f %f\n" % (0,bi))
        case_file.write("%d\n" % Q)
        random.shuffle(qs)
        for X,R in qs:
            case_file.write("%d %f\n" % (X,R))

#small
H = random.choice(H_SMALL)
bis = sorted_bis(H)
qs = random_queries(H, Q)
write_case("small-random-qs-sub3", H, Q, bis, qs)

H = random.choice(H_SMALL)
bis = sorted_bis(H)
qs = stratified_queries(H, Q)
write_case("small-stratified-qs-sub3", H, Q, bis, qs)

#med
H = random.choice(H_MED)
bis = sorted_bis(H)
qs = random_queries(H, Q)
write_case("med-random-qs-sub3", H, Q, bis, qs)

H = random.choice(H_MED)
bis = sorted_bis(H)
qs = stratified_queries(H, Q)
write_case("med-stratified-qs-sub3", H, Q, bis, qs)

#large
H = random.choice(H_LARGE)
bis = sorted_bis(H)
qs = random_queries(H, Q)
write_case("large-random-qs-sub3", H, Q, bis, qs)

H = random.choice(H_LARGE)
bis = sorted_bis(H)
qs = stratified_queries(H, Q)
write_case("large-stratified-qs-sub3", H, Q, bis, qs)
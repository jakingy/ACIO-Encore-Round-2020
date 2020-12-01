import random
random.seed(19877529)

MAXH = 17
MAXQ = 100000

def random_bis(H):
    return [random.random() for i in range(2**H-2)]

def rep_random(lo, hi, n):
    ret = 1
    for i in range(n):
        ret *= random.random() * (hi-lo) + lo
    return ret
 
# bis at the top are likely to be higher
def top_biased_bis(H, off_bias):
    N = 2**H-1
    vs = []
    for i in range(N-1):
        bi = random.random()
        vs.append((bi * rep_random(1 - off_bias, 1 + off_bias, 2),bi))
    vs.sort()
    vs.reverse()
    return [v[1] for v in vs]    

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

# small, medium and large of each of the following:
# random bis random queries
# random bis stratified queries
# top biased bis random queries
# top biased bis stratified queries
# top biased bis med stratified queries
# top biased bis lesser stratified queries
# sub3 already catered for fully sorted bis

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

Q = 100000

#small
H = random.choice(H_SMALL)
bis = random_bis(H)
qs = random_queries(H, Q)
write_case("small-random-bis-random-qs-sub4", H, Q, bis, qs)

H = random.choice(H_SMALL)
bis = random_bis(H)
qs = stratified_queries(H, Q)
write_case("small-random-bis-stratified-qs-sub4", H, Q, bis, qs)

H = random.choice(H_SMALL)
bis = top_biased_bis(H, 0.1)
qs = random_queries(H, Q)
write_case("small-top-biased-bis-random-qs-sub4", H, Q, bis, qs)

H = random.choice(H_SMALL)
bis = top_biased_bis(H, 0.05)
qs = stratified_queries(H, Q)
write_case("small-top-biased-bis-stratified-qs-1-sub4", H, Q, bis, qs)

H = random.choice(H_SMALL)
bis = top_biased_bis(H, 0.3)
qs = stratified_queries(H, Q)
write_case("small-top-biased-bis-stratified-qs-2-sub4", H, Q, bis, qs)

H = random.choice(H_SMALL)
bis = top_biased_bis(H, 0.7)
qs = stratified_queries(H, Q)
write_case("small-top-biased-bis-stratified-qs-3-sub4", H, Q, bis, qs)

#med
H = random.choice(H_MED)
bis = random_bis(H)
qs = random_queries(H, Q)
write_case("med-random-bis-random-qs-sub4", H, Q, bis, qs)

H = random.choice(H_MED)
bis = random_bis(H)
qs = stratified_queries(H, Q)
write_case("med-random-bis-stratified-qs-sub4", H, Q, bis, qs)

H = random.choice(H_MED)
bis = top_biased_bis(H, 0.1)
qs = random_queries(H, Q)
write_case("med-top-biased-bis-random-qs-sub4", H, Q, bis, qs)

H = random.choice(H_MED)
bis = top_biased_bis(H, 0.05)
qs = stratified_queries(H, Q)
write_case("med-top-biased-bis-stratified-qs-1-sub4", H, Q, bis, qs)

H = random.choice(H_MED)
bis = top_biased_bis(H, 0.3)
qs = stratified_queries(H, Q)
write_case("med-top-biased-bis-stratified-qs-2-sub4", H, Q, bis, qs)

H = random.choice(H_MED)
bis = top_biased_bis(H, 0.7)
qs = stratified_queries(H, Q)
write_case("med-top-biased-bis-stratified-qs-3-sub4", H, Q, bis, qs)

#large
H = random.choice(H_LARGE)
bis = random_bis(H)
qs = random_queries(H, Q)
write_case("large-random-bis-random-qs-sub4", H, Q, bis, qs)

H = random.choice(H_LARGE)
bis = random_bis(H)
qs = stratified_queries(H, Q)
write_case("large-random-bis-stratified-qs-sub4", H, Q, bis, qs)

H = random.choice(H_LARGE)
bis = top_biased_bis(H, 0.1)
qs = random_queries(H, Q)
write_case("large-top-biased-bis-random-qs-sub4", H, Q, bis, qs)

H = random.choice(H_LARGE)
bis = top_biased_bis(H, 0.05)
qs = stratified_queries(H, Q)
write_case("large-top-biased-bis-stratified-qs-1-sub4", H, Q, bis, qs)

H = random.choice(H_LARGE)
bis = top_biased_bis(H, 0.3)
qs = stratified_queries(H, Q)
write_case("large-top-biased-bis-stratified-qs-2-sub4", H, Q, bis, qs)

H = random.choice(H_LARGE)
bis = top_biased_bis(H, 0.7)
qs = stratified_queries(H, Q)
write_case("large-top-biased-bis-stratified-qs-3-sub4", H, Q, bis, qs)

H = random.choice(H_LARGE)
bis = top_biased_bis(H, 0.99)
qs = stratified_queries(H, Q)
write_case("large-top-biased-bis-stratified-qs-4-sub4", H, Q, bis, qs)




import random
random.seed(19877529)

MAXH = 17
MAXQ = 100000

def no_overlapping_ranges(H):
    rng = sorted([random.random()for i in range(2**(H+1)-4)])
    return [(rng[i],rng[i+1]) for i in range(0,len(rng),2)]

def random_ranges(H, lo = 0, hi = 1):
    ranges = []
    for i in range(2**H-2):
        ai = random.random() * (hi-lo) + lo
        bi = random.random() * (hi-lo) + lo
        ai,bi = min(ai,bi),max(ai,bi)
        ranges.append((ai,bi))
    return ranges

def random_sized_ranges(H, lo = 0, hi = 1):
    ranges = []
    for i in range(2**H-2):
        sz = random.random() * (hi-lo) + lo
        ai = random.random() * (1-sz)
        bi = ai + sz
        ranges.append((ai,bi))
    return ranges
 
# generate n random points, each range must contain at least one point.
def point_based_ranges(H, n = 1):
    pts = [random.random()for _ in range(n)]
    ranges = []
    while len(ranges) < 2**H-2:
        ai = random.random()
        bi = random.random()
        ai,bi = min(ai,bi),max(ai,bi)
        for pt in pts:
            if ai <= pt and pt <= bi:
                ranges.append((ai,bi))
                break
    return ranges

def rep_random(lo, hi, n):
    ret = 1
    for i in range(n):
        ret *= random.random() * (hi-lo) + lo
    return ret

def slight_shuffle(L, n, level):
    for i in range(n):
        i = random.randrange(0,len(L))
        mv = random.randrange(max(i-int(len(L)*rep_random(0, 1, level)),0),min(i+int(len(L)*rep_random(0, 1, level))+1,len(L)))
        L[i],L[mv] = L[mv],L[i]

# the upper ranges are usually bigger
def top_biased_ranges(H, off_bias):
    ranges = []
    nranges = 2**H-2
    sz_sort = []
    for i in range(nranges):
        bi = random.random()
        sz_sort.append((bi * rep_random(1 - off_bias, 1 + off_bias, 2),bi))
    sz_sort.sort()
    sz_sort.reverse()
    szs = [sz[1] for sz in sz_sort]  
    for i in range(nranges):
        sz = szs[i]
        ai = random.random() * (1-sz)
        bi = ai + sz
        ranges.append((ai,bi))
    return ranges

def patitioning_ranges(H):
    ranges = [(),(0,1)]
    for i in range(2,2**H):
        par = i//2
        if i%2:
            ranges.append((ranges[i-1][1],ranges[par][1]))
        else:
            split = random.random() * (ranges[par][1]-ranges[par][0]) + ranges[par][0]
            ranges.append((ranges[par][0],split))
    return ranges[2:]

# biases ai to be lower than bi and bottom ai to be less than top ai and top bi to be more than
def ai_bi_split(H):
    N = 2**H-1
    rs = [(1,i) for i in range(N-1)] + [(0,i) for i in range(N-1)]
    slight_shuffle(rs, N, 3)
    rng = sorted([random.random() for _ in range(2*N-2)])
    ranges = [[0,0] for _ in range(N-1)]
    for tp,i in rs:
        ranges[i][tp] = rng.pop()
    return [tuple(sorted(r)) for r in ranges]
        
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

def query_all_at_point(H, Q, pt):
    qs = []
    for i in range(Q):
        qs.append(((i-1)%(2**H-1)+1, pt))
    return qs

def query_root(H, Q):
    N = 2**H-1
    qs = []
    for i in range(Q):
        R = random.random()
        qs.append((1,R))
    return qs

def sub2_queries(H, Q):
    qs = []
    for i in range(Q):
        X = random.randrange(2**(H-2), 2**(H-1))
        R = random.random()
        qs.append((X,R))
    return qs

H_SMALL = list(range(4, 7))
H_MED = list(range(9, 13))
H_LARGE = [17]#list(range(15, 18))

def write_case(fname, H, Q, ranges, qs):
    print("Generating", fname)
    with open(fname + '.in', "w") as case_file:
        case_file.write("%d\n" % H)
        for r in ranges:
            case_file.write("%f %f\n" % r)
        case_file.write("%d\n" % Q)
        random.shuffle(qs)
        for q in qs:
            case_file.write("%d %f\n" % q)

Q = 100000

#tiny
H = 1
ranges = []
qs = random_queries(H, Q)
write_case("minH", H, Q, ranges, qs)

H = 2
ranges = random_ranges(H)
qs = random_queries(H, Q)
write_case("tiny2-sub5", H, Q, ranges, qs)

H = 2
ranges = random_ranges(H, 0.05, 0.06)
qs = random_queries(H, Q)
write_case("tiny2-small-ranges-sub5", H, Q, ranges, qs)

H = 3
ranges = random_ranges(H)
qs = random_queries(H, Q)
write_case("tiny3-sub5", H, Q, ranges, qs)

H = 3
ranges = random_ranges(H, 0.999, 1.0)
qs = random_queries(H, Q)
write_case("tiny3-small-ranges-sub5", H, Q, ranges, qs)

#small
H = random.choice(H_SMALL)
ranges = random_ranges(H, random.random() * .5, random.random() * .5 + .5)
qs = random_queries(H, Q)
write_case("small-random-ranges-random-qs-sub5", H, Q, ranges, qs)

H = random.choice(H_SMALL)
ranges = random_ranges(H)
qs = stratified_queries(H, Q)
write_case("small-random-ranges-stratified-qs-sub5", H, Q, ranges, qs)

H = random.choice(H_SMALL)
ranges = ai_bi_split(H)
qs = stratified_queries(H, Q)
write_case("small-ai-bi-split-stratified-qs-sub5", H, Q, ranges, qs)

H = random.choice(H_SMALL)
ranges = no_overlapping_ranges(H)
qs = random_queries(H, Q)
write_case("small-no-overlapping-ranges-random-qs-sub5", H, Q, ranges, qs)

H = random.choice(H_SMALL)
ranges = no_overlapping_ranges(H)
qs = stratified_queries(H, Q)
write_case("small-no-overlapping-ranges-stratified-qs-sub5", H, Q, ranges, qs)

H = random.choice(H_SMALL)
ranges = point_based_ranges(H)
qs = random_queries(H, Q)
write_case("small-point-based-ranges-random-qs-sub5", H, Q, ranges, qs)

H = random.choice(H_SMALL)
ranges = point_based_ranges(H)
qs = stratified_queries(H, Q)
write_case("small-point-based-ranges-stratified-qs-sub5", H, Q, ranges, qs)

H = random.choice(H_SMALL)
ranges = point_based_ranges(H, 2)
qs = random_queries(H, Q)
write_case("small-2-point-based-ranges-random-qs-sub5", H, Q, ranges, qs)

H = random.choice(H_SMALL)
ranges = point_based_ranges(H, 2)
qs = stratified_queries(H, Q)
write_case("small-2-point-based-ranges-stratified-qs-sub5", H, Q, ranges, qs)

H = random.choice(H_SMALL)
ranges = point_based_ranges(H, 4)
qs = random_queries(H, Q)
write_case("small-4-point-based-ranges-random-qs-sub5", H, Q, ranges, qs)

H = random.choice(H_SMALL)
ranges = point_based_ranges(H, 4)
qs = stratified_queries(H, Q)
write_case("small-4-point-based-ranges-stratified-qs-sub5", H, Q, ranges, qs)

H = random.choice(H_SMALL)
ranges = top_biased_ranges(H, 0.08)
qs = random_queries(H, Q)
write_case("small-top-biased-ranges-random-qs-sub5", H, Q, ranges, qs)

H = random.choice(H_SMALL)
ranges = top_biased_ranges(H, 0.08)
qs = stratified_queries(H, Q)
write_case("small-top-biased-ranges-stratified-qs-sub5", H, Q, ranges, qs)

H = random.choice(H_SMALL)
ranges = top_biased_ranges(H, 0.3)
qs = random_queries(H, Q)
write_case("small-top-biased-ranges2-random-qs-sub5", H, Q, ranges, qs)

H = random.choice(H_SMALL)
ranges = top_biased_ranges(H, 0.3)
qs = stratified_queries(H, Q)
write_case("small-top-biased-ranges2-stratified-qs-sub5", H, Q, ranges, qs)

H = random.choice(H_SMALL)
ranges = top_biased_ranges(H, 0.7)
qs = random_queries(H, Q)
write_case("small-top-biased-ranges3-random-qs-sub5", H, Q, ranges, qs)

H = random.choice(H_SMALL)
ranges = top_biased_ranges(H, 0.7)
qs = stratified_queries(H, Q)
write_case("small-top-biased-ranges3-stratified-qs-sub5", H, Q, ranges, qs)

H = random.choice(H_SMALL)
ranges = patitioning_ranges(H)
qs = random_queries(H, Q)
write_case("small-patitioning-ranges-random-qs-sub5", H, Q, ranges, qs)

H = random.choice(H_SMALL)
ranges = patitioning_ranges(H)
qs = stratified_queries(H, Q)
write_case("small-patitioning-ranges-stratified-qs-sub5", H, Q, ranges, qs)

#med
H = random.choice(H_MED)
ranges = random_ranges(H, random.random() * .5, random.random() * .5 + .5)
qs = random_queries(H, Q)
write_case("med-random-ranges-random-qs-sub5", H, Q, ranges, qs)

H = random.choice(H_MED)
ranges = random_ranges(H)
qs = stratified_queries(H, Q)
write_case("med-random-ranges-stratified-qs-sub5", H, Q, ranges, qs)

H = random.choice(H_MED)
ranges = no_overlapping_ranges(H)
qs = random_queries(H, Q)
write_case("med-no-overlapping-ranges-random-qs-sub5", H, Q, ranges, qs)

H = random.choice(H_MED)
ranges = no_overlapping_ranges(H)
qs = stratified_queries(H, Q)
write_case("med-no-overlapping-ranges-stratified-qs-sub5", H, Q, ranges, qs)

H = random.choice(H_MED)
ranges = point_based_ranges(H)
qs = random_queries(H, Q)
write_case("med-point-based-ranges-random-qs-sub5", H, Q, ranges, qs)

H = random.choice(H_MED)
ranges = point_based_ranges(H)
qs = stratified_queries(H, Q)
write_case("med-point-based-ranges-stratified-qs-sub5", H, Q, ranges, qs)

H = random.choice(H_MED)
ranges = point_based_ranges(H, 2)
qs = random_queries(H, Q)
write_case("med-2-point-based-ranges-random-qs-sub5", H, Q, ranges, qs)

H = random.choice(H_MED)
ranges = point_based_ranges(H, 2)
qs = stratified_queries(H, Q)
write_case("med-2-point-based-ranges-stratified-qs-sub5", H, Q, ranges, qs)

H = random.choice(H_MED)
ranges = point_based_ranges(H, 4)
qs = random_queries(H, Q)
write_case("med-4-point-based-ranges-random-qs-sub5", H, Q, ranges, qs)

H = random.choice(H_MED)
ranges = point_based_ranges(H, 4)
qs = stratified_queries(H, Q)
write_case("med-4-point-based-ranges-stratified-qs-sub5", H, Q, ranges, qs)

H = random.choice(H_MED)
ranges = top_biased_ranges(H, 0.08)
qs = random_queries(H, Q)
write_case("med-top-biased-ranges-random-qs-sub5", H, Q, ranges, qs)

H = random.choice(H_MED)
ranges = top_biased_ranges(H, 0.08)
qs = stratified_queries(H, Q)
write_case("med-top-biased-ranges-stratified-qs-sub5", H, Q, ranges, qs)

H = random.choice(H_MED)
ranges = top_biased_ranges(H, 0.3)
qs = random_queries(H, Q)
write_case("med-top-biased-ranges2-random-qs-sub5", H, Q, ranges, qs)

H = random.choice(H_MED)
ranges = top_biased_ranges(H, 0.3)
qs = stratified_queries(H, Q)
write_case("med-top-biased-ranges2-stratified-qs-sub5", H, Q, ranges, qs)

H = random.choice(H_MED)
ranges = top_biased_ranges(H, 0.7)
qs = random_queries(H, Q)
write_case("med-top-biased-ranges3-random-qs-sub5", H, Q, ranges, qs)

H = random.choice(H_MED)
ranges = top_biased_ranges(H, 0.7)
qs = stratified_queries(H, Q)
write_case("med-top-biased-ranges3-stratified-qs-sub5", H, Q, ranges, qs)

H = random.choice(H_MED)
ranges = patitioning_ranges(H)
qs = random_queries(H, Q)
write_case("med-patitioning-ranges-random-qs-sub5", H, Q, ranges, qs)

H = random.choice(H_MED)
ranges = patitioning_ranges(H)
qs = stratified_queries(H, Q)
write_case("med-patitioning-ranges-stratified-qs-sub5", H, Q, ranges, qs)

H = random.choice(H_MED)
ranges = ai_bi_split(H)
qs = stratified_queries(H, Q)
write_case("med-ai-bi-split-ranges-stratified-qs-sub5", H, Q, ranges, qs)

#large
H = random.choice(H_LARGE)
ranges = random_ranges(H, random.random() * .5, random.random() * .5 + .5)
qs = random_queries(H, Q)
write_case("large-random-ranges-random-qs-sub5", H, Q, ranges, qs)

H = random.choice(H_LARGE)
ranges = random_ranges(H)
qs = stratified_queries(H, Q)
write_case("large-random-ranges-stratified-qs-sub5", H, Q, ranges, qs)

H = random.choice(H_LARGE)
ranges = random_ranges(H)
qs = query_root(H, Q)
write_case("large-random-ranges-root-qs-sub5", H, Q, ranges, qs)

H = random.choice(H_LARGE)
ranges = no_overlapping_ranges(H)
qs = random_queries(H, Q)
write_case("large-no-overlapping-ranges-random-qs-sub5", H, Q, ranges, qs)

H = random.choice(H_LARGE)
ranges = no_overlapping_ranges(H)
qs = stratified_queries(H, Q)
write_case("large-no-overlapping-ranges-stratified-qs-sub5", H, Q, ranges, qs)

H = random.choice(H_LARGE)
ranges = point_based_ranges(H)
qs = random_queries(H, Q)
write_case("large-point-based-ranges-random-qs-sub5", H, Q, ranges, qs)

H = random.choice(H_LARGE)
ranges = point_based_ranges(H)
qs = stratified_queries(H, Q)
write_case("large-point-based-ranges-stratified-qs-sub5", H, Q, ranges, qs)

H = random.choice(H_LARGE)
ranges = point_based_ranges(H)
qs = query_root(H, Q)
write_case("large-point-based-ranges-root-qs-sub5", H, Q, ranges, qs)

H = random.choice(H_LARGE)
ranges = point_based_ranges(H)
qs = random_queries(H, Q)
write_case("large-point-based-ranges2-random-qs-sub5", H, Q, ranges, qs)

H = random.choice(H_LARGE)
ranges = point_based_ranges(H)
qs = stratified_queries(H, Q)
write_case("large-point-based-ranges2-stratified-qs-sub5", H, Q, ranges, qs)

H = random.choice(H_LARGE)
ranges = point_based_ranges(H, 2)
qs = random_queries(H, Q)
write_case("large-2-point-based-ranges-random-qs-sub5", H, Q, ranges, qs)

H = random.choice(H_LARGE)
ranges = point_based_ranges(H, 2)
qs = stratified_queries(H, Q)
write_case("large-2-point-based-ranges-stratified-qs-sub5", H, Q, ranges, qs)

H = random.choice(H_LARGE)
ranges = point_based_ranges(H, 2)
qs = random_queries(H, Q)
write_case("large-2-point-based-ranges2-random-qs-sub5", H, Q, ranges, qs)

H = random.choice(H_LARGE)
ranges = point_based_ranges(H, 2)
qs = stratified_queries(H, Q)
write_case("large-2-point-based-ranges2-stratified-qs-sub5", H, Q, ranges, qs)

H = random.choice(H_LARGE)
ranges = point_based_ranges(H, 4)
qs = random_queries(H, Q)
write_case("large-4-point-based-ranges-random-qs-sub5", H, Q, ranges, qs)

H = random.choice(H_LARGE)
ranges = point_based_ranges(H, 4)
qs = stratified_queries(H, Q)
write_case("large-4-point-based-ranges-stratified-qs-sub5", H, Q, ranges, qs)

H = random.choice(H_LARGE)
ranges = point_based_ranges(H, 8)
qs = random_queries(H, Q)
write_case("large-8-point-based-ranges-random-qs-sub5", H, Q, ranges, qs)

H = random.choice(H_LARGE)
ranges = point_based_ranges(H, 8)
qs = stratified_queries(H, Q)
write_case("large-8-point-based-ranges-stratified-qs-sub5", H, Q, ranges, qs)

H = random.choice(H_LARGE)
ranges = point_based_ranges(H, 16)
qs = random_queries(H, Q)
write_case("large-16-point-based-ranges-random-qs-sub5", H, Q, ranges, qs)

H = random.choice(H_LARGE)
ranges = point_based_ranges(H, 16)
qs = stratified_queries(H, Q)
write_case("large-16-point-based-ranges-stratified-qs-sub5", H, Q, ranges, qs)

H = random.choice(H_LARGE)
ranges = top_biased_ranges(H, 0.05)
qs = random_queries(H, Q)
write_case("large-top-biased-ranges-random-qs-sub5", H, Q, ranges, qs)

H = random.choice(H_LARGE)
ranges = top_biased_ranges(H, 0.05)
qs = stratified_queries(H, Q)
write_case("large-top-biased-ranges-stratified-qs-sub5", H, Q, ranges, qs)

H = random.choice(H_LARGE)
ranges = top_biased_ranges(H, 0.2)
qs = random_queries(H, Q)
write_case("large-top-biased-ranges2-random-qs-sub5", H, Q, ranges, qs)

H = random.choice(H_LARGE)
ranges = top_biased_ranges(H, 0.2)
qs = stratified_queries(H, Q)
write_case("large-top-biased-ranges2-stratified-qs-sub5", H, Q, ranges, qs)

H = random.choice(H_LARGE)
ranges = top_biased_ranges(H, 0.4)
qs = random_queries(H, Q)
write_case("large-top-biased-ranges3-random-qs-sub5", H, Q, ranges, qs)

H = random.choice(H_LARGE)
ranges = top_biased_ranges(H, 0.4)
qs = stratified_queries(H, Q)
write_case("large-top-biased-ranges3-stratified-qs-sub5", H, Q, ranges, qs)

H = random.choice(H_LARGE)
ranges = top_biased_ranges(H, 0.75)
qs = random_queries(H, Q)
write_case("large-top-biased-ranges4-random-qs-sub5", H, Q, ranges, qs)

H = random.choice(H_LARGE)
ranges = top_biased_ranges(H, 0.75)
qs = stratified_queries(H, Q)
write_case("large-top-biased-ranges4-stratified-qs-sub5", H, Q, ranges, qs)

H = random.choice(H_LARGE)
ranges = top_biased_ranges(H, 0.99)
qs = random_queries(H, Q)
write_case("large-top-biased-ranges5-random-qs-sub5", H, Q, ranges, qs)

H = random.choice(H_LARGE)
ranges = top_biased_ranges(H, 0.99)
qs = stratified_queries(H, Q)
write_case("large-top-biased-ranges5-stratified-qs-sub5", H, Q, ranges, qs)

H = random.choice(H_LARGE)
ranges = patitioning_ranges(H)
qs = random_queries(H, Q)
write_case("large-patitioning-ranges-random-qs-sub5", H, Q, ranges, qs)

H = random.choice(H_LARGE)
ranges = patitioning_ranges(H)
qs = stratified_queries(H, Q)
write_case("large-patitioning-ranges-stratified-qs-sub5", H, Q, ranges, qs)

H = random.choice(H_LARGE)
ranges = random_sized_ranges(H, 0, 0.5)
qs = stratified_queries(H, Q)
write_case("large-random-sized-ranges-stratified-qs-sub5", H, Q, ranges, qs)

H = random.choice(H_LARGE)
ranges = random_sized_ranges(H, 0.5, 1)
qs = stratified_queries(H, Q)
write_case("large-random-sized-ranges2-stratified-qs-sub5", H, Q, ranges, qs)

H = random.choice(H_LARGE)
ranges = random_sized_ranges(H, 0.9, 1)
qs = stratified_queries(H, Q)
write_case("large-random-sized-ranges3-stratified-qs-sub5", H, Q, ranges, qs)

H = random.choice(H_LARGE)
ranges = random_sized_ranges(H, 0.99, 1)
qs = stratified_queries(H, Q)
write_case("large-random-sized-ranges4-stratified-qs-sub5", H, Q, ranges, qs)

H = random.choice(H_LARGE)
ranges = random_sized_ranges(H, 0.45, 0.7)
qs = stratified_queries(H, Q)
write_case("large-random-sized-ranges5-stratified-qs-sub5", H, Q, ranges, qs)

H = random.choice(H_LARGE)
ranges = random_sized_ranges(H, 0, 0.1)
qs = stratified_queries(H, Q)
write_case("large-random-sized-ranges6-stratified-qs-sub5", H, Q, ranges, qs)

H = random.choice(H_LARGE)
ranges = random_sized_ranges(H, 0, 0.5)
qs = query_root(H, Q)
write_case("large-random-sized-ranges-root-qs-sub5", H, Q, ranges, qs)

H = random.choice(H_LARGE)
ranges = random_sized_ranges(H, 0.5, 1)
qs = query_root(H, Q)
write_case("large-random-sized-ranges2-root-qs-sub5", H, Q, ranges, qs)

H = random.choice(H_LARGE)
ranges = random_sized_ranges(H, 0.9, 1)
qs = query_root(H, Q)
write_case("large-random-sized-ranges3-root-qs-sub5", H, Q, ranges, qs)

H = random.choice(H_LARGE)
ranges = random_sized_ranges(H, 0.99, 1)
qs = query_root(H, Q)
write_case("large-random-sized-ranges4-root-qs-sub5", H, Q, ranges, qs)

H = random.choice(H_LARGE)
ranges = random_sized_ranges(H, 0.45, 0.7)
qs = query_root(H, Q)
write_case("large-random-sized-ranges5-root-qs-sub5", H, Q, ranges, qs)

H = random.choice(H_LARGE)
ranges = random_sized_ranges(H, 0, 0.1)
qs = query_root(H, Q)
write_case("large-random-sized-ranges6-root-qs-sub5", H, Q, ranges, qs)

H = random.choice(H_LARGE)
ranges = ai_bi_split(H)
qs = random_queries(H, Q)
write_case("large-ai-bi-split-ranges-random-qs-sub5", H, Q, ranges, qs)

H = random.choice(H_LARGE)
ranges = ai_bi_split(H)
qs = query_root(H, Q)
write_case("large-ai-bi-split-ranges-root-qs-sub5", H, Q, ranges, qs)

H = random.choice(H_LARGE)
ranges = ai_bi_split(H)
qs = stratified_queries(H, Q)
write_case("large-ai-bi-split-ranges-stratified-qs-sub5", H, Q, ranges, qs)

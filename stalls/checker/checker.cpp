#include <bits/stdc++.h>
using namespace std;

#define MAXS 1000001
int S, R, M, C, p[MAXS];
vector<int> adj[MAXS];

int ne(int x) {
    return ((long long)x * C) % M;
}

/* CMS DOCS
When there are multiple correct outputs, or when there is partial scoring, white-diff is not powerful enough. In this cases, a checker can be used to perform a complex validation. It is an executable manager, usually named checker.

It will receive as argument three filenames, in order: input, correct output, and contestant’s output. It will then write a standard manager output to stdout and stderr.

It is preferred to compile the checker statically (e.g., with -static using gcc or g++) to avoid potential problems with the sandbox.

A standard manager output is a format that managers can follow to write an outcome and a message for the contestant.

To follow the standard manager output, a manager must write on stdout a single line, containing a floating point number, the outcome; it must write to stderr a single line containing the message for the contestant. Following lines to stdout or stderr will be ignored.
*/

int main(int argc, char **argv) {
    assert(argc == 4);
    ifstream input(argv[1]), correct_output(argv[2]), contestant_output(argv[3]);
    assert(input.is_open());
    assert(correct_output.is_open());
    assert(contestant_output.is_open());

    input >> S >> R >> M >> C;
    for (int i = 1; i <= S; ++i) {
        input >> p[i];
        p[i] %= M;
    }
    for (int i = 0,a,b; i < R; ++i) {
        input >> a >> b;
        adj[a].push_back(b);
        adj[b].push_back(a);
    }
    int x;
    correct_output >> x;

    int n;
    bool ac = 1;
    contestant_output >> n;
    if (x == -1) {
        if (n != -1) {
            // cout << "Stall list is not valid\n";
            ac = 0; 
        }
    }
    else {
        vector<int> stalls;
        int stall;
        while (contestant_output >> stall) stalls.push_back(stall);
        if (n != stalls.size()) {
            // cerr << "The council's powers were not used the indicated number of times.\n";
            ac = 0;
        }
        if(set<int>(stalls.begin(), stalls.end()).size() != stalls.size()) {
            // cerr << "Used the council's power more than once on the same stall.\n";
            ac = 0;
        }
        for (int stall: stalls) {
            if (stall < 1 || stall > S) {
                // cerr << "Stall number outside range (1, S)\n";
                ac = 0;
                break;
            }
            p[stall] = ne(p[stall]);
        }
        for (int i = 1; i <= S && ac; ++i) {
            for (int v: adj[i]) {
                if (p[i] == p[v]) {
                    ac = 0;
                    // cerr << "Stall list is not valid\n";
                    break;
                }
            }
        }
    }

    if (ac)
        cout << 100;
    else
        cout << 0;
    cout << endl;
}
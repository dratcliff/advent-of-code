#include <vector>
#include <string>
#include <iostream>
#include <fstream>
#include <sstream>
#include <map>
#include <set>
#include <algorithm>
#include <deque>
#include <regex>
#include <unordered_set>
#include <stack>

using namespace std;

map<string, set<string>> pc_map;
vector<string> pcs;

bool init()
{
    ifstream file("p1.txt");
    if (!file.is_open())
    {
        cerr << "Error: Unable to open file!" << endl;
        return false;
    }

    string line;
    int row = 0;
    char cur_val;

    regex pattern("([a-z]+)-([a-z]+)");
    while (getline(file, line))
    {

        sregex_iterator begin(line.begin(), line.end(), pattern);
        sregex_iterator end;
        for (sregex_iterator i = begin; i != end; ++i)
        {
            smatch match = *i;
            string left = match.str(1);
            string right = match.str(2);
            pc_map[left].insert(right);
            pc_map[right].insert(left);
        }
    }

    for (const auto &pc : pc_map)
    {
        pcs.push_back(pc.first);
    }

    file.close();
    return true;
}

void p1()
{
    int t = 0;
    for (const auto &pc : pc_map)
    {
        t++;
    }
    set<set<string>> networks;
    string left, right, third;
    for (const auto &pc : pc_map)
    {
        set<string> maybe;
        left = pc.first;
        for (const auto &P : pc.second)
        {
            right = P;
            for (const auto &Q : pc_map[right])
            {
                third = Q;
                if (pc_map[left].find(third) != pc_map[left].end())
                {
                    networks.insert({left, right, third});
                }
            }
        }
    }
    t = 0;
    int t1 = 0;
    for (const auto &n : networks)
    {
        bool starts_with_t = false;
        if (n.size() == 3)
        {
            t++;
            for (const auto &p : n)
            {
                if (p[0] == 't')
                {
                    starts_with_t = true;
                }
            }
            if (starts_with_t)
            {
                t1++;
            }
        }
    }
    cout << "p1: " << t1 << endl;
    set<set<string>> networks3 = networks;
    while (true)
    {

        set<set<string>> networks4;
        set<string> n4;
        for (const auto &pc : pc_map)
        {

            for (const auto &nw : networks3)
            {
                bool could_add = true;
                for (const auto &n : nw)
                {
                    if (pc.second.find(n) == pc.second.end())
                    {
                        could_add = false;
                        break;
                    }
                }
                if (could_add && n4.find(pc.first) == n4.end())
                {
                    n4 = nw;
                    n4.insert(pc.first);
                    networks4.insert(n4);
                }
            }
        }
        networks3 = networks4;
        networks4.clear();
        if (networks3.size() == 1)
        {
            break;
        }
    }
    string s;
    for (const auto &nw : networks3)
    {
        s = "";
        for (const auto &nw3 : nw)
        {
            s += nw3;
            s += ",";
        }
        if (s.size() > 0)
        {
            s.pop_back();
            cout << "p2: " << s << endl;
        }
    }
}

int main()
{
    if (!init())
    {
        return 1;
    }

    p1();
}
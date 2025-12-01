#include <vector>
#include <string>
#include <iostream>
#include <fstream>
#include <sstream>
#include <map>
#include <set>
#include <algorithm>
#include <queue>
#include <regex>
#include <deque>

using namespace std;

set<string> towel_patterns;
vector<string> designs;

bool starts_with(const string &str, const string &prefix)
{
    return str.size() >= prefix.size() &&
           str.compare(0, prefix.size(), prefix) == 0;
}

bool init()
{
    ifstream file("p1.txt");
    if (!file.is_open())
    {
        cerr << "Error: Unable to open file!" << endl;
        return false;
    }
    string line;
    if (getline(file, line))
    {
        istringstream ss(line);
        string item;
        while (std::getline(ss, item, ','))
        {
            size_t start = item.find_first_not_of(" ");
            size_t end = item.find_last_not_of(" ");
            if (start != string::npos && end != string::npos)
            {
                item = item.substr(start, end - start + 1);
            }
            towel_patterns.insert(item);
        }
    }

    if (getline(file, line))
    {
    }

    while (getline(file, line))
    {
        designs.push_back(line);
    }

    file.close();

    return true;
}

map<string, bool> checked;
map<string, long long> counts;

long long num_ways(const string &design)
{
    if (counts.find(design) != counts.end())
    {
        return counts[design];
    }
    long long total = 0;
    string matched, remaining;
    vector<string> to_check;
    for (const auto &pattern : towel_patterns)
    {
        if (starts_with(design, pattern))
        {
            matched = pattern;
            remaining = design.substr(pattern.size());
            if (remaining.size() == 0)
            {
                total++;
            }
            else
            {
                to_check.push_back(remaining);
            }
        }
    }
    for (const auto &t : to_check)
    {
        total += num_ways(t);
    }
    counts[design] = total;
    return total;
}

bool check(const string &design, const string &orig)
{
    if (checked.find(design) != checked.end())
    {
        return checked[design];
    }
    string matched, remaining;
    if (design.size() == 0)
    {
        return true;
    }
    for (const auto &pattern : towel_patterns)
    {
        if (starts_with(design, pattern))
        {
            matched = pattern;
            remaining = design.substr(pattern.size());
            if (check(remaining, orig))
            {
                checked[remaining] = true;
                return true;
            }
        }
    }
    checked[design] = false;
    return false;
}

void p1()
{
    int ans = 0;
    for (const auto &d : designs)
    {
        if (check(d, d))
        {
            ans += 1;
        }
    }
    cout << "p1: " << ans << endl;
}

void p2()
{
    long long ans = 0;
    int64_t cur = 0;
    for (const auto &d : designs)
    {
        cur = num_ways(d);
        ans += cur;
    }
    cout << "p2: " << ans << endl;
    ;
}

int main()
{
    if (!init())
    {
        return 1;
    }

    p1();
    p2();
}
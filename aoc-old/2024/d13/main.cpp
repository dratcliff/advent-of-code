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
#include "main.h"

using namespace std;

vector<vector<tuple<int, int>>> entries;

tuple<long long, long long> D(vector<tuple<int, int>> entry, bool p2)
{
    long long a = get<0>(entry[0]);
    long long b = get<0>(entry[1]);
    long long c = get<0>(entry[2]);
    long long d = get<1>(entry[0]);
    long long e = get<1>(entry[1]);
    long long f = get<1>(entry[2]);

    if (p2)
    {
        c += 10000000000000;
        f += 10000000000000;
    }

    long double determinant = (a * e) - (b * d);
    if (determinant == 0)
    {
        return {-1, -1};
    }

    long double x = ((c * e) - (b * f)) / determinant;
    long double y = ((a * f) - (c * d)) / determinant;

    long long xi = x;
    long long yi = y;
    if (x > xi || y > yi)
    {
        return {-1, -1};
    }
    return {x, y};
}

void p(vector<vector<tuple<int, int>>> &entries, bool p2)
{
    long long ans = 0L;
    for (const auto &e : entries)
    {
        tuple<int64_t, int64_t> solution = D(e, p2);
        int64_t a = get<0>(solution);
        int64_t b = get<1>(solution);
        if (a >= 0 && b >= 0)
        {
            ans += 3 * a;
            ans += b;
        }
    }
    cout << "p" << p2 + 1 << ": " << ans << endl;
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
    int row = 0;
    char cur_val;

    vector<tuple<int, int>> entry;
    std::regex pattern("([0-9]+)[^0-9]+([0-9]+)");
    while (std::getline(file, line))
    {

        std::sregex_iterator begin(line.begin(), line.end(), pattern);
        std::sregex_iterator end;
        for (std::sregex_iterator i = begin; i != end; ++i)
        {
            std::smatch match = *i;
            int left = std::stoi(match.str(1));
            int right = std::stoi(match.str(2));
            entry.push_back({left, right});
        }

        if (++row % 4 == 0)
        {
            entries.push_back(entry);
            entry.clear();
        }
    }
    entries.push_back(entry);
    file.close();

    return true;
}

int main()
{
    if (!init())
    {
        return 1;
    }
    p(entries, false);
    p(entries, true);
}
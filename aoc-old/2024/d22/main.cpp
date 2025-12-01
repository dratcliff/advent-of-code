#include <vector>
#include <string>
#include <iostream>
#include <fstream>
#include <sstream>
#include <map>
#include <set>
#include <algorithm>
#include <deque>

using namespace std;

vector<long long> magic_numbers;

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
    while (std::getline(file, line))
    {

        magic_numbers.push_back(stoi(line));
    }

    file.close();
    return true;
}

map<tuple<int, int, int, int>, map<long long, int>> prices;

long long do_it(long long n)
{
    long long orig = n;
    tuple<int, int, int, int> seq;
    long long last_price = n % 10;
    long long this_price = n % 10;
    vector<int> last_4;
    // cout << "n: " << n << endl;
    for (int i = 0; i < 2000; i++)
    {

        int n2 = n * 64;
        n ^= n2;
        n = (16777216 + (n % 16777216)) % 16777216;
        n2 = n / 32;
        n ^= n2;
        n = (16777216 + (n % 16777216)) % 16777216;
        n2 = n * 2048;
        n ^= n2;
        n = (16777216 + (n % 16777216)) % 16777216;
        last_price = this_price;
        this_price = n % 10;

        last_4.push_back(this_price - last_price);
        if (last_4.size() == 4)
        {
            seq = {last_4[0], last_4[1], last_4[2], last_4[3]};
            if (prices[seq].find(orig) == prices[seq].end())
            {
                prices[seq][orig] = this_price;
            }
            last_4.erase(last_4.begin());
        }
    }
    return n;
}

int main()
{
    if (!init())
    {
        return 1;
    }

    long long ans = 0;
    for (const auto &n : magic_numbers)
    {
        ans += do_it(n);
    }
    cout << "p1: " << ans << endl;

    long long best = 0;

    for (const auto &pair : prices)
    {
        long long cur = 0;

        for (const auto &z : pair.second)
        {
            cur += z.second;
        }
        if (cur > best)
        {
            best = cur;
        }
    }
    cout << "p2: " << best << endl;
}
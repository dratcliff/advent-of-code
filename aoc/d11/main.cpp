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

vector<int64_t> stones;

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

        stringstream ss(line);
        string token;
        vector<string> tokens;
        while (getline(ss, token, ' '))
        {
            stones.push_back(stoll(token));
        }
    }

    file.close();
    return true;
}

map<int64_t, vector<int64_t>> changes_cache;

vector<int64_t> change(int64_t stone)
{
    vector<int64_t> ret;
    string stone_string = to_string(stone);
    size_t l = stone_string.length();
    if (changes_cache.find(stone) == changes_cache.end())
    {
        if (stone == 0)
        {
            ret.push_back(1);
        }
        else if (l % 2 == 0)
        {
            string left = stone_string.substr(0, l / 2);
            string right = stone_string.substr(l / 2, l / 2);
            ret.push_back(stoll(left));
            ret.push_back(stoll(right));
        }
        else
        {
            ret.push_back(stone * 2024);
        }
        changes_cache[stone] = ret;
    }
    return changes_cache[stone];
}
void print_stones()
{
    for (const auto &stone : stones)
    {
        cout << stone << " ";
    }
    cout << endl;
}

void blink(int n)
{
    map<int64_t, int64_t> stone_counts;
    for (const auto &stone : stones)
    {
        stone_counts[stone]++;
    }
    map<int64_t, int64_t> new_stone_counts;

    for (int i = 0; i < n; i++)
    {
        new_stone_counts.clear();
        for (const auto &pair : stone_counts)
        {
            for (const auto &changes : change(pair.first))
            {
                new_stone_counts[changes] += pair.second;
            }
        }
        stone_counts = new_stone_counts;
    }
    int64_t ans = 0;
    for (const auto &pair : stone_counts)
    {
        ans += pair.second;
    }
    cout << ans << endl;
}

int main()
{
    if (!init())
    {
        return 1;
    }

    cout << "p1: ";
    blink(25);
    cout << "p2: ";
    blink(75);
}
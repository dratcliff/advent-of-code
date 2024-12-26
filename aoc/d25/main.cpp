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
#include <optional>

using namespace std;

vector<vector<int>> keys;
vector<vector<int>> locks;

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
    vector<int> cur;
    bool is_key = false;
    while (getline(file, line))
    {
        if (row % 8 == 0)
        {
            if (line[0] == '.')
            {
                is_key = true;
                for (int j = 0; j < 5; j++)
                {
                    cur.push_back(6);
                }
            }
            else
            {
                for (int j = 0; j < 5; j++)
                {
                    cur.push_back(-1);
                }
            }
        }

        if (row % 8 == 7)
        {
            if (is_key)
            {
                keys.push_back(cur);
            }
            else
            {
                locks.push_back(cur);
            }
            is_key = false;
            cur.clear();
        }
        else
        {
            for (int i = 0; i < 5; i++)
            {
                if (is_key)
                {
                    if (line[i] == '.')
                    {
                        cur[i]--;
                    }
                }
                else
                {
                    if (line[i] == '#')
                    {
                        cur[i]++;
                    }
                }
            }
        }
        row++;
    }
    if (is_key)
    {
        keys.push_back(cur);
    }
    else
    {
        locks.push_back(cur);
    }
    file.close();
    return true;
}

int main()
{
    if (!init())
    {
        return 1;
    }
    int ans = 0;
    for (const auto &L : locks)
    {
        for (const auto &K : keys)
        {
            bool matches = true;
            for (int i = 0; i < 5; i++)
            {
                if (L[i] + K[i] >= 6)
                {
                    matches = false;
                }
            }
            if (matches)
            {
                ans++;
            }
        }
    }
    cout << "p1: " << ans << endl;
}
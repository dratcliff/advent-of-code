#include <iostream>
#include <fstream>
#include <sstream>
#include <vector>
#include <queue>
#include <tuple>
#include <cmath>

using namespace std;

bool check(vector<int64_t> &row, bool p2)
{
    queue<tuple<int64_t, int>> Q;
    queue<tuple<int64_t, int>> empty;
    tuple<int64_t, int> cur;
    int L = row.size();
    Q.push({row[1], 1});
    while (!Q.empty())
    {
        cur = Q.front();
        Q.pop();
        int64_t cur_val = get<0>(cur);
        if (cur_val > row[0])
        {
            continue;
        }
        int cur_idx = get<1>(cur);
        if (cur_idx == L - 1)
        {
            if (cur_val == row[0])
            {
                swap(Q, empty);
                return true;
            }
        }
        else
        {
            Q.push({cur_val + row[cur_idx + 1], cur_idx + 1});
            Q.push({cur_val * row[cur_idx + 1], cur_idx + 1});
            if (p2)
            {
                int digits = static_cast<int>(std::log10(row[cur_idx + 1])) + 1;
                Q.push({cur_val * pow(10, digits) + row[cur_idx + 1], cur_idx + 1});
            }
        }
    }
    return false;
}

int main()
{
    ifstream file("p1.txt");
    if (!file.is_open())
    {
        cerr << "Error: Unable to open file!" << endl;
        return 1;
    }

    vector<vector<int64_t>> tokens;
    string line;

    while (getline(file, line))
    {
        vector<int64_t> tokens2;
        stringstream ss(line);
        string token;
        while (getline(ss, token, ' '))
        {
            int idx = token.find(':');
            if (idx != string::npos)
            {
                token = token.erase(idx, 1);
            }
            tokens2.push_back(stoll(token));
        }
        tokens.push_back(tokens2);
    }

    int64_t ans = 0;
    int64_t ans2 = 0;

    for (vector<int64_t> &row : tokens)
    {
        if (check(row, false))
        {
            ans += row[0];
            ans2 += row[0];
        }
        else
        {
            if (check(row, true))
            {
                ans2 += row[0];
            }
        }
    }
    cout << "ans: " << ans << endl;
    cout << "ans2 " << ans2 << endl;
    return 0;
}
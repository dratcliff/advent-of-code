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

int height = 0;
int width = 0;
map<tuple<int, int>, int> grid;
vector<tuple<int, int>> trailheads;

vector<tuple<int, int>> offsets = {
    {0, 1}, {0, -1}, {1, 0}, {-1, 0}};

bool make_grid()
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
        for (int col = 0; col < line.size(); col++)
        {
            cur_val = line[col];
            grid[{col, row}] = cur_val - '0';
            if (cur_val == '0')
            {
                trailheads.push_back({col, row});
            }
            if (line.size() > width)
            {
                width = line.size();
            }
        }

        row++;
        if (row > height)
        {
            height = row;
        }
    }

    file.close();
    return true;
}

void print_grid()
{
    for (int y = 0; y < height; y++)
    {
        for (int x = 0; x < width; x++)
        {
            cout << grid[{x, y}];
        }
        cout << endl;
    }
}

void p1()
{
    map<tuple<int, int>, map<tuple<int, int>, int>> scores;
    for (const auto &pair : trailheads)
    {
        int cur_height = 0;
        tuple<int, int> cur_pos;
        int x = 0;
        int y = 0;
        tuple<int, int> nxt_pos;
        tuple<int, tuple<int, int>> cur_height_pos;
        deque<tuple<int, tuple<int, int>>> Q;
        Q.push_back({0, pair});
        while (!Q.empty())
        {
            cur_height_pos = Q.front();
            Q.pop_front();

            cur_height = get<0>(cur_height_pos);
            cur_pos = get<1>(cur_height_pos);
            if (cur_height == 9)
            {
                scores[pair][cur_pos] += 1;
            }

            x = get<0>(cur_pos);
            y = get<1>(cur_pos);
            for (const auto &o : offsets)
            {
                int xo = get<0>(o);
                int yo = get<1>(o);
                nxt_pos = {x + xo, y + yo};
                if (grid[nxt_pos] == cur_height + 1)
                {
                    Q.push_back({cur_height + 1, nxt_pos});
                }
            }
        }
    }
    int ans = 0;
    int paths = 0;
    for (const auto &trailhead : scores)
    {
        for (const auto &end : trailhead.second)
        {
            ans += 1;
            paths += end.second;
        }
    }
    cout << "score: " << ans << " paths: " << paths;
}

int main()
{
    if (!make_grid())
    {
        return 1;
    }

    // print_grid();

    p1();
}
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

int height = 0;
int width = 0;
tuple<int, int> S;
using Point = tuple<int, int>;

map<Point, char> grid;

vector<Point> offsets = {
    {1, 0},
    {0, -1},
    {-1, 0},
    {0, 1}};

bool make_grid(int num_bytes)
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

    vector<int> entry;
    regex pattern("([0-9]+),([0-9]+)");
    while (std::getline(file, line) && row < num_bytes)
    {

        sregex_iterator begin(line.begin(), line.end(), pattern);
        sregex_iterator end;
        for (sregex_iterator i = begin; i != end; ++i)
        {
            smatch match = *i;
            int x = stoi(match.str(1));
            int y = stoi(match.str(2));
            grid[{x, y}] = '#';
        }
        row++;
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

bool bfs(int size, bool p1)
{
    deque<tuple<Point, int>> Q;
    tuple<Point, int> start = {{0, 0}, 0};
    tuple<Point, int> cur;
    Point nxt_pt;
    Point cur_pt;
    set<Point> visited;
    int x, y, nx, ny;
    char direction;
    Q.push_back(start);

    map<int, set<tuple<int, int>>> best_paths;
    while (!Q.empty())
    {
        cur = Q.front();
        Q.pop_front();
        cur_pt = get<0>(cur);
        x = get<0>(cur_pt);
        y = get<1>(cur_pt);

        if (visited.find(cur_pt) == visited.end())
        {
            if (x == size - 1 && y == size - 1)
            {
                if (p1)
                {
                    cout << "p1: " << get<1>(cur) << endl;
                }
                return true;
            }
            visited.insert(cur_pt);
            for (const auto &o : offsets)
            {
                nx = x + get<0>(o);
                ny = y + get<1>(o);
                if (nx < size && nx >= 0 && ny < size && ny >= 0)
                {
                    nxt_pt = {nx, ny};
                    if (grid[nxt_pt] != '#')
                    {
                        Q.push_back({nxt_pt, get<1>(cur) + 1});
                    }
                }
            }
        }
    }
    return false;
}

int main()
{
    if (!make_grid(1024))
    {
        return 1;
    }

    bfs(71, true);

    for (int i = 1024; i < 3450; i++)
    {
        grid.clear();
        make_grid(i);
        if (!bfs(71, false))
        {
            cout << "p2: " << i << endl;
            break;
        }
    }
}
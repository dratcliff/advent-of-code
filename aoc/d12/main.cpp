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
map<tuple<int, int>, char> grid;

vector<tuple<int, int>> offsets = {
    {0, 1}, {0, -1}, {1, 0}, {-1, 0}};

vector<tuple<int, int>> offsets_2 = {
    {0, 0}, {0, 1}, {1, 0}, {1, 1}};

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
            grid[{col, row}] = cur_val;
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

vector<tuple<int, int>> bfs(tuple<int, int> start, set<tuple<int, int>> &visited)
{
    vector<tuple<int, int>> ret;
    deque<tuple<int, int>> Q;
    char start_letter = grid[start];
    tuple<int, int> cur;
    tuple<int, int> nxt;
    Q.push_back(start);
    while (!Q.empty())
    {
        cur = Q.back();
        Q.pop_back();
        if (visited.find(cur) == visited.end())
        {
            visited.insert(cur);
            ret.push_back(cur);
            for (const auto &o : offsets)
            {
                nxt = {get<0>(cur) + get<0>(o), get<1>(cur) + get<1>(o)};
                if (grid.find(nxt) != grid.end() && grid[nxt] == start_letter)
                {
                    Q.push_back(nxt);
                }
            }
        }
    }
    return ret;
}

vector<vector<tuple<int, int>>> regions()
{
    set<tuple<int, int>> visited;
    vector<vector<tuple<int, int>>> res;

    for (const auto &pair : grid)
    {
        tuple<int, int> coord = pair.first;
        if (visited.find(coord) == visited.end())
        {
            res.push_back(bfs(coord, visited));
        }
    }

    return res;
}

tuple<int, int> ap(vector<tuple<int, int>> region)
{
    int a = 0;
    int p = 0;
    char letter = grid[region.front()];
    for (const auto &r : region)
    {
        a++;
        int x = get<0>(r);
        int y = get<1>(r);
        for (const auto &o : offsets)
        {
            int xo = get<0>(o);
            int yo = get<1>(o);
            tuple<int, int> nxt = {x + xo, y + yo};
            if (grid.find(nxt) == grid.end() || grid[nxt] != letter)
            {
                p++;
            }
        }
    }
    return {a, p};
}

tuple<int, int> ab(vector<tuple<int, int>> region)
{
    int a = 0;
    int b = 0;
    char letter = grid[region.front()];
    set<tuple<int, int>> region_set;
    map<tuple<int, int>, map<char, int>> counts;
    for (const auto &r : region)
    {
        region_set.insert(r);
    }

    for (const auto &r : region)
    {
        a++;
        int n = 0;
        int x = get<0>(r);
        int y = get<1>(r);
        /*
        basically, convert each square into a square of coordinates, i.e.,
        the square at 0,0 becomes [(0,0), (0,1), (1,0), (1,1)].
        */
        for (const auto &o : offsets_2)
        {
            int xo = get<0>(o);
            int yo = get<1>(o);
            tuple<int, int> nxt = {x + xo, y + yo};
            char ud = yo == 0 ? 'U' : 'D';
            char rl = xo == 0 ? 'L' : 'R';
            counts[nxt][ud]++;
            counts[nxt][rl]++;
        }
    }
    for (const auto &pair : counts)
    {
        bool works = true;
        int ones = 0;
        int twos = 0;
        for (const auto &pair2 : pair.second)
        {
            if (pair2.second == 1)
            {
                ones++;
            }
            else if (pair2.second == 2)
            {
                twos++;
            }
        }
        /*
         didn't really figure out why this works, but it seems to cover all the cases
        */
        if (twos == 2)
        {
            b += 1;
        }
        else if (ones == 4)
        {
            b += 2;
        }
        else if (twos == 0 && ones == 2)
        {
            b += 1;
        }
    }
    return {a, b};
}

int main()
{
    if (!make_grid())
    {
        return 1;
    }

    // print_grid();

    int ans = 0;
    vector<vector<tuple<int, int>>> reg = regions();
    for (const auto &r : reg)
    {
        tuple<int, int> _ap = ap(r);
        ans += get<0>(_ap) * get<1>(_ap);
    }
    cout << "p1: " << ans << endl;
    ans = 0;
    for (const auto &r : reg)
    {
        tuple<int, int> _ab = ab(r);
        ans += get<0>(_ab) * get<1>(_ab);
    }
    cout << "p2: " << ans << endl;
}
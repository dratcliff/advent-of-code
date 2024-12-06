#include <vector>
#include <string>
#include <iostream>
#include <fstream>
#include <sstream>
#include <map>
#include <set>
#include <algorithm>

using namespace std;

int height = 0;
int width = 0;
map<tuple<int, int>, char> grid;
tuple<int, int> start;

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

    // Read file line by line
    while (std::getline(file, line))
    {
        for (int col = 0; col < line.size(); ++col)
        {
            grid[{col, row}] = line[col];
            if (grid[{col, row}] == '^')
            {
                start = {col, row};
                grid[{col, row}] = '.';
            }
            if (col > width)
            {
                width = col;
            }
        }
        ++row;
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

map<char, tuple<int, int>> directions = {
    {'^', {0, -1}},
    {'>', {1, 0}},
    {'<', {-1, 0}},
    {'v', {0, 1}}};

map<char, char> turn_right = {
    {'^', '>'},
    {'>', 'v'},
    {'v', '<'},
    {'<', '^'}};

set<tuple<int, int>> walk()
{
    char cur_dir = '^';
    tuple<int, int> cur_pos = start;
    set<tuple<int, int>> visited;
    tuple<int, int> nxt_offset;
    tuple<int, int> nxt_pos;
    char nxt_val;
    char nxt_dir;
    while (true)
    {
        visited.insert(cur_pos);
        nxt_offset = directions[cur_dir];
        nxt_pos = {get<0>(cur_pos) + get<0>(nxt_offset), get<1>(cur_pos) + get<1>(nxt_offset)};
        nxt_val = grid[nxt_pos];
        if (nxt_val == '#')
        {
            cur_dir = turn_right[cur_dir];
        }
        else if (nxt_val == '.')
        {
            cur_pos = nxt_pos;
        }
        else
        {
            cout << "p1: " << visited.size() << endl;
            break;
        }
    }
    return visited;
}

bool walk2()
{
    char cur_dir = '^';
    tuple<int, int> cur_pos = start;
    tuple<int, int, char> cur_pos_dir = {get<0>(start), get<1>(start), cur_dir};
    set<tuple<int, int, char>> visited;
    tuple<int, int> nxt_offset;
    tuple<int, int> nxt_pos;
    char nxt_val;
    char nxt_dir;
    while (true)
    {
        if (visited.find(cur_pos_dir) != visited.end())
        {
            return true;
        }
        visited.insert(cur_pos_dir);
        nxt_offset = directions[cur_dir];
        nxt_pos = {get<0>(cur_pos) + get<0>(nxt_offset), get<1>(cur_pos) + get<1>(nxt_offset)};
        nxt_val = grid[nxt_pos];
        if (nxt_val == '#')
        {
            cur_dir = turn_right[cur_dir];
            cur_pos_dir = {get<0>(cur_pos), get<1>(cur_pos), cur_dir};
        }
        else if (nxt_val == '.')
        {
            cur_pos = nxt_pos;
            cur_pos_dir = {get<0>(cur_pos), get<1>(cur_pos), cur_dir};
        }
        else
        {
            return false;
        }
    }
}

int main(int argc, char *argv[])
{
    if (!make_grid())
    {
        return 1;
    }
    set<tuple<int, int>> visited = walk();

    int ans = 0;
    char cur_val;
    tuple<int, int> cur_pos;
    // slow! ~24s
    for (tuple<int, int> seen : visited)
    {
        int x = get<0>(seen);
        int y = get<1>(seen);
        cur_val = grid[{x, y}];
        if (cur_val == '.' && cur_pos != start)
        {
            grid[{x, y}] = '#';
            bool good_obstruction = walk2();
            if (good_obstruction)
            {
                ans++;
            }
            grid[{x, y}] = '.';
        }
    }

    cout << "p2: " << ans << endl;
    return 0;
}

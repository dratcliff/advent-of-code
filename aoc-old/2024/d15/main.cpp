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

vector<char> moves;
tuple<int, int> start;
map<char, tuple<int, int>> offsets = {
    {'<', {-1, 0}},
    {'v', {0, 1}},
    {'>', {1, 0}},
    {'^', {0, -1}}};

tuple<bool, map<tuple<int, int>, char>> init()
{
    map<tuple<int, int>, char> grid;
    ifstream file("p1.txt");
    if (!file.is_open())
    {
        cerr << "Error: Unable to open file!" << endl;
        return {false, grid};
    }

    string line;
    int row = 0;
    char cur_val;
    bool in_grid = true;
    while (std::getline(file, line))
    {
        if (in_grid)
        {
            if (line.size() == 0)
            {
                in_grid = false;
                continue;
            }
            for (int col = 0; col < line.size(); col++)
            {
                cur_val = line[col];
                if (cur_val == '@')
                {
                    start = {col, row};
                }
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
        else
        {
            for (int col = 0; col < line.size(); col++)
            {
                cur_val = line[col];
                moves.push_back(cur_val);
            }
        }
    }

    file.close();
    return {true, grid};
}

tuple<int, int> move_robot(map<tuple<int, int>, char> &grid, tuple<int, int> start_pos, char direction)
{
    tuple<int, int> o = offsets[direction];
    tuple<int, int> cur_pos = start_pos;
    int x = get<0>(cur_pos);
    int y = get<1>(cur_pos);
    int xo = get<0>(o);
    int yo = get<1>(o);
    vector<tuple<int, int>> to_push;
    tuple<int, int> nxt = {x + xo, y + yo};
    char nxt_val = grid[nxt];
    while (nxt_val == 'O')
    {
        to_push.push_back(nxt);
        cur_pos = nxt;
        x = get<0>(cur_pos);
        y = get<1>(cur_pos);
        nxt = {x + xo, y + yo};
        nxt_val = grid[nxt];
    }
    if (nxt_val == '#')
    {
        return start_pos;
    }

    for (const auto &pos : to_push)
    {
        x = get<0>(pos);
        y = get<1>(pos);
        nxt = {x + xo, y + yo};
        grid[nxt] = 'O';
    }

    x = get<0>(start_pos);
    y = get<1>(start_pos);
    nxt = {x + xo, y + yo};
    grid[nxt] = '@';
    grid[start_pos] = '.';
    return nxt;
}

set<tuple<tuple<int, int>, char>> to_move(map<tuple<int, int>, char> &grid, tuple<int, int> start_pos, char direction)
{
    set<tuple<tuple<int, int>, char>> ret;
    set<tuple<tuple<int, int>, char>> cur_row;
    tuple<int, int> o = offsets[direction];
    tuple<int, int> cur_pos = start_pos;
    int x = get<0>(cur_pos);
    int y = get<1>(cur_pos);
    int xo = get<0>(o);
    int yo = get<1>(o);
    tuple<int, int> nxt = {x + xo, y + yo};
    char nxt_val = grid[nxt];
    cur_row.insert({nxt, nxt_val});
    ret.insert({nxt, nxt_val});
    if (nxt_val == '[')
    {
        nxt = {get<0>(nxt) + 1, get<1>(nxt)};
        nxt_val = ']';
        cur_row.insert({nxt, nxt_val});
        ret.insert({nxt, nxt_val});
    }
    else if (nxt_val == ']')
    {
        nxt = {get<0>(nxt) - 1, get<1>(nxt)};
        nxt_val = '[';
        cur_row.insert({nxt, nxt_val});
        ret.insert({nxt, nxt_val});
    }

    bool done = false;
    while (!done)
    {
        done = true;
        set<tuple<tuple<int, int>, char>> nxt_row;
        for (const auto &box : cur_row)
        {
            cur_pos = get<0>(box);
            x = get<0>(cur_pos);
            y = get<1>(cur_pos);
            xo = get<0>(o);
            yo = get<1>(o);
            nxt = {x + xo, y + yo};
            nxt_val = grid[nxt];
            if (nxt_val == '[')
            {
                nxt_row.insert({nxt, nxt_val});
                nxt = {get<0>(nxt) + 1, get<1>(nxt)};
                nxt_val = ']';
                nxt_row.insert({nxt, nxt_val});
                done = false;
            }
            else if (nxt_val == ']')
            {
                nxt_row.insert({nxt, nxt_val});
                nxt = {get<0>(nxt) - 1, get<1>(nxt)};
                nxt_val = '[';
                nxt_row.insert({nxt, nxt_val});
                done = false;
            }
            else if (nxt_val == '#')
            {
                ret.clear();
                return ret;
            }
        }
        cur_row = nxt_row;
        for (const auto &entry : nxt_row)
        {
            ret.insert(entry);
        }
        nxt_row.clear();
    }
    return ret;
}

tuple<int, int> move_ud(map<tuple<int, int>, char> &grid, tuple<int, int> start_pos, char direction)
{
    tuple<int, int> o = offsets[direction];
    tuple<int, int> cur_pos = start_pos;
    int x = get<0>(cur_pos);
    int y = get<1>(cur_pos);
    int xo = get<0>(o);
    int yo = get<1>(o);
    vector<tuple<tuple<int, int>, char>> to_push;
    vector<tuple<tuple<int, int>, char>> last_row;
    tuple<int, int> nxt = {x + xo, y + yo};
    char nxt_val = grid[nxt];
    if (nxt_val == '.')
    {
        x = get<0>(start_pos);
        y = get<1>(start_pos);
        nxt = {x + xo, y + yo};
        grid[nxt] = '@';
        grid[start_pos] = '.';
        return nxt;
    }
    if (nxt_val == '#')
    {
        return start_pos;
    }

    set<tuple<tuple<int, int>, char>> t = to_move(grid, start_pos, direction);

    if (t.size() == 0)
    {
        return start_pos;
    }

    for (const auto &pos_val : t)
    {
        tuple<int, int> pos = get<0>(pos_val);
        grid[pos] = '.';
    }
    for (const auto &pos_val : t)
    {
        tuple<int, int> pos = get<0>(pos_val);
        char val = get<1>(pos_val);
        x = get<0>(pos);
        y = get<1>(pos);
        nxt = {x + xo, y + yo};
        grid[nxt] = val;
    }

    x = get<0>(start_pos);
    y = get<1>(start_pos);
    nxt = {x + xo, y + yo};
    grid[nxt] = '@';
    grid[start_pos] = '.';
    return nxt;
}

tuple<int, int> move_lr(map<tuple<int, int>, char> &grid, tuple<int, int> start_pos, char direction)
{
    tuple<int, int> o = offsets[direction];
    tuple<int, int> cur_pos = start_pos;
    int x = get<0>(cur_pos);
    int y = get<1>(cur_pos);
    int xo = get<0>(o);
    int yo = get<1>(o);
    vector<tuple<tuple<int, int>, char>> to_push;
    tuple<int, int> nxt = {x + xo, y + yo};
    char nxt_val = grid[nxt];
    while (nxt_val == '[' || nxt_val == ']')
    {
        to_push.push_back({nxt, nxt_val});
        cur_pos = nxt;
        x = get<0>(cur_pos);
        y = get<1>(cur_pos);
        nxt = {x + xo, y + yo};
        nxt_val = grid[nxt];
    }
    if (nxt_val == '#')
    {
        return start_pos;
    }

    for (const auto &pos_val : to_push)
    {
        tuple<int, int> pos = get<0>(pos_val);
        char val = get<1>(pos_val);
        x = get<0>(pos);
        y = get<1>(pos);
        nxt = {x + xo, y + yo};
        grid[nxt] = val;
    }

    x = get<0>(start_pos);
    y = get<1>(start_pos);
    nxt = {x + xo, y + yo};
    grid[nxt] = '@';
    grid[start_pos] = '.';
    return nxt;
}

tuple<int, int> move_robot2(map<tuple<int, int>, char> &grid, tuple<int, int> start_pos, char direction)
{

    if (direction == 'v' || direction == '^')
    {
        return move_ud(grid, start_pos, direction);
    }
    else
    {
        return move_lr(grid, start_pos, direction);
    }
}

void print_grid(map<tuple<int, int>, char> &grid)
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

void box_calc(map<tuple<int, int>, char> &grid)
{
    int ans = 0;
    for (const auto &pair : grid)
    {
        if (pair.second == 'O' || pair.second == '[')
        {
            ans += 100 * get<1>(pair.first);
            ans += get<0>(pair.first);
        }
    }
    cout << "ans: " << ans << endl;
}

void expand_grid(map<tuple<int, int>, char> &grid)
{
    map<tuple<int, int>, char> new_grid;
    for (const auto &pair : grid)
    {
        tuple<int, int> left = {2 * get<0>(pair.first), get<1>(pair.first)};
        tuple<int, int> right = {2 * get<0>(pair.first) + 1, get<1>(pair.first)};
        if (pair.second == '#' || pair.second == '.')
        {
            new_grid[left] = pair.second;
            new_grid[right] = pair.second;
        }
        else if (pair.second == 'O')
        {
            new_grid[left] = '[';
            new_grid[right] = ']';
        }
        else if (pair.second == '@')
        {
            new_grid[left] = '@';
            new_grid[right] = '.';
        }
    }
    grid = new_grid;
    width *= 2;
    start = {get<0>(start) * 2, get<1>(start)};
}

int main()
{
    bool success;
    map<tuple<int, int>, char> grid;
    tuple<bool, map<tuple<int, int>, char>> i = init();
    if (!get<0>(i))
    {
        return 1;
    }
    grid = get<1>(i);
    map<tuple<int, int>, char> orig_grid = grid;

    tuple<int, int> robot_pos = start;
    for (const auto &move : moves)
    {
        robot_pos = move_robot(grid, robot_pos, move);
    }
    box_calc(grid);
    cout << endl;

    expand_grid(orig_grid);
    grid = orig_grid;
    print_grid(orig_grid);
    cout << endl;
    robot_pos = start;
    for (const auto &move : moves)
    {
        robot_pos = move_robot2(grid, robot_pos, move);
    }
    print_grid(grid);
    box_calc(grid);
}
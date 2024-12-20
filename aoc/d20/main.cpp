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
using Point = tuple<int, int>;
int height, width = 0;
Point S;
Point E;
map<Point, char> grid;

vector<Point> offsets = {
    {0, 1}, {0, -1}, {1, 0}, {-1, 0}};

map<int, int> cheats;
map<int, set<tuple<Point, int>>> cheats2;
map<Point, int> distances_E;
map<Point, int> distances_S;
map<Point, set<tuple<Point, int>>> valid_cheats;

void precalc()
{
    for (const auto &P : {E, S})
    {
        map<Point, int> &distances = P == E ? distances_E : distances_S;
        deque<tuple<int, Point>> Q;
        tuple<int, Point> cur, nxt;
        Point cur_pt, nxt_pt;
        set<Point> visited;
        int x = 0, y = 0, nx = 0, ny = 0, depth = 0;
        Q.push_back({depth, P});
        while (!Q.empty())
        {
            cur = Q.front();
            Q.pop_front();
            cur_pt = get<1>(cur);
            x = get<0>(cur_pt);
            y = get<1>(cur_pt);
            depth = get<0>(cur);
            if (visited.find(cur_pt) == visited.end())
            {
                visited.insert(cur_pt);
                distances[cur_pt] = depth;
                for (const auto &o : offsets)
                {
                    nx = get<0>(o);
                    ny = get<1>(o);
                    nxt_pt = {x + nx, y + ny};
                    if (grid.find(nxt_pt) != grid.end() && grid[nxt_pt] != '#')
                    {
                        Q.push_back({depth + 1, nxt_pt});
                    }
                }
            }
        }
    }
}

void find_cheats(Point start_pt)
{
    deque<tuple<int, Point>> Q;
    tuple<int, Point> cur, nxt;
    Point cur_pt, nxt_pt;
    set<Point> visited;
    int x = 0, y = 0, nx = 0, ny = 0, depth = 0;
    Q.push_back({depth, start_pt});
    while (!Q.empty())
    {
        cur = Q.front();
        Q.pop_front();
        cur_pt = get<1>(cur);
        x = get<0>(cur_pt);
        y = get<1>(cur_pt);
        depth = get<0>(cur);
        if (visited.find(cur_pt) == visited.end())
        {
            visited.insert(cur_pt);
            if (grid[cur_pt] != '#')
            {
                int new_distance_to_end = distances_E[cur_pt];
                int distance_to_start = distances_S[start_pt];
                if (new_distance_to_end + depth + distance_to_start < distances_E[start_pt] + distance_to_start)
                {
                    valid_cheats[start_pt].insert({cur_pt, depth});
                }
            }
            for (const auto &o : offsets)
            {
                nx = get<0>(o);
                ny = get<1>(o);
                nxt_pt = {x + nx, y + ny};
                if (grid.find(nxt_pt) != grid.end() && depth < 20)
                {
                    Q.push_back({depth + 1, nxt_pt});
                }
            }
        }
    }
}

void bfs()
{
    deque<tuple<int, Point, int>> Q;
    tuple<int, Point, int> cur, nxt;
    Point cur_pt, nxt_pt;
    map<int, set<Point>> visited;
    int x = 0, y = 0, nx = 0, ny = 0, depth = 0, cheat_id = 0, cur_cheat = 0;
    Q.push_back({depth, S, cheat_id});
    while (!Q.empty())
    {
        cur = Q.front();
        Q.pop_front();
        cur_pt = get<1>(cur);
        cur_cheat = get<2>(cur);
        x = get<0>(cur_pt);
        y = get<1>(cur_pt);
        depth = get<0>(cur);
        if (visited[cur_cheat].find(cur_pt) == visited[cur_cheat].end())
        {
            visited[cur_cheat].insert(cur_pt);
            if (cur_pt == E)
            {
                cheats[depth]++;
            }
            for (const auto &o : offsets)
            {
                nx = get<0>(o);
                ny = get<1>(o);
                nxt_pt = {x + nx, y + ny};
                if (grid.find(nxt_pt) != grid.end() && grid[nxt_pt] != '#')
                {
                    Q.push_back({depth + 1, nxt_pt, cur_cheat});
                }
                if (cur_cheat == 0)
                {
                    nxt_pt = {x + nx, y + ny};
                    if (grid.find(nxt_pt) != grid.end() && grid[nxt_pt] == '#')
                    {
                        nxt_pt = {x + nx + nx, y + ny + ny};
                        if (grid.find(nxt_pt) != grid.end() && grid[nxt_pt] != '#' && visited[cur_cheat].find(nxt_pt) == visited[cur_cheat].end())
                        {
                            int remaining = distances_E[nxt_pt];
                            cheats[depth + 2 + remaining]++;
                        }
                    }
                    for (const auto &cheat_point : valid_cheats[cur_pt])
                    {
                        int remaining = distances_E[get<0>(cheat_point)] + get<1>(cheat_point);
                        cheats2[depth + remaining].insert(cheat_point);
                    }
                }
            }
        }
    }
}

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
    while (getline(file, line))
    {
        for (int col = 0; col < line.size(); col++)
        {
            cur_val = line[col];
            if (cur_val == 'S')
            {
                S = {col, row};
            }
            if (cur_val == 'E')
            {
                E = {col, row};
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

int main()
{
    if (!make_grid())
    {
        return 1;
    }

    print_grid();
    precalc();
    for (const auto &entry : distances_E)
    {
        find_cheats(entry.first);
    }
    bfs();
    int worst = 0;
    int ge_hundred = 0;

    for (const auto &entry : cheats)
    {
        if (worst == 0 || entry.first > worst)
        {
            worst = entry.first;
        }
    }
    for (const auto &entry : cheats)
    {
        int saved = worst - entry.first;
        if (saved >= 100)
        {
            ge_hundred += entry.second;
        }
    }
    cout << "p1: " << ge_hundred << endl;
    ge_hundred = 0;
    for (const auto &entry : cheats2)
    {
        int saved = worst - entry.first;
        if (saved >= 100)
        {
            ge_hundred += entry.second.size();
        }
    }

    cout << "p2: " << ge_hundred << endl;
}
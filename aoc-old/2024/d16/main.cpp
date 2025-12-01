#include <vector>
#include <string>
#include <iostream>
#include <fstream>
#include <sstream>
#include <map>
#include <set>
#include <algorithm>
#include <queue>

using namespace std;

int height = 0;
int width = 0;
tuple<int, int> S;
using Point = tuple<int, int>;

map<Point, char> grid;

/*
 > :: (>, (1,0), 1), (v, (0, 0), 1000), (^, (0,0), 1000)
 v :: (>, (0,0), 1000), (v, (0, 1), 1), (<, (0,0), 1000)
 < :: (<, (-1,0), 1), (v, (0, 0), 1000), (^, (0,0), 1000)
 ^ :: (>, (0,0), 1000), (^, (0, -1), 1), (<, (0,0), 1000)

*/

struct state
{
    char direction;
    Point position;
    int score;
};

map<char, Point> offsets = {
    {'>', {1, 0}},
    {'^', {0, -1}},
    {'<', {-1, 0}},
    {'v', {0, 1}}};

map<char, vector<state>> transitions = {
    {
        '>',
        {{'>', {1, 0}, 1},
         {'v', {0, 0}, 1000},
         {'^', {0, 0}, 1000}},
    },
    {
        'v',
        {{'>', {0, 0}, 1000},
         {'v', {0, 1}, 1},
         {'<', {0, 0}, 1000}},
    },
    {
        '<',
        {{'<', {-1, 0}, 1},
         {'v', {0, 0}, 1000},
         {'^', {0, 0}, 1000}},
    },
    {
        '^',
        {{'^', {0, -1}, 1},
         {'<', {0, 0}, 1000},
         {'>', {0, 0}, 1000}},
    }};

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
            if (cur_val == 'S')
            {
                S = {col, row};
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

void bfs(tuple<int, int, int, char, vector<tuple<int, int>>> start)
{
    map<tuple<int, int, char>, int> visited;
    vector<tuple<int, int, char, int>> ret;
    priority_queue<tuple<int, int, int, char, vector<tuple<int, int>>>,
                   vector<tuple<int, int, int, char, vector<tuple<int, int>>>>,
                   greater<tuple<int, int, int, char, vector<tuple<int, int>>>>>
        Q;
    tuple<int, int> start_pos = {get<1>(start), get<2>(start)};
    char start_letter = grid[start_pos];
    char cur_letter;
    int cur_score;
    tuple<int, int, int, char, vector<tuple<int, int>>> cur_e, nxt_e;
    tuple<int, int, char> cur, nxt;
    vector<tuple<int, int>> path;
    int x, y, nx, ny;
    char direction;
    Q.push(start);
    int best = 0;
    map<int, set<tuple<int, int>>> best_paths;
    while (!Q.empty())
    {
        cur_e = Q.top();
        Q.pop();
        // x, y, dir
        cur = {get<1>(cur_e), get<2>(cur_e), get<3>(cur_e)};
        cur_score = get<0>(cur_e);
        if (best > 0 && cur_score > best)
        {
            continue;
        }
        x = get<0>(cur);
        y = get<1>(cur);
        cur_letter = grid[{x, y}];

        direction = get<2>(cur);

        if (visited.find(cur) == visited.end() || cur_score <= visited[cur])
        {
            if (cur_letter == 'E')
            {
                if (best == 0 || cur_score <= best)
                {
                    best = cur_score;
                    for (const auto &p : get<4>(cur_e))
                    {
                        best_paths[best].insert(p);
                    }
                }
                continue;
            }
            visited[cur] = cur_score;
            vector<state> &T = transitions[direction];
            for (const auto &S : T)
            {
                nx = x + get<0>(S.position);
                ny = y + get<1>(S.position);
                if (grid.find({nx, ny}) != grid.end() && grid[{nx, ny}] != '#')
                {
                    int nx2 = nx + get<0>(offsets[S.direction]);
                    int ny2 = ny + get<1>(offsets[S.direction]);
                    if (S.direction == direction || (grid.find({nx2, ny2}) != grid.end() && grid[{nx2, ny2}] != '#'))
                    {
                        path = get<4>(cur_e);
                        path.push_back({nx, ny});
                        nxt_e = {cur_score + S.score, nx, ny, S.direction, path};
                        Q.push(nxt_e);
                    }
                }
            }
        }
    }
    cout << "p1: " << best << endl;
    cout << "p2: " << best_paths[best].size() << endl;
}

int main()
{
    if (!make_grid())
    {
        return 1;
    }

    int ans = 0;
    bfs({0, get<0>(S), get<1>(S), '>', {{get<0>(S), get<1>(S)}}});
}
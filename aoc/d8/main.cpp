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
map<char, vector<tuple<int, int>>> antennae;
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
    char cur_val;
    while (std::getline(file, line))
    {
        for (int col = 0; col < line.size(); col++)
        {
            cur_val = line[col];
            grid[{col, row}] = cur_val;
            if (cur_val != '.')
            {
                antennae[cur_val].push_back({col, row});
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

bool in_bounds(tuple<int, int> node)
{
    if (get<0>(node) >= 0)
    {
        if (get<1>(node) >= 0)
        {
            if (get<0>(node) < width)
            {
                if (get<1>(node) < height)
                {
                    return true;
                }
            }
        }
    }
    return false;
}

void count()
{
    set<tuple<int, int, char>> antinodes;
    for (const auto &entry : antennae)
    {
        vector<tuple<int, int>> locs = entry.second;
        for (int i = 0; i < locs.size() - 1; i++)
        {
            tuple<int, int> left = locs[i];
            for (int j = i + 1; j < locs.size(); j++)
            {
                tuple<int, int> right = locs[j];
                int rise1 = get<1>(left) - get<1>(right);
                int run1 = get<0>(left) - get<0>(right);

                int rise2 = get<1>(right) - get<1>(left);
                int run2 = get<0>(right) - get<0>(left);

                tuple<int, int> left_right_antinode = {get<0>(right) + run2, get<1>(right) + rise2};

                if (in_bounds(left_right_antinode))
                {
                    antinodes.insert({get<0>(left_right_antinode), get<1>(left_right_antinode), '.'});
                }

                tuple<int, int> right_left_antinode = {get<0>(left) + run1, get<1>(left) + rise1};

                if (in_bounds(right_left_antinode))
                {
                    antinodes.insert({get<0>(right_left_antinode), get<1>(right_left_antinode), '.'});
                }
            }
        }
    }
    cout << "p1: " << antinodes.size() << endl;
}

void count2()
{
    set<tuple<int, int, char>> antinodes;
    for (const auto &entry : antennae)
    {
        vector<tuple<int, int>> locs = entry.second;
        for (int i = 0; i < locs.size() - 1; i++)
        {
            tuple<int, int> left = locs[i];
            for (int j = i + 1; j < locs.size(); j++)
            {
                tuple<int, int> right = locs[j];
                int rise1 = get<1>(left) - get<1>(right);
                int run1 = get<0>(left) - get<0>(right);

                int rise2 = get<1>(right) - get<1>(left);
                int run2 = get<0>(right) - get<0>(left);

                tuple<int, int> left_right_antinode = {get<0>(left) + run2, get<1>(left) + rise2};

                while (in_bounds(left_right_antinode))
                {
                    antinodes.insert({get<0>(left_right_antinode), get<1>(left_right_antinode), '.'});
                    left_right_antinode = {get<0>(left_right_antinode) + run2, get<1>(left_right_antinode) + rise2};
                }

                tuple<int, int> right_left_antinode = {get<0>(right) + run1, get<1>(right) + rise1};

                while (in_bounds(right_left_antinode))
                {
                    antinodes.insert({get<0>(right_left_antinode), get<1>(right_left_antinode), '.'});
                    right_left_antinode = {get<0>(right_left_antinode) + run1, get<1>(right_left_antinode) + rise1};
                }
            }
        }
    }
    cout << "p2: " << antinodes.size() << endl;
}

int main()
{
    if (!make_grid())
    {
        return 1;
    }

    count();
    count2();
}
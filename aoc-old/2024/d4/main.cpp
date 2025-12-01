#include <iostream>
#include <fstream>
#include <vector>
#include <string>

#include <iostream>
#include <fstream>
#include <string>
#include <map>
#include <tuple>

std::map<int, char> depth_map = {
    {3, 'X'},
    {2, 'M'},
    {1, 'A'},
    {0, 'S'}};

bool checkp1(std::map<std::tuple<int, int>, char> &grid, std::tuple<int, int> start, std::tuple<int, int> offset, int depth)
{
    if (depth < 0)
    {
        return true;
    }
    if (depth_map[depth] != grid[start])
    {
        return false;
    }
    std::tuple<int, int> next = {std::get<0>(start) + std::get<0>(offset), std::get<1>(start) + std::get<1>(offset)};
    return true && checkp1(grid, next, offset, depth - 1);
}

bool checkp2(std::map<std::tuple<int, int>, char> &grid, std::tuple<int, int> start)
{
    if (grid[start] != 'A')
    {
        return false;
    }

    int ss = 0;
    int ms = 0;

    std::tuple<int, int> top_left_pt = {std::get<0>(start) - 1, std::get<1>(start) - 1};
    char top_left_c = grid[top_left_pt];

    std::tuple<int, int> bottom_left_pt = {std::get<0>(start) - 1, std::get<1>(start) + 1};
    char bottom_left_c = grid[bottom_left_pt];

    std::tuple<int, int> top_right_pt = {std::get<0>(start) + 1, std::get<1>(start) - 1};
    char top_right_c = grid[top_right_pt];

    std::tuple<int, int> bottom_right_pt = {std::get<0>(start) + 1, std::get<1>(start) + 1};
    char bottom_right_c = grid[bottom_right_pt];

    for (char e : {top_left_c, top_right_c, bottom_left_c, bottom_right_c})
    {
        switch (e)
        {
        case 'M':
            ms++;
            break;
        case 'S':
            ss++;
            break;
        default:
            return false;
        }
    }
    return (ss == 2 && ms == 2 && top_left_c != bottom_right_c);
}

int main(int argc, char *argv[])
{
    std::ifstream file("p1.txt");
    if (!file.is_open())
    {
        std::cerr << "Error: Unable to open file!" << std::endl;
        return 1;
    }

    std::map<std::tuple<int, int>, char> grid; // Map with (x, y) as keys
    std::string line;
    int row = 0;

    int height = 0;
    int width = 0;

    // Read file line by line
    while (std::getline(file, line))
    {
        for (int col = 0; col < line.size(); ++col)
        {
            // Use (row, col) as the key and the character as the value
            grid[{col, row}] = line[col];
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

    std::vector<std::tuple<int, int>> offsets = {
        {-1, -1}, {-1, 1}, {1, -1}, {1, 1}, {1, 0}, {-1, 0}, {0, -1}, {0, 1}};

    int p1ans = 0;
    int p2ans = 0;
    for (const auto &pair : grid)
    {
        if (checkp2(grid, pair.first))
        {
            p2ans++;
        }
        if (pair.second != 'X')
        {
            continue;
        }
        for (const auto &o : offsets)
        {
            bool matches = checkp1(grid, pair.first, o, 3);
            if (matches)
            {
                p1ans++;
            }
        }
    }
    std::cout << "p1: " << p1ans << std::endl;
    std::cout << "p2: " << p2ans << std::endl;
    return 0;
}

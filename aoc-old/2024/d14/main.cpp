#include <vector>
#include <string>
#include <iostream>
#include <fstream>
#include <sstream>
#include <map>
#include <set>
#include <algorithm>
#include <deque>
#include <regex>

using namespace std;

vector<vector<int>> entries;

vector<tuple<int, int>> p1(int width, int height, int seconds)
{
    vector<tuple<int, int>> updated;
    vector<int> quadrants = {0, 0, 0, 0};
    int px = 0;
    int py = 0;
    int vx = 0;
    int vy = 0;
    for (const auto &entry : entries)
    {
        px = entry[0];
        py = entry[1];
        vx = entry[2];
        vy = entry[3];
        tuple<int, int> e = {(width + (px + vx * seconds) % width) % width, (height + (py + vy * seconds) % height) % height};
        updated.push_back(e);
    }

    int x_axis = (width - 1) / 2;
    int y_axis = (height - 1) / 2;

    for (const auto &entry : updated)
    {
        int x = get<0>(entry);
        int y = get<1>(entry);
        if (x < x_axis)
        {
            if (y < y_axis)
            {
                quadrants[0]++;
            }
            else if (y > y_axis)
            {
                quadrants[1]++;
            }
        }
        else if (x > x_axis)
        {
            if (y < y_axis)
            {
                quadrants[2]++;
            }
            else if (y > y_axis)
            {
                quadrants[3]++;
            }
        }
    }
    int64_t ans = 1;
    for (const auto &entry : quadrants)
    {
        ans *= entry;
    }
    cout << "p1: " << ans << endl;
    return updated;
}

bool init()
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
    std::regex pattern("(-?[0-9]+)");
    while (std::getline(file, line))
    {

        sregex_iterator begin(line.begin(), line.end(), pattern);
        sregex_iterator end;
        for (sregex_iterator i = begin; i != end; ++i)
        {
            smatch match = *i;
            int left = stoi(match.str(1));
            entry.push_back(left);
        }
        entries.push_back(entry);
        entry.clear();
    }

    file.close();

    return true;
}

void print_grid(map<tuple<int, int>, int> &counts)
{
    for (int y = 0; y < 103; y++)
    {
        for (int x = 0; x < 101; x++)
        {
            if (counts.find({x, y}) != counts.end())
            {
                cout << counts[{x, y}];
            }
            else
            {
                cout << ".";
            }
        }
        cout << endl;
    }
}

int main()
{
    if (!init())
    {
        return 1;
    }
    // p1(11, 7, 100);
    p1(101, 103, 100);
    // for (int i = 0; i < 1000; i++)
    // {
    //     map<tuple<int, int>, int> counts;
    //     vector<tuple<int, int>> updated = p1(101, 103, i);
    //     for (const auto &entry : updated)
    //     {
    //         counts[entry]++;
    //     }
    //     print_grid(counts);
    //     cout << endl;
    //     cout << i << endl;
    //     cout << endl;
    // }

    /*
     probably a better way to do this, but i just printed out a bunch
     of grids (see above) and noticed that two "patterns" were repeating
     with cycles of 47 + 103m and 82 + 101n, so i just did a dumb nested
     loop to see when the first time those would overlap would be.
     */
    int p2ans = 0;
    for (int i = 82; i < 100000; i = i + 101)
    {
        for (int j = 47; j < 100000; j = j + 103)
        {
            if (i == j)
            {
                p2ans = i;
                break;
            }
        }
        if (p2ans > 0)
        {
            break;
        }
    }
    cout << "p2: " << p2ans << endl;

    map<tuple<int, int>, int> counts;
    vector<tuple<int, int>> updated = p1(101, 103, p2ans);
    for (const auto &entry : updated)
    {
        counts[entry]++;
    }
    print_grid(counts);

    /*
    1.............................1
    1.............................1
    1.............................1
    1.............................1
    1..............1..............1
    1.............111.............1
    1............11111............1
    1...........1111111...........1
    1..........111111111..........1
    1............11111............1
    1...........1111111...........1
    1..........111111111..........1
    1.........11111111111.........1
    1........1111111111111........1
    1..........111111111..........1
    1.........11111111111.........1
    1........1111111111111........1
    1.......111111111111111.......1
    1......11111111111111111......1
    1........1111111111111........1
    1.......111111111111111.......1
    1......11111111111111111......1
    1.....1111111111111111111.....1
    1....111111111111111111111....1
    1.............111.............1
    1.............111.............1
    1.............111.............1
    1.............................1
    1.............................1
    1.............................1
    1.............................1
    1111111111111111111111111111111.
    */
}
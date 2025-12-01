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

vector<int> disk;
vector<int> disk2;
deque<int> free_segments;
deque<int> used_segments;
map<int, tuple<int, int>> file_stats; // (id, start, size)

bool make_vector()
{
    int file_id = 0;
    ifstream file("p1.txt");
    if (!file.is_open())
    {
        cerr << "Error: Unable to open file!" << endl;
        return false;
    }

    string line;
    char cur_val;
    while (std::getline(file, line))
    {
        for (int col = 0; col < line.size(); col++)
        {
            cur_val = line[col];
            bool in_file = col % 2 == 0;
            int cur_size = cur_val - '0';
            if (in_file)
            {
                file_stats[file_id] = {disk.size(), cur_size};
                for (int i = 0; i < cur_size; i++)
                {
                    disk.push_back(file_id);
                    disk2.push_back(file_id);
                    used_segments.push_back(disk.size() - 1);
                }

                file_id++;
            }
            else
            {
                for (int i = disk.size(); i < cur_size + disk.size(); i++)
                {
                    free_segments.push_back(i);
                }
                for (int i = 0; i < cur_size; i++)
                {
                    disk.push_back(-1);
                    disk2.push_back(-1);
                }
            }
        }
    }

    file.close();
    return true;
}

void defrag()
{
    while (!free_segments.empty())
    {
        int next_free = free_segments.front();
        free_segments.pop_front();
        int to_move = used_segments.back();
        used_segments.pop_back();
        if (to_move <= next_free)
        {
            break;
        }
        disk[next_free] = disk[to_move];
        disk[to_move] = -1;
    }
}

void defrag2()
{
    for (int i = file_stats.size() - 1; i >= 0; i--)
    {
        bool moved = false;
        tuple<int, int> stats = file_stats[i];
        int file_start = get<0>(stats);
        int file_size = get<1>(stats);
        int cur = 0;
        int end = 0;
        while (!moved && cur < file_start)
        {
            if (disk2[cur] != -1)
            {
                cur++;
                continue;
            }
            end = cur;
            while (disk2[end + 1] == -1)
            {
                end++;
            }
            if (end - cur + 1 < file_size)
            {
                cur = end + 1;
                continue;
            }
            for (int k = cur; k < cur + file_size; k++)
            {
                disk2[k] = i;
            }
            for (int k = file_start; k < file_start + file_size; k++)
            {
                disk2[k] = -1;
            }
            moved = true;
        }
    }
}

int64_t checksum2()
{
    int64_t ret = 0;
    for (int i = 0; i < disk2.size(); i++)
    {
        int id = disk2[i];
        if (id == -1)
        {
            continue;
        }
        ret += id * i;
    }
    return ret;
}

int64_t checksum()
{
    int64_t ret = 0;
    for (int i = 0; i < disk.size(); i++)
    {
        int id = disk[i];
        if (id == -1)
        {
            break;
        }
        ret += id * i;
    }
    return ret;
}

int main()
{
    make_vector();
    defrag();
    defrag2();
    cout << "p1: " << checksum() << endl;
    cout << "p2: " << checksum2() << endl;
}
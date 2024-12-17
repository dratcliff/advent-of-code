#include <vector>
#include <string>
#include <iostream>
#include <fstream>
#include <sstream>
#include <map>
#include <set>
#include <algorithm>
#include <queue>
#include <cmath>

using namespace std;

map<char, int64_t> registers = {
    {'A', 66752888},
    {'B', 0},
    {'C', 0}};

vector<int64_t> program = {

    2, 4, 1, 7, 7, 5, 1, 7, 0, 3, 4, 1, 5, 5, 3, 0};

string found_it = ",2,4,1,7,7,5,1,7,0,3,4,1,5,5,3,0";

map<tuple<int, int, int>, vector<int>> counts;

int64_t to_combo(int64_t operand)
{
    if (operand <= 3)
    {
        return operand;
    }
    if (operand == 4)
    {
        return registers['A'];
    }
    if (operand == 5)
    {
        return registers['B'];
    }
    if (operand == 6)
    {
        return registers['C'];
    }
    return -1;
}

int64_t exec(int64_t idx, int64_t opcode, int64_t operand, vector<int64_t> &outt)
{
    int64_t iptr = -1;
    int v;
    switch (opcode)
    {
    case 0:
        registers['A'] = registers['A'] / (pow(2, to_combo(operand)));
        break;
    case 1:
        registers['B'] = registers['B'] ^ operand;
        break;
    case 2:
        registers['B'] = (to_combo(operand) % 8);
        break;
    case 3:
        if (registers['A'] != 0)
        {
            iptr = operand;
        }
        break;
    case 4:
        registers['B'] = registers['B'] ^ registers['C'];
        break;
    case 5:
        outt.push_back(to_combo(operand) % 8);
        break;
    case 6:
        registers['B'] = registers['A'] / (pow(2, to_combo(operand)));
        break;
    case 7:
        registers['C'] = registers['A'] / (pow(2, to_combo(operand)));
        break;
    default:
        break;
    }
    return iptr;
}

int main()
{
    int64_t iptr = 0;
    int64_t nptr;
    vector<int64_t> outt;
    set<string> seen;
    while (iptr < program.size())
    {
        nptr = exec(0, program[iptr], program[iptr + 1], outt);
        if (nptr != -1)
        {
            iptr = nptr;
        }
        else
        {
            iptr += 2;
        }
    }
    cout << "p1: ";
    for (int z = 0; z < outt.size() - 1; z++)
    {
        cout << outt[z];
        cout << ",";
    }
    cout << outt[outt.size() - 1] << endl;
    int64_t i = 0;

    while (true)
    {
        registers['A'] = i;
        outt.clear();
        iptr = 0;
        nptr = 0;
        while (iptr < program.size())
        {
            nptr = exec(i, program[iptr], program[iptr + 1], outt);
            if (nptr != -1)
            {
                iptr = nptr;
            }
            else
            {
                iptr += 2;
            }
        }

        int j = outt.size() - 1;
        int k = program.size() - 1;
        string s;
        while (j >= 0)
        {
            if (outt[j] == program[k])
            {
                s = "," + to_string(outt[j]) + s;
            }
            else
            {
                break;
            }
            j -= 1;
            k -= 1;
        }
        if (s.size() > 0)
        {
            if (seen.find(s) == seen.end())
            {
                seen.insert(s);
                if (s != found_it)
                {
                    i *= 8;
                }
                else
                {
                    cout << "p2: " << i << endl;
                    break;
                }
            }
            else
            {
                i++;
            }
        }
        else
        {

            i++;
        }
    }
    return 0;
}
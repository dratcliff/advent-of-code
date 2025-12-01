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
#include <unordered_set>
#include <stack>
#include <optional>

using namespace std;

map<string, int> values;
long long x, y;
vector<tuple<string, char, string, string>> gates;
vector<int> gate_ids;

vector<string> split(const string &input, char delimiter)
{
    vector<string> result;
    size_t start = 0;
    size_t pos;

    while ((pos = input.find(delimiter, start)) != string::npos)
    {
        result.push_back(input.substr(start, pos - start));
        start = pos + 1;
    }
    if (start < input.size())
    {
        result.push_back(input.substr(start));
    }

    return result;
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
    vector<string> tokens;
    while (getline(file, line))
    {

        tokens = split(line, ' ');
        if (tokens.size() == 2)
        {
            string left = tokens[0];
            left.pop_back();
            int right = stoi(tokens[1]);
            values[left] = right;
        }
        else if (tokens.size() == 5)
        {
            string left = tokens[0];
            string op = tokens[1];
            string right = tokens[2];
            string dest = tokens[4];
            char opc;
            if (op == "AND")
            {
                opc = '&';
            }
            else if (op == "OR")
            {
                opc = '|';
            }
            else
            {
                opc = '^';
            }
            gates.push_back({left, opc, right, dest});
            if (values.find(left) == values.end())
            {
                values[left] = -1;
            }
            if (values.find(right) == values.end())
            {
                values[right] = -1;
            }
            if (values.find(dest) == values.end())
            {
                values[dest] = -1;
            }
        }
    }

    string xs, ys;
    for (const auto &v : values)
    {
        if (v.first.find('x') != string::npos)
        {
            if (v.second == 1)
            {
                xs.push_back('1');
            }
            else
            {
                xs.push_back('0');
            }
        }
    }
    for (const auto &v : values)
    {
        if (v.first.find('y') != string::npos)
        {
            if (v.second == 1)
            {
                ys.push_back('1');
            }
            else
            {
                ys.push_back('0');
            }
        }
    }
    reverse(xs.begin(), xs.end());
    reverse(ys.begin(), ys.end());
    x = stoll(xs, nullptr, 2);
    y = stoll(ys, nullptr, 2);

    for (int i = 0; i < gates.size(); i++)
    {
        gate_ids.push_back(i);
    }

    file.close();
    return true;
}

long long p1(map<string, int> values, vector<tuple<string, char, string, string>> gates)
{
    bool done = false;
    string left, right, dest;
    char op;
    bool updated = false;
    int i = 0;
    while (!done)
    {
        i++;
        if (i > 60)
        {
            return -1;
        }
        done = true;
        for (const auto &gate : gates)
        {
            left = get<0>(gate);
            op = get<1>(gate);
            right = get<2>(gate);
            dest = get<3>(gate);
            if (values[left] != -1 && values[right] != -1 && values[dest] == -1)
            {
                updated = true;
                switch (op)
                {
                case '^':
                    values[dest] = values[left] != values[right];
                    break;
                case '&':
                    if (values[left] == 1 && values[right] == 1)
                    {
                        values[dest] = 1;
                    }
                    else
                        values[dest] = 0;
                    break;
                case '|':
                    if (values[left] + values[right] > 0)
                    {
                        values[dest] = 1;
                    }
                    else
                        values[dest] = 0;
                    break;
                }
            }
        }
        for (const auto &kv : values)
        {
            if (kv.first.find('z') != string::npos && kv.second == -1)
            {
                done = false || !updated;
            }
        }
    }
    string res;
    for (const auto &v : values)
    {
        if (v.first.find('z') != string::npos)
        {
            if (v.second == 1)
            {
                res.push_back('1');
            }
            else
            {
                res.push_back('0');
            }
        }
    }
    reverse(res.begin(), res.end());
    // cout << res << endl;
    long long ans = stoll(res, nullptr, 2);
    // cout << "p1: " << ans << endl;
    // cout << i << endl;
    return ans;
}

void p2()
{
    // x00 & y00 -> sgv
    // x00 ^ y00 -> z00

    // x01 ^ y01 -> ntn
    // x01 & y01 -> gmn
    // sgv ^ ntn -> z01
    // sgv & ntn -> rsk
    // rsk | gmn > vbb

    // x02 ^ y02 -> gcd
    // x02 & y02 -> jtv
    // gcd ^ vbb -> z02
    // gcd & vbb -> mpg
    // mpg | jtv -> jmc

    // just doing this manually, i.e.,
    // running p2() with the given input will show discrepancies in the output
    // fix them manually, then move on
    // fixed so far:
    // mkk,z10,qbw,z14,cvp,wjb,wcb,z34
    // alphabetically: cvp,mkk,qbw,wcb,wjb,z10,z14,z34

    // this code is awful, but that's fine
    map<string, map<string, string>> ands;
    map<string, map<string, string>> ors;
    map<string, map<string, string>> xors;
    string carry, out;
    string left;
    string right;
    char op;
    string dest;
    string xt = "x00";
    string yt = "y00";

    for (const auto &g : gates)
    {
        left = get<0>(g);
        right = get<2>(g);
        op = get<1>(g);
        dest = get<3>(g);
        if (op == '^')
        {
            xors[left][right] = dest;
            xors[right][left] = dest;
        }
        else if (op == '|')
        {
            ors[left][right] = dest;
            ors[right][left] = dest;
        }
        else if (op == '&')
        {
            ands[left][right] = dest;
            ands[right][left] = dest;
        }
    }
    carry = ands["y00"]["x00"];
    dest = xors["y00"]["x00"];
    cout << carry << "," << dest << endl;
    cout << endl;

    string prev_carry = carry;
    string temp_dest = xors["y01"]["x01"];
    string temp_carry = ands["y01"]["x01"];
    string new_dest = xors[prev_carry][temp_dest];
    carry = ands[prev_carry][temp_dest];
    string something = ors[carry][temp_carry];
    string prev_something = something;
    cout << "x01 ^ y01 = " << temp_dest << endl;
    cout << "x01 & y01 = " << temp_carry << endl;
    cout << something << " ^ " << temp_dest << " = " << new_dest << endl;
    cout << something << " & " << temp_dest << " = " << carry << endl;
    cout << carry << " | " << temp_carry << " = " << something << endl;
    cout << endl;

    prev_carry = carry;
    temp_dest = xors["y02"]["x02"];
    temp_carry = ands["y02"]["x02"];
    new_dest = xors[prev_something][temp_dest];
    carry = ands[prev_something][temp_dest];
    prev_something = something;
    something = ors[carry][temp_carry];
    cout << "x02 ^ y02 = " << temp_dest << endl;
    cout << "x02 & y02 = " << temp_carry << endl;
    cout << prev_something << " ^ " << temp_dest << " = " << new_dest << endl;
    cout << prev_something << " & " << temp_dest << " = " << carry << endl;
    cout << carry << " | " << temp_carry << " = " << something << endl;
    cout << endl;

    prev_carry = carry;
    temp_dest = xors["y03"]["x03"];
    temp_carry = ands["y03"]["x03"];
    prev_something = something;
    new_dest = xors[prev_something][temp_dest];
    carry = ands[prev_something][temp_dest];
    something = ors[carry][temp_carry];
    cout << "x03 ^ y03 = " << temp_dest << endl;
    cout << "x03 & y03 = " << temp_carry << endl;
    cout << prev_something << " ^ " << temp_dest << " = " << new_dest << endl;
    cout << prev_something << " & " << temp_dest << " = " << carry << endl;
    cout << carry << " | " << temp_carry << " = " << something << endl;
    cout << endl;

    for (int i = 4; i < 10; i++)
    {
        prev_carry = carry;
        temp_dest = xors["y0" + to_string(i)]["x0" + to_string(i)];
        temp_carry = ands["y0" + to_string(i)]["x0" + to_string(i)];
        prev_something = something;
        new_dest = xors[prev_something][temp_dest];
        carry = ands[prev_something][temp_dest];
        something = ors[carry][temp_carry];
        cout << "x0" << to_string(i) << " ^ y0" << to_string(i) << " = " << temp_dest << endl;
        cout << "x0" << to_string(i) << " & y0" << to_string(i) << " = " << temp_carry << endl;
        cout << prev_something << " ^ " << temp_dest << " = " << new_dest << endl;
        cout << prev_something << " & " << temp_dest << " = " << carry << endl;
        cout << carry << " | " << temp_carry << " = " << something << endl;
        cout << endl;
    }
    for (int i = 10; i < 45; i++)
    {
        prev_carry = carry;
        temp_dest = xors["y" + to_string(i)]["x" + to_string(i)];
        temp_carry = ands["y" + to_string(i)]["x" + to_string(i)];
        prev_something = something;
        new_dest = xors[prev_something][temp_dest];
        carry = ands[prev_something][temp_dest];
        something = ors[carry][temp_carry];
        cout << "x" << to_string(i) << " ^ y" << to_string(i) << " = " << temp_dest << endl;
        cout << "x" << to_string(i) << " & y" << to_string(i) << " = " << temp_carry << endl;
        cout << prev_something << " ^ " << temp_dest << " = " << new_dest << endl;
        cout << prev_something << " & " << temp_dest << " = " << carry << endl;
        cout << carry << " | " << temp_carry << " = " << something << endl;
        cout << endl;
    }
}

int main()
{
    if (!init())
    {
        return 1;
    }
    long long ans;
    ans = p1(values, gates);

    p2();

    cout << x << ",,," << y << ",,," << ans << endl;
}
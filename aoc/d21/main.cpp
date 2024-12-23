#include <vector>
#include <string>
#include <iostream>
#include <fstream>
#include <sstream>
#include <map>
#include <set>
#include <algorithm>
#include <deque>
#include <conio.h>

using namespace std;
using Point = tuple<int, int>;

map<char, map<char, char>> dmoves = {
    {'v',
     {{'>', '>'},
      {'<', '<'},
      {'^', '^'}}},
    {'^',
     {
         {'>', 'A'},
         {'v', 'v'},
     }},
    {'>',
     {{'<', 'v'},
      {'^', 'A'}}},
    {'<',
     {{'>', 'v'}}},
    {'A',
     {{'<', '^'},
      {'v', '>'}}}};

map<char, map<char, char>> nmoves = {
    {'v', {
              {'7', '4'},
              {'8', '5'},
              {'9', '6'},
              {'4', '1'},
              {'5', '2'},
              {'6', '3'},
              {'2', '0'},
              {'3', 'A'},
          }},
    {'<', {
              {'8', '7'},
              {'5', '4'},
              {'2', '1'},
              {'9', '8'},
              {'6', '5'},
              {'3', '2'},
              {'A', '0'},
          }},
    {'>', {
              {'7', '8'},
              {'4', '5'},
              {'1', '2'},
              {'8', '9'},
              {'5', '6'},
              {'2', '3'},
              {'0', 'A'},
          }},
    {'^', {{'4', '7'}, {'5', '8'}, {'6', '9'}, {'1', '4'}, {'2', '5'}, {'3', '6'}, {'0', '2'}, {'A', '3'}}}};

vector<string> split_with_delimiter(const string &input, char delimiter)
{
    vector<string> result;
    size_t start = 0;
    size_t pos;

    while ((pos = input.find(delimiter, start)) != string::npos)
    {
        result.push_back(input.substr(start, pos - start + 1));
        start = pos + 1;
    }

    if (start < input.size())
    {
        result.push_back(input.substr(start));
    }

    return result;
}

map<string, set<string>> ec;

set<string> expand(const string &kp)
{

    if (kp == "A")
    {
        return {"A"};
    }
    /*
        ^ A
      < v >

      <A means press < then press A, i.e.,
      search until < then press A, search from < to A then press A
    */
    int best = 0;
    vector<char> press_target, to_press, to_press_nxt;
    for (const auto &s : kp)
    {
        press_target.push_back(s);
    }
    if (ec.find(kp) != ec.end())
    {
        return ec[kp];
    }
    string path, path_nxt;
    tuple<char, char> cur, nxt;
    set<string> visited;
    pair<string, string> entry;
    tuple<tuple<char, char>, string, vector<char>> cur_state;
    deque<tuple<tuple<char, char>, string, vector<char>>> Q;
    for (const auto &m : dmoves['A'])
    {
        to_press = press_target;
        Q.push_back({{'A', m.second}, {m.first}, to_press});
    }

    while (!Q.empty())
    {
        cur_state = Q.front();
        Q.pop_front();
        cur = get<0>(cur_state);
        path = get<1>(cur_state);
        to_press = get<2>(cur_state);
        if (best > 0 && path.size() > best)
        {
            break;
        }
        if (to_press.empty())
        {
            if (best == 0 || path.size() <= best)
            {
                best = path.size();
                ec[kp].insert(path);
            }
            continue;
        }
        if (visited.find(path) == visited.end())
        {
            visited.insert(path);
            if (get<1>(cur) == to_press.front())
            {
                to_press_nxt = to_press;
                to_press_nxt.erase(to_press_nxt.begin());
                path_nxt = path;
                path_nxt += "A";
                Q.push_back({cur, path_nxt, to_press_nxt});
            }
            else
            {
                for (const auto &m : dmoves[get<1>(cur)])
                {
                    to_press_nxt = to_press;
                    path_nxt = path;
                    path_nxt.push_back(m.first);
                    nxt = {get<1>(cur), m.second};
                    Q.push_back({nxt, path_nxt, to_press_nxt});
                }
            }
        }
    }
    return ec[kp];
}

map<string, string> something;
map<tuple<string, int>, set<string>> ec2;
set<string> seen_tokens;

set<string> expand2(const string &kp, int iterations)
{
    tuple<string, int> key = {kp, iterations};
    if (ec2.find(key) != ec2.end())
    {
        return ec2[key];
    }
    vector<string> tokens = split_with_delimiter(kp, 'A');
    for (const auto &t : tokens)
    {
        if (seen_tokens.find(t) == seen_tokens.end())
        {
            seen_tokens.insert(t);
        }
    }
    set<string> tokens2;
    set<string> tokens3;
    string s;
    while (!tokens.empty())
    {
        string t = tokens[0];
        tokens.erase(tokens.begin());
        set<string> expanded;
        set<string> expansions;
        expanded = expand(t);
        for (const auto &e : expanded)
        {
            something[e] = t;
            if (tokens2.empty())
            {
                tokens3.insert(e);
            }
            else
            {
                for (const auto &t : tokens2)
                {
                    tokens3.insert(t + e);
                }
            }
        }
        tokens2 = tokens3;
        tokens3.clear();
    }
    for (int i = 1; i < iterations; i++)
    {
        for (const auto &t : tokens2)
        {
            set<string> expanded;
            set<string> expansions;
            expanded = expand2(t, iterations - i);
            for (const auto &e : expanded)
            {
                something[e] = t;
                tokens3.insert(e);
            }
        }
        tokens2 = tokens3;
        tokens3.clear();
    }
    ec2[key] = tokens2;
    return tokens2;
}

set<string> numpad_kps(string code)
{
    int best = 0;
    set<string> best_paths;
    vector<char> to_find;
    for (const auto &c : code)
    {
        to_find.push_back(c);
    }
    deque<tuple<char, vector<char>, vector<char>, set<tuple<char, char>>>> Q;
    vector<char> path;
    set<tuple<char, char>> visited; // number, direction
    char cur;
    vector<char> pressed;
    tuple<char, vector<char>, vector<char>, set<tuple<char, char>>> cur_state;
    int depth;
    Q.push_back({'A', {}, {}, {}});
    while (!Q.empty())
    {
        cur_state = Q.front();
        Q.pop_front();
        path = get<1>(cur_state);
        cur = get<0>(cur_state);
        pressed = get<2>(cur_state);
        if (pressed == to_find)
        {
            if (best == 0 || path.size() < best)
            {
                best = path.size();
                best_paths.clear();
            }

            string s2;
            for (const auto &p : path)
            {
                s2 += p;
            }
            if (best != 0 && path.size() == best)
            {
                best_paths.insert(s2);
            }
            continue;
        }
        visited = get<3>(cur_state);
        if (path.size() == 0 || visited.find({cur, path.back()}) == visited.end())
        {
            if (path.size() != 0)
            {
                visited.insert({cur, path.back()});
            }
            for (const auto &pair : nmoves)
            {
                char dir = pair.first;
                if (pair.second.find(cur) != pair.second.end())
                {
                    map<char, char> p = pair.second;
                    char nxt = p[cur];
                    pressed = get<2>(cur_state);
                    visited = get<3>(cur_state);
                    path = get<1>(cur_state);
                    int num_pressed = pressed.size();
                    if (to_find[num_pressed] == cur)
                    {
                        path.push_back('A');
                        pressed.push_back(cur);
                    }
                    if (pressed.size() != to_find.size())
                    {
                        path.push_back(dir);
                    }
                    if (best == 0 || path.size() < best)
                    {
                        Q.push_back({nxt, path, pressed, visited});
                    }
                }
            }
        }
    }
    return best_paths;
}

map<tuple<string, int>, long long> cost_cache;
long long cost(string kp, int depth)
{
    if (depth == 0)
    {
        return kp.size();
    }
    tuple<string, int> cache_key = {kp, depth};
    if (cost_cache.find(cache_key) != cost_cache.end())
    {
        return cost_cache[cache_key];
    }
    vector<string> kps = split_with_delimiter(kp, 'A');
    long long total = 0;
    for (const auto &kp2 : kps)
    {
        set<string> nxtkps = expand2(kp2, 1);
        long long best = 0, C = 0;
        for (const auto &nxt_kp : nxtkps)
        {
            C = cost(nxt_kp, depth - 1);
            if (best == 0 || C < best)
            {
                best = C;
            }
        }
        total += best;
    }
    cost_cache[cache_key] = total;
    return total;
}

long long get_complexity(int robots)
{
    // with the amount of time i ended up spending on this, i could've just parsed the text
    vector<tuple<int, string>> codes = {
        {638, "638A"},
        {965, "965A"},
        {780, "780A"},
        {803, "803A"},
        {246, "246A"}};

    int id;
    string kp;
    long long complexity = 0;
    for (const auto &c : codes)
    {
        id = get<0>(c);
        kp = get<1>(c);
        long long cur_cost = 0, best = 0;
        string best_path = "";
        for (const auto &M : numpad_kps(kp))
        {
            cur_cost = cost(M, robots);
            if (best == 0 || cur_cost < best)
            {
                best = cur_cost;
                best_path = M;
            }
        }
        complexity += best * id;
    }
    return complexity;
}

int main()
{
    cout << "p1: " << get_complexity(2) << endl;
    cout << "p2: " << get_complexity(25) << endl;
    return 0;
}
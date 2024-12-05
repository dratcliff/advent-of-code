#include <vector>
#include <string>
#include <iostream>
#include <fstream>
#include <sstream>
#include <map>
#include <set>
#include <algorithm>

using namespace std;

int main(int argc, char *argv[])
{
    ifstream file("p1.txt");
    if (!file.is_open())
    {
        cerr << "Error: Unable to open file!" << endl;
        return 1;
    }

    map<int, set<int>> not_before;
    string line;
    int row = 0;

    int height = 0;
    int width = 0;

    int ans = 0;
    int ans2 = 0;
    while (getline(file, line))
    {

        bool contains_pipe = line.find('|') != string::npos;
        if (contains_pipe)
        {
            stringstream ss(line);
            string token;
            vector<string> tokens;
            while (getline(ss, token, '|'))
            {
                tokens.push_back(token);
            }
            not_before[stoi(tokens[1])].insert(stoi(tokens[0]));
        }

        bool contains_comma = line.find(',') != string::npos;
        if (contains_comma)
        {
            stringstream ss(line);
            string token;
            vector<int> tokens;
            while (getline(ss, token, ','))
            {
                tokens.push_back(stoi(token));
            }
            bool valid = true;
            for (int i = 0; i < tokens.size(); i++)
            {
                int cur = tokens[i];
                for (int j = i + 1; j < tokens.size(); j++)
                {
                    int nxt = tokens[j];
                    if (not_before[cur].find(nxt) != not_before[cur].end())
                    {
                        valid = false;
                    }
                }
            }
            if (valid)
            {
                int middle = (tokens.size() - 1) / 2;
                ans += tokens[middle];
            }
            else
            {
                sort(tokens.begin(), tokens.end(), [&not_before](int a, int b)
                     { 
                    // a < b means a is in not_before[b]
                    return not_before[b].find(a) != not_before[b].end(); });
                int middle = (tokens.size() - 1) / 2;
                ans2 += tokens[middle];
            }
        }
    }

    cout << "ans: " << ans << endl;
    cout << "ans2: " << ans2 << endl;

    file.close();

    return 0;
}

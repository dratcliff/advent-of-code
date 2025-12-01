#include <iostream>
#include <fstream>
#include <string>
#include <vector>
#include <regex>

int main()
{
    std::string filename = "p1.txt";
    std::ifstream file(filename);
    std::vector<std::string> lines;

    if (!file.is_open())
    {
        std::cerr << "Failed to open the file!" << std::endl;
        return 1;
    }

    std::string line;
    while (std::getline(file, line))
    {
        lines.push_back(line);
    }

    file.close();

    std::regex pattern("mul\\(([0-9]+),([0-9]+)\\)");
    int total = 0;
    for (const std::string &str : lines)
    {

        std::sregex_iterator begin(str.begin(), str.end(), pattern);
        std::sregex_iterator end;
        for (std::sregex_iterator i = begin; i != end; ++i)
        {
            std::smatch match = *i;
            int left = std::stoi(match.str(1));
            int right = std::stoi(match.str(2));
            total += left * right;
        }
    }
    std::cout << "ans: " << total << std::endl;

    std::regex pattern2("do\\(\\)|mul\\(([0-9]+),([0-9]+)\\)|don't\\(\\)");
    int total2 = 0;
    bool enabled = true;
    for (const std::string &str : lines)
    {

        std::sregex_iterator begin(str.begin(), str.end(), pattern2);
        std::sregex_iterator end;
        for (std::sregex_iterator i = begin; i != end; ++i)
        {
            std::smatch match = *i;
            if (match[1].length() == 0)
            {
                if (match[0].str() == "do()")
                {
                    enabled = true;
                }
                else
                {
                    enabled = false;
                }
            }
            else
            {
                if (enabled)
                {
                    int left = std::stoi(match[1]);
                    int right = std::stoi(match[2]);
                    total2 += left * right;
                }
            }
        }
    }
    std::cout << "ans2: " << total2 << std::endl;

    return 0;
}

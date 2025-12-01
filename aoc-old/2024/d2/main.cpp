#include <iostream>
#include <fstream>
#include <sstream>
#include <vector>
#include <string>

bool check(std::vector<int> row)
{
    bool all_increasing = true;
    bool all_decreasing = true;
    bool levels_safe = true;
    for (size_t j = 1; j < row.size(); j++)
    {
        int left = row[j - 1];
        int right = row[j];
        if (left <= right)
        {
            all_decreasing = false;
        }
        if (left >= right)
        {
            all_increasing = false;
        }
        int diff = std::abs(left - right);
        if (diff < 1 || diff > 3)
        {
            levels_safe = false;
        }
    }
    if ((all_decreasing || all_increasing) && levels_safe)
    {
        return true;
    }
    return false;
}

int main()
{
    std::ifstream file("p1.txt"); // Open the file
    if (!file)
    {
        std::cerr << "Unable to open file." << std::endl;
        return 1;
    }

    std::vector<std::vector<int>> data; // Container for storing the list of lists
    std::string line;

    while (std::getline(file, line))
    {                                 // Read each line
        std::istringstream iss(line); // Create a stringstream for the line
        std::vector<int> row;
        int number;

        while (iss >> number)
        { // Extract integers from the line
            row.push_back(number);
        }

        if (!row.empty())
        { // Add non-empty rows to the main vector
            data.push_back(row);
        }
    }

    file.close(); // Close the file

    int ans = 0;
    for (size_t i = 0; i < data.size(); i++)
    {
        auto &row = data[i];

        if (check(row))
        {
            ans += 1;
        }
    }
    std::cout << "ans: " << ans << std::endl;

    int p2ans = 0;
    for (size_t i = 0; i < data.size(); i++)
    {
        auto &row = data[i];

        if (check(row))
        {
            p2ans += 1;
        }
        else
        {
            bool could_fix = false;
            for (size_t j = 0; j < row.size(); j++)
            {
                std::vector<int> new_list;

                // Copy all elements except the one at index_to_remove
                for (size_t k = 0; k < row.size(); ++k)
                {
                    if (k != j)
                    {
                        new_list.push_back(row[k]);
                    }
                }
                if (check(new_list))
                {
                    could_fix = true;
                    break;
                }
            }
            if (could_fix)
            {
                p2ans += 1;
            }
        }
    }
    std::cout << "p2ans: " << p2ans << std::endl;

    return 0;
}
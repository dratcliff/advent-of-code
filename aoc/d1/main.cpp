#include <iostream>
#include <fstream>
#include <vector>
#include <algorithm>
#include <unordered_map>

int main()
{
    std::ifstream file("p1.txt");
    if (!file)
    {
        std::cerr << "Unable to open file." << std::endl;
        return 1;
    }

    std::vector<int> array1, array2;
    int a, b;

    while (file >> a >> b)
    {
        array1.push_back(a);
        array2.push_back(b);
    }

    file.close();

    std::sort(array1.begin(), array1.end());
    std::sort(array2.begin(), array2.end());

    int ans = 0;

    for (size_t i = 0; i < array1.size(); i++)
    {
        ans += std::abs(array1[i] - array2[i]);
    }

    std::cout << "p1: " << ans << std::endl;

    std::unordered_map<int, int> counter;
    for (int num : array2)
    {
        counter[num]++;
    }

    int p2ans = 0;
    for (int num : array1)
    {
        if (counter.find(num) != counter.end())
        {
            p2ans += num * counter[num];
        }
    }

    std::cout << "p2: " << p2ans << std::endl;

    return 0;
}
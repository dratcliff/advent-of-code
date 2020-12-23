package org.drat;

import java.util.HashMap;
import java.util.List;
import java.util.Map;

public class Day3 {
    static void run(List<String> strings) {
        Map<Integer, Map<Integer, Character>> grid = new HashMap<>();
        for (int i = 0; i < strings.size(); i++) {
            grid.put(i, new HashMap<>());
        }
        for (int i = 0; i < strings.size(); i++) {
            String line = strings.get(i);
            Map<Integer, Character> row = grid.get(i);
            char[] chars = line.toCharArray();
            for (int j = 0; j < chars.length; j++) {
                row.put(j, chars[j]);
            }
        }
        for (int i = 0; i < grid.size(); i++) {
            System.out.println(grid.get(i));
        }
    }

    public static void main(String[] args) {
        List<String> strings = AocUtils.fileToStrings("Day3sample.txt");
        run(strings);
    }
}

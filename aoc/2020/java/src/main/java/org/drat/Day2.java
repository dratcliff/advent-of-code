package org.drat;

import java.util.List;

public class Day2 {

    static void run(List<String> strings) {
        int count = 0;
        for (String string : strings) {
            String[] split = string.split(" ");
            String password = split[2];
            String range = split[0];
            char character = split[1].replace(":", "").toCharArray()[0];
            String[] characters = range.split("-");
            int low = Integer.parseInt(characters[0]);
            int high = Integer.parseInt(characters[1]);
            long charCount = password.chars().filter(value -> value == character).count();
            if (charCount <= high && charCount >= low) {
                count++;
            }
        }
        System.out.println(count);
    }

    static void run2(List<String> strings) {
        int count = 0;
        for (String string : strings) {
            String[] split = string.split(" ");
            String password = split[2];
            String range = split[0];
            char character = split[1].replace(":", "").toCharArray()[0];
            String[] characters = range.split("-");
            int first = Integer.parseInt(characters[0]);
            int second = Integer.parseInt(characters[1]);
            if ((password.charAt(first-1) == character) !=
                    (password.charAt(second-1) == character)) {
                count++;
            }
        }
        System.out.println(count);
    }

    public static void main(String[] args) {
        List<String> strings = AocUtils.fileToStrings("Day2sample.txt");
        run(strings);
        strings = AocUtils.fileToStrings("Day2.txt");
        run(strings);
        strings = AocUtils.fileToStrings("Day2sample.txt");
        run2(strings);
        strings = AocUtils.fileToStrings("Day2.txt");
        run2(strings);
    }

}

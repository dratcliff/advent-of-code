package org.drat;

import com.github.dakusui.combinatoradix.Combinator;

import java.util.List;
import java.util.stream.Collectors;

public class Day1 {

    public static void run(List<String> strings) {
        List<Integer> ints = strings.stream()
                .map(Integer::valueOf).collect(Collectors.toList());
        for (List<Integer> each : new Combinator<>(ints, 2)) {
            if (each.get(0) + each.get(1) == 2020) {
                System.out.println(each.get(0) * each.get(1));
            }
        }
    }

    public static void run2(List<String> strings) {
        List<Integer> ints = strings.stream()
                .map(Integer::valueOf).collect(Collectors.toList());
        for (List<Integer> each : new Combinator<>(ints, 3)) {
            int sum = each.get(0) + each.get(1) + each.get(2);
            if (sum == 2020) {
                System.out.printf("%d%n", each.get(0) * each.get(1) * each.get(2));
            }
        }
    }

    public static void main(String[] args) {
        List<String> strings = AocUtils.fileToStrings("Day1sample.txt");
        run(strings);
        strings = AocUtils.fileToStrings("Day1.txt");
        run(strings);
        strings = AocUtils.fileToStrings("Day1sample.txt");
        run2(strings);
        strings = AocUtils.fileToStrings("Day1.txt");
        run2(strings);
    }
}

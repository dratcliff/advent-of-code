package org.drat;

import java.util.List;

import static org.junit.jupiter.api.Assertions.*;

class AocUtilsTest {

    @org.junit.jupiter.api.Test
    void fileToStrings() {
        List<String> strings = AocUtils.fileToStrings("Day1.txt");
        for (String string : strings) {
            System.out.println(string + ":" + string.length());
        }
    }
}
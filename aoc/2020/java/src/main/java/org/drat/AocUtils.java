package org.drat;

import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.List;

public class AocUtils {
    public static List<String> fileToStrings(String filename) {
        try {
            return Files.readAllLines(Path.of("src/main/resources", filename));
        } catch (IOException e) {
            throw new RuntimeException(e);
        }
    }
}

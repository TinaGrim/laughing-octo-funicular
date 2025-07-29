
import java.util.List;
import java.util.ArrayList;

public class tempCodeRunnerFile {
    public static void main(String[] args) {

        List<String> fileNames = new ArrayList<>();
        for (int i = 2; i <= 10; i++) {
            fileNames.add("Driver" + i + ".py");
            System.out.println("Created : " + fileNames.get(i - 2));
        }
    }
}

import java.nio.file.*;

public class Driver {
    public static void main(String[] args) {
        try{
            String content = Files.readString(Paths.get("Driver1.py"));

            for (int i = 2; i <= 10; i++) {
                String fileName = "Driver" + i + ".py";
                Files.writeString(Paths.get(fileName), content);
                System.out.println("Created file: " + fileName);
            }


        } catch (Exception e) {
            System.out.println("Error: " + e.getMessage());
        }
    }
}
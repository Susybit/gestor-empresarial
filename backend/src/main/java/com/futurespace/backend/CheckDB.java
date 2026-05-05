
import java.sql.*;

public class CheckDB {
    public static void main(String[] args) {
        String url = "jdbc:mysql://localhost:3306/practica?useSSL=false&serverTimezone=UTC";
        String user = "root";
        String password = "";
        
        try (Connection conn = DriverManager.getConnection(url, user, password)) {
            Statement stmt = conn.createStatement();
            ResultSet rs = stmt.executeQuery("SELECT TX_EMAIL, TX_PASSWORD FROM US_USUARIOS");
            System.out.println("--- USUARIOS ENCONTRADOS ---");
            while (rs.next()) {
                System.out.println("Email: [" + rs.getString("TX_EMAIL") + "] | Password Hash: [" + rs.getString("TX_PASSWORD") + "]");
            }
            System.out.println("--- FIN ---");
        } catch (Exception e) {
            e.printStackTrace();
        }
    }
}

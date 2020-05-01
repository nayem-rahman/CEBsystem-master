package connect_db;
import java.sql.*;
public class Main{

    public static void main(String[] args){
        String url = "jdbc:mysql://localhost:3306/cbs";
        String user = "root";
        String password = "root";
        try {
            Connection myConn = DriverManager.getConnection(url,user,password);
            Statement myStmt = myConn.createStatement();

            // prints original table //
            String sql = "select * from cbs.user";
            ResultSet rs = myStmt.executeQuery(sql);
            System.out.println("INITIAL TABLE");
            while (rs.next()){
                int userId = rs.getInt("user_id");
                String fname = rs.getString("first_name");
                String lname = rs.getString("last_name");

                System.out.println(userId+" "+fname+" "+lname);
            }

            //adds a new admin account to table //
            String newFname = "Bob";
            String newLname = "Smith";
            String email = "admin456@gmail.com";
            String newPassword = "password789";
            String user_status = "2"; // admin = 2

            String addUser = "INSERT INTO `user` (`first_name`,`last_name`,`email`,`password`,`status`) VALUES ('"+
                                newFname+"','"+newLname+"','"+email+"','"+newPassword+"',"+user_status+");";
            int q = myStmt.executeUpdate(addUser);
            if (q > 0){
                System.out.println("Successfully Inserted");
            } else {
                System.out.println("Insert Failed");
            }

            // prints updated table after adding Bob Smith //
            System.out.println("\nUPDATED TABLE");
            ResultSet rs2 = myStmt.executeQuery(sql);
            while (rs2.next()){
                int userId = rs2.getInt("user_id");
                String fname = rs2.getString("first_name");
                String lname = rs2.getString("last_name");

                System.out.println(userId+" "+fname+" "+lname);
            }

            // deletes Bob Smith //
            String delUser = "DELETE from `user` WHERE first_name = '"+newFname+"' AND last_name = '"+newLname+"'";
            int q2 = myStmt.executeUpdate(delUser);
            if (q2 > 0){
                System.out.println(newFname+" "+newLname+" Successfully Deleted");
            } else {
                System.out.println("Could not delete: "+newFname+" "+newLname);
            }

            // prints updated table after deleting Bob Smith //
            System.out.println("\nUPDATED TABLE");
            rs2 = myStmt.executeQuery(sql);
            while (rs2.next()){
                int userId = rs2.getInt("user_id");
                String fname = rs2.getString("first_name");
                String lname = rs2.getString("last_name");

                System.out.println(userId+" "+fname+" "+lname);
            }


        } catch (SQLException e) {
            e.printStackTrace();
        }
    }


}

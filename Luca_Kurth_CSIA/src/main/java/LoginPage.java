
import javax.swing.*;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.util.HashMap;

public class LoginPage implements ActionListener {

    /*
    the main method to run the program 
    Created a hashmap and put in two users and passwords
    NEED TO CHANGE LATER TO A DATABASE
     */

    public static void main(String[] args)
    {
        HashMap<String, String> loginInfo = new HashMap<>();
        loginInfo.put("Luca_K", "admin");
        loginInfo.put("Lucas_Kur", "guest");
        new LoginPage(loginInfo);
    }

    /*
    Instantiates all the frames, labels, text fields, and buttons needed for the login page
     */

    JFrame loginFieldFrame = new JFrame();
    JButton loginButton = new JButton("Login");
    JButton resetButton = new JButton("Reset");
    JTextField userIDField = new JTextField(10);
    JTextField passwordField = new JPasswordField(10);
    JLabel userIDLabel = new JLabel("User ID:");
    JLabel passwordLabel = new JLabel("Password:");
    JLabel messageLabel = new JLabel("Enter Your Login Information", SwingConstants.CENTER);

    HashMap<String,String> logininfo = new HashMap<>();

    /*
    Constructor for the login page
    Sets the sizes of the frames, buttons, etc...
    Adds them to the frame
    Implements the action listener
     */

    LoginPage(HashMap<String,String> loginInfoOriginal)
    {
        logininfo = loginInfoOriginal;

        loginFieldFrame.setSize(350,200);
        loginFieldFrame.setLayout(null);
        loginFieldFrame.setVisible(true);
        loginFieldFrame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);

        userIDLabel.setBounds(50,50,100,20);
        passwordLabel.setBounds(50,80,100,20);

        userIDField.setBounds(150,50,100,20);
        passwordField.setBounds(150,80,100,20);

        loginButton.setBounds(50,120,100,20);
        resetButton.setBounds(150,120,100,20);

        userIDField.setText(logininfo.get("User ID"));
        passwordField.setText(logininfo.get("Password"));

        messageLabel.setBounds(50,10,200,20);

        loginFieldFrame.add(messageLabel);
        loginFieldFrame.add(userIDLabel);
        loginFieldFrame.add(passwordLabel);
        loginFieldFrame.add(userIDField);
        loginFieldFrame.add(passwordField);
        loginFieldFrame.add(loginButton);
        loginFieldFrame.add(resetButton);

        loginButton.addActionListener(this);
        resetButton.addActionListener(this);
    }

    public String getPassword()
    {
        return passwordField.getText();
    }

    /*
    Override method to use the action listener
    If statement to check if the login button was pressed
    Then checks if the entered UserID is a key in the hashmap and if the value matches the key
    Creates a pop-up message for either "Login Successful" or "Login Failed"
     */

    @Override
    public void actionPerformed(ActionEvent e)
    {
        if(e.getSource() == resetButton)
        {
            userIDField.setText("");
            passwordField.setText("");
        }

        if(e.getSource() == loginButton)
        {
            String enteredUserID = userIDField.getText();
            String enteredPassword = String.valueOf(passwordField.getText());

            if(logininfo.containsKey(enteredUserID) && logininfo.get(enteredUserID).equals(enteredPassword))
            {
                JOptionPane.showMessageDialog(loginFieldFrame,"Login Successful");
                loginFieldFrame.dispose();
                welcomePage welcomePage = new welcomePage();
                welcomePage.WelcomePage();
            }
            else
            {
                JOptionPane.showMessageDialog(loginFieldFrame,"Login Failed");
            }
        }
    }
}
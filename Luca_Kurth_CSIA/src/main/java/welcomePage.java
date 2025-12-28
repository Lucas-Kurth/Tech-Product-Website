import javax.swing.*;

public class welcomePage {

    JFrame welcomeFrame = new JFrame();
    JLabel welcomeLabel = new JLabel("Welcome to the Login Page");

    public void WelcomePage()
    {
        welcomeFrame.setSize(350,200);
        welcomeFrame.setLayout(null);
        welcomeFrame.setVisible(true);
        welcomeFrame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);

        welcomeLabel.setBounds(50,50,200,20);
        welcomeFrame.add(welcomeLabel);
    }

}

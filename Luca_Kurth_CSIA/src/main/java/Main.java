

public class Main {
    public static void main(String[] args)
    {
        iDandPass idandpass = new iDandPass();
        LoginPage loginPage = new LoginPage(iDandPass.getLoginInfo());
    }
}
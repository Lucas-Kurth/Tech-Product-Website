

import java.util.HashMap;

public class iDandPass {
    static HashMap<String,String> loginInfo = new HashMap<>();

    public iDandPass()
    {
        loginInfo.put("Luca_K","admin");
        loginInfo.put("Lucas_Kur","guest");
    }

    public static HashMap<String, String> getLoginInfo()
    {
        return loginInfo;
    }
}
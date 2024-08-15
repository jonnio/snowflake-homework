package ai.osborn.snowflake;

import org.springframework.beans.factory.annotation.Value;
import org.springframework.security.oauth2.client.OAuth2AuthorizedClient;
import org.springframework.security.oauth2.client.annotation.RegisteredOAuth2AuthorizedClient;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.GetMapping;

@Controller
public class MainController {

    @Value("${homework.api.url}")
    private String apiBaseUrl;


    @GetMapping("/")
    public String index(@RegisteredOAuth2AuthorizedClient("github") OAuth2AuthorizedClient authorizedClient, Model model) {
        model.addAttribute("apiBaseUrl", apiBaseUrl);
        model.addAttribute("module", "home");
        model.addAttribute("token", authorizedClient.getAccessToken().getTokenValue());
        return "index";
    }

    @GetMapping("/customers")
    public String customers(Model model) {
        model.addAttribute("apiBaseUrl", apiBaseUrl);
        model.addAttribute("module", "customers");
        return "customers";
    }

    @GetMapping("/plot")
    public String plot(Model model) {
        model.addAttribute("module", "plot");
        return "plot";
    }
}
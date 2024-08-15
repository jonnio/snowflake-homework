package ai.osborn.snowflake;

import jakarta.servlet.http.HttpServletRequest;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.security.oauth2.client.OAuth2AuthorizedClient;
import org.springframework.security.oauth2.client.annotation.RegisteredOAuth2AuthorizedClient;
import org.springframework.security.oauth2.client.web.OAuth2AuthorizedClientRepository;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.GetMapping;

@Controller
public class MainController {

    @Value("${homework.api.url}")
    private String apiBaseUrl;
    @Value("${spring.security.oauth2.client.registration.github.client-id}")
    private String clientId;

    private final OAuth2AuthorizedClientRepository authorizedClientRepository;

    public MainController(OAuth2AuthorizedClientRepository authorizedClientRepository) {
        this.authorizedClientRepository = authorizedClientRepository;
    }

    @GetMapping("/")
    public String index(@RegisteredOAuth2AuthorizedClient("github") OAuth2AuthorizedClient authorizedClient, HttpServletRequest request, Model model) {
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
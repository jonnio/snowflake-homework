package ai.osborn.snowflake;

import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.GetMapping;

@Controller
public class MainController {

    @Value("${homework.api.url}")
    private String apiBaseUrl;

    @GetMapping("/")
    public String index(Model model) {
        model.addAttribute("apiBaseUrl", apiBaseUrl);
        model.addAttribute("module", "home");
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
package ai.osborn.snowflake;

import io.jsonwebtoken.Jwts;
import io.jsonwebtoken.security.Keys;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.http.ResponseEntity;
import org.springframework.security.core.annotation.AuthenticationPrincipal;
import org.springframework.security.oauth2.client.OAuth2AuthorizedClient;
import org.springframework.security.oauth2.client.annotation.RegisteredOAuth2AuthorizedClient;
import org.springframework.security.oauth2.core.user.OAuth2User;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.GetMapping;

import java.util.Date;
import java.util.Optional;

@Controller
public class MainController {

    @Value("${homework.api.url}")
    private String apiBaseUrl;


    @GetMapping("/")
    public String index(@RegisteredOAuth2AuthorizedClient OAuth2AuthorizedClient authorizedClient,
                        @AuthenticationPrincipal OAuth2User principal, Model model) {
        model.addAttribute("apiBaseUrl", apiBaseUrl);
        model.addAttribute("module", "home");
        model.addAttribute("token", authorizedClient.getAccessToken().getTokenValue());
        model.addAttribute("jwt", getToken(authorizedClient, principal).getBody());
        return "index";
    }

    @GetMapping("/customers")
    public String customers(@RegisteredOAuth2AuthorizedClient OAuth2AuthorizedClient authorizedClient,
                            @AuthenticationPrincipal OAuth2User principal, Model model) {
        model.addAttribute("apiBaseUrl", apiBaseUrl);
        model.addAttribute("module", "customers");
        model.addAttribute("jwt", getToken(authorizedClient, principal).getBody());
        return "customers";
    }

    @GetMapping("/plot")
    public String plot(@RegisteredOAuth2AuthorizedClient OAuth2AuthorizedClient authorizedClient,
                       @AuthenticationPrincipal OAuth2User principal, Model model) {
        model.addAttribute("module", "plot");
        model.addAttribute("apiBaseUrl", apiBaseUrl);
        model.addAttribute("jwt", getToken(authorizedClient, principal).getBody());
        return "plot";
    }

    @GetMapping("/token")
    public ResponseEntity<String> getToken(@RegisteredOAuth2AuthorizedClient OAuth2AuthorizedClient authorizedClient,
                                           @AuthenticationPrincipal OAuth2User principal) {

        // Extracting user information from OAuth2User
        final var attributes = principal.getAttributes();
        String username = null;
        String userId = null;
        if (attributes.containsKey("login")) {
            username = attributes.get("login").toString();
        } else if (attributes.containsKey("sub")) {
            username = attributes.get("sub").toString();
            userId = attributes.get("sub").toString();
        }
        if (attributes.containsKey("id") && userId == null) {
            userId = attributes.get("id").toString();
        }
        if (username == null || userId == null) {
            throw new SecurityException("username or id is missing");
        }

        var jwt = Jwts.builder()
                .claims()
                .subject(username)
                .id(userId)
                .issuedAt(new Date())
                .expiration(new Date(System.currentTimeMillis() + 3600000))
                .and()
                //.signWith(SignatureAlgorithm.HS256, authorizedClient.getClientRegistration().getClientSecret().getBytes())
                .signWith(Keys.hmacShaKeyFor(authorizedClient.getClientRegistration().getClientSecret().getBytes()))
                .compact();


        return ResponseEntity.of(Optional.of(jwt));
    }
}
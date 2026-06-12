package com.veterinaria.diagnostico.service;

import org.springframework.stereotype.Service;
import org.springframework.web.client.RestTemplate;

import java.util.HashMap;
import java.util.Map;

@Service
public class NLPService {

    public String obtenerDiagnostico(String sintomas) {

        String url = "http://localhost:5000/analizar";

        RestTemplate restTemplate = new RestTemplate();

        Map<String, String> request = new HashMap<>();
        request.put("sintomas", sintomas);

        Map response = restTemplate.postForObject(url, request, Map.class);

        return (String) response.get("diagnostico");
    }
}

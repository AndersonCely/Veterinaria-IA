package com.veterinaria.diagnostico.controller;

import com.veterinaria.diagnostico.service.ConsultaService;
import com.veterinaria.diagnostico.model.Consulta;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;

import java.util.List;
import java.util.Map;

@RestController
@RequestMapping("/api/consultas")
@CrossOrigin(origins = "*")
public class ConsultaController {

    @Autowired
    private ConsultaService service;

    // Analizar síntomas
    @PostMapping
    public Map<String, Object> analizar(@RequestBody Map<String, String> request) {
        String sintomas = request.get("sintomas");
        return service.analizarSintomas(sintomas);
    }

    // Listar historial
    @GetMapping
    public List<Consulta> listar() {
        return service.listarConsultas();
    }
}
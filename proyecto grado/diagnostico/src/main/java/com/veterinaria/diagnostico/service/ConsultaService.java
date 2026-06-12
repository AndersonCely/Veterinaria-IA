package com.veterinaria.diagnostico.service;

import com.veterinaria.diagnostico.model.Consulta;
import com.veterinaria.diagnostico.repository.ConsultaRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import org.springframework.web.client.RestTemplate;

import java.time.LocalDateTime;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

@Service
public class ConsultaService {

        @Autowired
        private ConsultaRepository repository;

        private final String PYTHON_API = "http://localhost:5000/analizar";

        public Map<String, Object> analizarSintomas(String sintomas) {

                RestTemplate restTemplate = new RestTemplate();

                // Enviar síntomas a Python
                Map<String, String> request = new HashMap<>();
                request.put("sintomas", sintomas);

                Map<String, Object> response = restTemplate.postForObject(
                                PYTHON_API,
                                request,
                                Map.class);

                // Obtener diagnóstico
                String diagnostico = response.get("diagnostico") != null
                                ? response.get("diagnostico").toString()
                                : "Sin diagnóstico";

                // Obtener texto limpio desde Python
                String textoLimpio = response.get("texto_limpio") != null
                                ? response.get("texto_limpio").toString()
                                : sintomas;

                // Obtener métricas
                Double accuracy = response.get("accuracy") != null
                                ? Double.valueOf(response.get("accuracy").toString())
                                : 0.0;

                Double precision = response.get("precision") != null
                                ? Double.valueOf(response.get("precision").toString())
                                : 0.0;

                Double recall = response.get("recall") != null
                                ? Double.valueOf(response.get("recall").toString())
                                : 0.0;

                Double confianza = response.get("confianza") != null
                                ? Double.valueOf(response.get("confianza").toString())
                                : 0.0;

                String recomendacion = response.get("recomendacion") != null
                                ? response.get("recomendacion").toString()
                                : "No hay recomendación disponible.";

                // Guardar consulta en BD
                Consulta consulta = new Consulta();
                consulta.setSintomas(textoLimpio);
                consulta.setDiagnostico(diagnostico);
                consulta.setFecha(LocalDateTime.now());

                repository.save(consulta);

                // Respuesta al frontend
                Map<String, Object> resultado = new HashMap<>();

                resultado.put("id", consulta.getId());
                resultado.put("sintomas", textoLimpio);
                resultado.put("diagnostico", diagnostico);
                resultado.put("fecha", consulta.getFecha());

                resultado.put("accuracy", accuracy);
                resultado.put("precision", precision);
                resultado.put("recall", recall);

                resultado.put("confianza", confianza);

                resultado.put("recomendacion", recomendacion);

                return resultado;
        }

        // Historial de consultas
        public List<Consulta> listarConsultas() {
                return repository.findAll();
        }
}
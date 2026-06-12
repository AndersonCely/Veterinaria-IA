package com.veterinaria.diagnostico.repository;

import org.springframework.data.jpa.repository.JpaRepository;
import com.veterinaria.diagnostico.model.Consulta;

public interface ConsultaRepository extends JpaRepository<Consulta, Long> {
}

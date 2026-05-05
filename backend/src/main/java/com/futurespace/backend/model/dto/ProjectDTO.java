package com.futurespace.backend.model.dto;

import com.fasterxml.jackson.annotation.JsonProperty;
import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.NotNull;
import jakarta.validation.constraints.Size;
import lombok.Data;

import java.time.LocalDate;

/**
 * Objeto de transferencia de datos (DTO) para la entidad de proyectos.
 * Representa la unidad operativa de negocio y sus metadatos temporales y geográficos.
 */
@Data
public class ProjectDTO {

    /** Identificador único secuencial del proyecto. */
    private Integer idProject;

    /** Descripción detallada o nombre del proyecto corporativo. */
    @NotBlank
    @Size(max = 125)
    private String description;

    /** Fecha de inicio de las operaciones del proyecto. */
    @NotNull
    private LocalDate startDate;

    /** Fecha prevista de finalización. */
    @NotNull
    private LocalDate endDate;

    /** Fecha de baja técnica o cancelación (Solo lectura). */
    @JsonProperty(access = JsonProperty.Access.READ_ONLY)
    private LocalDate terminationDate;

    /** Ubicación física o centro de coste asociado. */
    @NotBlank
    @Size(max = 30)
    private String location;

    /** Notas adicionales o requisitos específicos del proyecto. */
    @NotBlank
    @Size(max = 300)
    private String observations;
}

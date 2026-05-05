package com.futurespace.backend.model.dto;

import com.fasterxml.jackson.annotation.JsonProperty;
import jakarta.validation.constraints.*;
import lombok.Data;

import java.time.LocalDate;

/**
 * Objeto de transferencia de datos (DTO) para la entidad de empleados.
 * Encapsula la información del capital humano con validaciones de integridad de negocio.
 */
@Data
public class EmployeeDTO {

    /** Identificador único secuencial. */
    private Integer idEmployee;

    /** Número de Identificación Fiscal (8 dígitos + letra). */
    @NotBlank
    @Pattern(regexp = "^[0-9]{8}[A-Za-z]$")
    private String nif;

    /** Nombre de pila del empleado. */
    @NotBlank
    @Size(min = 2, max = 30)
    private String firstName;

    /** Primer apellido. */
    @NotBlank
    @Size(min = 2, max = 40)
    private String lastName;

    /** Segundo apellido. */
    @NotBlank
    @Size(min = 2, max = 40)
    private String secondLastName;

    /** Fecha de nacimiento del empleado. */
    @NotNull
    @Past
    private LocalDate birthDate;

    /** Teléfono de contacto principal. */
    @NotBlank
    @Pattern(regexp = "^[0-9]{9,12}$")
    private String phone1;

    /** Teléfono de contacto secundario o de emergencia. */
    @NotBlank
    @Pattern(regexp = "^[0-9]{9,12}$")
    private String phone2;

    /** Dirección de correo electrónico corporativo. */
    @NotBlank
    @Email
    @Size(max = 40)
    private String email;

    /** Fecha de alta oficial en la compañía. */
    @NotNull
    @PastOrPresent
    private LocalDate hireDate;

    /** Fecha de rescisión de contrato (Solo lectura). */
    @JsonProperty(access = JsonProperty.Access.READ_ONLY)
    private LocalDate terminationDate;

    /** Estado civil: [S]oltero, [C]asado. */
    @NotBlank
    @Pattern(regexp = "^[SC]$")
    private String maritalStatus;

    /** Indicador de titulación superior: [S]í, [N]o. */
    @NotBlank
    @Pattern(regexp = "^[SN]$")
    private String hasUniversityEducation;
}

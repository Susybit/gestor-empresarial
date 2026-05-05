package com.futurespace.backend.model.dto;

import jakarta.validation.constraints.Email;
import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.Size;
import lombok.Data;

/**
 * DTO de entrada para el acceso de usuarios administradores.
 */
@Data
public class LoginRequestDTO {

    @NotBlank
    @Email
    @Size(max = 100)
    private String email;

    @NotBlank
    private String password;
}

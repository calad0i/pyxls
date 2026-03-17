#pragma once
#include <string>
#include <stdexcept>
#include <xls/public/c_api.h>

inline void check_result(bool ok, char *error_msg) {
    if (ok)
        return;
    std::string err = error_msg ? error_msg : "Unknown XLS error";
    if (error_msg)
        xls_c_str_free(error_msg);
    throw std::runtime_error(err);
}

// Helper: convert owned C string to std::string and free
inline std::string own_c_str(char *s) {
    if (!s)
        return {};
    std::string result(s);
    xls_c_str_free(s);
    return result;
}

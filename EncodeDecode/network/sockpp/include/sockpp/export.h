
#ifndef SOCKPP_EXPORT_H
#define SOCKPP_EXPORT_H

#ifdef SOCKPP_STATIC_DEFINE
#  define SOCKPP_EXPORT
#  define SOCKPP_NO_EXPORT
#else
#  ifndef SOCKPP_EXPORT
#    ifdef sockpp_shared_EXPORTS
        /* We are building this library */
#      define SOCKPP_EXPORT __attribute__((visibility("default")))
#    else
        /* We are using this library */
#      define SOCKPP_EXPORT __attribute__((visibility("default")))
#    endif
#  endif

#  ifndef SOCKPP_NO_EXPORT
#    define SOCKPP_NO_EXPORT __attribute__((visibility("hidden")))
#  endif
#endif

#ifndef SOCKPP_DEPRECATED
#  define SOCKPP_DEPRECATED __attribute__ ((__deprecated__))
#endif

#ifndef SOCKPP_DEPRECATED_EXPORT
#  define SOCKPP_DEPRECATED_EXPORT SOCKPP_EXPORT SOCKPP_DEPRECATED
#endif

#ifndef SOCKPP_DEPRECATED_NO_EXPORT
#  define SOCKPP_DEPRECATED_NO_EXPORT SOCKPP_NO_EXPORT SOCKPP_DEPRECATED
#endif

/* NOLINTNEXTLINE(readability-avoid-unconditional-preprocessor-if) */
#if 0 /* DEFINE_NO_DEPRECATED */
#  ifndef SOCKPP_NO_DEPRECATED
#    define SOCKPP_NO_DEPRECATED
#  endif
#endif

#endif /* SOCKPP_EXPORT_H */

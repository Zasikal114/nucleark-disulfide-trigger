NR==10 {
    sd = $2
    dG = $3
    dSs = $20
    ncys = 6
    F = 23.06
    bl = -0.220
    e1 = -dG / F / ncys + bl
    e1sd = sd / F / ncys
    e2 = -dSs / F / ncys + bl
    e2sd = sd / F / ncys
    e3 = -(dG + dSs) / F / ncys + bl
    e3sd = sqrt(2) * sd / F / ncys

    printf "=== Insulin --numberOfRuns=5 (--all, CYS->SER, -0.220V baseline) ===\n\n"
    printf "ΔΔG:       mean = %.4f  SD = %.4f (%.1f%%)\n", dG, sd, sd/dG*100
    printf "ΔΔG_S-S:   mean = %.4f\n\n", dSs
    printf "%-22s %12s %10s\n", "Method", "Mean (V)", "SD (mV)"
    printf "%-22s %12.4f %9.1f\n", "E(V) total dG", e1, e1sd*1000
    printf "%-22s %12.4f %9.1f\n", "E_disulfide(V)", e2, e2sd*1000
    printf "%-22s %12.4f %9.1f\n", "E_combined(V)", e3, e3sd*1000
}

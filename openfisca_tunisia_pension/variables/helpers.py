"""Helper functions"""

# Third Party
from numpy import minimum as min_


def pension_generique(
    duree_assurance,
    sal_ref,
    taux_annuite_base,
    taux_annuite_supplementaire,
    duree_stage,
    age_elig,
    periode_remplacement_base,
    plaf_taux_pension,
):

    bareme_annuite_en_trimestres = [
        {
            "threshold": 0,
            "annuity_rate": taux_annuite_base,
        },
        {
            "threshold": periode_remplacement_base,
            "annuity_rate": taux_annuite_supplementaire,
        },
        {
            "threshold": 40,
            "annuity_rate": 0,
        },
    ]

    taux_pension_test = 0.0
    first = True
    for bracket in bareme_annuite_en_trimestres:
        if first:
            lower_threshold = bracket["threshold"]
            between_threshold_annuity_rate = bracket["annuity_rate"]
            first = False
            continue

        upper_threshold = bracket["threshold"]

        print(
            f"duree_assurance: {duree_assurance / 4}, lower_threshold: {lower_threshold}, upper_threshold: {upper_threshold}, taux_pension: {taux_pension_test}"
        )
        taux_pension_test += max(
            0,
            min(
                (duree_assurance / 4 - lower_threshold),
                (upper_threshold - lower_threshold),
            )
            * between_threshold_annuity_rate,
        )

        lower_threshold = upper_threshold
        between_threshold_annuity_rate = bracket["annuity_rate"]

    # taux_pension = (
    #     (duree_assurance < 4 * periode_remplacement_base) * (duree_assurance / 4) * taux_annuite_base
    #     + (duree_assurance >= 4 * periode_remplacement_base) * (
    #         taux_annuite_base * periode_remplacement_base
    #         + (duree_assurance / 4 - periode_remplacement_base) * taux_annuite_supplementaire
    #         )
    #     )

    montant = min_(taux_pension_test, plaf_taux_pension) * sal_ref
    return montant

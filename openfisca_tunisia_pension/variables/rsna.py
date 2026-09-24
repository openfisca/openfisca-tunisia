"""Abstract regimes definition."""
import numpy as np
from openfisca_core.errors.variable_not_found_error import VariableNotFoundError
from openfisca_core.model_api import ETERNITY, MONTH, YEAR, Variable, date, max_, min_, set_input_divide_by_period
from openfisca_tunisia_pension.entities import Individu
from openfisca_tunisia_pension.tools import revalorise
'Régime des salariés non agricoles.'
import numpy as np
from openfisca_core.errors import ParameterNotFoundError
from openfisca_core.model_api import ADD, YEAR, Enum, Variable, apply_thresholds, max_
from openfisca_tunisia_pension.entities import Individu
from openfisca_tunisia_pension.regimes.regime import AbstractRegimeEnAnnuites

def dates_d_ouverture_du_droit(date_de_liquidation, annee):
    """Date d'ouverture du droit de chaque assuré, pour un exercice annuel.

    La date de liquidation est retenue quand elle tombe dans l'exercice ; sinon, le
    1er janvier de l'exercice, date à laquelle les variables annuelles du système
    lisent leurs paramètres.
    """
    annee_de_liquidation = date_de_liquidation.astype('datetime64[Y]').astype(int) + 1970
    premier_janvier = np.datetime64(f'{annee}-01-01', 'D')
    return np.where(annee_de_liquidation == annee, date_de_liquidation.astype('datetime64[D]'), premier_janvier)

def salaire_moyen_actualise(annee, salaire_par_annee, dates, salaire_reference_a):
    """Salaire moyen de référence, rédaction du décret n° 94-1429 (art. 18 et 19 nouveaux).

    Args:
        annee: année d'ouverture du droit ; ses salaires ne sont pas comptés.
        salaire_par_annee: fonction qui rend, pour une année de salaire, le salaire
            annuel de chaque assuré.
        dates: date d'ouverture du droit de chaque assuré (datetime64[D]).
        salaire_reference_a: fonction qui rend le nœud de paramètres
            `salaire_reference` à une date donnée.

    Sont retenues, en remontant depuis l'année qui précède l'ouverture du droit, les
    dernières années de salaire non nul, en nombre fixé par la durée de la fenêtre en
    vigueur à la date d'ouverture du droit ; si l'assuré en compte moins, la moyenne se
    fait sur celles-ci (art. 18, alinéa 2). Chaque salaire est multiplié par le
    coefficient de son année dans le barème d'actualisation applicable à cette même
    date. Le résultat est un montant annuel.
    """
    dates = np.asarray(dates, dtype='datetime64[D]')
    resultat = np.zeros(len(dates), dtype=np.float64)
    salaires_lus = {}

    def salaires(annee_de_salaire):
        if annee_de_salaire not in salaires_lus:
            salaires_lus[annee_de_salaire] = np.asarray(salaire_par_annee(annee_de_salaire), dtype=np.float64)
        return salaires_lus[annee_de_salaire]
    for date_d_ouverture in np.unique(dates):
        instant = str(date_d_ouverture)
        membres = dates == date_d_ouverture
        salaire_reference = salaire_reference_a(instant)
        nombre_annees = int(salaire_reference.duree_mois) // 12
        bareme = salaire_reference.actualisation
        premiere_annee = min((int(nom.removeprefix('annee_')) for nom in bareme))
        try:
            getattr(bareme, f'annee_{annee - 1}')
        except ParameterNotFoundError as error:
            raise ParameterNotFoundError(f"retraite.rsna.salaire_reference.actualisation.annee_{annee - 1} (aucun barème d'actualisation identifié pour les droits ouverts le {instant})", instant, variable_name='rsna_salaire_de_reference') from error
        total = np.zeros(membres.sum(), dtype=np.float64)
        retenues = np.zeros(membres.sum(), dtype=np.int64)
        for annee_de_salaire in range(annee - 1, premiere_annee - 1, -1):
            if (retenues >= nombre_annees).all():
                break
            salaire = salaires(annee_de_salaire)[membres]
            retenue = (salaire > 0) & (retenues < nombre_annees)
            if not retenue.any():
                continue
            try:
                coefficient = float(getattr(bareme, f'annee_{annee_de_salaire}'))
            except ParameterNotFoundError as error:
                raise ParameterNotFoundError(f"retraite.rsna.salaire_reference.actualisation.annee_{annee_de_salaire} (aucun barème d'actualisation identifié ne donne de coefficient aux salaires de {annee_de_salaire} pour un droit ouvert le {instant})", instant, variable_name='rsna_salaire_de_reference') from error
            total += np.where(retenue, salaire * coefficient, 0.0)
            retenues += retenue
        resultat[membres] = total / np.maximum(retenues, 1)
    return resultat

class rsna_RSNATypesRaisonDepartAnticipe(Enum):
    __order__ = 'non_concerne licenciement_economique usure_prematuree_organisme mere_3_enfants convenance_personnelle'
    non_concerne = 'Non concerné'
    licenciement_economique = 'Licenciement économique avec au minimum 60 mois de cotisations (20 trimestres)'
    usure_prematuree_organisme = "Usure prématurée de l'organisme médicalement constatée avec au minimum 60 mois de cotisations (20 trimestres)"
    mere_3_enfants = "Femme salariée, mère de 3 enfants en vie, justifiant d'au moins 180 mois de cotisations (60 trimestres)"
    convenance_personnelle = 'Convenance personnelle, avec 360 mois de cotisations (120 trimestres)'

class rsna_cotisation(Variable):
    value_type = float
    entity = Individu
    definition_period = YEAR
    label = 'cotisation retraite employeur'

    def formula(individu, period, parameters):
        NotImplementedError

class rsna_duree_assurance(Variable):
    value_type = int
    entity = Individu
    definition_period = YEAR
    label = "Durée d'assurance (trimestres validés)"

class rsna_duree_assurance_annuelle(Variable):
    value_type = float
    entity = Individu
    definition_period = YEAR
    label = "Durée d'assurance (en trimestres validés l'année considérée)"

class rsna_eligible(Variable):
    value_type = bool
    entity = Individu
    label = "L'individu est éligible à une pension CNRPS"
    definition_period = YEAR

    def formula(individu, period, parameters):
        duree_assurance = individu('rsna_duree_assurance', period=period)
        salaire_de_reference = individu('rsna_salaire_de_reference', period=period)
        age = individu('age', period=period)
        rsna = parameters(period).retraite.rsna
        duree_stage_accomplie = duree_assurance > 4 * rsna.stage_requis
        critere_age_verifie = age >= rsna.age_legal
        return duree_stage_accomplie * critere_age_verifie * (salaire_de_reference > 0)

class rsna_liquidation_date(Variable):
    value_type = date
    entity = Individu
    definition_period = ETERNITY
    label = 'Date de liquidation'
    default_value = date(2250, 12, 31)

class rsna_majoration_pension(Variable):
    value_type = int
    entity = Individu
    definition_period = MONTH
    label = 'Majoration de pension'

    def formula(individu, period, parameters):
        NotImplementedError

class rsna_pension(Variable):
    value_type = float
    entity = Individu
    definition_period = YEAR
    label = 'Pension'

    def formula(individu, period):
        pension_brute = individu('rsna_pension_brute', period)
        eligible = individu('rsna_eligible', period)
        try:
            pension_minimale = individu('rsna_pension_minimale', period)
        except VariableNotFoundError:
            pension_minimale = 0
        try:
            pension_maximale = individu('rsna_pension_maximale', period)
        except (VariableNotFoundError, NotImplementedError):
            return max_(pension_brute, pension_minimale)
        return eligible * min_(pension_maximale, max_(pension_brute, pension_minimale))

class rsna_pension_brute(Variable):
    value_type = float
    entity = Individu
    definition_period = YEAR
    label = 'Pension brute'

    def formula(individu, period, parameters):
        taux_de_liquidation = individu('rsna_taux_de_liquidation', period)
        salaire_de_reference = individu('rsna_salaire_de_reference', period)
        return (taux_de_liquidation * salaire_de_reference,)

class rsna_pension_maximale(Variable):
    value_type = float
    default_value = np.inf
    entity = Individu
    definition_period = YEAR
    label = 'Pension maximale'

    def formula(individu, period, parameters):
        NotImplementedError

class rsna_pension_minimale(Variable):
    value_type = float
    default_value = 0
    entity = Individu
    definition_period = YEAR
    label = 'Pension minimale'

    def formula(individu, period, parameters):
        rsna = parameters(period).retraite.rsna
        pension_minimale = rsna.pension_minimale
        smig_annuel = 12 * parameters(period).marche_travail.smig_40h_mensuel
        duree_assurance = individu('rsna_duree_assurance', period)
        return apply_thresholds(duree_assurance / 4, [rsna.stage_derog, rsna.stage_requis], [0, pension_minimale.inf * smig_annuel, pension_minimale.sup * smig_annuel])

class rsna_pension_servie(Variable):
    value_type = float
    entity = Individu
    definition_period = YEAR
    label = 'Pension servie'

    def formula(individu, period, parameters):
        annee_de_liquidation = individu('rsna_liquidation_date', period).astype('datetime64[Y]').astype(int) + 1970
        if all(annee_de_liquidation > period.start.year):
            return individu.empty_array()
        last_year = period.last_year
        pension_au_31_decembre_annee_precedente = individu('rsna_pension_au_31_decembre', last_year)
        revalorisation = parameters(period).rsna.revalarisation_pension_servie
        pension = individu('rsna_pension_au_31_decembre', period)
        return revalorise(pension_au_31_decembre_annee_precedente, pension, annee_de_liquidation, revalorisation, period)

class rsna_salaire_de_base(Variable):
    value_type = float
    entity = Individu
    definition_period = MONTH
    label = 'Salaire de base (salaire brut)'
    set_input = set_input_divide_by_period

class rsna_salaire_de_reference(Variable):
    value_type = float
    entity = Individu
    label = 'Salaires de référence du régime des salariés non agricoles'
    definition_period = YEAR

    def formula_1974_01_01(individu, period, parameters):
        """Articles 18 et 19 du décret n° 74-499, dans leur rédaction de 1974.

            Les salaires des trois ou des cinq dernières années, la période la plus
            avantageuse étant retenue ; ces années sont celles qui précèdent le 1er janvier
            de l'année d'ouverture du droit, laquelle n'est donc pas comptée. Le salaire
            mensuel moyen est le 1/36 ou le 1/60 du total ; il est rendu ici en montant
            annuel, comme dans la rédaction de 1994.
            """
        salaire_reference = parameters(period).retraite.rsna.salaire_reference

        def moyenne_annuelle(nombre_annees, diviseur_mois):
            total = sum((individu('rsna_salaire_de_base', period=period.offset(-rang, 'year'), options=[ADD]) for rang in range(1, int(nombre_annees) + 1)))
            return 12 * total / diviseur_mois
        return max_(moyenne_annuelle(salaire_reference.periode_courte_annees, salaire_reference.diviseur_court_mois), moyenne_annuelle(salaire_reference.periode_longue_annees, salaire_reference.diviseur_long_mois))

    def formula_1990_09_23(individu, period, parameters):
        """Décret n° 90-1455 : dix années (article 18 nouveau), divisées par 36 ou 60 mois.

            L'article 18 nouveau retient dix années ; l'article 19, non modifié, divise
            toujours le total par 36 ou 60 mois. Les deux articles ne se concilient pas, et
            aucun texte publié ne dit lequel l'a emporté jusqu'au décret n° 94-1429. Aucune
            valeur n'est calculée plutôt qu'une valeur inventée.

            L'exercice 1994 fait exception pour les droits ouverts à compter du
            1er juillet 1994, date d'effet de la rédaction du décret n° 94-1429 : quand la
            date de liquidation de chaque assuré tombe entre le 1er juillet et le
            31 décembre 1994, le calcul suit cette rédaction.
            """
        if period.start.year == 1994:
            dates = dates_d_ouverture_du_droit(individu('rsna_liquidation_date', period), 1994)
            if (dates >= np.datetime64('1994-07-01')).all():
                return salaire_moyen_actualise(1994, lambda annee: individu('rsna_salaire_de_base', period=period.offset(annee - 1994, 'year'), options=[ADD]), dates, lambda instant: parameters(instant).retraite.rsna.salaire_reference)
        raise NotImplementedError("Salaire de référence du régime des salariés non agricoles du 23 septembre 1990 au 30 juin 1994 : l'article 18 du décret n° 74-499, récrit par le décret n° 90-1455, retient dix années, et l'article 19, non modifié, divise leur total par 36 ou 60 mois. Les textes ne disent pas lequel l'emporte.")

    def formula_1994_07_01(individu, period, parameters):
        """Décret n° 94-1429 : articles 18 et 19 nouveaux, et barème d'actualisation.

            Les cinq, sept puis dix dernières années de salaire (au 1er juillet 1994, 1995
            et 1996) qui précèdent le 1er janvier de l'année d'ouverture du droit, chacune
            actualisée par le coefficient de son année au barème applicable à la date
            d'ouverture du droit. Cette date est la date de liquidation quand elle tombe
            dans l'exercice, le 1er janvier de l'exercice sinon.

            L'absence de barème pour l'année d'ouverture du droit arrête le calcul sur
            une erreur : c'est le cas à partir de 2025, faute de barème identifié après
            celui de 2024.
            """
        annee = period.start.year
        return salaire_moyen_actualise(annee, lambda annee_de_salaire: individu('rsna_salaire_de_base', period=period.offset(annee_de_salaire - annee, 'year'), options=[ADD]), dates_d_ouverture_du_droit(individu('rsna_liquidation_date', period), annee), lambda instant: parameters(instant).retraite.rsna.salaire_reference)

class rsna_taux_de_liquidation(Variable):
    value_type = float
    entity = Individu
    definition_period = YEAR
    label = 'Taux de liquidation de la pension'

    def formula(individu, period, parameters):
        bareme_annuite = parameters(period).retraite.rsna.bareme_annuite
        duree_assurance = individu('rsna_duree_assurance', period)
        taux_annuite = bareme_annuite.calc(duree_assurance)
        return taux_annuite
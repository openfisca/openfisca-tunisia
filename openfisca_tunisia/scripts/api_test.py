import urllib2


def test_validation():
    request = urllib2.Request(url = "http://localhost:2019/api/1/simulate", headers = {"Content-Type": "application/json"})
    body = """
    {
        "scenarios": [
          {
            "test_case": {
              "foyers_fiscaux": {
                "d319eb95-bf31-48a5-85b2-195dea2d7730": {
                  "declarants": [
                    "3da028c8-4c7f-4259-ace8-fb5103bb2e97"
                  ],
                  "personnes_a_charge": [],
                  "nom_foyer_fiscal": "1"
                }
              },
              "individus": {
                "3da028c8-4c7f-4259-ace8-fb5103bb2e97": {
                  "nom_individu": "Personne 1"
                }
              },
              "menages": {
                "b827e13d-cfb5-4632-ac41-70db26d0fbd5": {
                  "personne_de_reference": "3da028c8-4c7f-4259-ace8-fb5103bb2e97",
                  "conjoint": null,
                  "enfants": [],
                  "autres": [],
                  "nom_menage": "1"
                }
              }
            },
            "year": 2011
          }
        ],
        "validate": true
      }
    """

    try:
        response = urllib2.urlopen(request, body)
    except urllib2.HTTPError as response:
        print response.read()
    else:
        print response.read()


def test_validation_repair():
    request = urllib2.Request(url = "http://localhost:2019/api/1/simulate", headers = {"Content-Type": "application/json"})
    body = """
    {
        "scenarios": [
          {
            "test_case": {
              "individus": {
                "3da028c8-4c7f-4259-ace8-fb5103bb2e97": {
                  "nom_individu": "Personne 1"
                }
              }
            },
            "year": 2011
          }
        ],
        "validate": true
      }
    """
    try:
        response = urllib2.urlopen(request, body)
    except urllib2.HTTPError as response:
        print response.read()
    else:
        print response.read()


def test_simulation():
    request = urllib2.Request(url = "http://localhost:2019/api/1/simulate", headers = {"Content-Type": "application/json"})
    body = """
    {
        "scenarios": [
          {
            "test_case": {
              "foyers_fiscaux": {
                "d319eb95-bf31-48a5-85b2-195dea2d7730": {
                  "declarants": [
                    "3da028c8-4c7f-4259-ace8-fb5103bb2e97"
                  ],
                  "personnes_a_charge": [],
                  "nom_foyer_fiscal": "1"
                }
              },
              "individus": {
                "3da028c8-4c7f-4259-ace8-fb5103bb2e97": {
                  "nom_individu": "Personne 1"
                }
              },
              "menages": {
                "b827e13d-cfb5-4632-ac41-70db26d0fbd5": {
                  "personne_de_reference": "3da028c8-4c7f-4259-ace8-fb5103bb2e97",
                  "conjoint": null,
                  "enfants": [],
                  "autres": [],
                  "nom_menage": "1"
                }
              }
            },
            "year": 2011
          }
        ]
      }
    """

    try:
        response = urllib2.urlopen(request, body)
    except urllib2.HTTPError as response:
        print response.read()
    else:
        print response.read()


if __name__ == '__main__':
    test_validation_repair()

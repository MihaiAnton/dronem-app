# Proiect VVSS - testare in Python folosind Pytest

Anton Mihai              - antonmihai58@gmail.com

Avram Vasile-Cosmin      - cosminavram26@gmail.com

Bacotiu Gabriel-Octavian - gabibac5@gmail.com

Badita Marin-Georgian    - geo.badita@gmail.com

Hasmasan Dragos-Catalin  - hasmasandragos13@gmail.com


```python
import warnings
warnings.filterwarnings("ignore")
!pip install Faker -q
!pip install ipytest -q
!pip install pytest -q
```

## Table of contents

[1.Introducere](#Introducere)

[2.Configurare proiect](#Configurareproiect)

[3.Configurare Framework](#ConfigurareFramework)

[4.PyTest](#PyTest)

[5.Faker](#Faker)

[6.Fixtures](#Fixtures)

[7.Monkey Patch](#MonkeyPatch)

[8.PyTest Parametrize](#Parametrize)

<a id='Introducere'></a>
## 1. Introducere

Python are o gama larga de utilitare de testare care nu sunt doar eficiente, dar si versatile. Unul dintre cele mai populare dintre aceste utilitare este PyTest. In acesta prezentare vom vedea capabilitatile sale in diverse cazuri de utilizare. 

<a id='Configurareproiect'></a>

## 2. Configurare proiect

Toate dependintele proiectelui sunt in fisierul requirements.txt. Pentru a instala aceste dependente, trebuie doar sa folosim urmatoarea comanda:

```python -m pip install -r requirements.txt```

Pentru rularea proiectului trebuie folosite urmatoarele trei comenzi:

```python manage.py makemigrations```

```python manage.py migrate```

```python manage.py runserver```

<a id='ConfigurareFramework'></a>

## 3. Configurare Framework

Framework-ul este un package pip, fiind nevoie doar de a fi instalat folosind comanda:

```pip install pytest```

Dar nu ar fi nevoie sa rulam aceasta comanda daca avem deja declarat pytest in fisierul requirements.txt.

<a id='PyTest'></a>

## 4. PyTest

PyTest este un framework care permite testarea aplicatiilor scrise in Python, acesta putand fi folosit atat pentru a testa o baza de date, API-uri sau UI, dar de cele mai multe ori in industrie acest framework este folosit pentru testarea API-urilor.
Cateva dintre avantajele folosirii PyTest sunt:
- Usor de configurat, sintaxa simpla
- Poate rula teste in paralel
- Poate detecta automat teste
- Poate rula teste/subteste speicifice
- Open source


Pentru a intelege conceptele aduse de PyTest, vom prezenta un exemplu simplu de
inteles, testand o functie care calculeaza cel mai mare divizor comun


```python
def computeGCD(x, y):
    """
    Function for computing the gcd of two numbers
    :param x: integer
    :param y: integer
    :return: gcd of x and y
    """
    while (y):
        x, y = y, x % y

    return x
```

Vom prezenta doua situatii. In prima situatie vom testa functie cu date valide, 
iar in cea de a doua o vom testa cu date de intrare invalide.
Crearea unui test in PyTest este foarte simpla, este nevoie doar ca numele functiei sa inceapa cu "test_".


```python
import pytest
from computeGCD import computeGCD

def test_gcd_valid():
    assert computeGCD(60, 48) == 12

def test_gcd_invalid():
    assert computeGCD(60, 48) == 13, "Test failed!"


```


```python
!pytest test_gcd.py
```

    ============================= test session starts =============================
    platform win32 -- Python 3.7.6, pytest-5.3.5, py-1.8.1, pluggy-0.13.1
    rootdir: C:\Users\cesmon\PycharmProjects\DRONEM-APP\dronem-app
    plugins: Faker-4.1.0, hypothesis-5.4.1, arraydiff-0.3, astropy-header-0.1.2, doctestplus-0.5.0, openfiles-0.4.0, remotedata-0.3.2
    collected 2 items
    
    test_gcd.py .F                                                           [100%]
    
    ================================== FAILURES ===================================
    ______________________________ test_gcd_invalid _______________________________
    
        def test_gcd_invalid():
    >       assert computeGCD(60, 48) == 13, "Test failed!"
    E       AssertionError: Test failed!
    E       assert 12 == 13
    E        +  where 12 = computeGCD(60, 48)
    
    test_gcd.py:8: AssertionError
    ========================= 1 failed, 1 passed in 0.15s =========================
    

Putem observa ca un test a trecut, iar cel de-al doilea nu a trecut. In sectiunea de failures putem observa rezultatele de rulare a testelor care nu au trecut, reusind sa printam si anumite mesaje.

<a id='Faker'></a>

## 5. Faker

De multe ori in situatii de testing este nevoie sa se foloseasca date cat mai aproape de realitate, imitand utilizarea reala a aplicatiei, pentru a depista eventuale erori. __Faker__ este o librarie Python ce permite generarea de date fake diverse pentru a popula baze de date si a crea mock-uri.

Pentru generare de date random, __Faker__ expune o serie de metode default, pentru atribute uzuale, dar si optiunea de a crea provideri custom, pentru a simula business case-ul propriu.
    
In continuare, vor fi prezentate o serie de experimente si explicatii in legatura cu folosirea API-ului oferit de aceasta librarie.

#### Initializarea unui obiect Faker


```python
from faker import Faker
fake = Faker()
```

Metodele de baza sunt cele pentru generare de atribute simple, precum nume, adrese, secvente de text si altele, dupa cum se poate observa in exemplele de mai jos.

#### Generare de nume


```python
fake_name = fake.name()
print(fake_name)
```

    Susan Tyler
    

#### Generare de adresa


```python
fake_address = fake.address()
print(fake_address)
```

    11897 Taylor Coves Suite 855
    Brownland, DE 83218
    

#### Generare de text


```python
fake_text = fake.paragraph()
print(fake_text)
```

    Address ever would when alone. Democrat unit improve.
    

#### Generare de data


```python
fake_date = fake.date()
print(fake_date)
```

    2009-06-23
    

#### Generare de numar de inmatriculare


```python
fake_license = fake.license_plate()
print(fake_license)
```

    LJ 4741
    

#### Generare de cont bancar


```python
fake_account = fake.iban()
print(fake_account)
```

    GB03SCUF52966935700793
    

#### Generare de mail


```python
fake_mail = fake.email()
print(fake_mail)
```

    yodom@yahoo.com
    

#### Generare de nume de companie


```python
fake_company = fake.company() + " " + fake.company_suffix()
print(fake_company)
```

    Nguyen Ltd Inc
    

#### Generare de culori


```python
color_name = fake.color_name()
fake_color = fake.color(hue=(100, 200), color_format='rgb')
fake_hex_color = fake.hex_color()
fake_css_color = fake.rgb_css_color()
print(color_name,"  |  ", fake_color,"  |  ", fake_hex_color,"  |  ", fake_css_color)
```

    Orchid   |   rgb(27, 214, 158)   |   #e6b333   |   rgb(138,53,28)
    

#### Generare de cursuri valutare


```python
fake_crypto = fake.cryptocurrency()
fake_currency = fake.currency()
fake_symbol = fake.currency_symbol()
print(fake_crypto,"  |  ", fake_currency, "  |  ", fake_symbol)
```

    ('BTC', 'Bitcoin')   |   ('SRD', 'Surinamese dollar')   |   ₸
    

#### Generare de nume de fisiere


```python
fake_file = fake.file_name()
print(fake_file)
```

    foreign.wav
    

#### Generarea unui profil de utilizator


```python
fake_profile = fake.profile()
print(fake_profile)
```

    {'job': 'Community education officer', 'company': 'Adams-Jordan', 'ssn': '219-86-6547', 'residence': '5096 Alfred Corners Apt. 705\nAndersonside, RI 32084', 'current_location': (Decimal('-80.7217205'), Decimal('-62.798318')), 'blood_group': 'A-', 'website': ['https://foster-hernandez.com/', 'https://perez-martinez.net/'], 'username': 'utaylor', 'name': 'Frank Chandler', 'sex': 'M', 'address': '42435 Brandi Place\nAndrewfort, SD 10137', 'mail': 'nhunter@hotmail.com', 'birthdate': datetime.date(2004, 4, 4)}
    

#### Generare de device-uri si platforme


```python
fake_android = fake.android_platform_token()
fake_chrome = fake.chrome()
fake_ios = fake.ios_platform_token()

print(fake_android + "\n" + fake_chrome + "\n" + fake_ios)
```

    Android 3.2.2
    Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/534.0 (KHTML, like Gecko) Chrome/21.0.873.0 Safari/534.0
    iPad; CPU iPad OS 5_1_1 like Mac OS X
    

Pe langa capacitatea acestui frameworks de a genera date pseudo-reale, generarea de date poate fi parametrizata cu locatiile din care acestea sa provina, generand astfel informatii custom pentru diverse locatii/tari.


```python
fake = Faker(['ro_RO', 'es_MX','ru_RU', 'ja_JP'])
for _ in range(20):
    print(fake.name())
```

    Dorin Tabacu
    Eugen Mazilescu
    Надежда Егоровна Матвеева
    Dr. Irene Valencia
    Francesca Gheorghiu
    Кира Никифоровна Ситникова
    Andrés Reina Cano Luevano
    Кудрявцев Геннадий Якубович
    Filofteia Mazilescu
    Elena Araceli Miramontes Rangel
    Eugen Oprea
    Емельянов Семен Исидорович
    Алексеев Ярополк Терентьевич
    Pamela Arias Ybarra
    Lic. Humberto Solorzano
    Irene Claudio Rosas
    Itzel Victoria Naranjo Ocampo
    Monica Oprea
    Прасковья Павловна Комиссарова
    Abigail Gilberto Cervántez
    

#### Crearea unui obiect faker pentru o anumita regiune


```python
from faker import Factory
fake = Factory.create('fr_FR')
```


```python
fake.address()
```




    'rue de Perrin\n93574 Perrin'




```python
fake.city()
```




    'Cohen'




```python
fake.department()
```




    ('44', 'Loire-Atlantique')



Pe langa metodele oferite de aceasta librarie, ne ofera optinuea de a crea generatoare random, denumite "Providers". Cu aceastea, utilizatorul poate geenra date random dupa o logica custom, in interiorul unei clase similare cu cea de jos.


```python
fake = Faker()
from faker.providers import BaseProvider
from random import choice

class UniversityProvider(BaseProvider):
    def course(self):
        return choice(["VVSS", "CN", "TRSI", "FP", "BI", "AI"])
    def lab_room(self):
        return choice([513, 301, 304,339])
    
fake.add_provider(UniversityProvider)
```

Orice metoda specificata intr-o clasa custom care extinde BaseProvider poate fi folosita in mod normal ca metoda a obiectului fake, similar ca ccele folosite anterior, precum .name() sau .date().


```python
fake.lab_room()
```




    301




```python
fake.course()
```




    'AI'



Pe langa suita de metode prezentata pana acum, Faker este capabil sa genereze date utile in procesul de creare de software si anume date specifice limbajului Python dar si alte date tehnice precum informatii despre IP-uri.


```python
fake_dict = fake.pydict()
fake_dict
```




    {'local': 4451,
     'magazine': -1749.88670828,
     'member': Decimal('402201.218'),
     'number': datetime.datetime(1992, 2, 15, 20, 13, 13),
     'contain': 'kristen24@yahoo.com',
     'bed': 'http://www.franco.com/faq.html',
     'success': 'wGDXicpLCcsHZvudWeKG',
     'send': Decimal('491.0'),
     'everything': datetime.datetime(1986, 1, 9, 17, 7, 55)}




```python
fake_list = fake.pylist()
fake_list
```




    ['xwxJlcjCTYbNxBeDkcJp',
     datetime.datetime(2014, 3, 6, 23, 31, 19),
     'sCNGIAUVrXnyEyBAZNSI',
     'VAaKnJTVaNFpjnqwkdkc',
     'olopez@arroyo.com',
     4133,
     'eVggHaYaRIBBFjInHYJu',
     'JDmodlqfwnzbfnGvcruS',
     'awNRoYincKKerrtTUSvg',
     'https://hernandez-hess.biz/blog/search/',
     'OcZYwxBjpCnVqDbUioxb',
     Decimal('-64.99')]




```python
from faker.providers import internet
```


```python
fake = Faker()
fake.add_provider(internet)

print(fake.ipv4_private())
```

    192.168.11.45
    

Sumarizand, Faker este o librarie utila pentru generarea de date random pseudo-reale, utile in testarea aplicatiilor.

<a id='Fixtures'></a>

## 6. Fixtures

Fixturile sunt functii care initializeaza alte functii de test. Initializarea se poate referi la setarea unei baze de date, a unui serviciu, sau a unor anumite proprietati (ex: logarea fortata a unui utilizator). Utilizarea fixturilor, imbunatateste cu mult calitatea testelor, fara de stilul clasic xUnit de testare (setup/teardown). In PyTest fixturile sunt functii simple, iar acestea sunt semnalate folosind decoratorul @pytest.fixture.


```python
class User:
    """
    Class for representing a user in our application
    """
    def __init__(self, username: str, email: str, password: str):
        self.__username = username
        self.__email = email
        self.__password = password
    
    ### @property -> getter
    @property
    def username(self) -> str:
        return self.__username
    
    @property
    def email(self) -> str:
        return self.__email
    
    @property
    def password(self) -> str:
        return self.__password
    
    ### @attribute -> setter
    @username.setter
    def username(self, val: str):
        self.__username = val
    
    @password.setter
    def password(self, val: str):
        self.__password = val
    
    @email.setter
    def email(self, val: str):
        self.__email = val
    
    def __str__(self):
        return f"Username: {self.__username} - Password: {self.__password} - Email: {self.email}\n"

```


```python
import pytest
import ipytest # in order to use pytest in jupyter notebook

@pytest.fixture
def user():
    """
    Create user with random username, password, email, using fake
    """
    return User(username=fake.name(), password=fake.password(), 
               email=fake.email())


def test_user(user):
    print(f"\nFake user is: {user}")
```


```python
!pytest test_user_fixtures.py -s
```

    ============================= test session starts =============================
    platform win32 -- Python 3.7.6, pytest-5.3.5, py-1.8.1, pluggy-0.13.1
    rootdir: C:\Users\cesmon\PycharmProjects\DRONEM-APP\dronem-app
    plugins: Faker-4.1.0, hypothesis-5.4.1, arraydiff-0.3, astropy-header-0.1.2, doctestplus-0.5.0, openfiles-0.4.0, remotedata-0.3.2
    collected 1 item
    
    test_user_fixtures.py Fake user is: Username: Kevin Williams - Password: @o36fMYs1V - Email: odonnellamber@yahoo.com
    
    .
    
    ============================== warnings summary ===============================
    C:\Users\cesmon\Anaconda3\lib\site-packages\ipytest\_unittest_support.py:18
      C:\Users\cesmon\Anaconda3\lib\site-packages\ipytest\_unittest_support.py:18: FutureWarning: pandas.util.testing is deprecated. Use the functions in the public API at pandas.testing instead.
        import pandas.util.testing as _pd_testing
    
    -- Docs: https://docs.pytest.org/en/latest/warnings.html
    ======================== 1 passed, 1 warning in 1.26s =========================
    


```python
@pytest.fixture
def user_invalid_name():
    """
    Create user with random password, email, and invalid name using fake
    """
    return User(username=".p123axzc~wqq ", password=fake.password(), 
               email=fake.email())


def is_username_valid(username: str):
    for char in username:
        if char in "?~ -":
            return False
    
    return True

def test_user_invalid_name(user_invalid_name):
    username = user_invalid_name.username

    assert is_username_valid(username) is False 
```


```python
!pytest test_user_invalid_name_fixtures.py -s
```

    ============================= test session starts =============================
    platform win32 -- Python 3.7.6, pytest-5.3.5, py-1.8.1, pluggy-0.13.1
    rootdir: C:\Users\cesmon\PycharmProjects\DRONEM-APP\dronem-app
    plugins: Faker-4.1.0, hypothesis-5.4.1, arraydiff-0.3, astropy-header-0.1.2, doctestplus-0.5.0, openfiles-0.4.0, remotedata-0.3.2
    collected 1 item
    
    test_user_invalid_name_fixtures.py .
    
    ============================== warnings summary ===============================
    C:\Users\cesmon\Anaconda3\lib\site-packages\ipytest\_unittest_support.py:18
      C:\Users\cesmon\Anaconda3\lib\site-packages\ipytest\_unittest_support.py:18: FutureWarning: pandas.util.testing is deprecated. Use the functions in the public API at pandas.testing instead.
        import pandas.util.testing as _pd_testing
    
    -- Docs: https://docs.pytest.org/en/latest/warnings.html
    ======================== 1 passed, 1 warning in 1.23s =========================
    

<a id='MonkeyPatch'></a>

## 7. Monkey Patch

Monkey Patch este simpla inlocuire dinamica a atributelor la momentul rularii.
Avand in vedere faptul ca in Python clasele sunt mutabile, monkey patch doar inlocuieste un atribut al unei clase cu un alt atribut, astfel putem obtine comportament similar cu cel al mock-ului (precum Mockito din limbajul Java).



```python
import pytest

# contents of test_module.py with source code and the test
from pathlib import Path


def getssh():
    """Simple function to return expanded homedir ssh path."""
    return Path.home() / ".ssh"


def test_getssh(monkeypatch):
    # mocked return function to replace Path.home
    # always return '/abc'
    def mockreturn():
        return Path("/abc")

    # Application of the monkeypatch to replace Path.home
    # with the behavior of mockreturn defined above.
    monkeypatch.setattr(Path, "home", mockreturn)

    # Calling getssh() will use mockreturn in place of Path.home
    # for this test with the monkeypatch.
    x = getssh()
    assert x == Path("/abc/.ssh")
```


```python
!pytest test_monkey_patch.py
```

    ============================= test session starts =============================
    platform win32 -- Python 3.7.6, pytest-5.3.5, py-1.8.1, pluggy-0.13.1
    rootdir: C:\Users\cesmon\PycharmProjects\DRONEM-APP\dronem-app
    plugins: Faker-4.1.0, hypothesis-5.4.1, arraydiff-0.3, astropy-header-0.1.2, doctestplus-0.5.0, openfiles-0.4.0, remotedata-0.3.2
    collected 1 item
    
    test_monkey_patch.py .                                                   [100%]
    
    ============================== 1 passed in 0.12s ==============================
    

<a id='Parametrize'></a>

## 8. Pytest Parametrize

Framework-ul Pytest ne permite definirea valorilor parametrilor unei functii direct in fisierul in care a fost definit
testul folosind decoratorul @pytest.mark.parametrize.

Avantajul acestei metode este ca se pot scrie rapid cazuri de testare functiile cu un numar mic de parametrii. Insa in
cazul in care functia care trebuie sa fie testate, parametrizarea este folosita impreuna cu fixturile. Fixturile asigura
un set de date de baza pentru fiecare test, iar parametrizarea asigura variatia
parametrilor intre teste.

Parametrizarea nu este limitata doar la tipuri primitive. Orice alt tip poate fi trimis.



```python
import pytest
import math


@pytest.mark.parametrize(
    "a,b,expected_output",
    [
        (6, 3, 3),
        (17, 23, 1),
        (4, 4, 2)
    ]
)
def test_gcd(a, b, expected_output):
    assert math.gcd(a, b) == expected_output
```


```python
!pytest test_parametrize.py
```

    ============================= test session starts =============================
    platform win32 -- Python 3.7.6, pytest-5.3.5, py-1.8.1, pluggy-0.13.1
    rootdir: C:\Users\cesmon\PycharmProjects\DRONEM-APP\dronem-app
    plugins: Faker-4.1.0, hypothesis-5.4.1, arraydiff-0.3, astropy-header-0.1.2, doctestplus-0.5.0, openfiles-0.4.0, remotedata-0.3.2
    collected 3 items
    
    test_parametrize.py ..F                                                  [100%]
    
    ================================== FAILURES ===================================
    _______________________________ test_gcd[4-4-2] _______________________________
    
    a = 4, b = 4, expected_output = 2
    
        @pytest.mark.parametrize(
            "a,b,expected_output",
            [
                (6, 3, 3),
                (17, 23, 1),
                (4, 4, 2)
            ]
        )
        def test_gcd(a, b, expected_output):
    >       assert math.gcd(a, b) == expected_output
    E       assert 4 == 2
    E        +  where 4 = <built-in function gcd>(4, 4)
    E        +    where <built-in function gcd> = math.gcd
    
    test_parametrize.py:14: AssertionError
    ========================= 1 failed, 2 passed in 0.15s =========================
    

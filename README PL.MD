# Terrain converter
*Pobierz wersję exe: https://serwerentazis.quickconnect.to/d/s/z4hpWRFozIXdlaGqxLmNmcn83hc9UwDh/cKQVD-AU__qI3Q_wE2_5GUfUHc_X5zwK-OrFAByRZeQs

## Opis

Aplikacja powstawała z potrzeby sprawnego implementowania modeli terenowych pochodzących z portalu https://mapy.geoportal.gov.pl/imap/Imgp_2.html?gpmap=gp0 do oprogramowania BIM (Building Information Modeling) oraz silnika graficznego Unreal Engine.
Program ten służy do konwersji plików ASCII GRID (.asc) [NMT] pobranych z serwisów takich jak np https://mapy.geoportal.gov.pl/imap/Imgp_2.html?gpmap=gp0 i konwersji ich do formatu xyz Archline (.csv) oraz map wysokościowch Unreal Engine (.png). Konwenter umożliwia szybką konwersję plików co pozwala na sprawne wqykorzystanie ich w projektach bim jak i fotorealistycznych wizualizacjach obiektów budowolanych. Sposób wykorzystania przedstawiony został w poniższym linku: https://youtu.be/xCaH5lte604

### Funkcje aplikacji

- Wczytania pliku ASCII GRID (.asc) oraz sprawdzenie czy struktura pliku posiada niezbędne dane do prawidłowego wykorzystania pliku
- Modyfikacja gęstości siatki rzednych terenowych która pozwala na dostsowanie ilości punktów ze względu na potrzeby projektu. Umożliwia to dostosowanie gęstości siatki w taki sposób aby nie obciążała znacząco projektu
- Konwersja pliku ASCII GRID (.asc) do formatu xyz akceptowanego przez program Archline.XP (BIM)
- Konwersja pliku ASCII GRID (.asc) do formatu map height (.png) akceptowanego przez silnik graficzny Unreal Engine

## Instalacja

Program jest zawarty w jednym pliku (`Terrain converter.exe`) i nie wymaga instalacji.

## Sposób użycia

### Pobranie pliku ASCII GRID - NMT

1. Odwiedź portal [Geoportal](https://mapy.geoportal.gov.pl/imap/Imgp_2.html?gpmap=gp0).
2. Przybliż się do interesującego obszaru.
3. Skorzystaj z jednego z dwóch sposobów na pobranie pliku:

#### Sposób 1 

a) Za pomocą narzędzia zlokalizowanego w lewym górnym rogu [pobieranie danych].  
b) Wybierz usługę WCS [Numeryczny Model Terenu - Arc/Info ASCII Grid].  
c) Wybierz warstwę [DTM_PL-EVRF2007-NH], alternatywnie [DTM_PL-KRON86-NH].  
d) Wybierz narzędzie [Rysuj obs...] aby zaznaczyć interesujący teren.  
e) Kliknij pobierz plik.

#### Sposób 2

a) W menu 'zawartość mapy' rozwiń katalog [Dane do pobrania].  
b) Rozwiń katalog [Numeryczny Model Terenu].  
c) Rozwiń katalog [siatka <= 1m] (zaleca się wybór gęstości siatki 1m).  
d) Zaznacz pozycję [NMT PL - EVRF2007- NH], alternatywnie [NMT PL-KRON86-NH].  
e) Kliknij lewym przyciskiem w interesujący obszar, z pojawiającego się menu wybierz zaznaczoną wcześniej usługę.  
f) Wybierz zasób i kliknij [pobierz plik danych dla tej sekcji].

### Wczytanie pliku ASCII GRID

1. Otwórz Terrain converter.
2. W panelu kliknij przycisk 'Wybierz plik [.asc] do konwersji'.
3. Po pomyślnym załadowaniu się pliku w prawej części pokaże się podgląd Numerycznego Modelu Terenu.

### Konwersja do Archline.XP (BIM) - Format XYZ (.csv)

1. Wybierz docelową ścieżkę zapisu pliku za pomocą przycisku 'Podaj nazwę i ścieżkę zapisywanego pliku'.
2. Kliknij 'KONWERTUJ'.
3. Importuj plik do Archline za pomocą [Architektura] -> [Teren] -> [Utwórz] -> [Utwórz przez wczytanie danych].

### Konwersja do Unreal Engine (silnik graficzny) - Format Height Map (.png)

1. Wybierz docelową ścieżkę zapisu pliku za pomocą przycisku 'Podaj nazwę i ścieżkę zapisywanego pliku'.
2. Kliknij 'KONWERTUJ'.
3. Importuj plik do Unreal Engine za pomocą [Krajobraz] -> [Zarządzaj] -> [Nowe] -> [Importuj z pliku].

* Sposób użycia link: https://youtu.be/xCaH5lte604

## Sposób działania aplikacji

### Genrowanie GUI

GUI programu zostało stworzone z wykorzystaniem biblioteki PySide6. Wszystkie elementy GUI takie jak przyciski, pola tekstowe itp. zostały zaimplementowane w pliku gui/converter_window.py. Poza funkcjami tworzącymi interfejs w tym pliku znajduje się również funkcja przypisująca funkcjonalności do poszeczególnych przycisków. W celu zachowania przejrzystości kodu, formatowanie stylów GUI jak i geometria poszczególnych elementów została przeniesiona do pliku utilis/styles.py

### Pobieranie danych z pliku ASCII GRID i aktualizowanie zmiennych na czas działania programu

Pobieranie danych z pliku ASCII GRID odbywa się za pomoca modułu logic/get_ascii_grid_data.py. Moduł ten korzysta z modułu utilis/settings_and_data.py w którym to są zaimplementowane zmienne w postaci aktualizującej się klasy Variables. Instancja klasy Variables posiada dwie funkcje update_variable oraz get_variable korzystające z funkcji 'setattr' i 'getattr'. Takie rozwiązanie pozwala na dynamiczną wymianę danych pomiędzy poszczególnymi modułami, a implementowaną w tym pliku instancją klasy ActualVariablesInstance = Variables(). 

Pierwszym krokiem jest pobranie ścieżki do pliku za pomocą klasy QFileDialog. Następnie za pomocą funkcji def is_ascii_grid_file jest sprawdzane czy plik (asc.) jest plikiem NMT czy może w ogóle nie jest plikiem ASCII GRID. Odbywa się poprzez sprawdzenie wartości nagłówków w 6 pierwszych linijkach tekstu zaimprotowanego pliku. Program porównuje je z listami zaimportowanymi z utilis/settings_and_data.py czyli ascii_grid_data_set_dx_dy_wariant i ascii_grid_data_set_dx_dy_wariant. Jeżeli plik jest zgodny z którymś z formatów funkcja zapisuje dane do zmiennych oczywiście w zależności czy to jest plikl NMT i zwraca je aktualizując zmienne w klasie ActualVariablesInstance, dzięki czemu pozostałe moduły od tej pory posiadają dostęp do wartości nagłówków pliku takich jak "ncols", "nrows", "xllcorner" itd. oraz siatki danych - data_grid

Podczas pobierania kolejnych linijek danych z pliku aktualizowany jest pasek postępu aplikacji. Po pobraniu danych i zapisaniu ich do zmiennych instancji klasy ActualVariablesInstance aktualizowane są elementy GUI oraz zosatją odblokowane funkcje przycisków zmniejsz i zwiększ gęstość siatki, podaj ścieżkę do zapisu pliku png oraz csv. Rysowana jest również mapa za pomocą funkcji draw_map z modułu logic/draw_map.py.

### Zmiana gęstości siatki

Odbywa się poprzez zastosowanie funkcji z modułu logic/mesh_density_manipulator.py która przypisana jest do przycisków increase_grid_density_button oraz reduce_grid_density_button. 

Funkcja ta pobiera gęstość siatki z instancji klasy ActualVariablesInstance któa wcześniej została tam zaimportowana z pliku ASCII GIRD. Funkcja posiada dwa alternatywne tryby działania tzn. zwiększenie gęstości siatki lub jej zmniejszenie. W zależności od opcji wartość gęstości zostaje zmniejszona lub zwiększona o 1 w przedziale od 1 do 100. Następnie aktualizowana zostaje zmienna w instancji klasy ActualVariablesInstance. Po aktualizacji wartości zostaje narysowana mapa za pomocą funkcji draw_map z modułu logic/draw_map.py.

### Rysowanie mapy - Podglądu Numerycznego Modelu Terenu

Rysowanie mapy odbywa się za pomocą funkcji draw_map znajdującej się w module logic/draw_map.py. Rysowanie mapy następuje przy imporcie pliku ASCII GRID, a później prz każdorazowej manipulacjji gęstością siatki.

Pierwszym etapem jest pobranie wszystkich niezbędnych zmiennych z instancji klasy ActualVariablesInstance takich jak wartości nagłówków (xllcorner yllcorner dx  dy), gęstości siatki (mesh_denisty), oraz wartości rzędnych terenowych (data_gird). Te wartości posłużą do stworzenia wykresu przedstawiającego rzędne terenowe odwzorowane za pomocą kolorów na osiach przedstawiających długość i szerokość geodeyzjną x i y. Pobrane zostają również wartości canvas i figure które domyślnie są ustawione jako None -  pozwolą one na zidentyfikowanie czy wykres oraz płótno są rysowane pierwszy raz czy może funkcja jest wywoływana w celu nadpisania już istniejącego płótna i wykresu.

Po zaktualizowaniu zmennych z instancji klasy ActualVariablesInstance następuje ustalenie zmiennej data_grid_filtered. Jest to pojemnik na przefiltrowaną siatkę data_grid na podstawie wartości _mesh_density. Następnie klasa ActualVariablesInstance zostaje zaktualizowana o utworzoną zmienną data_grid_filtered. Zostają również zaktualizowane elementy GUI w postaci etykiet information_grid_density oraz information_amount_of_points co pozwala na dokładne sprawdzenie ilości punktów w siatce. Umożliwia to przede wszystkim zaimportowanie dużego obszaru do programu Archline (BIM) z praktycznie dowolną ilością punktów.

Nastepnym etapem jest sprawdzenie czy istnieją już jakieś wykresy, jeżeli tak to zostają wyczyszczone. Analogicznie z płótnem canvas.

Następnie zostaje utworzony figure oraz canvas i zostają one zaktualizowane w klasie ActualVariablesInstance.

Rysowanie mapy danych data_grid_filtered zostaje zainicjowane poprzez funkcję imshow z uwzględnieniem zaktualizowanych wartości dx i dy poprzez skalowanie tych wartości przez mesh_denisty

### Konwersja do Archline (csv.)

Konwersja do pliku (csv.) odbywa się za pomoca modułu logic/convert_to_csv.py. Pierwszym krotkiem jest pobranie danych z instancji klasy ActualVariablesInstance.
Po zainicjalizowaniu danych zostaje obliczona ilość punktów przygotowanych do konwersji amount_of_points oraz określona zmienna actual_converted_amount_of_points.

Funkcja wypisuje linijki tekstu do pliku o ścieżce ustalonej wcześniej przez moduł logic/save_as_function.py, któa to przypięta jest do przycisku save_as_xyz_button z wariantem .csv.
Każda z linijek twrzonego pliku csv odpowiadającyh każdej z wartości przefiltowanej siatki data_grid_filtered musi wyglądać następująco:

    com_x.value_x;com_y.value_y;com_z.value_z

        com_x - jest to komentarz do wartości x. Pojawia się przy siatce generowanej prze Archline (BIM) Program przyjdziela dla niego aktualną wartość actual_converted_amount_of_points także numeruje wszystkie punkty od 1 do ostatniego punktu w siatce data_grid_filtered
        
        value_x - jest to wartość współrzednej geodezyjnej która jest obliczana jako (xllcorner + dx * (nr kolumny siatki))

        com_y - jest to komentarz do wartości y. Nie jest on widoczny w archline więc w każdym wypadku przyjmuje wartość 0
        
        value_y - jest to wartość współrzednej geodezyjnej która jest obliczana jako (yllcorner + dy * (nr wiersza siatki))

        com_z - jest to komentarz do wartości y. Nie jest on widoczny w archline więc w każdym wypadku przyjmuje wartość 0
        
        value_z - jest to wartość rzędnej wysokościowej odczytanej z siatki data_grid_filtered

    Z racji że '.' w zapisie jest zarezerwowana jako spójnik łączący wartość i komentarz, a ',' jest równoważny z ';' czyli rozdziela poszczególne wartości x y i z to aby przedstawić liczby zmiennoprzecinkowe niezbędnym było dopisanie funkcji format która to rozdziela liczbę na cześć całkowitą i czesć dziesiętną, a następnie zestawia je w równanie które archline przy improtoniu wykonuje w celu otrzymania liczny zmiennoprzecinkowej. Działnie przedsyawione na poniższym przykładzie

        142,26
        142 + (0,27*100)/100
        142 + 26/100  - taką formę otrzymuje archline

        Przykładowa docelowa linijka => 1.574405+98/100;0.148516+26/100;0.1819+70/100

    Po stworzeniu wszystkich linijek docelowego pliku (csv.) pasek postępu zostaje zaaktualizowany do 100% a następnie zostaje wyświetlony komunikat o pomyślnym zakończeniu operacju

### Konwersja do Unreal Engine (png.)
Konwersja do pliku (.png) odbywa się za pomocą modułu logic/convert_to_png.py. Aby przygotować odpowiednio plik (.png) trzeba najpierw ustalić zasady importowania go przez silnik graficzny Unreal Engine:

- plik png musi być skalą szarości w formacie 16 bitowym
- 16 bitowy plik pozwala na przedstawianie wartości (skali szarości) od 0 - kolor czarny do 65535 - kolor biały
- szerokośc i wysokość tworoznej płaszczyzny krajobrazu powstaje na wzór płaszczyzny tworzonej przez mapę bitową pliku png, skala szarości danego pixela przenosi wartość dzięki któej program deforuje płaszczyznę aby odwzorować rzędne wysokościowe. Kolor biały (65535) jest najwyższym punktem naszego krajobrazu a kolor czarny (0) jest najniższym punktem krajobrazu

Każdy landscape w Unreal Engine możeli skalować wg współrzędnych x y i z.
jg = jednostka gry 
płaszczyzna - W podstawowej wersji tzn przy skali (x=1, y=1)  1 pixel tworzy płaszczyznę o wymiarach 1 jg na 1 jg co przekłada się na 1cm x 1cm (0,01m x 0,01m)
rzędna wysokościwoa - W podstawoej wersji (z=1) różnica pomiędzy kolorem czarnym (0), a kolorem czarnym (65535) daje różnice wysokości 512jg co odpowiada dla 512cm (5,12m)

Silnik domyślnie importując plik png tworzy krajobraz który ma skalę (x=100, y=100, z=100) co daje teren z 1 px o wymiarach 1m² i różnicy wysokości 512m
Taka różnica to jest jednak za mało aby móc bez przeszkód podstawić wszystkie wysokości występujące w polsce dlatego przy imporcie pliku do Unreal Engine zostanie użyta skala (x=100, y=100, z=600) co pozowoli z 1px strworzyć teren o wymiarach 1m² oraz różnicy wysokości pomiedzy kolorem czarnym (0) a kolorem białym (65535) o wartości 3072m. Gdyby była potrzeba przedstawiania większej różnicy wysokości należy analogicznie zwiększyć skalę wartości z w Unrealu oraz w konwerterze przestawić wartości unreal_engline_min_val oraz unreal_engline_max_val tak aby swoją różnicą objeły ten zakres.

Działanie konwertera:
Polega na skalowaniu wszystkich otrzymanych rzędnych wysokościowych z zmiennej data_grid_filtered w przedziale od 0 do 1 zakładając że 0 = unreal_engine_min_val = -512, a 1 = unreal_engline_max_val = 2560. Następnie wszystkie te wartości są mnożone przez 65535 dzięki czemu otrzymujemy proporcjonalny rozkład rzędnych w przdziale od 0 do 65535, zakładając że 0 = -512, a 65535 = 2560

Następnie otrzymany zbiór liczb za pomoca klasy Image z biblioteki PIL przekształcamy na 16 bitową mapę w skali szarości. Następnie mapa jest skalowana do rozmiarów imgae_width = round(ncols) -1 imgae_height = round(nrows) -1 co pozwla na stałe zachowanie wymiarów nawet gdy ilość punktów zostanie zredukowana podczas filtrowania danych z data_grid na filtered_data_grid.

Po tej operacji obraz zostaje zapisany do pliku png oraz zostaje wyświetlony komunikat o pomyślnej konwersji wraz z przypomnieniem ustawienia skali w Unreal Engine

## Wykorzystane technologie

*Python 3.12.3*         - Szkielet aplikacji, tworzenie klas, metod

*Biblioteka Pyside6*    - tworzenie elemetów GUI takich jak widgety, przyciski itd,
                        - organizacja położenia elementów za pomocą QVBoxLayout oraz QHBoxLayout
                        - implementacja ikon do programu
                        - generowanie okna dialogowego za pomocą QFileDialog
                        - Tworzenie nowego wątku dla funkcji trwających w czasie (dziedziczenie po klasie QThread) takich jak konwersja, dzięki podczas wykonywania czasochłonnycn operacji okno interfejsu nie jest blokowane

*Biblioteka Numpy*      - Działania na zbiorach danych, zaokrąglanie, wyciąganie co któryś z rzadu wartości

*Biblioteka PIL*        - Rysowanie map bitowych z zbiorów danych

*Matplotlib*            - Rysowanie dynamicznych wykresów pokazujących rozkład rzędnych wysokościowych na współrzędnych geodezyjnych x i y

## Planowany rozwój

1. Dodanie generatora map (.dxf) przedstawiających elementy takie jak granice działek, uzbrojenie terenu itp.
2. Łączenie wielu plików asc w celu tworzenia większych terenów (ponad 7km²).

## Autorzy

Karolczuk Kamil.
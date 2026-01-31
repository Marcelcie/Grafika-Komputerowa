# Grafika Komputerowa i Komunikacja Człowiek-Komputer

Repozytorium zawiera komplet zadań laboratoryjnych realizowanych w ramach kursu na **Politechnice Wrocławskiej**.Projekty przedstawiają ewolucję technik renderowania obrazu 3D — od klasycznego modelu oświetlenia po nowoczesny, programowalny potok graficzny.

---

## 🛠️ Technologie i Narzędzia
Wszystkie projekty zostały zrealizowane w języku **Python** przy wykorzystaniu następujących bibliotek:
* **PyOpenGL**: Implementacja API OpenGL dla środowiska Python.
* **glfw**: Zarządzanie oknami oraz obsługa zdarzeń (klawiatura, mysz).
* **NumPy**: Wydajne przetwarzanie tablic z danymi wierzchołkowymi.
* **PyGLM**: Matematyka wektorowa i macierzowa (zgodna ze standardem GLSL).

---

## 📂 Zawartość Projektu

### Laboratoria 2 - 6: Metody Klasyczne (Legacy OpenGL)
Początkowe etapy kursu skupiały się na zrozumieniu podstaw budowy sceny 3D przy użyciu funkcji stałego potoku:
* **Modelowanie brył**: Tworzenie obiektów (sześcian, czajnik, jajko) oraz ich transformacje.
* **Oświetlenie**: Implementacja modelu Phonga (ambient, diffuse, specular).
* **Wektory normalne**: Matematyczne wyznaczanie wektorów prostopadłych do powierzchni dla oświetlenia dynamicznego.
* **Interakcja**: Obsługa kamery oraz źródeł światła za pomocą myszy i klawiatury.

### Laboratorium 7: Potok Programowalny (Modern OpenGL)
Przejście na nowoczesne podejście oparte o jednostki cieniujące (shadery) w celu zwiększenia wydajności:
* **Shadery (GLSL 330 core)**: Wykorzystanie programowalnych shaderów wierzchołków i fragmentów.
* **Zarządzanie pamięcią**: Przesyłanie danych do karty graficznej za pomocą **VBO** (Vertex Buffer Object) oraz **VAO** (Vertex Array Object).
* **Zmienne Uniform**: Przekazywanie macierzy transformacji bezpośrednio do procesora graficznego (GPU).

---

## 📐 Kluczowe Obliczenia
W nowoczesnym potoku graficznym pozycja każdego wierzchołka obliczana jest bezpośrednio na karcie graficznej przy użyciu macierzy modelu, widoku i projekcji:

$$gl\_Position = P\_matrix \times V\_matrix \times M\_matrix \times position$$

---

## 🚀 Uruchamianie
1. Zainstaluj wymagane zależności:
   ```bash
   pip install numpy PyGLM glfw PyOpenGL
   ```
